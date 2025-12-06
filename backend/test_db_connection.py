# test_db_connection.py

import os
from dotenv import load_dotenv

# Ensure the environment variables are loaded
load_dotenv() 

# Import the function you are trying to use
from database.mysql import get_preapproved_limit 

# The phone number currently in main.py memory
TEST_PHONE = "9999988888" 

try:
    print(f"Attempting to fetch pre-approved data for {TEST_PHONE}...")
    result = get_preapproved_limit(TEST_PHONE)
    
    if result:
        print("✅ SUCCESS: Found data in the database!")
        print(f"   Amount: {result.get('preapproved_amount')}")
        print(f"   Score: {result.get('credit_score')}")
    else:
        print(f"⚠️ FAILURE: Database connected, but NO record found for {TEST_PHONE}.")
        
except Exception as e:
    print(f"❌ CRITICAL ERROR: Database connection failed.")
    print(f"   Details: {e}")