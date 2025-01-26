import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [authToken, setAuthToken] = useState(null);

  useEffect(() => {
    // Load token from localStorage if it exists
    const storedToken = localStorage.getItem('jwtToken');
    if (storedToken) {
      setAuthToken(storedToken);
    }
  }, []);

  const login = (token) => {
    setAuthToken(token);
    localStorage.setItem('jwtToken', token);
  };

  const logout = () => {
    setAuthToken(null);
    localStorage.removeItem('jwtToken');
  };

  return (
    <AuthContext.Provider value={{ authToken, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
