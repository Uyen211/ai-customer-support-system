import React, { useState } from 'react';
import { Mail, Lock, ArrowLeft, AlertTriangle, ShieldAlert } from 'lucide-react';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { authService } from '../../services/authService';
import { useAuth } from '../../hooks/useAuth';

export function CustomerLogin({ onNavigate }) {
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState(null);
  const [isLocked, setIsLocked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const validate = () => {
    const errs = {};
    if (!formData.email.trim()) {
      errs.email = 'Vui lòng nhập địa chỉ email';
    }
    if (!formData.password) {
      errs.password = 'Vui lòng nhập mật khẩu';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
    setApiError(null);
    setIsLocked(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setApiError(null);
    setIsLocked(false);

    try {
      const res = await authService.loginCustomer({
        email: formData.email,
        password: formData.password,
      });

      if (res && res.access_token) {
        login(res.access_token, res.customer);
        onNavigate('chat');
      }
    } catch (err) {
      const status = err.response?.status;
      const detail = err.response?.data?.detail || 'Đăng nhập thất bại.';

      if (status === 423 || detail.includes('15')) {
        setIsLocked(true);
        setApiError('Tài khoản đã bị tạm khóa 15 phút do nhập sai mật khẩu quá 5 lần liên tiếp.');
      } else if (status === 401) {
        setApiError('Email hoặc mật khẩu không chính xác. Vui lòng kiểm tra lại.');
      } else {
        setApiError(detail);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] flex flex-col justify-center items-center p-6 selection:bg-[#930500] selection:text-[#FFF8E7]">
      <div className="w-full max-w-md">
        
        {/* Back button */}
        <button
          onClick={() => onNavigate('landing')}
          className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#2B2523]/70 hover:text-[#930500] mb-6 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Quay lại Trang Chủ
        </button>

        {/* Card */}
        <div className="bg-[#FFF8E7] rounded-3xl p-8 sm:p-10 border border-[#EFE7D3] shadow-editorial">
          
          <div className="text-center mb-8">
            <div className="w-12 h-12 rounded-full bg-[#930500] text-[#FFF8E7] flex items-center justify-center font-serif-editorial text-2xl mx-auto mb-3">
              🐾
            </div>
            <h2 className="font-serif-editorial text-3xl font-bold text-[#2B2523]">Đăng Nhập Khách Hàng</h2>
            <p className="text-xs text-[#2B2523]/70 mt-1 font-light">
              Chào mừng bạn trở lại với hệ thống hỗ trợ PetHome.
            </p>
          </div>

          {/* Account Lockout Banner */}
          {isLocked && (
            <div className="mb-6 p-4 rounded-2xl bg-[#FEF3C7] border border-[#FDE68A] text-xs text-[#92400E] flex items-start gap-3 animate-fade-in">
              <ShieldAlert className="w-5 h-5 shrink-0 text-[#D97706] mt-0.5" />
              <div>
                <p className="font-bold text-[#78350F]">Tài khoản tạm thời bị khóa!</p>
                <p className="mt-0.5 leading-relaxed">
                  Để bảo mật thông tin, tài khoản bị tạm khóa 15 phút do nhập sai quá 5 lần. Vui lòng thử lại sau.
                </p>
              </div>
            </div>
          )}

          {/* Generic Error Banner */}
          {apiError && !isLocked && (
            <div className="mb-6 p-4 rounded-2xl bg-[#930500]/10 border border-[#930500]/20 flex items-start gap-3 text-xs text-[#930500] animate-fade-in">
              <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{apiError}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Địa chỉ Email"
              name="email"
              type="email"
              placeholder="khachhang@example.com"
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

            <div className="pt-2">
              <Button
                type="submit"
                variant="primary"
                size="lg"
                isLoading={isLoading}
                disabled={isLocked}
                className="w-full justify-center"
              >
                Đăng Nhập
              </Button>
            </div>
          </form>

          <div className="mt-8 pt-6 border-t border-[#EFE7D3] text-center">
            <p className="text-xs text-[#2B2523]/70 font-light">
              Chưa có tài khoản?{' '}
              <button
                onClick={() => onNavigate('register')}
                className="font-semibold text-[#930500] hover:underline"
              >
                Đăng ký ngay
              </button>
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}
