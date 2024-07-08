import React, { useState } from "react";

const FileUploader: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const backendUrl = "http://localhost:8000"; // Adjust this URL to match your Django server URL

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setFile(files[0]);
    }
  };

  const handleFileUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(`${backendUrl}/upload/`, {
          method: "POST",
          body: formData,
          credentials: "include", // Include cookies for CSRF and session handling
        });
        const data = await response.json();
        if (response.ok) {
          alert(`Success: ${data.message}`);
        } else {
          alert(`Error: ${data.error}`);
        }
      } catch (error) {
        alert("Error uploading file: " + error);
      }
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload File</button>
    </div>
  );
};

export default FileUploader;
