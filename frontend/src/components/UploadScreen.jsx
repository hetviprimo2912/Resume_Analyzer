import UploadResume from "./UploadResume";
import "../styles/upload.css";

function UploadScreen({ onUploadSuccess }) {
  return (
    <div className="upload-page">
      <div className="upload-card">

        <div className="logo">
          🤖
        </div>

        <h1>AI Resume Analyzer</h1>

        <p>
          Upload your resume and start chatting with your AI assistant.
        </p>

        <UploadResume onUploadSuccess={onUploadSuccess} />

      </div>
    </div>
  );
}

export default UploadScreen;