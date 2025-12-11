from agents import sales
from agents import verification
from agents import underwriting as uw_agent
from agents import sanction as sanction_agent
from agents import salary
from agents import emi as emi_agent
from agents.loan_advisor import loan_advisor

from database.mongo import get_customer_by_phone



# =====================================================================
# Unified Response
# =====================================================================
def build_response(text: str, type: str, memory: dict, extra: dict = None):
    response = {
        "text": text,
        "type": type,
        "memory": memory
    }
    if extra:
        response.update(extra)
    return response, memory


# =====================================================================
# Underwriting Wrapper
# =====================================================================
def run_underwriting(memory):
    return uw_agent.underwriting_agent(memory)


# =====================================================================
# MASTER AGENT LOGIC
# =====================================================================
def master_agent(query: str, memory: dict):

    # -----------------------------------------------------------------
    # NATURAL GREETING HANDLING
    # -----------------------------------------------------------------
    if query.lower() in ["hi", "hello", "hey", "good morning", "good evening"] \
            and memory.get("loan_amount") is None:
        return build_response(
            "Hello! 👋 I'm AgentLend. I can assist you with loan eligibility, EMI calculation, KYC or plans.\n\n"
            "To begin, what loan amount are you looking for?",
            "greeting",
            memory
        )

    # -----------------------------------------------------------------
    # ADVISOR FLOW — user picks 1 / 2 / 3 options
    # -----------------------------------------------------------------
    if memory.get("stage") == "advisor_suggestion":
        choice = query.strip()

        if choice not in ["1", "2", "3"]:
            return build_response(
                "Please choose option 1, 2, or 3.",
                "ask_option",
                memory
            )

        selected = None
        for opt in memory["advisor_options"]:
            if str(opt["id"]) == choice:
                selected = opt
                break

        # Apply selected modification
        if selected["new_amount"]:
            memory["loan_amount"] = selected["new_amount"]
        if selected["new_tenure"]:
            memory["tenure"] = selected["new_tenure"]

        memory["stage"] = "final_underwriting"

        return build_response(
            f"Got it! Retrying evaluation with:\n"
            f"Loan Amount: ₹{memory['loan_amount']}\nTenure: {memory['tenure']} months",
            "retry_underwriting",
            memory
        )

    # -----------------------------------------------------------------
    # 1️⃣ LOAN AMOUNT
    # -----------------------------------------------------------------
    if memory.get("loan_amount") is None:
        amount = sales.extract_loan_amount(query)
        if amount:
            memory["loan_amount"] = amount
            memory["stage"] = "ask_tenure"
            return build_response("Great! What loan tenure (in months) do you prefer?",
                                  "ask_tenure", memory)

        return build_response("Sure! What loan amount are you looking for?",
                              "ask_loan_amount", memory)

    # -----------------------------------------------------------------
    # 2️⃣ TENURE
    # -----------------------------------------------------------------
    if memory.get("tenure") is None:
        tenure = sales.extract_tenure(query)
        if tenure:
            memory["tenure"] = tenure
            memory["stage"] = "ask_phone"
            return build_response("Please share your registered phone number for KYC verification.",
                                  "ask_phone", memory)

        return build_response("For how many months do you want the loan?",
                              "ask_tenure", memory)

    # -----------------------------------------------------------------
    # 3️⃣ PHONE NUMBER
    # -----------------------------------------------------------------
    if memory.get("phone") is None:
        phone = verification.extract_phone(query)
        if phone:
            memory["phone"] = phone
            memory["stage"] = "verify_kyc"
        else:
            return build_response("Please provide a valid 10-digit phone number.",
                                  "ask_phone", memory)

    # -----------------------------------------------------------------
    # 4️⃣ KYC + UNDERWRITING (FIRST CHECK)
    # -----------------------------------------------------------------
    if memory.get("kyc_status") is None and memory["stage"] == "verify_kyc":

        customer = get_customer_by_phone(memory["phone"])

        if not customer:
            memory["kyc_status"] = "failed"
            return build_response("❌ KYC failed. Phone number not found.",
                                  "kyc_failed", memory)

        if customer.get("kyc_status") != "verified":
            memory["kyc_status"] = "failed"
            return build_response("⚠️ Your KYC is pending. Please complete it to continue.",
                                  "kyc_pending", memory)

        memory["kyc_status"] = "verified"
        memory["customer_name"] = customer["name"]

        # Run underwriting
        result = run_underwriting(memory)

        # ----- AUTO APPROVED -----
        if result["status"] == "approved":
            memory["underwriting_status"] = "approved"
            memory["eligible_amount"] = memory["loan_amount"]
            memory["stage"] = "emi"
            return build_response(
                f"Hi {memory['customer_name']}! ✅ Your loan is pre-approved. Calculating EMI…",
                "auto_approved",
                memory
            )

        # ----- NEED SALARY -----
        if result["status"] == "need_salary":
            memory["needs_salary_slip"] = True
            memory["stage"] = "ask_salary"
            return build_response("To continue, please tell me your monthly salary.",
                                  "ask_salary", memory)

        # ----- REJECTED → GO TO ADVISOR -----
        advisor = loan_advisor(memory)
        memory["advisor_options"] = advisor["suggestions"]
        memory["stage"] = "advisor_suggestion"

        list_text = "\n".join([
            f"{o['id']}️⃣ {o['title']} (Loan: ₹{o['new_amount'] or memory['loan_amount']}, "
            f"Tenure: {o['new_tenure'] or memory['tenure']} months)"
            for o in advisor["suggestions"]
        ])

        return build_response(
            f"❌ Loan rejected: {result['reason']}\n\n"
            f"Here are better options:\n{list_text}\n\n"
            f"Select 1, 2, or 3.",
            "advisor_suggestion",
            memory
        )

    # -----------------------------------------------------------------
    # 5️⃣ SALARY INPUT
    # -----------------------------------------------------------------
    if memory.get("needs_salary_slip") and memory.get("salary") is None:
        sal = salary.extract_salary(query)

        if not sal:
            return build_response("Please enter your monthly salary (e.g., 45000 or 50k).",
                                  "ask_salary", memory)

        # Save salary
        memory["salary"] = sal
        memory["stage"] = "final_underwriting"

    # -----------------------------------------------------------------
    # 6️⃣ FINAL UNDERWRITING (AFTER SALARY OR RETRY)
    # -----------------------------------------------------------------
    if memory.get("stage") == "final_underwriting":

        result = run_underwriting(memory)

        # ❌ STILL REJECTED → GO BACK TO ADVISOR
        if result["status"] == "rejected":
            advisor = loan_advisor(memory)
            memory["advisor_options"] = advisor["suggestions"]
            memory["stage"] = "advisor_suggestion"

            list_text = "\n".join([
                f"{o['id']}️⃣ {o['title']} (Loan: ₹{o['new_amount'] or memory['loan_amount']}, "
                f"Tenure: {o['new_tenure'] or memory['tenure']} months)"
                for o in advisor["suggestions"]
            ])

            return build_response(
                f"❌ Loan rejected again: {result['reason']}\n\n"
                f"Try one of these options:\n{list_text}\n\n"
                f"Select 1, 2, or 3.",
                "advisor_retry",
                memory
            )

        # APPROVED AFTER ADJUSTMENTS
        memory["underwriting_status"] = "approved"
        memory["stage"] = "emi"

        return build_response(
            "Great! Your updated plan is approved. Calculating EMI…",
            "approved_after_retry",
            memory
        )

    # -----------------------------------------------------------------
    # 7️⃣ EMI CALCULATION
    # -----------------------------------------------------------------
    if memory.get("stage") == "emi" and memory.get("emi") is None:

        emi_value, rate = emi_agent.calculate_emi(
            memory["loan_amount"], memory["tenure"]
        )

        memory["emi"] = emi_value
        memory["interest_rate"] = rate
        memory["stage"] = "sanction"

        return build_response(
            f"📌 Your EMI is ₹{emi_value} at {rate}% interest.\nWould you like your sanction letter?",
            "emi_result",
            memory
        )

    # -----------------------------------------------------------------
    # 8️⃣ SANCTION LETTER
    # -----------------------------------------------------------------
    if memory.get("stage") == "sanction":
        letter = sanction_agent.generate_sanction_letter(memory)
        memory["stage"] = "end"

        return build_response(
            "Here is your sanction letter!",
            "sanction_letter",
            memory,
            extra={
                "letter_text": letter["letter_text"],
                "pdf_url": f"/download/{memory['phone']}"
            }
        )

    # -----------------------------------------------------------------
    # DEFAULT FALLBACK
    # -----------------------------------------------------------------
    return build_response(
        "I can help with loan eligibility, EMI calculation, KYC or plans. Continue!",
        "fallback",
        memory
    )
