import React, { useEffect, useState } from 'react';
import { AlertTriangle, BriefcaseBusiness, CheckCircle2, LogOut, Plus, RefreshCw, ShieldCheck, UserPlus, Users, MessageSquare } from 'lucide-react';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { useAuth } from '../../hooks/useAuth';
import { staffService } from '../../services/staffService';
import { ticketService } from '../../services/ticketService';
import { useWebSocket } from '../../hooks/useWebSocket';

const STATUS_OPTIONS = [
  { value: 'ONLINE', label: 'Trực tuyến', tone: 'bg-emerald-500', message: 'Bạn đã sẵn sàng tiếp nhận hỗ trợ!' },
  { value: 'BUSY', label: 'Bận', tone: 'bg-amber-500', message: 'Bạn sẽ tạm dừng nhận phân công mới.' },
  { value: 'OFFLINE', label: 'Ngoại tuyến', tone: 'bg-stone-400', message: 'Bạn đã kết thúc trạng thái trực ca.' },
];

const ROLE_OPTIONS = ['AGENT', 'MANAGER', 'ADMIN'];

function statusLabel(status) {
  return STATUS_OPTIONS.find((item) => item.value === status)?.label || status;
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
    full_name: '', email: '', phone: '', role: 'AGENT', skills: '', password: '',
  });
  const [errors, setErrors] = useState({});
  const [notice, setNotice] = useState(null);
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [isLoadingList, setIsLoadingList] = useState(false);

  const canManageStaff = currentUser && ['ADMIN', 'MANAGER'].includes(currentUser.role);
  
  // Connect to global alerts WebSocket
  // Note: Backend port is assumed 8000
  const { popMessage, isConnected } = useWebSocket('ws://127.0.0.1:8000/api/v1/ws/alerts');

  useEffect(() => {
    setCurrentUser(user);
  }, [user]);

  useEffect(() => {
    if (canManageStaff) {
      loadStaffList();
    }
  }, [canManageStaff]);

  // Handle WebSocket messages
  useEffect(() => {
    const msg = popMessage();
    if (msg) {
      if (msg.event === 'UNASSIGNED_TICKET_ALERT' && canManageStaff) {
        setRedAlerts(prev => [msg.payload, ...prev]);
      } else if (msg.event === 'TICKET_ASSIGNED') {
        // If this agent was assigned the ticket
        if (msg.payload.agent_id === currentUser?.id) {
          setActiveTickets(prev => [msg.payload, ...prev]);
          showNotice('success', `Bạn vừa được phân công một Ticket mới!`);
        }
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
      login(localStorage.getItem('token'), updated, 'STAFF');
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
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCreateStaff = async (event) => {
    event.preventDefault();
    if (!validateStaffForm()) return;
    setIsCreating(true);
    try {
      await staffService.createStaff({ ...formData, skills: formData.skills.split(',').filter(Boolean) });
      setFormData({ full_name: '', email: '', phone: '', role: 'AGENT', skills: '', password: '' });
      showNotice('success', 'Tạo tài khoản nhân viên thành công!');
      loadStaffList();
    } catch (error) {
      showNotice('error', 'Tạo tài khoản thất bại.');
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
          <Button variant="soft" size="sm" icon={LogOut} onClick={handleLogout}>Đăng xuất</Button>
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
                      <p className="text-xs opacity-70 mt-1">Ticket ID: {alert.ticket_id.slice(0,8)}... | Không tìm thấy Agent có kỹ năng phù hợp.</p>
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

          {canManageStaff ? (
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
                  <Input label="Mật khẩu" name="password" type="password" value={formData.password} onChange={handleFormChange} error={errors.password} />
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
          ) : (
            <div className="space-y-6">
              {/* Agent Active Tickets Workspace */}
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
                      <div key={ticket.ticket_id} className="rounded-2xl bg-[#95BBEA]/10 border border-[#95BBEA]/30 p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 group hover:bg-[#95BBEA]/20 transition-all duration-300">
                        <div>
                          <div className="flex items-center gap-2 mb-2">
                            <span className="px-2.5 py-1 bg-white rounded-full text-[10px] font-bold tracking-wider uppercase text-[#95BBEA] drop-shadow-sm">Mới Phân Công</span>
                          </div>
                          <h3 className="font-semibold text-lg text-[#2B2523]">Phòng chat: {ticket.conversation_id.slice(0, 8)}...</h3>
                        </div>
                        <Button variant="primary" size="sm" className="shrink-0 bg-[#2B2523] hover:bg-black text-[#FFF8E7]">Vào phòng chat</Button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
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
