import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Mail, Lock, User, Phone, ArrowLeft, AlertCircle } from 'lucide-react';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { authService } from '../../services/authService';
import { useAuth } from '../../hooks/useAuth';

import logoAsset from '../../assets/logo.png';

export function CustomerRegister({ onNavigate }) {
  const { login } = useAuth();
  const [apiError, setApiError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm({
    mode: 'onTouched',
    defaultValues: {
      full_name: '',
      email: '',
      phone_number: '',
      password: '',
      confirm_password: '',
    },
  });

  const passwordValue = watch('password');

  const onSubmit = async (data) => {
    setIsLoading(true);
    setApiError(null);

    try {
      const res = await authService.registerCustomer({
        full_name: data.full_name.trim(),
        email: data.email.trim(),
        password: data.password,
        phone: data.phone_number ? data.phone_number.trim() : undefined,
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

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
            <Input
              label="Họ và tên"
              placeholder="Nguyễn Văn A"
              icon={User}
              error={errors.full_name?.message}
              required
              {...register('full_name', {
                required: 'Vui lòng không để trống họ và tên',
                minLength: {
                  value: 2,
                  message: 'Họ và tên phải có ít nhất 2 ký tự',
                },
                maxLength: {
                  value: 50,
                  message: 'Họ và tên không được vượt quá 50 ký tự',
                },
              })}
            />

            <Input
              label="Địa chỉ Email"
              type="email"
              placeholder="khachhang@example.com"
              icon={Mail}
              error={errors.email?.message}
              required
              {...register('email', {
                required: 'Vui lòng không để trống địa chỉ email',
                pattern: {
                  value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                  message: 'Địa chỉ email không đúng định dạng (VD: ten@domain.com)',
                },
              })}
            />

            <Input
              label="Số điện thoại (tùy chọn)"
              type="tel"
              placeholder="0912345678"
              icon={Phone}
              error={errors.phone_number?.message}
              {...register('phone_number', {
                validate: (value) => {
                  if (!value || !value.trim()) return true;
                  return /^0\d{9}$/.test(value.trim()) || 'Số điện thoại phải gồm 10 chữ số bắt đầu bằng 0';
                },
              })}
            />

            <Input
              label="Mật khẩu"
              type="password"
              placeholder="Ít nhất 8 ký tự (gồm cả chữ & số)"
              icon={Lock}
              error={errors.password?.message}
              required
              {...register('password', {
                required: 'Vui lòng không để trống mật khẩu',
                minLength: {
                  value: 8,
                  message: 'Mật khẩu tối thiểu 8 ký tự gồm chữ và số',
                },
                validate: (value) =>
                  /(?=.*[A-Za-z])(?=.*\d)/.test(value) || 'Mật khẩu bắt buộc phải chứa cả chữ cái và chữ số',
              })}
            />

            <Input
              label="Xác nhận mật khẩu"
              type="password"
              placeholder="Nhập lại mật khẩu..."
              icon={Lock}
              error={errors.confirm_password?.message}
              required
              {...register('confirm_password', {
                required: 'Vui lòng xác nhận lại mật khẩu',
                validate: (value) =>
                  value === passwordValue || 'Mật khẩu xác nhận không trùng khớp',
              })}
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
