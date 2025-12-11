def loan_advisor(memory):
    loan = memory["loan_amount"]
    salary = memory.get("salary", 0)
    preapproved = memory.get("preapproved_limit", 0)

    suggestions = []

    # 1️⃣ Suggest reducing loan amount
    reduced_amount = int(preapproved * 0.9)
    suggestions.append({
        "id": 1,
        "title": f"Reduce loan amount to ₹{reduced_amount}",
        "new_amount": reduced_amount,
        "new_tenure": None
    })

    # 2️⃣ Suggest increasing tenure
    increased_tenure = memory.get("tenure", 12) + 12
    suggestions.append({
        "id": 2,
        "title": f"Increase tenure to {increased_tenure} months",
        "new_amount": None,
        "new_tenure": increased_tenure
    })

    # 3️⃣ Suggest co-applicant (no change in numbers)
    suggestions.append({
        "id": 3,
        "title": "Apply with co-applicant to increase eligibility",
        "new_amount": loan,
        "new_tenure": memory.get("tenure")
    })

    return {
        "reason": memory.get("rejection_reason", "Loan rejected"),
        "suggestions": suggestions
    }
