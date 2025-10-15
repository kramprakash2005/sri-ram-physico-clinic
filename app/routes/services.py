from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId

from app.db import treatment_collection
from app.models import TreatmentCreate, TreatmentResponse

router = APIRouter()

@router.post("/", response_model=TreatmentResponse, status_code=status.HTTP_201_CREATED)
async def create_service(treatment: TreatmentCreate):
    """
    Create a new treatment/service.
    """
    treatment_dict = treatment.model_dump()
    result = await treatment_collection.insert_one(treatment_dict)
    created_treatment = await treatment_collection.find_one({"_id": result.inserted_id})
    return created_treatment

@router.get("/", response_model=List[TreatmentResponse])
async def get_all_services():
    """
    Retrieve all services.
    """
    services = await treatment_collection.find().to_list(1000)
    return services

@router.get("/{service_id}", response_model=TreatmentResponse)
async def get_service(service_id: str):
    """
    Retrieve a single service by its ID.
    """
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=400, detail="Invalid service ID format")
    
    service = await treatment_collection.find_one({"_id": ObjectId(service_id)})
    if service is None:
        raise HTTPException(status_code=404, detail=f"Service with ID {service_id} not found")
    return service

@router.put("/{service_id}", response_model=TreatmentResponse)
async def update_service(service_id: str, treatment: TreatmentCreate):
    """
    Update an existing service.
    """
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    update_result = await treatment_collection.update_one(
        {"_id": ObjectId(service_id)},
        {"$set": treatment.model_dump()}
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Service with ID {service_id} not found")

    updated_service = await treatment_collection.find_one({"_id": ObjectId(service_id)})
    return updated_service

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(service_id: str):
    """
    Delete a service by its ID.
    """
    if not ObjectId.is_valid(service_id):
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    delete_result = await treatment_collection.delete_one({"_id": ObjectId(service_id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Service with ID {service_id} not found")
    
    return