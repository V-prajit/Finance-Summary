import React, { useState } from "react";
import "./App.css";

const backendUrl = "http://localhost:3000"; // Make sure this is the correct URL for your Django server

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

  const onFileUpload = (): void => {
    const formData = new FormData();
    if (file) {
      formData.append("file", file);
    }

    fetch(`${backendUrl}/upload/`, {
      method: "POST",
      body: formData,
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data: UploadData) => {
        if (data.error) {
          alert("Error: " + data.error);
        } else {
          alert(
            "Success: " +
              data.message +
              " transactions_added:" +
              data.transactions_added +
              " errors:" +
              data.errors +
              " duplicates:" +
              data.duplicates
          );
        }
      })
      .catch((error) => alert("Error uploading file: " + error));
  };

  const handleLogin = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    fetch(`${backendUrl}/api/accounts/login/`, {
      method: "POST",
      body: formData,
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data: LoginData) => {
        if (data.success) {
          setIsLoggedIn(true);
        } else {
          alert("Login failed. Please check your credentials.");
        }
      })
      .catch((error) => alert("Error logging in: " + error));
  };

  const handleRegister = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    formData.append("email", email);

    fetch(`${backendUrl}/api/accounts/register/`, {
      method: "POST",
      body: formData,
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data: LoginData) => {
        if (data.success) {
          setIsLoggedIn(true);
          alert("Registration successful. You are now logged in.");
        } else {
          alert("Registration failed: " + data.error);
        }
      })
      .catch((error) => alert("Error registering: " + error));
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
    </div>
  );
};

export default App;
