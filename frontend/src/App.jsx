import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);

  const suggestions = [
    "How can I volunteer?",
    "How can I donate?",
    "What programs does NayePankh run?",
    "How can I contact NayePankh?"
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const sendMessage = async (customMessage = null) => {
    const currentMessage = customMessage || message;

    if (!currentMessage.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: currentMessage,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: res.data.answer,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Unable to connect to the assistant.",
        },
      ]);

      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="chat-container">

        <div className="header">
          <h1>🕊️ NayePankh AI Assistant</h1>
        </div>

        <div className="messages">

          {messages.length === 0 && (
            <div className="welcome-screen">

              <div className="welcome-icon"></div>

              <h2>NayePankh AI Assistant</h2>

              <p>
                Ask me anything about volunteering,
                donations, programs, campaigns,
                and foundation activities.
              </p>

              <div className="suggestions">

                {suggestions.map((item, index) => (
                  <button
                    key={index}
                    className="suggestion-btn"
                    onClick={() => sendMessage(item)}
                  >
                    {item}
                  </button>
                ))}

              </div>
            </div>
          )}

          {messages.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender}`}
            >
              {msg.text}
            </div>
          ))}

          {loading && (
            <div className="message bot">
              Thinking...
            </div>
          )}

          <div ref={messagesEndRef}></div>

        </div>

        <div className="input-area">

          <input
            type="text"
            placeholder="Ask a question..."
            value={message}
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <button onClick={() => sendMessage()}>
            Send
          </button>

        </div>

      </div>
    </div>
  );
}

export default App;