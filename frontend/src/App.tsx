import React, { useState, useEffect } from "react";
import "./App.css";
import TransactionTable from "./Transactiontable";
import { login, logout, refreshToken, isTokenExpired, register } from "./auth"
import axios from 'axios';

const API_URL = "http://localhost:3000/api/";
const UPLOAD_URL = "http://localhost:3000/upload/";

interface LoginData {
  success: boolean;
  error?: string;
}

interface UploadData {
  error?: string;
  message?: string;
  transactions_added?: number;
  errors?: number;
  duplicates?: number;
}


const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [isRegistering, setIsRegistering] = useState<boolean>(false);

  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      setFile(files[0]);
    }
  };

  const onFileUpload = async (): Promise<void> => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const token = localStorage.getItem('access_token');
      if (token && isTokenExpired(token)) {
        const refreshed = await refreshToken();
        if (!refreshed) {
          throw new Error('Session expired. Please login again.');
        }
      }

      const response = await axios.post(`${UPLOAD_URL}`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`          
        }
      });
      const data: UploadData = response.data;
      alert(
        `Success: ${data.message} transactions_added: ${data.transactions_added} errors: ${data.errors} duplicates: ${data.duplicates}`
      );
    } catch (error) {
      alert("Error uploading file: " + (error as Error).message);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token && !isTokenExpired(token)) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    const success = await login(username, password);
    if (success) {
      setIsLoggedIn(true);
    } else {
      alert("Login failed. Please check your credentials.");
    }
  };

  const handleLogout = () => {
    logout();
    setIsLoggedIn(false);
  };

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    try{
      const success = await register(username, password, email);
      if (success) {
        setIsLoggedIn(true);
        alert("Registration successful. You are now logged in.");
      } else {
        alert("Registration failed. Please try again.");
      }
    } catch (error) {
      alert("Error registering: " + (error as Error).message);
    }
  };

  if (!isLoggedIn) {
    return (
      <div>
        <h1>{isRegistering ? "Register" : "Login"}</h1>
        <form onSubmit={isRegistering ? handleRegister : handleLogin}>
          <input
            type="text"
            value={username}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setUsername(e.target.value)
            }
            placeholder="Username"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setPassword(e.target.value)
            }
            placeholder="Password"
            required
          />
          {isRegistering && (
            <input
              type="email"
              value={email}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setEmail(e.target.value)
              }
              placeholder="Email"
              required
            />
          )}
          <button type="submit">{isRegistering ? "Register" : "Login"}</button>
        </form>
        <button onClick={() => setIsRegistering(!isRegistering)}>
          {isRegistering ? "Switch to Login" : "Switch to Register"}
        </button>
      </div>
    );
  }

  return (
    <div>
      <h1>Upload CSV File</h1>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>Upload!</button>
      <h2>Transactions</h2>
      <TransactionTable/>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default App;
