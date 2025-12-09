import re

def extract_salary(query: str):
    """
    Extracts monthly salary from user message.
    Supports formats like:
    - 45000
    - 45,000
    - 50k / 50 k
    - Rs 60000
    - salary is 40000
    """

    q = query.lower().replace(",", "")

    # Match "50k", "70 k"
    k_match = re.search(r"(\d+)\s*k", q)
    if k_match:
        return int(k_match.group(1)) * 1000

    # Match "45000", "60000"
    num_match = re.search(r"(\d{4,7})", q)
    if num_match:
        return int(num_match.group(1))

    return None
