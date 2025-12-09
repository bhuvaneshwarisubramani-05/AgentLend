from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database.mongo import get_customer_by_phone
import os


def generate_sanction_letter(memory: dict):
    """
    Generates both TEXT and PDF sanction letter.
    """

    phone = memory.get("phone")
    amount = memory.get("eligible_amount")
    tenure = memory.get("tenure")
    emi = memory.get("emi")
    rate = memory.get("interest_rate")

    # Get customer name
    customer_name = "Customer"
    try:
        customer = get_customer_by_phone(phone)
        if customer and customer.get("name"):
            customer_name = customer["name"]
    except:
        pass

    # -------------------------------
    # TEXT LETTER
    # -------------------------------
    letter_text = f"""
Dear {customer_name},

Congratulations! Your loan has been approved.

Loan Details:
- Amount: ₹{amount}
- Tenure: {tenure} months
- EMI: ₹{emi}
- Interest Rate: {rate}%

Regards,
AgentLend Loan Department
""".strip()

    # -------------------------------
    # PDF GENERATION
    # -------------------------------
    pdf_folder = "pdfs"
    os.makedirs(pdf_folder, exist_ok=True)

    pdf_path = os.path.join(pdf_folder, f"sanction_{phone}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 80, "SANCTION LETTER")

    c.setFont("Helvetica", 12)
    y = height - 130
    lines = letter_text.split("\n")

    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.save()

    return {
        "letter_text": letter_text,
        "pdf_path": pdf_path
    }
