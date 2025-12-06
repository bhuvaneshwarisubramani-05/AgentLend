from langchain_openai import ChatOpenAI

from config import OPENAI_API_KEY

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

def verification_agent(query):
    prompt = f"""
    You are a Document Verification Agent.
    Explain required documents, check if provided details are complete.

    User query: {query}
    """
    return llm.invoke(prompt).content
