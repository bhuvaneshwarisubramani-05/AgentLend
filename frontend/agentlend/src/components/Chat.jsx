import React, { useState, useRef, useEffect } from "react";
import "./chat.css";
import { sendMessage } from "../services/api";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [memory, setMemory] = useState({});
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef();

  const handleSend = async () => {
    if (!text.trim()) return;

    const userMsg = { sender: "user", text };
    setMessages(prev => [...prev, userMsg]);
    setText("");
    setLoading(true);

    try {
      const res = await sendMessage(userMsg.text, memory);

      let botMsg = { sender: "bot", text: res.response.text };

      // ⭐ ADD SANCTION LETTER BUTTON IF AVAILABLE
      if (res.response.pdf_url) {
        botMsg.pdf_url = res.response.pdf_url;
      }

      setMessages(prev => [...prev, botMsg]);
      setMemory(res.memory);

    } catch (error) {
      setMessages(prev => [
        ...prev,
        { sender: "bot", text: "⚠️ Server error, please try again." }
      ]);
    }

    setLoading(false);
  };

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-container">

      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`bubble ${msg.sender === "user" ? "right" : "left"}`}>

            {/* NORMAL CHAT TEXT */}
            {msg.text}

            {/* ⭐ DOWNLOAD SANCTION LETTER BUTTON */}
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
        ))}

        {loading && <div className="typing">AgentLend is typing...</div>}

        <div ref={scrollRef}></div>
      </div>

      <div className="input-box">
        <input
          placeholder="Type your message..."
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>

    </div>
  );
}
