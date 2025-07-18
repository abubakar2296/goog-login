import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Configure axios defaults
  axios.defaults.withCredentials = true;
  axios.defaults.baseURL = 'http://localhost:8000';

  const checkAuthStatus = async () => {
    try {
      const response = await axios.get('/api/auth-status');
      if (response.data.authenticated) {
        setUser(response.data.user);
      }
    } catch (error) {
      console.error('Auth status check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    window.location.href = 'http://localhost:8000/auth/google';
  };

  const logout = async () => {
    try {
      await axios.post('/api/logout');
      setUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const value = {
    user,
    loading,
    login,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 