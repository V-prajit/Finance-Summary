import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const API_URL = "/api/";

export const setAuthToken = (token:string) => {
    if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        delete axios.defaults.headers.common['Authorization'];
    }
};

export const login = async (username: string, password: string) => {
    try {
        const response = await axios.post(`${API_URL}accounts/login/`, { username, password });
        const { access, refresh } = response.data;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        setAuthToken(access);
        return true;
    } catch (error) {
        console.error('Login error: ', error);
        return false;
    }
};

export const register = async (username: string, password: string, email: string) => {
    try {
        const response = await axios.post(`${API_URL}accounts/register/`, 
            { username, password, email },
            {
                headers: { 'Content-Type': 'application/json' },
                withCredentials: true
            }
          );
        if (response.data.success) {
        return await login(username, password);
      }
      return false;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

export const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setAuthToken('');
};

export const refreshToken = async() => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        const response = await axios.post(`${API_URL}token/refresh/`, { refresh: refreshToken });
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        setAuthToken(access);
        return true;
      } catch (error) {
        console.error('Token refresh error:', error);
        logout();
        return false;
      }
    }
    return false;
};

export const isTokenExpired = (token: string) => {
    try {
      const decoded: any = jwtDecode(token);
      if (decoded.exp < Date.now() / 1000) {
        return true;
      }
      return false;
    } catch (error) {
      return true;
    }
  };
