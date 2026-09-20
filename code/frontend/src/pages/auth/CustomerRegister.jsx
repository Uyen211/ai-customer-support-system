import React, { useState } from 'react';
import { Mail, Lock, User, Phone, ArrowLeft, AlertCircle, CheckCircle } from 'lucide-react';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { authService } from '../../services/authService';
import { useAuth } from '../../hooks/useAuth';

import logoAsset from '../../assets/logo.png';

export function CustomerRegister({ onNavigate }) {
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    phone_number: '',
  });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const validate = () => {
    const errs = {};
    if (!formData.full_name.trim()) {
      errs.full_name = 'Vui lòng nhập họ và tên';
    }
    if (!formData.email.trim()) {
      errs.email = 'Vui lòng nhập địa chỉ email';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errs.email = 'Email không hợp lệ (ví dụ: user@example.com)';
    }

    if (!formData.password) {
      errs.password = 'Vui lòng nhập mật khẩu';
    } else if (formData.password.length < 8) {
      errs.password = 'Mật khẩu phải có ít nhất 8 ký tự';
    } else if (!/(?=.*[A-Za-z])(?=.*\d)/.test(formData.password)) {
      errs.password = 'Mật khẩu phải bao gồm cả chữ cái và chữ số';
    }

    if (formData.phone_number && !/^(0[3|5|7|8|9])+([0-9]{8})$/.test(formData.phone_number)) {
      errs.phone_number = 'Số điện thoại không hợp lệ (10 chữ số bắt đầu bằng 0)';
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
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setApiError(null);

    try {
      const res = await authService.registerCustomer({
        full_name: formData.full_name,
        email: formData.email,
        password: formData.password,
        phone_number: formData.phone_number || undefined,
      });

      if (res && res.access_token) {
        login(res.access_token, res.customer);
        onNavigate('chat');
      } else {
        onNavigate('login');
      }
    } catch (err) {
      const detail = err.response?.data?.detail || 'Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.';
      setApiError(detail);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FFF8E7] flex flex-col justify-center items-center p-6 selection:bg-[#930500] selection:text-[#FFF8E7]">
      <div className="w-full max-w-md">
        
        {/* Back Button */}
        <button
          onClick={() => onNavigate('landing')}
          className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#2B2523]/70 hover:text-[#930500] mb-6 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" /> Quay lại Trang Chủ
        </button>

        {/* Form Card */}
        <div className="bg-[#FFF8E7] rounded-3xl p-8 sm:p-10 border border-[#EFE7D3] shadow-editorial">
          
          <div className="text-center mb-8">
            <img src={logoAsset} alt="PetHome Logo" className="w-16 h-16 rounded-full object-cover mx-auto mb-3 shadow-diffused border border-[#930500]/20" />
            <h2 className="font-serif-editorial text-3xl font-bold text-[#2B2523]">Đăng Ký Tài Khoản</h2>
            <p className="text-xs text-[#2B2523]/70 mt-1 font-light">
              Tạo tài khoản PetHome để trò chuyện với Trợ lý AI và lưu lịch sử hỗ trợ.
            </p>
          </div>

          {apiError && (
            <div className="mb-6 p-4 rounded-2xl bg-[#930500]/10 border border-[#930500]/20 flex items-start gap-3 text-xs text-[#930500]">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
              <span>{apiError}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Họ và tên"
              name="full_name"
              placeholder="Nguyễn Văn A"
              icon={User}
              value={formData.full_name}
              onChange={handleChange}
              error={errors.full_name}
              required
            />

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
              label="Số điện thoại (tùy chọn)"
              name="phone_number"
              type="tel"
              placeholder="0912345678"
              icon={Phone}
              value={formData.phone_number}
              onChange={handleChange}
              error={errors.phone_number}
            />

            <Input
              label="Mật khẩu"
              name="password"
              type="password"
              placeholder="Ít nhất 8 ký tự (gồm chữ & số)"
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
                className="w-full justify-center"
              >
                Tạo Tài Khoản Ngay
              </Button>
            </div>
          </form>

          <div className="mt-8 pt-6 border-t border-[#EFE7D3] text-center">
            <p className="text-xs text-[#2B2523]/70 font-light">
              Đã có tài khoản PetHome?{' '}
              <button
                onClick={() => onNavigate('login')}
                className="font-semibold text-[#930500] hover:underline"
              >
                Đăng nhập ngay
              </button>
            </p>
          </div>

        </div>
      </div>
    </div>
  );
}
