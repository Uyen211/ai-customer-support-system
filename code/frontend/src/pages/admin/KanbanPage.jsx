import React, { useState, useEffect } from 'react';
import { BriefcaseBusiness, LogOut } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { staffService } from '../../services/staffService';
import { ticketService } from '../../services/ticketService';
import { Button } from '../../components/common/Button';
import KanbanBoard from '../../components/kanban/KanbanBoard';

export function KanbanPage({ onNavigate }) {
  const { user, logout } = useAuth();

  const [staffList, setStaffList] = useState([]);
  const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [selectedAgentId, setSelectedAgentId] = useState('');
  const [isAssigning, setIsAssigning] = useState(false);

  useEffect(() => {
    if (user && ['ADMIN', 'MANAGER'].includes(user.role)) {
      staffService.getStaffList().then(list => setStaffList(list || [])).catch(() => {});
    }
  }, [user]);

  const handleOpenAssignModal = (ticket) => {
    setSelectedTicket(ticket);
    setSelectedAgentId('');
    setIsAssignModalOpen(true);
  };

  const handleManualAssign = async () => {
    if (!selectedAgentId || !selectedTicket) return;
    setIsAssigning(true);
    try {
      await ticketService.assignTicket(selectedTicket.id || selectedTicket.ticket_id, selectedAgentId);
      setIsAssignModalOpen(false);
      // Dispatch a custom event to tell KanbanBoard to refresh
      window.dispatchEvent(new Event('kanban:refresh'));
    } catch (err) {
      alert(err.response?.data?.detail || 'Lỗi khi phân công.');
    } finally {
      setIsAssigning(false);
    }
  };

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
            <button onClick={() => onNavigate('staff-console')} className="text-sm font-semibold text-[#2B2523]/60 hover:text-[#930500] transition-colors">
              Hàng đợi & Live Chat
            </button>
            <button className="text-sm font-bold text-[#930500] border-b-2 border-[#930500] pb-1">
              Bảng công việc Kanban
            </button>
            {user.role !== 'AGENT' && (
              <button onClick={() => onNavigate('reports')} className="text-sm font-semibold text-[#2B2523]/60 hover:text-[#930500] transition-colors">
                Báo cáo thống kê
              </button>
            )}
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
        <KanbanBoard 
          currentUser={user}
          onAssignClick={handleOpenAssignModal}
        />

        {/* Manual Assign Modal */}
        {isAssignModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#2B2523]/40 backdrop-blur-sm animate-fade-in">
            <div className="bg-[#FFF8E7] w-full max-w-md rounded-[32px] p-8 shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-32 h-32 bg-[#930500]/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
              <h3 className="font-serif-editorial text-2xl font-bold mb-2">Phân công thủ công</h3>
              <p className="text-sm text-[#2B2523]/70 mb-6">Chọn một Agent trực tuyến để xử lý vé {selectedTicket?.category}</p>

              <div className="space-y-4 mb-8">
                <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80 block">Chọn Nhân viên (Agent)</label>
                <select
                  value={selectedAgentId}
                  onChange={(e) => setSelectedAgentId(e.target.value)}
                  className="w-full bg-white text-[#2B2523] border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#930500]/20 transition-all"
                >
                  <option value="">-- Lựa chọn Agent --</option>
                  {staffList.filter(s => s.role === 'AGENT' && s.status !== 'OFFLINE').map(agent => (
                    <option key={agent.id} value={agent.id}>
                      {agent.full_name} ({agent.status === 'ONLINE' ? 'Trực tuyến' : agent.status === 'BUSY' ? 'Bận' : agent.status})
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center justify-end gap-3">
                <button
                  onClick={() => setIsAssignModalOpen(false)}
                  className="px-6 py-3 rounded-full text-sm font-semibold text-[#2B2523]/70 hover:bg-black/5 transition-colors"
                >
                  Hủy
                </button>
                <button
                  onClick={handleManualAssign}
                  disabled={!selectedAgentId || isAssigning}
                  className="px-6 py-3 rounded-full bg-[#930500] text-white text-sm font-semibold shadow-md shadow-[#930500]/20 disabled:opacity-50 transition-all hover:bg-[#7a0400]"
                >
                  {isAssigning ? 'Đang phân công...' : 'Xác nhận phân công'}
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
