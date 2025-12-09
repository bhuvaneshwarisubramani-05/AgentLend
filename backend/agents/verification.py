import re

# -------------------------------------------------------------
# Extract Phone Number
# -------------------------------------------------------------
def extract_phone(query: str):
    """
    Extracts a 10-digit Indian phone number from user message.
    Returns phone number string or None.
    """

    # Remove spaces and non-digit formatting
    cleaned = re.sub(r"[^\d]", "", query)

    # Look for 10-digit number at the end
    match = re.search(r"(?:\+?91)?(\d{10})$", cleaned)
    if match:
        return match.group(1)

    return None


# -------------------------------------------------------------
# Optional - Ask a question
# -------------------------------------------------------------
def ask_for_phone():
    return "Please share your registered 10-digit phone number for KYC verification."
