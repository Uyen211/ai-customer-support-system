import React, { useState } from 'react';
import { ArrowLeft, BriefcaseBusiness, Lock, Mail, AlertTriangle } from 'lucide-react';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { staffService } from '../../services/staffService';
import { useAuth } from '../../hooks/useAuth';

export function StaffLogin({ onNavigate }) {
  const { login } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const validate = () => {
    const nextErrors = {};
    if (!formData.email.trim()) nextErrors.email = 'Vui lòng nhập email nội bộ';
    if (!formData.password) nextErrors.password = 'Vui lòng nhập mật khẩu';
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => ({ ...prev, [name]: null }));
    setApiError(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setApiError(null);
    try {
      const res = await staffService.loginStaff(formData);
      login(res.access_token, res.user, 'STAFF');
      onNavigate('staff-console');
    } catch (error) {
      setApiError(error.response?.data?.detail || 'Đăng nhập nhân viên thất bại.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] flex flex-col justify-center items-center p-6 selection:bg-[#930500] selection:text-[#FFF8E7]">
      <div className="w-full max-w-md">
        <button
          onClick={() => onNavigate('landing')}
          className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#2B2523]/70 hover:text-[#930500] mb-6 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Quay lại Trang Chủ
        </button>

        <div className="bg-[#FFF8E7] rounded-3xl p-8 sm:p-10 border border-[#EFE7D3] shadow-editorial">
          <div className="text-center mb-8">
            <div className="w-12 h-12 rounded-full bg-[#2B2523] text-[#FFF8E7] flex items-center justify-center mx-auto mb-3">
              <BriefcaseBusiness className="w-6 h-6" />
            </div>
            <h2 className="font-serif-editorial text-3xl font-bold text-[#2B2523]">Cổng Nhân Viên</h2>
            <p className="text-xs text-[#2B2523]/70 mt-1 font-light">
              Đăng nhập Bàn làm việc CSKH PetHome.
            </p>
          </div>

          {apiError && (
            <div className="mb-6 p-4 rounded-2xl bg-[#930500]/10 border border-[#930500]/20 flex items-start gap-3 text-xs text-[#930500]">
              <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{apiError}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Email nội bộ"
              name="email"
              type="email"
              placeholder="agent.an@brand.com"
              icon={Mail}
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              required
            />
            <Input
              label="Mật khẩu"
              name="password"
              type="password"
              placeholder="Nhập mật khẩu..."
              icon={Lock}
              value={formData.password}
              onChange={handleChange}
              error={errors.password}
              required
            />
            <Button type="submit" variant="primary" size="lg" isLoading={isLoading} className="w-full justify-center">
              Đăng Nhập Nhân Viên
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
