from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime, time
from zoneinfo import ZoneInfo

from app.db import bill_collection, patient_collection, visit_collection
from app.models import BillUpdate, BillResponse

router = APIRouter()

# Define IST once for consistency
IST = ZoneInfo("Asia/Kolkata")

def get_bill_aggregation_pipeline(match_filter: dict):
    """
    Helper function to create the MongoDB aggregation pipeline for fetching bills.
    """
    return [
        {"$match": match_filter},
        {"$lookup": {"from": "visits", "localField": "visit_id", "foreignField": "_id", "as": "visitInfo"}},
        {"$unwind": "$visitInfo"},
        {"$lookup": {"from": "patients", "localField": "visitInfo.patient_id", "foreignField": "_id", "as": "patientInfo"}},
        {"$unwind": "$patientInfo"},
        {
            "$project": {
                "_id": 1, "bill_id": 1, "totalAmount": 1, "paymentStatus": 1,
                "paymentMethod": 1, "medicalRemark": 1, "treatments": 1, "paymentDate": 1,
                "visit": {
                    "_id": "$visitInfo._id", "visit_id": "$visitInfo.visit_id", "entryDate": "$visitInfo.entryDate"
                },
                "patient": {"fullName": "$patientInfo.fullName"}
            }
        }
    ]

@router.get("/pending", response_model=List[BillResponse])
async def get_pending_bills():
    pipeline = get_bill_aggregation_pipeline({"paymentStatus": "Unpaid"})
    return await bill_collection.aggregate(pipeline).to_list(1000)

@router.get("/paid-today", response_model=List[BillResponse])
async def get_paid_today_bills():
    today_start = datetime.combine(datetime.now(IST).date(), time.min).astimezone(IST)
    today_end = datetime.combine(datetime.now(IST).date(), time.max).astimezone(IST)
    pipeline = get_bill_aggregation_pipeline({
        "paymentStatus": "Paid",
        "paymentDate": {"$gte": today_start, "$lte": today_end}
    })
    return await bill_collection.aggregate(pipeline).to_list(1000)

# --- NEW ENDPOINT ---
@router.get("/by-patient/{patient_id}", response_model=List[BillResponse])
async def get_bills_by_patient(patient_id: str):
    """
    Retrieve all bills for a specific patient.
    """
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID format")

    # Find all visits for the given patient
    visits = await visit_collection.find({"patient_id": ObjectId(patient_id)}).to_list(1000)
    visit_ids = [visit["_id"] for visit in visits]

    # Use the visit IDs to find all related bills
    pipeline = get_bill_aggregation_pipeline({"visit_id": {"$in": visit_ids}})
    bills = await bill_collection.aggregate(pipeline).to_list(1000)
    return bills

@router.get("/{bill_id}", response_model=BillResponse)
async def get_bill(bill_id: str):
    if not ObjectId.is_valid(bill_id):
        raise HTTPException(status_code=400, detail="Invalid bill ID format")
    pipeline = get_bill_aggregation_pipeline({"_id": ObjectId(bill_id)})
    bills = await bill_collection.aggregate(pipeline).to_list(1)
    if not bills:
        raise HTTPException(status_code=404, detail=f"Bill with ID {bill_id} not found")
    return bills[0]

@router.put("/{bill_id}", response_model=BillResponse)
async def update_bill(bill_id: str, bill: BillUpdate):
    if not ObjectId.is_valid(bill_id):
        raise HTTPException(status_code=400, detail="Invalid bill ID format")

    update_data = bill.model_dump(by_alias=True, exclude_unset=True)
    if bill.treatments is not None:
        update_data["treatments"] = [t.model_dump() for t in bill.treatments]

    if bill.paymentStatus == "Paid":
        update_data["paymentDate"] = datetime.now(IST)

    update_result = await bill_collection.update_one(
        {"_id": ObjectId(bill_id)},
        {"$set": update_data}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Bill with ID {bill_id} not found")

    return await get_bill(bill_id)

