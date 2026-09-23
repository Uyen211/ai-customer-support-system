import React, { useState, useEffect } from 'react';
import { ticketService } from '../../services/ticketService';
import TicketDetailModal from './TicketDetailModal';

const KANBAN_COLUMNS = [
  { id: 'PENDING', title: 'Chờ tiếp nhận' },
  { id: 'IN_PROGRESS', title: 'Đang xử lý' },
  { id: 'RESOLVED', title: 'Đã giải quyết' },
  { id: 'CLOSED', title: 'Đóng phiếu' }
];

function KanbanCard({ ticket, onDragStart, onDoubleClick }) {
  const [timeLeft, setTimeLeft] = useState(0);

  useEffect(() => {
    if (ticket.status === 'RESOLVED' || ticket.status === 'CLOSED') {
      setTimeLeft(0);
      return;
    }
    const deadline = new Date(ticket.sla_deadline).getTime();
    const updateTimer = () => {
      const now = new Date().getTime();
      const diff = Math.max(0, deadline - now);
      setTimeLeft(diff);
    };
    updateTimer(); // initial call
    const interval = setInterval(updateTimer, 1000);
    return () => clearInterval(interval);
  }, [ticket]);

  const isOverdue = timeLeft <= 0 || ticket.sla_breached;

  const formatTime = (ms) => {
    if (ms <= 0) return "00:00:00";
    const totalSeconds = Math.floor(ms / 1000);
    const h = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
    const s = String(totalSeconds % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
  };

  return (
    <div
      draggable
      onDragStart={(e) => onDragStart(e, ticket)}
      onDoubleClick={() => onDoubleClick(ticket)}
      className={`p-4 mb-3 bg-white border rounded-xl shadow-sm cursor-grab active:cursor-grabbing transition-colors ${ticket.status !== 'RESOLVED' && ticket.status !== 'CLOSED' && isOverdue ? 'border-[#930500] bg-[#930500]/5' : 'border-[#EFE7D3] hover:border-[#95BBEA]'}`}
    >
      <div className="flex justify-between items-start mb-1.5">
        <div className="text-[10px] text-[#2B2523]/50 font-mono">#{ticket.id.split('-')[0]}</div>
        <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${ticket.priority === 'P1' ? 'bg-[#930500]/10 text-[#930500]' : ticket.priority === 'P2' ? 'bg-orange-100 text-orange-800' : 'bg-[#95BBEA]/20 text-[#1F242B]'}`}>
          {ticket.priority}
        </span>
      </div>
      <div className="text-sm font-semibold text-[#2B2523] mb-3 line-clamp-2 leading-tight">{ticket.summary}</div>
      <div className="flex items-center text-[11px]">
        {ticket.status !== 'RESOLVED' && ticket.status !== 'CLOSED' ? (
          <span className={`font-mono font-medium flex items-center gap-1 ${isOverdue ? 'text-[#930500]' : 'text-[#2B2523]/70'}`}>
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {formatTime(timeLeft)}
          </span>
        ) : (
          <span className="text-emerald-700 font-medium flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            Đã dừng đếm
          </span>
        )}
      </div>
    </div>
  );
}

export default function KanbanBoard() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedTicket, setSelectedTicket] = useState(null);

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = async () => {
    try {
      setLoading(true);
      // Giả định backend có endpoint /admin/tickets trả về tất cả ticket
      // Do trong code mẫu getActiveTickets chỉ gọi /active (IN_PROGRESS)
      // Ta sẽ dùng getActiveTickets tạm hoặc tự custom, ở đây ta fake gọi lấy tất cả
      const data = await ticketService.getKanbanTickets();
      setTickets(data);
    } catch (err) {
      setError(err.message || 'Lỗi khi tải danh sách phiếu hỗ trợ.');
    } finally {
      setLoading(false);
    }
  };

  const handleDragStart = (e, ticket) => {
    e.dataTransfer.setData('ticketId', ticket.id);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = async (e, targetStatus) => {
    e.preventDefault();
    const ticketId = e.dataTransfer.getData('ticketId');
    const ticket = tickets.find(t => t.id === ticketId);
    
    if (!ticket) return;
    if (ticket.status === targetStatus) return; // Same column

    const statusOrder = { "PENDING": 1, "IN_PROGRESS": 2, "RESOLVED": 3, "CLOSED": 4 };
    
    if (statusOrder[targetStatus] <= statusOrder[ticket.status]) {
      alert("Tiến độ phiếu chỉ được phép chuyển tiến lên theo quy trình, không thể chuyển ngược lại trạng thái trước đó!");
      return;
    }

    if (targetStatus === 'RESOLVED') {
      // Show modal for resolution note
      setSelectedTicket({ ...ticket, pendingTargetStatus: targetStatus });
      return;
    }

    await executeStatusUpdate(ticket.id, targetStatus);
  };

  const executeStatusUpdate = async (ticketId, targetStatus, resolutionNote = null) => {
    // Optimistic UI update
    const previousTickets = [...tickets];
    setTickets(prev => prev.map(t => t.id === ticketId ? { ...t, status: targetStatus } : t));

    try {
      await ticketService.updateTicketStatus(ticketId, targetStatus, resolutionNote);
      // Optional: fetchTickets() if backend adds more data
      alert("Cập nhật trạng thái phiếu hỗ trợ thành công!");
    } catch (err) {
      // Revert on error
      setTickets(previousTickets);
      alert(err.response?.data?.detail || "Mất kết nối mạng, chưa cập nhật được trạng thái. Vui lòng thử lại!");
    }
  };

  const handleDoubleClick = (ticket) => {
    setSelectedTicket(ticket);
  };

  const handleSaveModal = async (status, note) => {
    if (selectedTicket) {
      await executeStatusUpdate(selectedTicket.id, status, note);
      setSelectedTicket(null);
    }
  };

  if (loading) return <div>Đang tải bảng Kanban...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="flex h-full gap-6 p-2 overflow-x-auto custom-scrollbar">
      {KANBAN_COLUMNS.map(column => (
        <div 
          key={column.id} 
          className="flex flex-col flex-1 min-w-[280px] bg-[#FFF8E7]/50 border border-[#EFE7D3] rounded-2xl shrink-0"
          onDragOver={handleDragOver}
          onDrop={(e) => handleDrop(e, column.id)}
        >
          <div className="p-4 font-serif-editorial text-lg font-bold border-b border-[#EFE7D3] text-[#2B2523]">
            {column.title}
            <span className="ml-2 text-sm text-gray-500">
              ({tickets.filter(t => t.status === column.id).length})
            </span>
          </div>
          
          <div className="flex-1 p-3 overflow-y-auto custom-scrollbar">
            {tickets.filter(t => t.status === column.id).map(ticket => (
              <KanbanCard 
                key={ticket.id} 
                ticket={ticket} 
                onDragStart={handleDragStart} 
                onDoubleClick={handleDoubleClick} 
              />
            ))}
          </div>
        </div>
      ))}

      {selectedTicket && (
        <TicketDetailModal
          ticket={selectedTicket}
          onClose={() => setSelectedTicket(null)}
          onSave={handleSaveModal}
        />
      )}
    </div>
  );
}
