import React, { useEffect, useState } from 'react';
import { AlertTriangle, BriefcaseBusiness, CheckCircle2, LogOut, Plus, RefreshCw, ShieldCheck, UserPlus, Users, MessageSquare } from 'lucide-react';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { useAuth } from '../../hooks/useAuth';
import { staffService } from '../../services/staffService';
import { ticketService } from '../../services/ticketService';
import { useWebSocket } from '../../hooks/useWebSocket';
import { getWsBaseUrl } from '../../utils/constants';
import { AgentLiveChat } from '../../components/agent/AgentLiveChat';
const STATUS_OPTIONS = [
  { value: 'ONLINE', label: 'Trực tuyến', tone: 'bg-emerald-500', message: 'Bạn đã sẵn sàng tiếp nhận hỗ trợ!' },
  { value: 'BUSY', label: 'Bận', tone: 'bg-amber-500', message: 'Bạn sẽ tạm dừng nhận phân công mới.' },
  { value: 'OFFLINE', label: 'Ngoại tuyến', tone: 'bg-stone-400', message: 'Bạn đã kết thúc trạng thái trực ca.' },
];

const ROLE_OPTIONS = ['AGENT', 'MANAGER', 'ADMIN'];
const SKILL_OPTIONS = ['Đổi trả', 'Giao hàng', 'Tư vấn sản phẩm', 'Khiếu nại'];

function statusLabel(status) {
  return STATUS_OPTIONS.find((item) => item.value === status)?.label || status;
}

function TicketCard({ ticket, onResolve, currentUser }) {
  const [timeLeft, setTimeLeft] = useState(0);
  const [totalTime, setTotalTime] = useState(1); // To calculate percentage
  const [showResolveForm, setShowResolveForm] = useState(false);
  const [resolutionNote, setResolutionNote] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    // Parse total time based on priority if possible, or just deduce from deadline vs created_at
    const deadline = new Date(ticket.sla_deadline).getTime();
    const created = new Date(ticket.created_at).getTime();
    setTotalTime(deadline - created);

    const interval = setInterval(() => {
      const now = new Date().getTime();
      const diff = Math.max(0, deadline - now);
      setTimeLeft(diff);
    }, 1000);

    return () => clearInterval(interval);
  }, [ticket]);

  const isOverdue = timeLeft <= 0 || ticket.sla_breached;
  const isWarning = !isOverdue && (timeLeft / totalTime) <= 0.2;

  const formatTime = (ms) => {
    if (ms <= 0) return "00:00:00";
    const totalSeconds = Math.floor(ms / 1000);
    const h = String(Math.floor(totalSeconds / 3600)).padStart(2, '0');
    const m = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, '0');
    const s = String(totalSeconds % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
  };

  const minutesLeft = Math.ceil(timeLeft / 60000);
  const isEarlyResolve = timeLeft > 0;

  const handleResolve = async (e) => {
    e.preventDefault();
    if (resolutionNote.trim().length < 10 || resolutionNote.length > 1000) {
      setError('Nội dung phải từ 10 đến 1000 ký tự');
      return;
    }
    setError('');
    setSubmitting(true);
    try {
      await onResolve(ticket.id || ticket.ticket_id, resolutionNote);
    } catch (err) {
      setError('Lỗi khi hoàn tất. Vui lòng thử lại.');
      setSubmitting(false);
    }
  };
  const handleSecondaryAction = (actionName) => {
    alert(`Tính năng "${actionName}" đang được phát triển.`);
  };

  const handleTakeoverOpen = () => {
    if (ticket.conversation_id) {
      window.dispatchEvent(new CustomEvent('agent:select_chat', {
        detail: { conversation_id: ticket.conversation_id, autoTakeover: true }
      }));
    } else {
      alert('Không tìm thấy mã phòng chat cho thẻ này.');
    }
  };

  const isAssignedToMe = currentUser && ticket.assigned_to === currentUser.id;

  return (
    <div className={`rounded-2xl border p-5 flex flex-col gap-4 group transition-all duration-300 ${
      isOverdue ? 'bg-[#930500]/10 border-[#930500] animate-pulse shadow-md shadow-[#930500]/20' : 
      isWarning ? 'bg-amber-50 border-amber-300' : 'bg-[#95BBEA]/10 border-[#95BBEA]/30'
    }`}>
      <div className="flex items-start justify-between gap-4 mb-1">
        <div className="flex flex-wrap items-center gap-2">
          <Badge variant="outline">{ticket.priority || 'P3'}</Badge>
          <span className={`px-2.5 py-1 bg-white rounded-full text-[10px] font-bold tracking-wider uppercase drop-shadow-sm border ${isOverdue ? 'border-[#930500] text-[#930500]' : 'border-[#95BBEA] text-[#1F242B]'}`}>
            Đang xử lý
          </span>
        </div>
        <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-lg border border-[#EFE7D3] shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={isOverdue ? 'text-[#930500]' : isWarning ? 'text-amber-600' : 'text-[#2B2523]'}><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <div className={`text-base font-mono font-bold tracking-tight ${isOverdue ? 'text-[#930500]' : isWarning ? 'text-amber-600' : 'text-[#2B2523]'}`}>
            {formatTime(timeLeft)}
          </div>
          <span className={`text-xs font-semibold ${isOverdue ? 'text-[#930500]' : 'text-[#2B2523]/70'}`}>
            ({isOverdue ? 'Đã quá hạn' : `Còn ${minutesLeft} phút`})
          </span>
        </div>
      </div>

      <div>
        <h3 className="font-semibold text-lg text-[#2B2523]">{ticket.category || 'Hỗ trợ khách hàng'}</h3>
        {ticket.summary && (
          <p className="text-sm text-[#2B2523]/90 mt-1.5 mb-1.5 line-clamp-2 leading-snug">
            {ticket.summary}
          </p>
        )}
        <p className="text-xs opacity-70 mt-1 truncate max-w-sm font-mono">
          Ticket ID: {ticket.id || ticket.ticket_id} | Phòng: {ticket.conversation_id?.slice(0, 8)}...
        </p>
      </div>

      <form onSubmit={handleResolve} className="mt-2 flex flex-col gap-3 bg-white p-4 rounded-xl border border-[#EFE7D3] shadow-sm">
        <div>
          <textarea 
            value={resolutionNote} 
            onChange={e => setResolutionNote(e.target.value)}
            placeholder="Ghi chú xử lý (Bắt buộc, 10 - 1000 ký tự)..."
            className={`w-full bg-[#FFF8E7]/50 text-[#2B2523] border rounded-xl px-4 py-3 text-sm outline-none resize-y min-h-[80px] transition-colors ${error ? 'border-[#930500] focus:ring-1 focus:ring-[#930500]' : 'border-[#EFE7D3] focus:border-[#95BBEA] focus:ring-1 focus:ring-[#95BBEA]'}`}
          />
          {error && <p className="text-xs text-[#930500] mt-1 font-medium">{error}</p>}
          {isEarlyResolve && resolutionNote.length > 0 && !error && (
            <p className="text-[11px] text-amber-600 mt-1.5 font-medium flex items-center gap-1.5">
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
              Bạn đang hoàn tất phiếu sớm hơn thời gian cam kết. Vui lòng kiểm tra kỹ trước khi gửi.
            </p>
          )}
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-center gap-3 pt-3 border-t border-[#EFE7D3]/50">
          <div className="flex gap-2 w-full sm:w-auto">
            <Button type="button" variant="soft" size="sm" onClick={handleTakeoverOpen} className="flex-1 sm:flex-none">
              {isAssignedToMe ? 'Mở hội thoại' : 'Tiếp quản'}
            </Button>
            <Button type="button" variant="soft" size="sm" onClick={() => handleSecondaryAction('Chuyển tiếp')} className="flex-1 sm:flex-none">
              Chuyển tiếp
            </Button>
            <Button type="button" variant="soft" size="sm" onClick={() => handleSecondaryAction('Tạm dừng')} className="flex-1 sm:flex-none">
              Tạm dừng
            </Button>
          </div>
          
          <button 
            type="submit" 
            disabled={submitting}
            className="w-full sm:w-auto px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm rounded-full shadow-md shadow-emerald-600/20 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 active:scale-95"
          >
            {submitting ? (
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            )}
            Xác nhận đã xử lý
          </button>
        </div>
      </form>
    </div>
  );
}

export function StaffConsole({ onNavigate }) {
  const { user, login, logout } = useAuth();
  const [currentUser, setCurrentUser] = useState(user);
  const [staffList, setStaffList] = useState([]);

  // Agent Tickets State
  const [activeTickets, setActiveTickets] = useState([]);

  // Admin Alert & Assign State
  const [redAlerts, setRedAlerts] = useState([]);
  const [isAssignModalOpen, setIsAssignModalOpen] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [selectedAgentId, setSelectedAgentId] = useState('');
  const [isAssigning, setIsAssigning] = useState(false);

  const [formData, setFormData] = useState({
    full_name: '', email: '', phone: '', role: 'AGENT', skills: [], password: '', confirm_password: '',
  });
  const [errors, setErrors] = useState({});
  const [notice, setNotice] = useState(null);
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [isLoadingList, setIsLoadingList] = useState(false);

  const canManageStaff = currentUser && ['ADMIN', 'MANAGER'].includes(currentUser.role);

  // Connect to global alerts WebSocket (URL theo env VITE_API_BASE_URL để khớp port backend docker)
  const { popMessage, isConnected } = useWebSocket(`${getWsBaseUrl()}/ws/alerts`);

  useEffect(() => {
    setCurrentUser(user);
  }, [user]);

  useEffect(() => {
    if (canManageStaff) {
      loadStaffList();
    }
  }, [canManageStaff]);

  // Fetch active tickets on load
  useEffect(() => {
    if (currentUser?.role === 'AGENT' || canManageStaff) {
      ticketService.getActiveTickets().then(tickets => {
        setActiveTickets(tickets);
      }).catch(err => console.error("Failed to load active tickets", err));
    }
  }, [currentUser, canManageStaff]);
  // Handle WebSocket messages
  useEffect(() => {
    const msg = popMessage();
    if (msg) {
      if (msg.event === 'UNASSIGNED_TICKET_ALERT' && canManageStaff) {
        setRedAlerts(prev => [msg.payload, ...prev]);
      } else if (msg.event === 'TICKET_ASSIGNED') {
        if (msg.payload.agent_id === currentUser?.id) {
          // Instead of just relying on payload, fetch to get full ticket with sla_deadline
          ticketService.getActiveTickets().then(tickets => setActiveTickets(tickets));
          showNotice('success', `Bạn vừa được phân công một Ticket mới!`);
        } else {
          // Nếu vé được gán cho người khác (hoặc bị thu hồi), hãy xóa nó khỏi danh sách của mình nếu đang có
          setActiveTickets(prev => prev.filter(t => (t.id || t.ticket_id) !== msg.payload.ticket_id));
        }
      } else if (msg.event === 'SLA_BREACH_ALERT') {
        if (msg.payload.assigned_to === currentUser?.id) {
          showNotice('error', 'CẢNH BÁO: Bạn có một phiếu hỗ trợ đã QUÁ HẠN XỬ LÝ!');
          // Play alert sound if possible
          try {
            const audio = new Audio('/sounds/alert.mp3'); // We might not have this file but it's a good effort
            audio.play().catch(e => console.log('Audio blocked', e));
          } catch (e) {}
          // Mark the ticket as breached in state to immediately show red
          setActiveTickets(prev => prev.map(t => t.id === msg.payload.ticket_id ? { ...t, sla_breached: true } : t));
        }
        if (canManageStaff) {
          setRedAlerts(prev => [msg.payload, ...prev]);
        }
      } else if (msg.event === 'TICKET_RESOLVED') {
          // Remove from active list
          setActiveTickets(prev => prev.filter(t => t.id !== msg.payload.ticket_id));
      }
    }
  }, [popMessage, canManageStaff, currentUser]);

  const showNotice = (type, message) => {
    setNotice({ type, message });
    setTimeout(() => setNotice(null), 5000);
  };

  const loadStaffList = async () => {
    setIsLoadingList(true);
    try {
      const data = await staffService.listStaff();
      setStaffList(data);
    } catch (error) {
      showNotice('error', error.response?.data?.detail || 'Không thể tải danh sách nhân viên.');
    } finally {
      setIsLoadingList(false);
    }
  };

  const handleStatusChange = async (status) => {
    setIsUpdatingStatus(true);
    setNotice(null);
    try {
      const updated = await staffService.updateStatus(status);
      setCurrentUser(updated);
      login(sessionStorage.getItem('token'), updated, 'STAFF');
      const option = STATUS_OPTIONS.find((item) => item.value === status);
      showNotice('success', `Đã chuyển sang trạng thái ${option.label}`);
      if (canManageStaff) loadStaffList();
    } catch (error) {
      showNotice('error', error.response?.data?.detail || 'Cập nhật trạng thái thất bại.');
    } finally {
      setIsUpdatingStatus(false);
    }
  };

  const handleOpenAssignModal = (alert) => {
    setSelectedAlert(alert);
    setIsAssignModalOpen(true);
    setSelectedAgentId('');
  };

  const handleManualAssign = async () => {
    if (!selectedAgentId) return;
    setIsAssigning(true);
    try {
      await ticketService.assignTicket(selectedAlert.ticket_id, selectedAgentId);
      showNotice('success', `Đã phân công vé thành công!`);
      // Remove from alert list
      setRedAlerts(prev => prev.filter(a => a.ticket_id !== selectedAlert.ticket_id));
      setIsAssignModalOpen(false);
      setSelectedAlert(null);
    } catch (error) {
      showNotice('error', error.response?.data?.detail || 'Phân công thất bại.');
    } finally {
      setIsAssigning(false);
    }
  };

  const validateStaffForm = () => { /* ... existing validation ... */
    const nextErrors = {};
    if (!formData.full_name.trim()) nextErrors.full_name = 'Vui lòng nhập họ và tên';
    if (!formData.email.trim()) nextErrors.email = 'Vui lòng nhập email';
    if (!formData.password) nextErrors.password = 'Vui lòng nhập mật khẩu';
    else if (formData.password.length < 8 || !/[A-Za-z]/.test(formData.password) || !/\d/.test(formData.password)) {
      nextErrors.password = 'Mật khẩu phải tối thiểu 8 ký tự, gồm cả chữ và số';
    }
    if (formData.confirm_password !== formData.password) nextErrors.confirm_password = 'Mật khẩu xác nhận không trùng khớp';
    if (formData.phone && !/^0\d{9}$/.test(formData.phone.trim())) nextErrors.phone = 'Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0';
    if (formData.role === 'AGENT' && formData.skills.length === 0) nextErrors.skills = 'Tài khoản Agent bắt buộc chọn ít nhất 1 kỹ năng xử lý';
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: null }));
  };

  const handleSkillToggle = (skill) => {
    setFormData((prev) => {
      const has = prev.skills.includes(skill);
      return { ...prev, skills: has ? prev.skills.filter((s) => s !== skill) : [...prev.skills, skill] };
    });
    setErrors((prev) => ({ ...prev, skills: null }));
  };

  const handleCreateStaff = async (event) => {
    event.preventDefault();
    if (!validateStaffForm()) return;
    setIsCreating(true);
    try {
      await staffService.createStaff({
        full_name: formData.full_name,
        email: formData.email,
        phone: formData.phone || null,
        role: formData.role,
        skills: formData.skills,
        password: formData.password,
      });
      setFormData({ full_name: '', email: '', phone: '', role: 'AGENT', skills: [], password: '', confirm_password: '' });
      showNotice('success', 'Tạo tài khoản nhân viên thành công!');
      loadStaffList();
    } catch (error) {
      showNotice('error', error.response?.data?.detail || 'Tạo tài khoản thất bại.');
    } finally {
      setIsCreating(false);
    }
  };

  const handleLogout = () => {
    logout();
    onNavigate('staff-login');
  };

  if (!currentUser) return null;

  const currentStatusOption = STATUS_OPTIONS.find((item) => item.value === currentUser.status) || STATUS_OPTIONS[2];

  return (
    <div className="min-h-screen bg-[#FFF8E7] text-[#2B2523] selection:bg-[#930500] selection:text-[#FFF8E7] font-sans">
      <header className="sticky top-0 z-40 bg-[#FFF8E7]/90 backdrop-blur-md border-b border-[#EFE7D3]">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between gap-4">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-[#2B2523] text-[#FFF8E7] flex items-center justify-center">
                <BriefcaseBusiness className="w-5 h-5" />
              </div>
              <div>
                <h1 className="font-serif-editorial text-2xl font-bold tracking-tight">Live Support Console</h1>
                <p className="text-[10px] uppercase tracking-widest text-[#930500] font-semibold">
                  {isConnected ? 'Connected' : 'Reconnecting...'}
                </p>
              </div>
            </div>
            
            <nav className="flex items-center gap-6 border-l border-[#EFE7D3] pl-6">
              <button 
                className="text-sm font-bold text-[#930500] border-b-2 border-[#930500] pb-1"
              >
                Hàng đợi & Live Chat
              </button>
              <button 
                onClick={() => onNavigate('kanban')}
                className="text-sm font-semibold text-[#2B2523]/60 hover:text-[#930500] transition-colors"
              >
                Bảng công việc Kanban
              </button>
              {currentUser.role !== 'AGENT' && (
                <button 
                  onClick={() => onNavigate('reports')}
                  className="text-sm font-semibold text-[#2B2523]/60 hover:text-[#930500] transition-colors"
                >
                  Báo cáo thống kê
                </button>
              )}
            </nav>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-3 pl-4 border-l border-[#EFE7D3]">
              <div className="text-right">
                <p className="text-sm font-bold leading-none">{currentUser.full_name}</p>
                <p className="text-[10px] text-[#2B2523]/70 mt-0.5">{currentUser.email} • {currentUser.role}</p>
              </div>
              <Button variant="soft" size="sm" icon={LogOut} onClick={handleLogout} className="px-3 py-1.5 h-8 text-xs">Thoát</Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-6 relative">
        <section className="lg:col-span-4 space-y-6">
          <div className="rounded-3xl border border-[#EFE7D3] bg-white shadow-editorial p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-widest text-[#930500] font-semibold">Tài khoản trực ca</p>
                <h2 className="font-serif-editorial text-3xl font-bold mt-1">{currentUser.full_name}</h2>
                <p className="text-sm text-[#2B2523]/70 mt-1">{currentUser.email}</p>
              </div>
              <Badge variant="outline">{currentUser.role}</Badge>
            </div>

            <div className="mt-6 rounded-2xl bg-[#95BBEA]/20 border border-[#95BBEA]/40 p-4 transition-all duration-300">
              <div className="flex items-center gap-2 text-sm font-semibold">
                <span className={`w-3 h-3 rounded-full ${currentStatusOption.tone}`} />
                {statusLabel(currentUser.status)}
              </div>
              <p className="text-xs text-[#2B2523]/70 mt-1">{currentStatusOption.message}</p>
            </div>

            <div className="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
              {STATUS_OPTIONS.map((option) => (
                <Button
                  key={option.value}
                  variant={currentUser.status === option.value ? 'primary' : 'soft'}
                  size="sm"
                  disabled={isUpdatingStatus}
                  onClick={() => handleStatusChange(option.value)}
                  className="w-full"
                >
                  {option.label}
                </Button>
              ))}
            </div>
          </div>

          {notice && (
            <div className={`rounded-2xl p-4 border flex items-start gap-3 text-sm animate-fade-in transition-all ${notice.type === 'success' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-[#930500]/10 border-[#930500]/20 text-[#930500]'}`}>
              {notice.type === 'success' ? <CheckCircle2 className="w-5 h-5 shrink-0" /> : <AlertTriangle className="w-5 h-5 shrink-0" />}
              <span>{notice.message}</span>
            </div>
          )}
        </section>

        <section className="lg:col-span-8 space-y-6">

          {/* Admin Red Alert Zone */}
          {canManageStaff && redAlerts.length > 0 && (
            <div className="rounded-3xl bg-[#930500] text-[#FFF8E7] p-6 shadow-2xl shadow-[#930500]/20 animate-fade-in border border-[#930500]">
              <div className="flex items-center gap-3 mb-4">
                <AlertTriangle className="w-6 h-6 text-[#FFF8E7]" />
                <h2 className="font-serif-editorial text-2xl font-bold">Cảnh Báo Đỏ (SLA Risk)</h2>
              </div>
              <p className="text-sm opacity-80 mb-5">Hệ thống phát hiện vé không có tư vấn viên tiếp nhận. Cần xử lý thủ công ngay!</p>

              <div className="space-y-3">
                {redAlerts.map(alert => (
                  <div key={alert.ticket_id} className="bg-black/20 rounded-2xl p-4 flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-lg">{alert.category || 'Vé hỗ trợ chung'}</p>
                      <p className="text-xs opacity-70 mt-1">Ticket ID: {alert.ticket_id.slice(0, 8)}... | Không tìm thấy Agent có kỹ năng phù hợp.</p>
                    </div>
                    <button
                      onClick={() => handleOpenAssignModal(alert)}
                      className="px-4 py-2 bg-[#FFF8E7] text-[#930500] rounded-full text-sm font-bold hover:bg-white transition-all shadow-sm"
                    >
                      Phân công ngay
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {canManageStaff && (
            <>
              {/* Existing Admin Management Tools */}
              <div className="rounded-3xl border border-[#EFE7D3] bg-white shadow-editorial p-6">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-2xl bg-[#930500] text-[#FFF8E7] flex items-center justify-center">
                    <UserPlus className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="font-serif-editorial text-2xl font-bold">Tạo tài khoản nhân sự</h2>
                  </div>
                </div>
                <form onSubmit={handleCreateStaff} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input label="Họ và tên" name="full_name" value={formData.full_name} onChange={handleFormChange} error={errors.full_name} />
                  <Input label="Email nội bộ" name="email" type="email" value={formData.email} onChange={handleFormChange} error={errors.email} />
                  <div className="w-full flex flex-col gap-1.5">
                    <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80">Vai trò</label>
                    <select name="role" value={formData.role} onChange={handleFormChange} className="w-full bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm outline-none">
                      {ROLE_OPTIONS.map((role) => <option key={role} value={role}>{role}</option>)}
                    </select>
                  </div>
                  <Input label="Số điện thoại (tùy chọn)" name="phone" value={formData.phone} onChange={handleFormChange} placeholder="0912345678" error={errors.phone} />
                  <Input label="Mật khẩu" name="password" type="password" value={formData.password} onChange={handleFormChange} error={errors.password} />
                  <Input label="Xác nhận mật khẩu" name="confirm_password" type="password" value={formData.confirm_password} onChange={handleFormChange} error={errors.confirm_password} />
                  {formData.role === 'AGENT' && (
                    <div className="md:col-span-2">
                      <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80 block mb-1.5">
                        Kỹ năng chuyên môn <span className="text-[#930500]">*</span>
                      </label>
                      <div className="flex flex-wrap gap-2">
                        {SKILL_OPTIONS.map((skill) => {
                          const active = formData.skills.includes(skill);
                          return (
                            <button
                              key={skill}
                              type="button"
                              onClick={() => handleSkillToggle(skill)}
                              className={`px-4 py-2 rounded-full text-xs font-semibold border transition-all cursor-pointer ${
                                active
                                  ? 'bg-[#930500] text-white border-[#930500] shadow-md shadow-[#930500]/20'
                                  : 'bg-white text-[#2B2523] border-[#EFE7D3] hover:border-[#930500]/40'
                              }`}
                            >
                              {skill}
                            </button>
                          );
                        })}
                      </div>
                      {errors.skills && <p className="text-xs text-[#930500] mt-1.5">{errors.skills}</p>}
                    </div>
                  )}
                  <div className="md:col-span-2">
                    <Button type="submit" variant="primary" isLoading={isCreating}>Tạo tài khoản</Button>
                  </div>
                </form>
              </div>

              {/* Staff List */}
              <div className="rounded-3xl border border-[#EFE7D3] bg-white shadow-editorial p-6">
                {/* ... (Existing List Logic minimized for brevity but keeping styling) ... */}
                <div className="flex items-center justify-between mb-5">
                  <h2 className="font-serif-editorial text-2xl font-bold">Danh sách nhân viên</h2>
                  <Button variant="soft" size="sm" onClick={loadStaffList}>Làm mới</Button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {staffList.map(staff => (
                    <article key={staff.id} className="rounded-2xl border border-[#EFE7D3] p-4 bg-[#FFF8E7]/50">
                      <div className="flex justify-between items-start">
                        <h3 className="font-semibold text-[#2B2523]">{staff.full_name}</h3>
                        <Badge variant="outline">{staff.role}</Badge>
                      </div>
                      <p className="text-xs text-[#2B2523]/60 mt-1">{staff.email}</p>
                    </article>
                  ))}
                </div>
              </div>
            </>
          )}

          <div className="space-y-6">
            {/* UC 3.3: Hàng đợi hội thoại trực tuyến + tiếp quản + chat realtime */}
            <AgentLiveChat currentUser={currentUser} />

            {currentUser?.role === 'AGENT' && (
              <div className="rounded-3xl border border-[#EFE7D3] bg-white shadow-editorial p-6">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-2xl bg-[#95BBEA] text-[#2B2523] flex items-center justify-center shadow-inner">
                    <MessageSquare className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="font-serif-editorial text-2xl font-bold">Vé Hỗ Trợ Đang Xử Lý</h2>
                    <p className="text-xs text-[#2B2523]/70 mt-1">Các phiên hỗ trợ khách hàng được hệ thống phân công cho bạn.</p>
                  </div>
                </div>

                {activeTickets.length === 0 ? (
                  <div className="py-12 text-center rounded-2xl bg-[#FFF8E7] border border-[#EFE7D3]/50 border-dashed">
                    <ShieldCheck className="w-10 h-10 mx-auto text-[#2B2523]/30 mb-3" />
                    <p className="text-sm font-medium text-[#2B2523]/60">Chưa có công việc nào đang diễn ra.</p>
                    <p className="text-xs text-[#2B2523]/40 mt-1">Hệ thống sẽ tự động gửi vé khi có khách hàng cần hỗ trợ.</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 gap-4">
                    {activeTickets.map(ticket => (
                      <TicketCard 
                        currentUser={currentUser}
                        key={ticket.id || ticket.ticket_id} 
                        ticket={ticket} 
                        onResolve={async (id, note) => {
                          await ticketService.resolveTicket(id, note);
                          setActiveTickets(prev => prev.filter(t => (t.id || t.ticket_id) !== id));
                          showNotice('success', 'Đã hoàn tất xử lý phiếu hỗ trợ!');
                        }} 
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

          </div>
        </section>
      </main>

      {/* Manual Assign Modal */}
      {isAssignModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#2B2523]/40 backdrop-blur-sm animate-fade-in">
          <div className="bg-[#FFF8E7] w-full max-w-md rounded-[32px] p-8 shadow-2xl relative overflow-hidden">
            {/* Soft decorative blur */}
            <div className="absolute top-0 left-0 w-32 h-32 bg-[#930500]/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2 pointer-events-none" />

            <h3 className="font-serif-editorial text-2xl font-bold mb-2">Phân công thủ công</h3>
            <p className="text-sm text-[#2B2523]/70 mb-6">Chọn một Agent trực tuyến để xử lý vé {selectedAlert?.category}</p>

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
                    {agent.full_name} ({statusLabel(agent.status)})
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
    </div>
  );
}
