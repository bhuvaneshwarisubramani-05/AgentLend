from agents import sales
from agents import verification
from agents import underwriting as uw_agent
from agents import sanction as sanction_agent
from agents import salary
from agents import emi as emi_agent

from database.mongo import get_customer_by_phone


# ============================================================
# Unified Response Builder
# ============================================================
def build_response(text: str, type: str, memory: dict, extra: dict = None):
    response = {
        "text": text,
        "type": type,
        "memory": memory
    }
    if extra:
        response.update(extra)
    return response, memory


# ============================================================
# Underwriting Wrapper → Converts dict into unified format
# ============================================================
def run_underwriting(memory):
    result = uw_agent.underwriting_agent(memory)

    # Already correct dict:
    # { "status": "approved" / "need_salary" / "rejected", "reason": ... }

    return result  


# ============================================================
# MASTER AGENT — FINAL RULE-BASED FLOW
# ============================================================
def master_agent(query: str, memory: dict):

    # ------------------------------------------------------------
    # 1️⃣ LOAN AMOUNT
    # ------------------------------------------------------------
    if memory.get("loan_amount") is None:
        amount = sales.extract_loan_amount(query)
        if amount:
            memory["loan_amount"] = amount
            memory["stage"] = "ask_tenure"
            return build_response("Great! What loan tenure (in months) do you prefer?",
                                  "ask_tenure", memory)

        return build_response("Sure! What loan amount are you looking for?",
                              "ask_loan_amount", memory)

    # ------------------------------------------------------------
    # 2️⃣ TENURE
    # ------------------------------------------------------------
    if memory.get("tenure") is None:
        tenure = sales.extract_tenure(query)
        if tenure:
            memory["tenure"] = tenure
            memory["stage"] = "ask_phone"
            return build_response("Please share your registered phone number for KYC verification.",
                                  "ask_phone", memory)

        return build_response("For how many months do you want the loan?",
                              "ask_tenure", memory)

    # ------------------------------------------------------------
    # 3️⃣ PHONE NUMBER
    # ------------------------------------------------------------
    if memory.get("phone") is None:
        phone = verification.extract_phone(query)
        if phone:
            memory["phone"] = phone
            memory["stage"] = "verify_kyc"
        else:
            return build_response("Please provide your 10-digit phone number for KYC.",
                                  "ask_phone", memory)

    # ------------------------------------------------------------
    # 4️⃣ KYC + INSTANT UNDERWRITING
    # ------------------------------------------------------------
    if memory.get("kyc_status") is None and memory["stage"] == "verify_kyc":

        customer = get_customer_by_phone(memory["phone"])

        if not customer:
            memory["kyc_status"] = "failed"
            return build_response("❌ KYC failed. Phone number not found.",
                                  "kyc_failed", memory)

        if customer.get("kyc_status") != "verified":
            memory["kyc_status"] = "failed"
            return build_response("⚠️ Your KYC is pending. Complete KYC to proceed.",
                                  "kyc_pending", memory)

        # SUCCESS
        memory["kyc_status"] = "verified"
        memory["customer_name"] = customer["name"]

        # ⭐ INSTANT UNDERWRITING
        result = run_underwriting(memory)

        # ---- APPROVED ----
        if result["status"] == "approved":
            memory["underwriting_status"] = "approved"
            memory["eligible_amount"] = memory["loan_amount"]
            memory["stage"] = "emi"
            return build_response(f"Hi {memory['customer_name']}! ✅ Your loan is pre-approved. Calculating EMI…",
                                  "auto_approved", memory)

        # ---- NEED SALARY ----
        if result["status"] == "need_salary":
            memory["needs_salary_slip"] = True
            memory["stage"] = "ask_salary"
            return build_response("To continue, please tell me your monthly salary.",
                                  "ask_salary", memory)

        # ---- REJECTED ----
        memory["stage"] = "end"
        return build_response(f"❌ Loan rejected: {result['reason']}",
                              "rejected", memory)

    # ------------------------------------------------------------
    # 5️⃣ SALARY PARSING
    # ------------------------------------------------------------
    if memory.get("needs_salary_slip") and memory.get("salary") is None:
        sal = salary.extract_salary(query)
        if sal:
            memory["salary"] = sal
            memory["stage"] = "final_underwriting"
        else:
            return build_response("Please enter your monthly salary (e.g., 45000 or 50k).",
                                  "ask_salary", memory)

    # ------------------------------------------------------------
    # 6️⃣ FINAL UNDERWRITING (AFTER SALARY)
    # ------------------------------------------------------------
    if memory.get("stage") == "final_underwriting" and memory.get("underwriting_status") is None:

        result = run_underwriting(memory)

        if result["status"] == "rejected":
            memory["stage"] = "end"
            return build_response(f"❌ Loan rejected: {result['reason']}",
                                  "rejected", memory)

        memory["underwriting_status"] = "approved"
        memory["eligible_amount"] = memory["loan_amount"]
        memory["stage"] = "emi"

        return build_response("✅ Loan approved! Calculating EMI…",
                              "approved_after_salary", memory)

    # ------------------------------------------------------------
    # 7️⃣ EMI CALCULATION
    # ------------------------------------------------------------
    if memory.get("stage") == "emi" and memory.get("emi") is None:

        emi_value, rate = emi_agent.calculate_emi(memory["loan_amount"], memory["tenure"])

        memory["emi"] = emi_value
        memory["interest_rate"] = rate
        memory["stage"] = "sanction"

        return build_response(
            text=f"📌 Your EMI is ₹{emi_value} at {rate}% interest.\nWould you like your sanction letter?",
            type="emi_result",
            memory=memory
        )

    # ------------------------------------------------------------
    # 8️⃣ SANCTION LETTER
    # ------------------------------------------------------------
    if memory.get("stage") == "sanction":
        letter = sanction_agent.generate_sanction_letter(memory)
        memory["stage"] = "end"

        return build_response(
            text="Here is your sanction letter!",
            type="sanction_letter",
            memory=memory,
            extra={
                "letter_text": letter["letter_text"],
                "pdf_url": f"/download/{memory['phone']}"
            }
        )

    # ------------------------------------------------------------
    # 9️⃣ DEFAULT FALLBACK
    # ------------------------------------------------------------
    return build_response("I can help with loan amount, tenure, KYC, eligibility or EMI. Continue!",
                          "fallback", memory)
