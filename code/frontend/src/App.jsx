import React, { useState, Component } from 'react';
import { AuthProvider } from './context/AuthContext';
import { useAuth } from './hooks/useAuth';
import { LandingPage } from './pages/customer/LandingPage';
import { CustomerLogin } from './pages/auth/CustomerLogin';
import { CustomerRegister } from './pages/auth/CustomerRegister';
import { StaffLogin } from './pages/auth/StaffLogin';
import { ChatPage } from './pages/customer/ChatPage';
import { StaffConsole } from './pages/admin/StaffConsole';
import AlertConfigPage from './pages/admin/AlertConfigPage';
import { KanbanPage } from './pages/admin/KanbanPage';
import { PerformanceReportPage } from './pages/admin/PerformanceReportPage';

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }
  componentDidCatch(error, errorInfo) {
    this.setState({ hasError: true, error, errorInfo });
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-[#FFF8E7] p-8 text-[#930500] font-mono whitespace-pre-wrap">
          <h1 className="text-2xl font-bold mb-4">React App Crashed</h1>
          <p className="font-bold">{this.state.error && this.state.error.toString()}</p>
          <details className="mt-4 opacity-80 text-sm">
            <summary>Component Stack Trace</summary>
            {this.state.errorInfo && this.state.errorInfo.componentStack}
          </details>
        </div>
      );
    }
    return this.props.children;
  }
}

function AppContent() {
  const { isLoggedIn, loading, accountType, user } = useAuth();
  const [currentPage, setCurrentPage] = useState('landing');

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#FFF8E7] flex flex-col items-center justify-center">
        <div className="w-10 h-10 border-4 border-[#95BBEA] border-t-[#930500] rounded-full animate-spin" />
        <p className="mt-3 text-xs text-[#2B2523]/70 font-medium font-serif-editorial">
          Đang khởi tạo PetHome CSKH AI...
        </p>
      </div>
    );
  }

  // Simple URL based routing for Admin without RBAC
  if (window.location.pathname === '/admin/alerts') {
    return <AlertConfigPage />;
  }

  // Route routing logic
  if (currentPage === 'login') {
    return <CustomerLogin onNavigate={handleNavigate} />;
  }

  if (currentPage === 'register') {
    return <CustomerRegister onNavigate={handleNavigate} />;
  }

  if (currentPage === 'staff-login') {
    return <StaffLogin onNavigate={handleNavigate} />;
  }

  if (currentPage === 'staff-console') {
    if (!isLoggedIn || accountType !== 'STAFF') {
      return <StaffLogin onNavigate={handleNavigate} />;
    }
    return <StaffConsole onNavigate={handleNavigate} />;
  }

  if (currentPage === 'kanban') {
    if (!isLoggedIn || accountType !== 'STAFF') {
      return <StaffLogin onNavigate={handleNavigate} />;
    }
    return <KanbanPage onNavigate={handleNavigate} />;
  }
  if (currentPage === 'reports') {
    if (!isLoggedIn || accountType !== 'STAFF') {
      return <StaffLogin onNavigate={handleNavigate} />;
    }
    // RBAC for Reports: Only MANAGER or ADMIN
    if (user?.role === 'AGENT') {
      return <StaffConsole onNavigate={handleNavigate} />; // Fallback to console
    }
    return <PerformanceReportPage onNavigate={handleNavigate} />;
  }

  if (currentPage === 'chat') {
    // If not logged in, show login page first
    if (!isLoggedIn) {
      return <CustomerLogin onNavigate={handleNavigate} />;
    }
    if (accountType === 'STAFF') {
      return <StaffConsole onNavigate={handleNavigate} />;
    }
    return <ChatPage onNavigate={handleNavigate} />;
  }

  // Default: Landing Page
  return <LandingPage onNavigate={handleNavigate} />;
}

export default function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ErrorBoundary>
  );
}
