from pydantic import BaseModel, Field
from typing import Optional, List, Any
from bson import ObjectId
from datetime import datetime

# Final PyObjectId Class
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema
        def validate(value: str) -> ObjectId:
            if not ObjectId.is_valid(value): raise ValueError("Invalid ObjectId")
            return ObjectId(value)
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    core_schema.chain_schema([core_schema.str_schema(), core_schema.no_info_plain_validator_function(validate)])
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

# --- Base & Create Models ---
class TreatmentBase(BaseModel): name: str; cost: float; duration: str
class TreatmentCreate(TreatmentBase): pass

class PatientBase(BaseModel): fullName: str; contactNumber: str; dob: Optional[datetime] = None; gender: Optional[str] = None; address: Optional[str] = None; medicalHistory: Optional[str] = None; dateRegistered: datetime
class PatientCreate(PatientBase): pass

class VisitBase(BaseModel): problem: str
class VisitCreate(VisitBase): patient_id: str

class TreatmentInBill(BaseModel): treatment_id: PyObjectId; name: str; cost: float
class BillUpdate(BaseModel): treatments: List[TreatmentInBill]; totalAmount: float; paymentStatus: str; paymentMethod: Optional[str] = None; medicalRemark: Optional[str] = None; paymentDate: Optional[datetime] = None

# --- Response Models ---
class TreatmentResponse(TreatmentBase):
    id: PyObjectId = Field(alias="_id", default=None)
    model_config = {"arbitrary_types_allowed": True, "populate_by_name": True, "json_encoders": {ObjectId: str}}

class PatientResponse(PatientBase):
    id: PyObjectId = Field(alias="_id", default=None); patient_id: str
    model_config = {"arbitrary_types_allowed": True, "populate_by_name": True, "json_encoders": {ObjectId: str}}

class PatientInVisitResponse(BaseModel): id: PyObjectId = Field(alias="_id"); patient_id: str; fullName: str
class VisitResponse(VisitBase):
    id: PyObjectId = Field(alias="_id"); visit_id: str; entryDate: str
    patient: PatientInVisitResponse
    model_config = {"arbitrary_types_allowed": True, "populate_by_name": True, "json_encoders": {ObjectId: str}}

class VisitInBillResponse(BaseModel): id: PyObjectId = Field(alias="_id"); visit_id: str; entryDate: datetime
class PatientInBillResponse(BaseModel): fullName: str
class BillResponse(BaseModel):
    id: PyObjectId = Field(alias="_id"); bill_id: str; totalAmount: float; paymentStatus: str
    paymentMethod: Optional[str] = None; medicalRemark: Optional[str] = None; paymentDate: Optional[datetime] = None
    treatments: List[TreatmentInBill]; visit: VisitInBillResponse; patient: PatientInBillResponse
    model_config = {"arbitrary_types_allowed": True, "populate_by_name": True, "json_encoders": {ObjectId: str}}

class ReportSummary(BaseModel): totalRevenue: float; newPatients: int; totalVisits: int
class PaymentReportRow(BaseModel): bill_id: str; patientName: str; paymentDate: datetime; amount: float; paymentMethod: str
class ServiceReportRow(BaseModel): serviceName: str; timesPerformed: int; totalRevenue: float
class NewPatientReportRow(BaseModel): patient_id: str; fullName: str; contactNumber: str; dateRegistered: datetime
class FullReportResponse(BaseModel):
    summary: ReportSummary; payments: List[PaymentReportRow]; services: List[ServiceReportRow]; newPatients: List[NewPatientReportRow]

# --- NEW: Dashboard Model ---
class DashboardStats(BaseModel):
    totalVisits: int
    completedVisits: int # This might require a status in the visit model later
    pendingBills: int
    amountDue: float
    paidToday: float

