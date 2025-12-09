import math
from database.mysql import get_interest_rate

def calculate_emi(loan_amount: int, tenure_months: int):
    """
    Calculates EMI based on loan amount, tenure, and DB interest rate.
    Returns:
        emi (int)
        interest_rate (float)
    """

    try:
        annual_rate = float(get_interest_rate())
    except Exception:
        annual_rate = 12.0   # fallback

    R = annual_rate / (12 * 100)  # monthly rate
    P = loan_amount
    N = tenure_months

    try:
        emi = (P * R * (1 + R)**N) / ((1 + R)**N - 1)
    except ZeroDivisionError:
        emi = P / N

    return int(emi), annual_rate
