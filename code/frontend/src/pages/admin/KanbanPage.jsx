import React from 'react';
import { BriefcaseBusiness, LogOut } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../../components/common/Button';
import KanbanBoard from '../../components/kanban/KanbanBoard';

export function KanbanPage({ onNavigate }) {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    onNavigate('staff-login');
  };

  if (!user) return null;

  return (
    <div className="h-screen bg-[#FFF8E7] text-[#2B2523] selection:bg-[#930500] selection:text-[#FFF8E7] font-sans flex flex-col overflow-hidden">
      {/* Header / Topbar */}
      <header className="shrink-0 h-16 bg-[#FFF8E7] border-b border-[#EFE7D3] px-6 flex items-center justify-between z-10 shadow-sm">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-[#2B2523] text-[#FFF8E7] flex items-center justify-center">
              <BriefcaseBusiness className="w-4 h-4" />
            </div>
            <div>
              <h1 className="font-serif-editorial text-lg font-bold tracking-tight leading-none">PetHome Live Support</h1>
            </div>
          </div>
          
          <nav className="flex items-center gap-6 border-l border-[#EFE7D3] pl-6">
            <button 
              onClick={() => onNavigate('staff-console')}
              className="text-sm font-semibold text-[#2B2523]/60 hover:text-[#930500] transition-colors"
            >
              Hàng đợi & Live Chat
            </button>
            <button 
              className="text-sm font-bold text-[#930500] border-b-2 border-[#930500] pb-1"
            >
              Bảng công việc Kanban
            </button>
          </nav>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3 pl-4">
            <div className="text-right">
              <p className="text-sm font-bold leading-none">{user.full_name}</p>
              <p className="text-[10px] text-[#2B2523]/70 mt-0.5">{user.email} • {user.role}</p>
            </div>
            <Button variant="soft" size="sm" icon={LogOut} onClick={handleLogout} className="px-3 py-1.5 h-8 text-xs">Thoát</Button>
          </div>
        </div>
      </header>

      {/* Main Content - Full Screen Kanban */}
      <main className="flex-1 overflow-hidden min-h-0 relative bg-white">
        <KanbanBoard />
      </main>
    </div>
  );
}
