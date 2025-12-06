from langchain_openai import ChatOpenAI
from agents.sales import sales_agent
from agents.verification import verification_agent
from agents.underwriting import underwriting_agent
from agents.sanction import sanction_agent

from config import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)


def master_agent(query, memory):
    """
    memory contains:
    {
        "salary": 50000,
        "credit_score": 750,
        "emi": 0
    }
    """
    
    intent_prompt = f"""
    You are a Master Router Agent.

    Categorize the user query into one of these:
    - sales
    - verification
    - underwriting
    - sanction
    - chat

    Query: {query}

    Give ONLY category name.
    """

    category = llm.invoke(intent_prompt).content.strip().lower()

    if "sales" in category:
        return sales_agent(query)
    if "verification" in category:
        return verification_agent(query)
    if "underwriting" in category:
        return underwriting_agent(memory)
    if "sanction" in category:
        # Pass the phone number (instead of "Customer") and eligible amount
        phone_number = memory.get("phone", "Unknown") 
        return sanction_agent(phone_number, memory.get("eligible_amount", 0))

    return "I can help with loan info, documents, eligibility, or sanction letters."
