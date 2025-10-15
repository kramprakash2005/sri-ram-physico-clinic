from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. Import the CORSMiddleware
from app.routes import services
from app.routes import patients
from app.routes import visits
from app.routes import billing
from app.routes import reports
from app.routes import dashboard

# Create the FastAPI app instance
app = FastAPI(
    title="Sri Ram Physico Clinic API",
    description="API for managing patients, visits, and billing for the Sri Ram Physico Clinic.",
    version="1.0.0"
)

# 2. Define the origins that are allowed to connect.
# Using ["*"] allows all origins, which is fine for local development.
origins = ["*"]

# 3. Add the CORSMiddleware to your application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Define a root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the Sri Ram Physico Clinic API"}

# Include the services router
app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(visits.router, prefix="/visits", tags=["Visits"])
app.include_router(billing.router,prefix="/billing", tags=["Billing"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(dashboard.router,prefix="/dashboard", tags=["Dashboard"])