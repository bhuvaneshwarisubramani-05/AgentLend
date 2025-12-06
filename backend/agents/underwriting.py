from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from database.mysql import get_preapproved_limit # <-- NEW IMPORT

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

def underwriting_agent(data):
    # Assume the phone number is provided in the memory/data
    phone_number = data.get("phone", None)
    
    # 1. Check for Pre-Approved Limit
    if phone_number:
        try:
            pre_approved_data = get_preapproved_limit(phone_number)
            if pre_approved_data:
                # --- Pre-Approved Logic (Data from MySQL) ---
                approved_amt = pre_approved_data.get("preapproved_amount", 0)
                credit_score = pre_approved_data.get("credit_score", 0)
                
                # Update memory with the final eligible amount from DB
                data["eligible_amount"] = approved_amt
                
                return f"""
                Eligibility Check (Pre-Approved):
                Credit Score (from DB): {credit_score}
                ✅ Approved — Pre-Approved amount: ₹{approved_amt}
                """
        except Exception as e:
            # Fallback if DB connection fails
            print(f"MySQL DB Error during pre-approval check: {e}") 

    # 2. Manual Logic (Fallback using memory data)
    # This logic runs if no pre-approved limit is found or if the phone number is missing/invalid.
    salary = data.get("salary", 0)
    credit_score = data.get("credit_score", 0)
    emi = data.get("emi", 0)
    
    dbr = (emi / salary) * 100 if salary > 0 else 0
    
    result = f"""
    Eligibility Check (Manual):
    Salary: ₹{salary}
    Credit Score: {credit_score}
    Existing EMI Burden: {dbr:.2f}%
    """

    if credit_score < 650:
        result += "❌ Rejected: Low credit score."
    elif dbr > 40:
        result += "❌ Rejected: Too much EMI burden."
    else:
        approved_amt = salary * 20
        result += f"✅ Approved — Estimated eligible amount: ₹{approved_amt}"
        data["eligible_amount"] = approved_amt # Update memory
        
    return result