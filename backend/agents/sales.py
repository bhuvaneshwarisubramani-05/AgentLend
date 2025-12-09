import re
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from database.mysql import get_interest_rate

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)


# -------------------------------------------------------------
# 1️⃣ Loan Amount Extraction
# -------------------------------------------------------------
def extract_loan_amount(query: str):
    """
    Extracts loan amount if mentioned (e.g. "2 lakh", "200k", "200000")
    Returns integer amount or None
    """

    q = query.lower()

    # Match formats like "2 lakh" or "2 lakhs"
    lakh_match = re.search(r"(\d+)\s*lakh", q)
    if lakh_match:
        return int(lakh_match.group(1)) * 100000

    # Match pure numbers (e.g. 200000)
    num_match = re.search(r"(\d{4,7})", q)
    if num_match:
        return int(num_match.group(1))

    # Match "200k"
    k_match = re.search(r"(\d+)\s*k", q)
    if k_match:
        return int(k_match.group(1)) * 1000

    return None


# -------------------------------------------------------------
# 2️⃣ Tenure Extraction (in months)
# -------------------------------------------------------------
def extract_tenure(query: str):
    """
    Extracts tenure from text (e.g. "24 months", "2 years")
    Returns tenure in months or None
    """

    q = query.lower()

    # Match "24 months"
    month_match = re.search(r"(\d+)\s*month", q)
    if month_match:
        return int(month_match.group(1))

    # Match "2 years"
    year_match = re.search(r"(\d+)\s*year", q)
    if year_match:
        return int(year_match.group(1)) * 12

    return None


# -------------------------------------------------------------
# 3️⃣ Interest Rate Explanation (LLM-based)
# -------------------------------------------------------------
def answer_interest_query(query: str):
    """
    Uses LLM to explain interest rates but injects DB value.
    """

    try:
        rate = get_interest_rate()
        rate_text = f"Our official personal loan interest rate is {rate:.2f}%."
    except Exception:
        rate_text = "Currently unable to fetch the official rate."

    prompt = f"""
    You are a Sales Loan Officer Agent.
    Explain interest rates in SIMPLE terms.

    Use THIS interest rate: {rate_text}

    User query: {query}
    """

    return llm.invoke(prompt).content
