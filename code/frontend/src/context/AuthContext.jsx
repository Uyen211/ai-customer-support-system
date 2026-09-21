import React, { createContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';
import { staffService } from '../services/staffService';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  // Dùng sessionStorage thay vì localStorage → mỗi tab có session riêng
  const [token, setToken] = useState(() => sessionStorage.getItem('token') || null);
  const [user, setUser] = useState(() => {
    const saved = sessionStorage.getItem('user');
    return saved ? JSON.parse(saved) : null;
  });
  const [accountType, setAccountType] = useState(() => sessionStorage.getItem('accountType') || 'CUSTOMER');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function initAuth() {
      if (token) {
        try {
          const meData = accountType === 'STAFF' ? await staffService.getMe() : await authService.getMe();
          setUser(meData);
          sessionStorage.setItem('user', JSON.stringify(meData));
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
    sessionStorage.setItem('token', newToken);
    sessionStorage.setItem('user', JSON.stringify(userData));
    sessionStorage.setItem('accountType', type);
    setToken(newToken);
    setUser(userData);
    setAccountType(type);
  };

  const logout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    sessionStorage.removeItem('accountType');
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
