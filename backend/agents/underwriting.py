from database.mysql import get_preapproved_limit

def underwriting_agent(memory: dict):
    phone = memory.get("phone")
    requested_amount = memory.get("loan_amount")
    salary = memory.get("salary", None)

    if not phone or not requested_amount:
        return {"status": "error", "reason": "Missing phone or loan amount"}

    # -----------------------------
    # 1️⃣ MySQL Lookup
    # -----------------------------
    pre_data = get_preapproved_limit(phone)

    if not pre_data:
        return {"status": "error", "reason": "No pre-approved data found"}

    preapproved_amount = int(pre_data["preapproved_amount"])
    credit_score = int(pre_data["credit_score"])

    memory["preapproved_limit"] = preapproved_amount
    memory["credit_score"] = credit_score

    # -----------------------------
    # 2️⃣ Credit Score Rule
    # -----------------------------
    if credit_score < 700:
        return {"status": "rejected", "reason": f"Low credit score ({credit_score})"}

    # -----------------------------
    # 3️⃣ Auto Approve
    # -----------------------------
    if requested_amount <= preapproved_amount:
        memory["eligible_amount"] = requested_amount
        return {"status": "approved"}

    # -----------------------------
    # 4️⃣ Salary Required
    # -----------------------------
    if requested_amount <= 2 * preapproved_amount:
        # Salary not yet provided
        if salary is None:
            return {"status": "need_salary"}

        # Salary given → evaluate
        required_salary = requested_amount / 100  # Example: 5 lakh needs 50k
        if salary < required_salary:
            return {
                "status": "rejected",
                "reason": f"Salary too low. Required ₹{required_salary:.0f}, got ₹{salary}"
            }

        # Salary OK → approve
        memory["eligible_amount"] = requested_amount
        return {"status": "approved"}

    # -----------------------------
    # 5️⃣ Reject Above 2× Limit
    # -----------------------------
    return {
        "status": "rejected",
        "reason": f"Requested ₹{requested_amount} exceeds allowable limit"
    }
