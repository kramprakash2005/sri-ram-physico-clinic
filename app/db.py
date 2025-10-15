from motor.motor_asyncio import AsyncIOMotorClient

MONGO_CONNECTION_STRING = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)

database = client.sriRamPhysicoClinic

patient_collection = database.get_collection("patients")
visit_collection = database.get_collection("visits")
bill_collection = database.get_collection("bills")
treatment_collection = database.get_collection("treatments")
counter_collection = database.get_collection("counters")
