from database.mysql import get_preapproved_limit

def underwriting_agent(memory: dict):
    phone = memory.get("phone")
    requested_amount = memory.get("loan_amount")

    if not phone or not requested_amount:
        return {"status": "error", "reason": "Missing phone or loan amount"}

    # -----------------------------
    # 1️⃣ Fetch data from MySQL
    # -----------------------------
    pre_data = get_preapproved_limit(phone)

    if not pre_data:
        return {"status": "error", "reason": "No pre-approved data for this customer"}

    # pre_data is a DICTIONARY — so use dict keys:
    preapproved_amount = int(pre_data["preapproved_amount"])
    credit_score = int(pre_data["credit_score"])

    # Save to memory
    memory["preapproved_limit"] = preapproved_amount
    memory["credit_score"] = credit_score

    # -----------------------------
    # 2️⃣ Apply underwriting rules
    # -----------------------------
    
    # Rule 1: Reject for low credit score
    if credit_score < 700:
        return {
            "status": "rejected",
            "reason": f"Low credit score ({credit_score})"
        }

    # Rule 2: Auto Approve
    if requested_amount <= preapproved_amount:
        memory["eligible_amount"] = requested_amount
        return {"status": "approved"}

    # Rule 3: Salary Slip Needed
    if requested_amount <= 2 * preapproved_amount:
        memory["needs_salary_slip"] = True
        return {"status": "need_salary"}

    # Rule 4: Reject above 2× limit
    return {
        "status": "rejected",
        "reason": f"Requested ₹{requested_amount} exceeds allowable limit"
    }
