import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    // Dùng sessionStorage (riêng biệt cho từng tab) thay vì localStorage
    const token = sessionStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Biến cờ để tránh gọi logout nhiều lần liên tiếp (401 loop)
let isLoggingOut = false;

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Chỉ logout 1 lần, tránh vòng lặp 401 vô hạn
      if (!isLoggingOut) {
        isLoggingOut = true;

        // Xóa toàn bộ thông tin đăng nhập (sessionStorage cho tab hiện tại)
        sessionStorage.removeItem('token');
        sessionStorage.removeItem('user');
        sessionStorage.removeItem('accountType');

        // Force reload trang để React khởi tạo lại AuthContext
        // với token = null → tự động hiển thị trang login
        window.location.reload();

        // Reset cờ sau 3 giây (phòng trường hợp reload bị chậm)
        setTimeout(() => { isLoggingOut = false; }, 3000);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
