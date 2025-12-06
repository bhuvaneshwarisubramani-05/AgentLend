import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

crm_db = client["crm_db"]  # database name
customers = crm_db["customers"]  # collection name

def get_customer_by_phone(phone: str):
    return customers.find_one({"phone": phone})
