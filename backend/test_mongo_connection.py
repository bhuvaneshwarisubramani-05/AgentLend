# test_mongo_connection.py

import os
from dotenv import load_dotenv

load_dotenv() 

# Import the function you are trying to use
from database.mongo import get_customer_by_phone 

# The phone number currently in main.py memory
TEST_PHONE = "9999988888" 

try:
    print(f"Attempting MongoDB lookup for {TEST_PHONE}...")
    result = get_customer_by_phone(TEST_PHONE)
    
    if result:
        print("✅ SUCCESS: Found customer data in MongoDB!")
        print(f"   Name: {result.get('name')}")
    else:
        print("⚠️ FAILURE: MongoDB connected, but NO record found or 'name' key is missing.")
        
except Exception as e:
    print(f"❌ CRITICAL ERROR: MongoDB connection failed.")
    print(f"   Details: {e}")