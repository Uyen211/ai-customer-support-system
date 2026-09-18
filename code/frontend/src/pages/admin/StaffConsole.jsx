import React, { useEffect, useState } from 'react';
import { AlertTriangle, BriefcaseBusiness, CheckCircle2, LogOut, Plus, RefreshCw, ShieldCheck, UserPlus, Users } from 'lucide-react';
import { Badge } from '../../components/common/Badge';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { useAuth } from '../../hooks/useAuth';
import { staffService } from '../../services/staffService';

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
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    role: 'AGENT',
    skills: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [notice, setNotice] = useState(null);
  const [isUpdatingStatus, setIsUpdatingStatus] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [isLoadingList, setIsLoadingList] = useState(false);

  const canManageStaff = currentUser && ['ADMIN', 'MANAGER'].includes(currentUser.role);

  useEffect(() => {
    setCurrentUser(user);
  }, [user]);

  useEffect(() => {
    if (canManageStaff) {
      loadStaffList();
    }
  }, [canManageStaff]);

  const showNotice = (type, message) => {
    setNotice({ type, message });
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
      showNotice('success', `Đã chuyển sang trạng thái ${option.label} - ${option.message}`);
      if (canManageStaff) loadStaffList();
    } catch (error) {
      showNotice('error', error.response?.data?.detail || 'Cập nhật trạng thái thất bại.');
    } finally {
      setIsUpdatingStatus(false);
    }
  };

  const validateStaffForm = () => {
    const nextErrors = {};
    if (!formData.full_name.trim()) nextErrors.full_name = 'Vui lòng nhập họ và tên';
    if (!formData.email.trim()) nextErrors.email = 'Vui lòng nhập email nội bộ';
    if (!formData.password) nextErrors.password = 'Vui lòng nhập mật khẩu';
    if (formData.password && !/(?=.*[A-Za-z])(?=.*\d).{8,}/.test(formData.password)) {
      nextErrors.password = 'Mật khẩu tối thiểu 8 ký tự, gồm chữ và số';
    }
    if (formData.phone && !/^0\d{9}$/.test(formData.phone)) {
      nextErrors.phone = 'Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0';
    }
    if (formData.role === 'AGENT' && !formData.skills.trim()) {
      nextErrors.skills = 'Agent bắt buộc chọn ít nhất 1 kỹ năng';
    }
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: null }));
    setNotice(null);
  };

  const handleCreateStaff = async (event) => {
    event.preventDefault();
    if (!validateStaffForm()) return;

    setIsCreating(true);
    setNotice(null);
    try {
      const payload = {
        full_name: formData.full_name,
        email: formData.email,
        password: formData.password,
        phone: formData.phone || undefined,
        role: formData.role,
        skills: formData.skills.split(',').map((item) => item.trim()).filter(Boolean),
      };
      await staffService.createStaff(payload);
      setFormData({ full_name: '', email: '', phone: '', role: 'AGENT', skills: '', password: '' });
      showNotice('success', 'Tạo tài khoản nhân viên thành công!');
      loadStaffList();
    } catch (error) {
      showNotice('error', error.response?.data?.detail || 'Tạo tài khoản nhân viên thất bại.');
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
    <div className="min-h-screen bg-[#FFF8E7] text-[#2B2523] selection:bg-[#930500] selection:text-[#FFF8E7]">
      <header className="sticky top-0 z-40 bg-[#FFF8E7]/90 backdrop-blur-md border-b border-[#EFE7D3]">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-[#2B2523] text-[#FFF8E7] flex items-center justify-center">
              <BriefcaseBusiness className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-serif-editorial text-2xl font-bold tracking-tight">Live Support Console</h1>
              <p className="text-[10px] uppercase tracking-widest text-[#930500] font-semibold">PetHome Internal</p>
            </div>
          </div>
          <Button variant="soft" size="sm" icon={LogOut} onClick={handleLogout}>Đăng xuất</Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-6">
        <section className="lg:col-span-4 space-y-6">
          <div className="rounded-3xl border border-[#EFE7D3] bg-[#FFF8E7] shadow-editorial p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-widest text-[#930500] font-semibold">Tài khoản trực ca</p>
                <h2 className="font-serif-editorial text-3xl font-bold mt-1">{currentUser.full_name}</h2>
                <p className="text-sm text-[#2B2523]/70 mt-1">{currentUser.email}</p>
              </div>
              <Badge variant="outline">{currentUser.role}</Badge>
            </div>

            <div className="mt-6 rounded-2xl bg-[#95BBEA]/20 border border-[#95BBEA]/40 p-4">
              <div className="flex items-center gap-2 text-sm font-semibold">
                <span className={`w-3 h-3 rounded-full ${currentStatusOption.tone}`} />
                {statusLabel(currentUser.status)}
              </div>
              <p className="text-xs text-[#2B2523]/70 mt-1">Trạng thái này quyết định khả năng nhận ticket tự động.</p>
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
            <div className={`rounded-2xl p-4 border flex items-start gap-3 text-sm ${notice.type === 'success' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' : 'bg-[#930500]/10 border-[#930500]/20 text-[#930500]'}`}>
              {notice.type === 'success' ? <CheckCircle2 className="w-5 h-5 shrink-0" /> : <AlertTriangle className="w-5 h-5 shrink-0" />}
              <span>{notice.message}</span>
            </div>
          )}
        </section>

        <section className="lg:col-span-8 space-y-6">
          {canManageStaff ? (
            <>
              <div className="rounded-3xl border border-[#EFE7D3] bg-[#FFF8E7] shadow-editorial p-6">
                <div className="flex items-center gap-3 mb-5">
                  <div className="w-10 h-10 rounded-2xl bg-[#930500] text-[#FFF8E7] flex items-center justify-center">
                    <UserPlus className="w-5 h-5" />
                  </div>
                  <div>
                    <h2 className="font-serif-editorial text-2xl font-bold">Tạo tài khoản nhân sự</h2>
                    <p className="text-xs text-[#2B2523]/70">Dành cho Admin/Manager theo Use Case 3.1.</p>
                  </div>
                </div>

                <form onSubmit={handleCreateStaff} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input label="Họ và tên" name="full_name" value={formData.full_name} onChange={handleFormChange} error={errors.full_name} required />
                  <Input label="Email nội bộ" name="email" type="email" value={formData.email} onChange={handleFormChange} error={errors.email} required />
                  <Input label="Số điện thoại" name="phone" value={formData.phone} onChange={handleFormChange} error={errors.phone} />
                  <div className="w-full flex flex-col gap-1.5">
                    <label className="text-xs uppercase tracking-wider font-semibold text-[#2B2523]/80">Vai trò <span className="text-[#930500]">*</span></label>
                    <select name="role" value={formData.role} onChange={handleFormChange} className="w-full bg-[#FFF8E7] text-[#2B2523] border border-[#EFE7D3] rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#930500]/30 focus:border-[#930500]">
                      {ROLE_OPTIONS.map((role) => <option key={role} value={role}>{role}</option>)}
                    </select>
                  </div>
                  <Input label="Kỹ năng" name="skills" placeholder="Đổi trả, Giao hàng, Khiếu nại" value={formData.skills} onChange={handleFormChange} error={errors.skills} required={formData.role === 'AGENT'} />
                  <Input label="Mật khẩu" name="password" type="password" value={formData.password} onChange={handleFormChange} error={errors.password} required />
                  <div className="md:col-span-2 flex justify-end pt-2">
                    <Button type="submit" variant="primary" icon={Plus} isLoading={isCreating}>Tạo tài khoản nhân viên</Button>
                  </div>
                </form>
              </div>

              <div className="rounded-3xl border border-[#EFE7D3] bg-[#FFF8E7] shadow-editorial p-6">
                <div className="flex items-center justify-between gap-4 mb-5">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-2xl bg-[#95BBEA] text-[#2B2523] flex items-center justify-center">
                      <Users className="w-5 h-5" />
                    </div>
                    <div>
                      <h2 className="font-serif-editorial text-2xl font-bold">Danh sách nhân viên</h2>
                      <p className="text-xs text-[#2B2523]/70">Theo dõi vai trò, kỹ năng và trạng thái trực ca.</p>
                    </div>
                  </div>
                  <Button variant="soft" size="sm" icon={RefreshCw} isLoading={isLoadingList} onClick={loadStaffList}>Làm mới</Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {staffList.map((staff) => {
                    const option = STATUS_OPTIONS.find((item) => item.value === staff.status) || STATUS_OPTIONS[2];
                    return (
                      <article key={staff.id} className="rounded-2xl border border-[#EFE7D3] p-4 bg-white/30">
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <h3 className="font-semibold text-[#2B2523]">{staff.full_name}</h3>
                            <p className="text-xs text-[#2B2523]/60 mt-0.5">{staff.email}</p>
                          </div>
                          <Badge variant="outline">{staff.role}</Badge>
                        </div>
                        <div className="mt-4 flex items-center gap-2 text-xs font-semibold">
                          <span className={`w-2.5 h-2.5 rounded-full ${option.tone}`} />
                          {statusLabel(staff.status)}
                        </div>
                        <p className="mt-3 text-xs text-[#2B2523]/70 leading-relaxed">
                          Kỹ năng: {(staff.skills && staff.skills.length > 0) ? staff.skills.join(', ') : 'Chưa cấu hình'}
                        </p>
                      </article>
                    );
                  })}
                </div>
              </div>
            </>
          ) : (
            <div className="rounded-3xl border border-[#EFE7D3] bg-[#FFF8E7] shadow-editorial p-8 text-center">
              <ShieldCheck className="w-12 h-12 mx-auto text-[#930500]" />
              <h2 className="font-serif-editorial text-3xl font-bold mt-4">Bàn làm việc Agent</h2>
              <p className="text-sm text-[#2B2523]/70 mt-2 max-w-xl mx-auto">
                Tài khoản Agent có thể đổi trạng thái trực ca. Các chức năng hàng đợi và tiếp quản hội thoại sẽ thuộc Use Case 3.3.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
