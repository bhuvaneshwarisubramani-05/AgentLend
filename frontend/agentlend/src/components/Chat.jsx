import React, { useState, useRef, useEffect } from "react";
import "./chat.css";
import { sendMessage } from "../services/api";
import logo from "../assets/agentlend_logo.png";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [memory, setMemory] = useState({});
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef();

  const handleSend = async () => {
    if (!text.trim()) return;

    const userMsg = { sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setText("");
    setLoading(true);

    try {
      const res = await sendMessage(userMsg.text, memory);

      let botMsg = { sender: "bot", text: res.response.text };

      if (res.response.pdf_url) botMsg.pdf_url = res.response.pdf_url;

      setMessages((prev) => [...prev, botMsg]);
      setMemory(res.memory);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error. Try again." },
      ]);
    }

    setLoading(false);
  };

  useEffect(() => {
    // Scroll to the bottom whenever messages change
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-container">

      {/* HEADER WITH LOGO (Updated Design) */}
      <div className="chat-header">
        <img src={logo} className="logo" alt="AgentLend" />
        <div className="header-text">
          <h2>AGENTLEND</h2>
          <p className="tagline">Your Smart AI Loan Assistant</p>
        </div>
      </div>

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`bubble ${msg.sender}`}>

            {/* Bot Avatar */}
            {msg.sender === "bot" && (
              <img className="avatar" src={logo} alt="bot" />
            )}

            {/* Message Content Container (Required for stacking text and button) */}
            <div className="message-content">
              {/* Message Text */}
              <div className="msg-text">{msg.text}</div>

              {/* PDF Button */}
              {msg.pdf_url && (
                <a
                  href={`http://127.0.0.1:8000${msg.pdf_url}`}
                  className="pdf-button"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  📄 Download Sanction Letter
                </a>
              )}
            </div>
          </div>
        ))}

        {loading && <div className="typing">AgentLend is typing...</div>}
        <div ref={scrollRef}></div>
      </div>

      <div className="input-box">
        <input
          placeholder="Type your message..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend} disabled={loading}>Send</button>
      </div>
    </div>
  );
}