from langchain_openai import ChatOpenAI
from graph.loan_graph import loan_graph

import os


api_key = os.getenv("OPENAI_API_KEY")

# Example if loan_graph uses ChatOpenAI internally
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)

# -----------------------------------------------------
# ADDED PHONE NUMBER TO MEMORY FOR DATABASE LOOKUPS
# NOTE: Replace '9999988888' with a phone number that 
# exists in your MySQL (preapproved_limits) and 
# MongoDB (customers) tables for testing.
# -----------------------------------------------------
memory = {
    "salary": 55000,
    "credit_score": 720,
    "emi": 5000,
    "eligible_amount": 1100000,
    "phone": "9999988888" 
}
# -----------------------------------------------------

while True:
    try:
        user_input = input("You: ")
        
        # Check for exit commands
        if user_input.lower() in ['exit', 'quit']:
            print("Session ended.")
            break

        result = loan_graph.invoke(
            {
            "query": user_input,
            "memory": memory,
            "llm": llm # pass the LLM with the api_key
            }
        )

        # Update the memory state with any changes made by the agents
        # (e.g., if the underwriting agent sets a new eligible_amount from the DB)
        if 'memory' in result:
             memory.update(result['memory'])

        print("\nAI:", result["response"], "\n")

    except Exception as e:
        # Catch any errors during graph invocation (e.g., database connection failure)
        print(f"\nAn error occurred: {e}\n")