import React, { createContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { staffService } from '../services/staffService';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token') || null);
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('user');
    return saved ? JSON.parse(saved) : null;
  });
  const [accountType, setAccountType] = useState(() => localStorage.getItem('accountType') || 'CUSTOMER');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function initAuth() {
      if (token) {
        try {
          const meData = accountType === 'STAFF' ? await staffService.getMe() : await authService.getMe();
          setUser(meData);
          localStorage.setItem('user', JSON.stringify(meData));
        } catch (error) {
          console.error("Auth verification failed:", error);
          logout();
        }
      }
      setLoading(false);
    }
    initAuth();
  }, [token, accountType]);

  const login = (newToken, userData, type = 'CUSTOMER') => {
    localStorage.setItem('token', newToken);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('accountType', type);
    setToken(newToken);
    setUser(userData);
    setAccountType(type);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('accountType');
    setToken(null);
    setUser(null);
    setAccountType('CUSTOMER');
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        accountType,
        isLoggedIn: !!token,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
