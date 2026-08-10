import { useState } from "react";
import axios from "axios";

function UploadResume({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF.");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {
      setUploading(true);

      const response = await axios.post(
        "http://localhost:8000/upload/",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      onUploadSuccess(response.data.resume_id);
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files[0])
        }
      />

      <button
        className="upload-btn"
        disabled={uploading}
        onClick={handleUpload}
      >
        {uploading
          ? "Analyzing Resume..."
          : "Upload & Analyze Resume"}
      </button>
    </div>
  );
}

export default UploadResume;