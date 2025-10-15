from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime, time
from zoneinfo import ZoneInfo

from app.db import visit_collection, patient_collection, bill_collection
from app.models import VisitCreate, VisitResponse
from app.utils import get_next_sequence

router = APIRouter()

# Define IST once for consistency
IST = ZoneInfo("Asia/Kolkata")

@router.post("/", response_model=VisitResponse, status_code=status.HTTP_201_CREATED)
async def create_visit(visit: VisitCreate):
    """
    Create a new visit for a patient and an associated unpaid bill.
    """
    if not ObjectId.is_valid(visit.patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID format")
    
    patient = await patient_collection.find_one({"_id": ObjectId(visit.patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {visit.patient_id} not found")

    visit_id_num = await get_next_sequence("visits")
    bill_id_num = await get_next_sequence("bills")
    
    current_ist_time = datetime.now(IST)

    new_visit = {
        "visit_id": f"V-{visit_id_num:03d}",
        "patient_id": ObjectId(visit.patient_id),
        "entryDate": current_ist_time,
        "problem": visit.problem,
    }
    visit_result = await visit_collection.insert_one(new_visit)

    new_bill = {
        "bill_id": f"B-{bill_id_num:03d}", "visit_id": visit_result.inserted_id,
        "treatments": [], "totalAmount": 0, "paymentStatus": "Unpaid",
        "paymentMethod": None, "medicalRemark": "", "paymentDate": None
    }
    await bill_collection.insert_one(new_bill)

    created_visit = await visit_collection.find_one({"_id": visit_result.inserted_id})
    
    # Manually shape the response here to match the 12-hour format
    response_data = {
        **created_visit,
        "entryDate": created_visit["entryDate"].strftime("%I:%M %p"), # Format time here for the immediate response
        "patient": patient
    }
    return response_data

@router.get("/today", response_model=List[VisitResponse])
async def get_todays_visits():
    """
    Retrieve all visits created today, based on the IST timezone.
    """
    today_start = datetime.combine(datetime.now(IST).date(), time.min).astimezone(IST)
    today_end = datetime.combine(datetime.now(IST).date(), time.max).astimezone(IST)

    pipeline = [
        {"$match": {"entryDate": {"$gte": today_start, "$lte": today_end}}},
        {"$lookup": {"from": "patients", "localField": "patient_id", "foreignField": "_id", "as": "patientInfo"}},
        {"$unwind": "$patientInfo"},
        {
            "$project": {
                "_id": 1,
                "visit_id": 1,
                "problem": 1,
                "patient": {
                    "_id": "$patientInfo._id",
                    "patient_id": "$patientInfo.patient_id",
                    "fullName": "$patientInfo.fullName"
                },
                "entryDate": {
                    "$let": {
                        "vars": {
                            "hour24": { "$toInt": { "$dateToString": { "format": "%H", "date": "$entryDate", "timezone": "Asia/Kolkata" } } },
                            "minute": { "$dateToString": { "format": "%M", "date": "$entryDate", "timezone": "Asia/Kolkata" } }
                        },
                        "in": {
                            "$concat": [
                                { "$toString": {
                                    "$cond": [
                                        { "$eq": ["$$hour24", 0] }, 12,
                                        { "$cond": [ { "$gt": ["$$hour24", 12] }, { "$subtract": ["$$hour24", 12] }, "$$hour24" ]}
                                    ]
                                }},
                                ":", "$$minute",
                                { "$cond": [ { "$gte": ["$$hour24", 12] }, " PM", " AM" ] }
                            ]
                        }
                    }
                }
            }
        }
    ]
    visits = await visit_collection.aggregate(pipeline).to_list(1000)
    return visits

# --- NEW ENDPOINT ---
@router.get("/by-patient/{patient_id}", response_model=List[VisitResponse])
async def get_visits_by_patient(patient_id: str):
    """
    Retrieve all visits for a specific patient.
    """
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID format")
    
    # Find the patient to embed in the response
    patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    visits = await visit_collection.find({"patient_id": ObjectId(patient_id)}).to_list(1000)
    
    # Manually format the response for each visit
    response_list = []
    for visit in visits:
        response_list.append({
            **visit,
            "entryDate": visit["entryDate"].strftime("%Y-%m-%d"), # Format as YYYY-MM-DD
            "patient": patient
        })

    return response_list

