import './App.css';
import React, { useState } from "react";

const backendUrl = 'http://localhost:3000'; // Make sure this is the correct URL for your Django server

function App() {
  const [file, setFile] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  const onFileUpload = () => {
    const formData = new FormData();
    formData.append('file', file);

    fetch(`${backendUrl}/upload/`, {
      method: 'POST',
      body: formData,
      credentials: 'include',
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert('Error: '+ data.error);
      }
      else {
        alert('Success: ' + data.message +' transactions_added:' + data.transactions_added + ' errors:' + data.errors + ' duplicates:' + data.duplicates);
      }
    })
    .catch(error => alert('Error uploading file: '+error));
  };

  const handleLogin = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    fetch(`${backendUrl}/api/accounts/login/`, {
      method: 'POST',
      body: formData,
      credentials: 'include',
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        setIsLoggedIn(true);
      } else {
        alert('Login failed. Please check your credentials.');
      }
    })
    .catch(error => alert('Error logging in: '+error));
  };

  const handleRegister = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('email', email);

    fetch(`${backendUrl}/api/accounts/register/`, {
      method: 'POST',
      body: formData,
      credentials: 'include',
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        setIsLoggedIn(true);
        alert('Registration successful. You are now logged in.');
      } else {
        alert('Registration failed: ' + data.error);
      }
    })
    .catch(error => alert('Error registering: '+error));
  };

  if (!isLoggedIn) {
    return (
      <div>
        <h1>{isRegistering ? 'Register' : 'Login'}</h1>
        <form onSubmit={isRegistering ? handleRegister : handleLogin}>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
          {isRegistering && (
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              required
            />
          )}
          <button type="submit">{isRegistering ? 'Register' : 'Login'}</button>
        </form>
        <button onClick={() => setIsRegistering(!isRegistering)}>
          {isRegistering ? 'Switch to Login' : 'Switch to Register'}
        </button>
      </div>
    );
  }

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