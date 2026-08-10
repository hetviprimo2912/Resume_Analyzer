import { useState } from "react";
import axios from "axios";
import "../styles/chat.css";

function ChatLayout({ resumeId }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  // Job Description
  const [showJDModal, setShowJDModal] = useState(false);
  const [jobDescription, setJobDescription] = useState("");
  const [jdFile, setJdFile] = useState(null);
  const [analyzingJD, setAnalyzingJD] = useState(false);

  // ATS
  const [atsData, setAtsData] = useState(null);

  const [messages, setMessages] = useState([
    {
      type: "ai",
      answer:
        "👋 Your resume has been analyzed successfully. Ask me anything about your resume.",
    },
  ]);

  // --------------------------------------------------
  // Ask Resume Question
  // --------------------------------------------------

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
    } finally {
      setLoading(false);
    }
  };

  // --------------------------------------------------
  // Analyze Job Description
  // --------------------------------------------------

  const analyzeJobDescription = async () => {
    if (!jobDescription.trim() && !jdFile) {
      alert("Please paste a job description or upload a PDF.");
      return;
    }

    setAnalyzingJD(true);

    try {
      const formData = new FormData();

      formData.append("resume_id", resumeId);

      if (jobDescription.trim()) {
        formData.append(
          "job_description",
          jobDescription
        );
      }

      if (jdFile) {
        formData.append("file", jdFile);
      }

      const response = await axios.post(
        "http://localhost:8000/job-description/analyze",
        formData
      );

      setAtsData(response.data);

      setShowJDModal(false);

      setJobDescription("");
      setJdFile(null);

    } catch (error) {
      console.error(error);

      const message =
        error.response?.data?.detail ||
        "Failed to analyze job description.";

      alert(message);
    } finally {
      setAnalyzingJD(false);
    }
  };

  // --------------------------------------------------
  // Enter to send
  // --------------------------------------------------

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <>
      <div className="chat-container">

        {/* ================================================= */}
        {/* HEADER */}
        {/* ================================================= */}

        <div className="chat-header">

          <div className="brand-area">

            <div className="brand-icon">
              🤖
            </div>

            <div>
              <h2>AI Resume Analyzer</h2>

              <p>
                Resume analyzed and ready
              </p>
            </div>

          </div>

          <button
            className="new-resume-btn"
            onClick={() => window.location.reload()}
          >
            + New Resume
          </button>

        </div>


        {/* ================================================= */}
        {/* MAIN CONTENT */}
        {/* ================================================= */}

        <div className="chat-body">

          {/* ================================================= */}
          {/* RESUME OVERVIEW */}
          {/* ================================================= */}

          <section className="resume-overview">

            <div className="section-heading">

              <div>
                <h3>Resume Overview</h3>

                <p>
                  Quick insights from your uploaded resume
                </p>
              </div>

            </div>


            <div className="overview-grid">

              {/* Resume Summary */}

              <div className="overview-card summary-card">

                <div className="card-icon">
                  ✦
                </div>

                <span className="card-label">
                  RESUME SUMMARY
                </span>

                <h4>
                  Resume analyzed successfully
                </h4>

                <p>
                  Your resume is indexed and ready.
                  Ask questions about your experience,
                  skills, projects, education, and more.
                </p>

              </div>


              {/* ATS */}

              <div className="overview-card ats-card">

                <div className="card-icon">
                  ◈
                </div>

                <span className="card-label">
                  ATS READINESS
                </span>

                {atsData ? (
                  <>
                    <div className="ats-score">
                      {atsData.ats_score}
                      <span>/100</span>
                    </div>

                    <div className="score-bar">
                      <div
                        className="score-fill"
                        style={{
                          width: `${atsData.ats_score}%`,
                        }}
                      />
                    </div>

                    <p>
                      {atsData.match_percentage}% match
                      with the provided job description.
                    </p>
                  </>
                ) : (
                  <>
                    <div className="ats-score empty">
                      --
                    </div>

                    <p>
                      Add a job description to calculate
                      your ATS score and job match.
                    </p>
                  </>
                )}

                <button
                  className="add-jd-btn"
                  onClick={() => setShowJDModal(true)}
                >
                  + {atsData
                    ? "Update Job Description"
                    : "Add Job Description"}
                </button>

              </div>


              {/* Improvement Areas */}

              <div className="overview-card improvement-card">

                <div className="card-icon">
                  ↗
                </div>

                <span className="card-label">
                  KEY IMPROVEMENT AREAS
                </span>

                <div className="improvement-list">

                  {atsData?.feedback?.areas_to_improve?.length ? (

                    atsData.feedback.areas_to_improve.map(
                      (item, index) => (
                        <div
                          className="improvement-item"
                          key={index}
                        >
                          <span>
                            {String(index + 1).padStart(2, "0")}
                          </span>

                          <p>{item}</p>
                        </div>
                      )
                    )

                  ) : (

                    <>
                      <div className="improvement-item">
                        <span>01</span>
                        <p>Quantify project achievements</p>
                      </div>

                      <div className="improvement-item">
                        <span>02</span>
                        <p>Highlight measurable impact</p>
                      </div>

                      <div className="improvement-item">
                        <span>03</span>
                        <p>
                          Add relevant keywords for target roles
                        </p>
                      </div>
                    </>

                  )}

                </div>

              </div>

            </div>

          </section>


          {/* ================================================= */}
          {/* ATS RESULTS */}
          {/* ================================================= */}

          {atsData && (

            <section className="ats-results">

              <div className="results-header">
                <div>
                  <h3>Job Match Analysis</h3>
                  <p>
                    How your resume compares with the job description
                  </p>
                </div>

                <div className="match-badge">
                  {atsData.match_percentage}% Match
                </div>
              </div>


              <div className="skills-grid">

                {/* Matched */}

                <div className="skill-panel matched-panel">

                  <div className="skill-panel-title">
                    <span className="success-icon">
                      ✓
                    </span>

                    Matching Skills
                  </div>

                  <div className="skill-tags">

                    {atsData.matched_skills.map(
                      (skill, index) => (
                        <span
                          className="skill-tag matched"
                          key={index}
                        >
                          ✓ {skill}
                        </span>
                      )
                    )}

                  </div>

                </div>


                {/* Missing */}

                <div className="skill-panel missing-panel">

                  <div className="skill-panel-title">
                    <span className="missing-icon">
                      !
                    </span>

                    Missing Skills
                  </div>

                  <div className="skill-tags">

                    {atsData.missing_skills.length > 0 ? (

                      atsData.missing_skills.map(
                        (skill, index) => (
                          <span
                            className="skill-tag missing"
                            key={index}
                          >
                            × {skill}
                          </span>
                        )
                      )

                    ) : (

                      <span className="no-missing">
                        No major missing skills detected.
                      </span>

                    )}

                  </div>

                </div>

              </div>


              {/* Feedback */}

              <div className="feedback-card">

                <div className="feedback-title">
                  <span>✦</span>
                  Resume Feedback
                </div>


                <div className="feedback-columns">

                  <div>
                    <h4>Strengths</h4>

                    {atsData.feedback.strengths.map(
                      (item, index) => (
                        <div
                          className="feedback-item positive"
                          key={index}
                        >
                          <span>✓</span>
                          {item}
                        </div>
                      )
                    )}
                  </div>


                  <div>
                    <h4>Areas to improve</h4>

                    {atsData.feedback.areas_to_improve.map(
                      (item, index) => (
                        <div
                          className="feedback-item"
                          key={index}
                        >
                          <span>•</span>
                          {item}
                        </div>
                      )
                    )}
                  </div>


                  <div>
                    <h4>Suggestions</h4>

                    {atsData.feedback.suggestions.map(
                      (item, index) => (
                        <div
                          className="feedback-item"
                          key={index}
                        >
                          <span>→</span>
                          {item}
                        </div>
                      )
                    )}
                  </div>

                </div>

              </div>

            </section>

          )}


          {/* ================================================= */}
          {/* CHAT */}
          {/* ================================================= */}

          <section className="resume-chat">

            <div className="chat-section-header">

              <div>
                <h3>
                  Chat with your resume
                </h3>

                <p>
                  Ask questions about your experience,
                  skills and projects.
                </p>
              </div>

              <div className="ai-status">
                <span />
                AI Ready
              </div>

            </div>


            <div className="messages">

              {messages.map((msg, index) => (

                <div
                  key={index}
                  className={
                    msg.type === "user"
                      ? "user-message"
                      : "ai-message"
                  }
                >

                  {msg.type === "ai" && (
                    <div className="message-avatar">
                      ✦
                    </div>
                  )}

                  <div className="message-content">

                    <span className="message-label">
                      {msg.type === "user"
                        ? "You"
                        : "AI Assistant"}
                    </span>

                    <div className="bubble">
                      {msg.answer}
                    </div>

                  </div>

                </div>

              ))}


              {loading && (

                <div className="ai-message">

                  <div className="message-avatar">
                    ✦
                  </div>

                  <div className="message-content">

                    <span className="message-label">
                      AI Assistant
                    </span>

                    <div className="bubble">

                      <div className="typing">
                        <span />
                        <span />
                        <span />
                      </div>

                    </div>

                  </div>

                </div>

              )}

            </div>

          </section>

        </div>


        {/* ================================================= */}
        {/* INPUT */}
        {/* ================================================= */}

        <div className="chat-input-wrapper">

          <div className="chat-input">

            <textarea
              placeholder="Ask anything about your resume..."
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={handleKeyDown}
              rows={1}
            />

            <button
              onClick={askQuestion}
              disabled={loading}
            >
              {loading ? "..." : "Send ↑"}
            </button>

          </div>

          <div className="input-hint">
            Press Enter to send · Shift + Enter for a new line
          </div>

        </div>

      </div>


      {/* ================================================= */}
      {/* JOB DESCRIPTION MODAL */}
      {/* ================================================= */}

      {showJDModal && (

        <div
          className="modal-overlay"
          onClick={() => setShowJDModal(false)}
        >

          <div
            className="jd-modal"
            onClick={(e) => e.stopPropagation()}
          >

            <div className="modal-header">

              <div>
                <h3>
                  Add Job Description
                </h3>

                <p>
                  Compare your resume against a target role.
                </p>
              </div>

              <button
                className="modal-close"
                onClick={() =>
                  setShowJDModal(false)
                }
              >
                ×
              </button>

            </div>


            <label className="modal-label">
              Paste Job Description
            </label>

            <textarea
              className="jd-textarea"
              placeholder="Looking for a React Developer with experience in..."
              value={jobDescription}
              onChange={(e) =>
                setJobDescription(e.target.value)
              }
            />


            <div className="or-divider">
              <span>OR</span>
            </div>


            <label className="upload-jd-box">

              <input
                type="file"
                accept=".pdf"
                onChange={(e) =>
                  setJdFile(
                    e.target.files?.[0] || null
                  )
                }
              />

              <div className="upload-jd-icon">
                ↑
              </div>

              <strong>
                {jdFile
                  ? jdFile.name
                  : "Upload Job Description PDF"}
              </strong>

              <span>
                PDF files only
              </span>

            </label>


            <div className="modal-actions">

              <button
                className="cancel-btn"
                onClick={() =>
                  setShowJDModal(false)
                }
              >
                Cancel
              </button>

              <button
                className="analyze-jd-btn"
                onClick={analyzeJobDescription}
                disabled={analyzingJD}
              >
                {analyzingJD
                  ? "Analyzing..."
                  : "Analyze Resume"}
              </button>

            </div>

          </div>

        </div>

      )}

    </>
  );
}

export default ChatLayout;