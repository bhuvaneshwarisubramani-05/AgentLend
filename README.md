# 🏦 AgentLend — AI-Driven Loan Assistance Platform

AgentLend is a smart Agentic AI lending system that automates end-to-end personal loan processing for NBFCs.  
It uses a Master Agent and multiple Worker Agents to handle:

- 💬 **Loan conversation**  
- 🪪 **KYC verification**  
- 📊 **Credit evaluation**  
- 📈 **EMI visualization**  
- ⚖️ **Fairness & explainability**  
- 📄 **Sanction letter generation**

Built with **FastAPI**, **React**, **LangFlow**, **Groq LLM**, **MongoDB Atlas**, and **MySQL**.

---

## 🚀 Tech Stack

### **Frontend**
- React  
- Vite  
- CSS

### **Backend**
- FastAPI  
- LangFlow  
- Groq LLM  
- ReportLab (PDF generation)  
- python-dotenv

### **Databases**
- MongoDB Atlas (CRM / KYC)  
- MySQL (loan + underwriting data)

---

## 🧠 Agent Architecture

### **Master Agent**
Controls the conversation flow and orchestrates worker agents.

### **Worker Agents**
- **Sales Agent** — collects loan details & negotiates terms  
- **Verification Agent** — checks KYC (MongoDB)  
- **Underwriting Agent** — evaluates eligibility (MySQL rules)  
- **Fair Check Agent** — bias detection & explainability  
- **EMI View Agent** — computes EMI & shows chart  
- **Loan Guide Agent** — suggests alternate offers  
- **Sanction Agent** — generates sanction letters (PDF)

---

##  Setup (Quick)
```bash
Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

Frontend
cd frontend
npm install
npm run dev
