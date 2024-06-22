import './App.css';
import React, { useState } from "react";

const backendUrl = 'http://localhost:3000';

function App() {
  const [file, setFile] = useState(null);
  const [getResponse, setGetResponse] = useState(null);

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
        alert('Success: ' + data.message);
      }
    })
    .catch(error => alert('Error uploading file: '+error));
  };

  const testGetRequest = () => {
    fetch(`${backendUrl}/test/`, {
      method: 'GET',
    })
    .then(response => response.text())
    .then(data => {
      setGetResponse(data);
    })
    .catch(error => alert('Error with GET request: ' + error));
  };


  return (
    <div>
      <h1>Upload CSV File</h1>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>
        Upload!
      </button>
      <br /><br />
      <button onClick={testGetRequest}>
        Test GET Request
      </button>
      {getResponse && (
        <div>
          <h2>GET Response:</h2>
          <p>{getResponse}</p>
        </div>
      )}
    </div>
  );
}

export default App;
