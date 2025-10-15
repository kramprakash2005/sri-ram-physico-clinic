from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId

from app.db import patient_collection
from app.models import PatientCreate, PatientResponse
from app.utils import get_next_sequence

router = APIRouter()

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate):
    """
    Create a new patient.
    """
    # Generate the next readable patient ID
    next_id_num = await get_next_sequence("patients")
    readable_id = f"PT-{next_id_num:03d}"

    patient_dict = patient.model_dump()
    patient_dict["patient_id"] = readable_id
    
    result = await patient_collection.insert_one(patient_dict)
    created_patient = await patient_collection.find_one({"_id": result.inserted_id})
    return created_patient

@router.get("/", response_model=List[PatientResponse])
async def get_all_patients():
    """
    Retrieve all patients.
    """
    patients = await patient_collection.find().to_list(1000)
    return patients

@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    """
    Retrieve a single patient by their MongoDB ObjectId.
    """
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID format")
        
    patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    if patient is None:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: str, patient: PatientCreate):
    """
    Update an existing patient's details.
    """
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID format")

    update_result = await patient_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$set": patient.model_dump()}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")

    updated_patient = await patient_collection.find_one({"_id": ObjectId(patient_id)})
    return updated_patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: str):
    """
    Delete a patient by their MongoDB ObjectId.
    """
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID format")

    delete_result = await patient_collection.delete_one({"_id": ObjectId(patient_id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found")
    
    return
