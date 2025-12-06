from fastapi import FastAPI
from pydantic import BaseModel
from graph.loan_graph import loan_graph

app = FastAPI()

class Query(BaseModel):
    message: str
    salary: int
    credit_score: int
    emi: int

@app.post("/ask")
def ask_bot(q: Query):
    memory = {
        "salary": q.salary,
        "credit_score": q.credit_score,
        "emi": q.emi
    }
    
    result = loan_graph.invoke({
        "query": q.message,
        "memory": memory
    })

    return {"response": result["response"]}
