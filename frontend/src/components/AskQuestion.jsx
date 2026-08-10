import { useState } from "react";
import axios from "axios";

function AskQuestion({ resumeId }) {
  const [question, setQuestion] = useState("");
  const [askedQuestion, setAskedQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const [answer, setAnswer] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [sources, setSources] = useState([]);

  const askQuestion = async () => {
    if (!question.trim() || loading) {
      return;
    }

    const currentQuestion = question.trim();
    setAskedQuestion(currentQuestion);

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze/",
        {
          resume_id: resumeId,
          query: currentQuestion,
          top_k: 3,
        }
      );

      setAnswer(response.data.answer);
      setConfidence(response.data.confidence);
      setSources(response.data.sources || []);
      setQuestion("");
    } catch (error) {
      console.error(error);
      alert("Failed to analyze resume.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      askQuestion();
    }
  };

  const getConfidenceLevel = (score) => {
    if (score >= 80) {
      return {
        label: "High confidence",
        className: "confidence-high",
      };
    }

    if (score >= 50) {
      return {
        label: "Moderate confidence",
        className: "confidence-medium",
      };
    }

    return {
      label: "Low confidence",
      className: "confidence-low",
    };
  };

  const formatSourceName = (section) => {
    if (!section) {
      return "Resume";
    }

    const normalized = section
      .replace(/\s+/g, " ")
      .trim();

    const compact = normalized.replace(/\s/g, "").toUpperCase();

    const sourceNames = {
      ABOUTME: "About Me",
      ABOUT: "About Me",
      PROJECT: "Projects",
      PROJECTS: "Projects",
      SKILL: "Skills",
      SKILLS: "Skills",
      EDUCATION: "Education",
      CONTACT: "Contact",
      EMAIL: "Contact",
      PHONE: "Contact",
      LINKEDIN: "Contact",
      GITHUB: "Contact",
      ADDRESS: "Contact",
      EXPERIENCE: "Experience",
      SUMMARY: "Summary",
      PROFILE: "Profile",
    };

    if (sourceNames[compact]) {
      return sourceNames[compact];
    }

    // Handles values such as:
    // "H E T V I P R A J A P A T I"
    if (/^[A-Z](\s[A-Z])+$/i.test(normalized)) {
      return normalized.replace(/\s+/g, "");
    }

    return normalized
      .toLowerCase()
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const confidenceInfo =
    confidence !== null
      ? getConfidenceLevel(confidence)
      : null;

  return (
    <div className="resume-chat">
      {/* ------------------------------------------------ */}
      {/* Chat Header */}
      {/* ------------------------------------------------ */}

      <div className="resume-chat-header">
        <div className="resume-chat-brand">
          <div className="resume-chat-logo">
            🤖
          </div>

          <div>
            <h2>AI Resume Analyzer</h2>
            <p>Ask anything about your resume</p>
          </div>
        </div>

        <div className="resume-status">
          <span className="status-dot"></span>
          Resume ready
        </div>
      </div>

      {/* ------------------------------------------------ */}
      {/* Conversation */}
      {/* ------------------------------------------------ */}

      <div className="resume-chat-content">
        {!answer && !loading && (
          <div className="resume-welcome">
            <div className="welcome-icon">👋</div>

            <h3>Your resume is ready</h3>

            <p>
              Ask me about your experience, skills, projects,
              education, or anything else in your resume.
            </p>

            <div className="suggestion-list">
              <button
                type="button"
                onClick={() =>
                  setQuestion("What is the candidate's name?")
                }
              >
                What is the candidate's name?
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "What programming languages does the candidate know?"
                  )
                }
              >
                What programming languages are listed?
              </button>

              <button
                type="button"
                onClick={() =>
                  setQuestion(
                    "What projects has the candidate built?"
                  )
                }
              >
                What projects has the candidate built?
              </button>
            </div>
          </div>
        )}

        {/* User question */}

        {answer && (
          <div className="message-row message-row-user">
            <div className="user-message">
                  {askedQuestion}
            </div>
          </div>
        )}

        {/* AI answer */}

        {loading && (
          <div className="message-row message-row-ai">
            <div className="ai-answer-card loading-card">
              <div className="thinking-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>

              <span>Analyzing your resume...</span>
            </div>
          </div>
        )}

        {answer && !loading && (
          <div className="message-row message-row-ai">
            <div className="ai-answer-card">
              <div className="answer-label">
                <span className="answer-icon">✦</span>
                AI Answer
              </div>

              <div className="answer-text">
                {answer}
              </div>

              {/* Confidence */}

              {confidence !== null && confidenceInfo && (
                <div
                  className={`confidence-badge ${confidenceInfo.className}`}
                >
                  <span className="confidence-dot"></span>

                  <span>{confidenceInfo.label}</span>

                  <span className="confidence-score">
                    {confidence}%
                  </span>
                </div>
              )}

              {/* Sources */}

              {sources.length > 0 && (
                <div className="evidence-section">
                  <div className="evidence-header">
                    <div>
                      <span className="evidence-icon">◈</span>
                      Evidence
                    </div>

                    <span className="evidence-count">
                      {sources.length}
                    </span>
                  </div>

                  <div className="evidence-list">
                    {sources.map((source, index) => {
                      const sourceName = formatSourceName(
                        source.section
                      );

                      return (
                        <div
                          className="evidence-card"
                          key={index}
                        >
                          <div className="evidence-card-icon">
                            {sourceName === "Projects"
                              ? "⌘"
                              : sourceName === "Skills"
                              ? "✦"
                              : sourceName === "Education"
                              ? "🎓"
                              : sourceName === "Contact"
                              ? "⌁"
                              : "◉"}
                          </div>

                          <div className="evidence-card-content">
                            <div className="evidence-card-title">
                              {sourceName}
                            </div>

                            {source.subsection && (
                              <div className="evidence-card-subtitle">
                                {source.subsection}
                              </div>
                            )}

                            {source.page && (
                              <div className="evidence-card-meta">
                                Page {source.page}
                              </div>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* ------------------------------------------------ */}
      {/* Input */}
      {/* ------------------------------------------------ */}

      <div className="resume-chat-input-area">
        <div className="resume-input-wrapper">
          <textarea
            rows={1}
            placeholder="Ask anything about the resume..."
            value={question}
            onChange={(event) =>
              setQuestion(event.target.value)
            }
            onKeyDown={handleKeyDown}
            disabled={loading}
          />

          <button
            type="button"
            className="send-button"
            onClick={askQuestion}
            disabled={loading || !question.trim()}
          >
            {loading ? (
              <span className="button-loader"></span>
            ) : (
              <>
                Send
                <span className="send-arrow">↗</span>
              </>
            )}
          </button>
        </div>

        <div className="input-hint">
          Press Enter to ask · Shift + Enter for a new line
        </div>
      </div>
    </div>
  );
}

export default AskQuestion;