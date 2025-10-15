from fastapi import APIRouter, status, Query
from typing import List
from datetime import datetime, time, date
from zoneinfo import ZoneInfo

from app.db import bill_collection, patient_collection, visit_collection
from app.models import FullReportResponse, ReportSummary, PaymentReportRow, ServiceReportRow, NewPatientReportRow

router = APIRouter()
IST = ZoneInfo("Asia/Kolkata")

@router.get("/", response_model=FullReportResponse)
async def get_full_report(
    start_date: date = Query(...), 
    end_date: date = Query(...)
):
    """
    Generate a full report for a given date range.
    """
    # Convert date objects to timezone-aware datetime objects for querying
    start_dt = datetime.combine(start_date, time.min).astimezone(IST)
    end_dt = datetime.combine(end_date, time.max).astimezone(IST)

    # --- 1. Calculate Summary Cards ---
    # Total Revenue
    revenue_pipeline = [
        {"$match": {"paymentStatus": "Paid", "paymentDate": {"$gte": start_dt, "$lte": end_dt}}},
        {"$group": {"_id": None, "total": {"$sum": "$totalAmount"}}}
    ]
    revenue_result = await bill_collection.aggregate(revenue_pipeline).to_list(1)
    total_revenue = revenue_result[0]['total'] if revenue_result else 0

    # New Patients
    new_patients_count = await patient_collection.count_documents({"dateRegistered": {"$gte": start_dt, "$lte": end_dt}})

    # Total Visits
    total_visits_count = await visit_collection.count_documents({"entryDate": {"$gte": start_dt, "$lte": end_dt}})
    
    summary = ReportSummary(totalRevenue=total_revenue, newPatients=new_patients_count, totalVisits=total_visits_count)

    # --- 2. Generate Report Tables ---
    # Payments Report
    payments_pipeline = [
        {"$match": {"paymentStatus": "Paid", "paymentDate": {"$gte": start_dt, "$lte": end_dt}}},
        {"$lookup": {"from": "visits", "localField": "visit_id", "foreignField": "_id", "as": "visitInfo"}},
        {"$unwind": "$visitInfo"},
        {"$lookup": {"from": "patients", "localField": "visitInfo.patient_id", "foreignField": "_id", "as": "patientInfo"}},
        {"$unwind": "$patientInfo"},
        {"$project": {
            "_id": 0, "bill_id": 1, "patientName": "$patientInfo.fullName", 
            "paymentDate": 1, "amount": "$totalAmount", "paymentMethod": 1
        }}
    ]
    payments_data = await bill_collection.aggregate(payments_pipeline).to_list(1000)
    payments_report = [PaymentReportRow(**p) for p in payments_data]

    # Services Report
    services_pipeline = [
        {"$match": {"paymentStatus": "Paid", "paymentDate": {"$gte": start_dt, "$lte": end_dt}}},
        {"$unwind": "$treatments"},
        {"$group": {
            "_id": "$treatments.name",
            "timesPerformed": {"$sum": 1},
            "totalRevenue": {"$sum": "$treatments.cost"}
        }},
        {"$project": {"_id": 0, "serviceName": "$_id", "timesPerformed": 1, "totalRevenue": 1}}
    ]
    services_data = await bill_collection.aggregate(services_pipeline).to_list(1000)
    services_report = [ServiceReportRow(**s) for s in services_data]
    
    # New Patients Report
    new_patients_data = await patient_collection.find(
        {"dateRegistered": {"$gte": start_dt, "$lte": end_dt}},
        {"_id": 0, "patient_id": 1, "fullName": 1, "contactNumber": 1, "dateRegistered": 1}
    ).to_list(1000)
    new_patients_report = [NewPatientReportRow(**p) for p in new_patients_data]

    return FullReportResponse(
        summary=summary,
        payments=payments_report,
        services=services_report,
        newPatients=new_patients_report
    )
