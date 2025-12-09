from fastapi import FastAPI
from fastapi.responses import FileResponse   # <-- ADD THIS
from pydantic import BaseModel
from graph.loan_graph import loan_graph
import os   # <-- ADD THIS



app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    memory: dict  # frontend will store & send this every turn

@app.post("/chat")
def chat_api(req: ChatRequest):
    result = loan_graph.invoke({
        "query": req.message,
        "memory": req.memory
    })

    # result["response"] is already structured JSON from master_agent
    return {
        "response": result["response"],
        "memory": result["memory"]
    }
@app.get("/download/{phone}")
def download_sanction_letter(phone: str):
    pdf_path = f"pdfs/sanction_{phone}.pdf"
    if not os.path.exists(pdf_path):
        return {"error": "PDF not generated yet"}

    return FileResponse(
        path=pdf_path,
        filename=f"sanction_letter_{phone}.pdf",
        media_type="application/pdf"
    )
