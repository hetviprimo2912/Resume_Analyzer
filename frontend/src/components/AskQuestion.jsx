import { useState } from "react";
import axios from "axios";

function AskQuestion({ resumeId }) {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const [answer, setAnswer] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [sources, setSources] = useState([]);

  const askQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question.");
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze/",
        {
          resume_id: resumeId,
          query: question,
          top_k: 3,
        }
      );

      setAnswer(response.data.answer);
      setConfidence(response.data.confidence);
      setSources(response.data.sources || []);
    } catch (error) {
      console.error(error);
      alert("Failed to analyze resume.");
    }

    setLoading(false);
  };

  return (
    <div style={{ marginTop: "40px" }}>
      <h2>Ask AI</h2>

      <textarea
        rows={4}
        placeholder="Ask anything about the resume..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "15px",
        }}
      />

      <button onClick={askQuestion} disabled={loading}>
        {loading ? "Thinking..." : "Ask AI"}
      </button>

      {answer && (
        <div style={{ marginTop: "30px" }}>
          <h3>Answer</h3>

          <p>{answer}</p>

          <h4>Confidence</h4>

          <p>{confidence}%</p>

          <h4>Sources</h4>

          {sources.map((source, index) => (
            <div
              key={index}
              style={{
                border: "1px solid #ddd",
                padding: "10px",
                marginBottom: "10px",
              }}
            >
              <strong>{source.section}</strong>

              {source.subsection && (
                <>
                  <br />
                  {source.subsection}
                </>
              )}

              <br />

              Page {source.page}

              <br />
              <br />

              {source.preview}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AskQuestion; 