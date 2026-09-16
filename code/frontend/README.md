# 🎨 Omnichannel Support Frontend (React + Vite + Tailwind CSS)

> Mã nguồn Giao diện Người dùng (Frontend Single Page Application) phục vụ Hệ thống Trợ lý Trực ca CSKH AI & Giám sát Vận hành Tự động. Đã hoàn thiện **Trang chủ Marketing Landing Page**, **Phân hệ Xác thực Khách hàng**, và **Khối 1: Customer RAG Chatbot** chuẩn phong cách **Editorial Calm & Organic Minimalism** ([`design_pattern.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/design_pattern.md)).

---

## 🎨 Ngôn Ngữ Thị Giác (Editorial Calm Design Tokens)

* **60% Canvas / Background**: `Cosmic Latte` (`#FFF8E7`) — Kem bơ ấm áp bao phủ toàn bộ trang web và bàn chat.
* **30% Secondary / Block**: `Cornflower Blue` (`#95BBEA`) — Màu xanh lam pastel mờ cho các mảng khối tính năng và thẻ phụ trợ.
* **10% Primary Accent**: `Sangria Red` (`#930500`) — Sắc đỏ rượu đậm kiêu hãnh cho các nút Hero CTA, tiêu đề nghệ thuật và nhãn chú ý.
* **Neutral Dark / Typography**: `Deep Espresso` (`#2B2523`) — Tương phản tự nhiên, không dùng đen thuần `#000000`.
* **Editorial Typography**: Headings Serif (`Playfair Display`, `Instrument Serif`) + Body Sans (`Plus Jakarta Sans`, `Be Vietnam Pro`).

---

## 📁 Cấu trúc Thư mục Kỹ thuật (Project Directory Structure)

Mã nguồn Frontend được tổ chức chuẩn hóa theo mô hình **Feature-driven Modular Design**:

```text
code/frontend/
├── public/                            # Tài nguyên tĩnh phục vụ public URL
│   ├── sounds/                        # Âm thanh thông báo & chuông báo động
│   └── vite.svg
│
├── src/
│   ├── assets/                        # Hình ảnh, biểu tượng (icons) tĩnh nội bộ
│   │
│   ├── components/                    # Bộ các React UI Components tái sử dụng
│   │   ├── common/                    # Các UI Component nguyên tử chuẩn Editorial
│   │   │   ├── Button.jsx             # Nút bấm viên nhộng pill (Primary #930500, Secondary #95BBEA)
│   │   │   ├── Input.jsx              # Ô nhập dữ liệu bo góc rounded-2xl kèm kiểm tra lỗi
│   │   │   ├── Modal.jsx              # Hộp thoại Modal Popup bo góc rounded-3xl
│   │   │   ├── Badge.jsx              # Nhãn trạng thái (P1/P2/P3, ONLINE/BUSY, BOT/HUMAN/CLOSED)
│   │   │   └── LoadingSpinner.jsx     # Biểu tượng chờ nạp dữ liệu
│   │   │
│   │   ├── chat/                      # Các Components cho Khối 1 (Customer Chatbot)
│   │   │   ├── ChatWindow.jsx         # Khung hội thoại chính ghép nối tin nhắn & ô nhập
│   │   │   ├── MessageList.jsx        # Khung danh sách tin nhắn & lazy loading 50 tin nhắn cũ
│   │   │   ├── MessageItem.jsx        # Bong bóng tin nhắn & hiệu ứng gõ chữ thời gian thực
│   │   │   ├── CitationsDrawer.jsx    # Popover / Drawer hiển thị trích dẫn nguồn tài liệu RAG
│   │   │   └── SuggestionButtons.jsx  # Các nút viên nhộng gợi ý câu hỏi mẫu
│   │   │
│   │   ├── agent/                     # Các Components cho Khối 3 (Live Support Console - Đang phát triển)
│   │   └── kanban/                    # Các Components cho Khối 4 (Kanban & SLA Engine - Đang phát triển)
│   │
│   ├── context/                       # Quản lý State toàn cục bằng React Context API
│   │   └── AuthContext.jsx            # State lưu trữ JWT token, thông tin user & đăng nhập/đăng xuất
│   │
│   ├── hooks/                         # Custom React Hooks đóng gói logic nghiệp vụ
│   │   ├── useAuth.js                 # Hook truy cập AuthContext nhanh
│   │   └── useSSEChat.js              # Hook kết nối luồng SSE Stream (`/api/chat/stream`) token-by-token
│   │
│   ├── pages/                         # Các trang màn hình chính (Pages)
│   │   ├── auth/                      # Phân hệ Xác thực
│   │   │   ├── CustomerLogin.jsx      # Trang đăng nhập Khách hàng (xử lý cảnh báo khóa 15p / 423)
│   │   │   └── CustomerRegister.jsx   # Trang đăng ký tài khoản Khách hàng (validate real-time)
│   │   │
│   │   ├── customer/                  # Phân hệ Khách hàng
│   │   │   ├── LandingPage.jsx        # Trang chủ Marketing phong cách Editorial giới thiệu PetHome & CSKH AI
│   │   │   └── ChatPage.jsx           # Màn hình Chat tư vấn RAG tự động 24/7 (Sidebar + ChatWindow)
│   │   │
│   │   └── admin/                     # Phân hệ Quản trị & Nhân sự CSKH (Đang phát triển)
│   │
│   ├── services/                      # Tầng gọi API mạng (Network API Layer - Axios)
│   │   ├── api.js                     # Cấu hình Axios Instance (Base URL, Interceptor đính kèm Bearer JWT)
│   │   ├── authService.js             # API đăng ký, đăng nhập Customer & lấy thông tin người dùng
│   │   └── chatService.js             # API lấy phiên trò chuyện, mở phiên mới, nạp 50 tin nhắn, đóng phiên
│   │
│   ├── utils/                         # Hàm tiện ích & Hằng số dùng chung
│   │   ├── formatters.js              # Định dạng tiền tệ VNĐ (VD: `145.000đ`), định dạng ngày giờ Tiếng Việt
│   │   └── constants.js               # Định nghĩa Base URL, Enums MODE, STATUS, các câu hỏi mẫu gợi ý
│   │
│   ├── App.jsx                        # Component gốc điều phối Navigation & Provider Wrappers
│   ├── main.jsx                       # Điểm gắn kết React DOM
│   └── index.css                      # Import Tailwind CSS directives & Google Fonts Editorial
│
├── package.json                       # Khai báo thư viện phụ thuộc (React 19, Vite, Tailwind, Axios, Lucide)
└── vite.config.js                     # Cấu hình Vite Dev Server & Proxy API về Backend
```

---

## 🔑 Tài Khoản Kiểm Thử Mẫu (Test Credentials)

Chi tiết danh sách tài khoản được lưu trữ tại [`docs/database/accounts.md`](file:///d:/Study/TLU/kiemthu/project/docs/database/accounts.md):
* **Mật khẩu chung:** `123456`
* **Khách hàng 1:** `khachhang1@gmail.com`
* **Khách hàng 2:** `khachhang2@gmail.com`

---

## 🚀 Khởi Chạy Nhanh (Quick Start)

### 1. Cài đặt Thư viện
```bash
cd code/frontend
npm install
```

### 2. Khởi chạy ở Chế độ Development
```bash
npm run dev
```
Giao diện chạy tại: [http://localhost:5173](http://localhost:5173).

### 3. Build Sản Xuất (Production Build)
```bash
npm run build
```
Kết quả kiểm thử build: **100% PASS (0 Error, 0 Warning)**.
