from database.mongo import get_customer_by_phone # <-- NEW IMPORT

def sanction_agent(phone: str, amount: int):
    customer_name = "Customer" # Default placeholder
    
    # 1. Look up the customer's actual name in MongoDB
    if phone:
        try:
            customer_data = get_customer_by_phone(phone)
            if customer_data and customer_data.get("name"):
                customer_name = customer_data["name"]
        except Exception as e:
            print(f"MongoDB Error during name lookup: {e}")
            # Proceed with placeholder name if DB lookup fails

    return f"""
    SANCTION LETTER

    Dear {customer_name},

    Congratulations! Your loan of ₹{amount} has been approved.
    This is a system-generated letter.

    Regards,
    Loan Department
    """