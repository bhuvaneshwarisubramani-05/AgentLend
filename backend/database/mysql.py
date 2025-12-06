import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def get_preapproved_limit(phone):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT preapproved_amount, credit_score FROM preapproved_limits WHERE phone = %s"
    cursor.execute(query, (phone,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_interest_rate():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT interest_rate FROM loan_interest_rates WHERE category = 'personal'"
    cursor.execute(query)
    rate = cursor.fetchone()
    cursor.close()
    conn.close()
    return rate["interest_rate"]
