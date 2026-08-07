import { useState } from "react";
import axios from "axios";
import "../styles/chat.css";

function ChatLayout({ resumeId }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      type: "ai",
      answer:
        "👋 Hello! Your resume has been analyzed successfully.\n\nAsk me anything about your resume.",
    },
  ]);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        answer: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/analyze/",
        {
          resume_id: resumeId,
          query: userQuestion,
        }
      );

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          answer: response.data.answer,
          confidence: response.data.confidence,
          sources: response.data.sources,
        },
      ]);
    } catch (err) {
        console.error(err);

        setMessages((prev) => [
            ...prev,
            {
            type: "ai",
            answer: "Something went wrong while analyzing the resume.",
            },
        ]);
    }

    setLoading(false);
  };

    return (

    <div className="chat-container">

        <div className="chat-header">

        <div>
          <h2>🤖 AI Resume Analyzer</h2>
          <p>Your resume is ready for questions.</p>
        </div>
            <button
            className="new-resume-btn"
            onClick={() => window.location.reload()}
            >
            Upload New Resume
            </button>

      </div>

      <div className="chat-body">

        {messages.map((msg, index) => (

          <div
            key={index}
            className={
              msg.type === "user"
                ? "user-message"
                : "ai-message"
            }
          >

            <div className="bubble">

              <p>{msg.answer}</p>

              {msg.confidence && (
                <small>
                  Confidence : {msg.confidence}%
                </small>
              )}

              {msg.sources && (
                <div className="sources">

                  <strong>Sources</strong>

                  {msg.sources.map((src, i) => (

                    <div key={i} className="source-card">

                      <b>{src.section}</b>

                      <br />

                      {src.subsection}

                    </div>

                  ))}

                </div>
              )}

            </div>

          </div>

        ))}

        {loading && (

          <div className="ai-message">

            <div className="bubble">

              <div className="typing">
                <span></span>
                <span></span>
                <span></span>
              </div>

            </div>

          </div>

        )}

      </div>

      <div className="chat-input">

        <textarea
          placeholder="Ask anything about the resume..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button onClick={askQuestion}>
          Send
        </button>

      </div>

    </div>
  );
}

export default ChatLayout;