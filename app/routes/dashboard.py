from fastapi import APIRouter
from datetime import datetime, time
from zoneinfo import ZoneInfo

from app.db import visit_collection, bill_collection
from app.models import DashboardStats

router = APIRouter()
IST = ZoneInfo("Asia/Kolkata")

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """
    Calculate and return the key statistics for today's dashboard.
    """
    now_ist = datetime.now(IST)
    today_start = now_ist.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now_ist.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Total visits today
    total_visits = await visit_collection.count_documents({
        "entryDate": {"$gte": today_start, "$lte": today_end}
    })

    # Pending bills (all time)
    pending_bills_count = await bill_collection.count_documents({"paymentStatus": "Unpaid"})

    # Amount due from all pending bills
    amount_due_pipeline = [
        {"$match": {"paymentStatus": "Unpaid"}},
        {"$group": {"_id": None, "total": {"$sum": "$totalAmount"}}}
    ]
    amount_due_result = await bill_collection.aggregate(amount_due_pipeline).to_list(1)
    total_amount_due = amount_due_result[0]['total'] if amount_due_result else 0
    
    # Amount paid today
    paid_today_pipeline = [
        {"$match": {"paymentStatus": "Paid", "paymentDate": {"$gte": today_start, "$lte": today_end}}},
        {"$group": {"_id": None, "total": {"$sum": "$totalAmount"}}}
    ]
    paid_today_result = await bill_collection.aggregate(paid_today_pipeline).to_list(1)
    total_paid_today = paid_today_result[0]['total'] if paid_today_result else 0

    # Note: "Completed Visits" is simplified here. A real implementation might
    # need a 'status' field in the visit document itself.
    # For now, we can count visits associated with a 'Paid' bill as "completed".
    completed_pipeline = [
        {"$match": {"entryDate": {"$gte": today_start, "$lte": today_end}}},
        {"$lookup": {"from": "bills", "localField": "_id", "foreignField": "visit_id", "as": "billInfo"}},
        {"$unwind": "$billInfo"},
        {"$match": {"billInfo.paymentStatus": "Paid"}},
        {"$count": "completed_count"}
    ]
    completed_result = await visit_collection.aggregate(completed_pipeline).to_list(1)
    completed_visits = completed_result[0]['completed_count'] if completed_result else 0


    return DashboardStats(
        totalVisits=total_visits,
        completedVisits=completed_visits,
        pendingBills=pending_bills_count,
        amountDue=total_amount_due,
        paidToday=total_paid_today
    )
