import './App.css';
import React, { useState } from "react";

const backendUrl = 'http://localhost:3000';

function App() {
  const [file, setFile] = useState(null);

  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  const onFileUpload = () => {
    const formData = new FormData();
    formData.append('file', file);

    fetch(`${backendUrl}/upload/`, {
      method: 'POST',
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert('Error: '+ data.error);
      }
      else {
        alert('Success: ' + data.message +' ' + data.transactions_added + ' ' + data.errors + ' ' + data.duplicates);
      }
    })
    .catch(error => alert('Error uploading file: '+error));
  };

  return (
    <div>
      <h1>Upload CSV File</h1>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>
        Upload!
      </button>
    </div>
  );
}

export default App;
