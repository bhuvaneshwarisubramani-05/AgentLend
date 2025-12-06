from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from database.mysql import get_interest_rate # <-- NEW IMPORT

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

def sales_agent(query):
    # 1. Check if the query asks for the interest rate
    if "interest rate" in query.lower() or "rate" in query.lower():
        try:
            db_rate = get_interest_rate()
            # Craft a prompt that forces the LLM to use the accurate rate
            prompt_modifier = f"Our current official personal loan interest rate is {db_rate:.2f}%. Answer the user's query about interest rates and product details, ensuring you prominently feature this specific rate."
        except Exception as e:
            print(f"MySQL DB Error during interest rate lookup: {e}")
            prompt_modifier = "Our official rate is temporarily unavailable. Answer the user's query about interest rates and product details using general knowledge."
    else:
        prompt_modifier = ""
        
    prompt = f"""
    You are a Sales Loan Officer Agent.
    Provide loan product details in SIMPLE terms.

    {prompt_modifier}

    User query: {query}
    """
    return llm.invoke(prompt).content