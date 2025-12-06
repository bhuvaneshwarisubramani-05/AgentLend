// frontend/agentlend/src/components/Chat.jsx
import { useState } from "react";
import axios from "axios";

export default function Chat() {
  const [msg, setMsg] = useState("");
  const [response, setResponse] = useState("");
  const [salary, setSalary] = useState(55000);
  const [creditScore, setCreditScore] = useState(720);
  const [emi, setEmi] = useState(5000);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!msg.trim()) {
      setResponse("Please type a message first!");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", {
        message: msg,
        salary,
        credit_score: creditScore,
        emi
      });
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error: Could not get a response from server.");
    } finally {
      setLoading(false);
      setMsg(""); // clear message after sending
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "10px",
        width: "350px",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "8px",
        fontFamily: "Arial, sans-serif",
        boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
      }}
    >
      <h2>AgentLend Chat</h2>

      {/* User Inputs */}
      <input
        type="number"
        value={salary}
        onChange={(e) => setSalary(Number(e.target.value))}
        placeholder="Salary"
      />
      <input
        type="number"
        value={creditScore}
        onChange={(e) => setCreditScore(Number(e.target.value))}
        placeholder="Credit Score"
      />
      <input
        type="number"
        value={emi}
        onChange={(e) => setEmi(Number(e.target.value))}
        placeholder="EMI"
      />

      {/* Message Input */}
      <input
        type="text"
        value={msg}
        onChange={(e) => setMsg(e.target.value)}
        placeholder="Ask about your loan..."
      />

      {/* Send Button */}
      <button
        onClick={sendMessage}
        disabled={loading}
        style={{
          padding: "8px 12px",
          cursor: loading ? "not-allowed" : "pointer",
          backgroundColor: "#4CAF50",
          color: "white",
          border: "none",
          borderRadius: "4px"
        }}
      >
        {loading ? "Sending..." : "Send"}
      </button>

      {/* Response */}
      {response && (
        <div
          style={{
            marginTop: "10px",
            padding: "10px",
            backgroundColor: "#f5f5f5",
            borderRadius: "4px",
            minHeight: "40px"
          }}
        >
          {response}
        </div>
      )}
    </div>
  );
}
