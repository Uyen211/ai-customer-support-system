# Kế hoạch Kỹ thuật (Implementation Plan): Xây Dựng Giao Diện Frontend Khối 1 & Trang Chủ Marketing

> **TL;DR:** Xây dựng toàn bộ giao diện Frontend cho **Khối 1 (Trợ lý Tra cứu Thông tin Khách hàng)** và **Trang chủ Marketing Landing Page** giới thiệu chuỗi cửa hàng PetHome. Chuẩn hóa 100% ngôn ngữ thiết kế **Editorial Calm & Organic Minimalism** ([`design_pattern.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/design_pattern.md)) sử dụng React 18, Vite, Tailwind CSS, Lucide Icons, Axios API Services, React Context (`AuthContext`), và Custom Hook `useSSEChat` kết nối luồng SSE streaming token-by-token từ Backend.

---

## 1. 🎨 Ngôn Ngữ Thiết Kế & Design Tokens (Editorial Calm Style)

Hệ thống giao diện tuân thủ tuyệt đối triết lý thẩm mỹ và quy chuẩn thị giác tại [`docs/overview/design_pattern.md`](file:///d:/Study/TLU/kiemthu/project/docs/overview/design_pattern.md):

### 1.1. Bảng Màu chuẩn (Color Tokens & Quy tắc 60 - 30 - 10)
* **60% Canvas / Background (`Cosmic Latte` - `#FFF8E7`):** Nền kem bơ ấm áp bao phủ toàn bộ trang web và ứng dụng chat, thay thế màu trắng tinh khiết (`#FFFFFF`) để tạo chiều sâu mộc mạc, dịu mắt.
* **30% Secondary / Atmospheric (`Cornflower Blue` - `#95BBEA`):** Màu xanh lam pastel mờ dùng cho mảng nền phân khối (background blocks), khối phụ trợ, thẻ tính năng, container tin nhắn phụ để tạo nhịp nghỉ thị giác mát mẻ.
* **10% Primary Accent / Statement (`Sangria Red` - `#930500`):** Màu đỏ rượu đậm dùng cho Hero CTA buttons, điểm nhấn highlight, tiêu đề đặc biệt, nhãn thông báo quan trọng.
* **Neutral Dark / Typography (`Deep Espresso` - `#2B2523`):** Màu chữ chính tương phản cao trên nền bơ kem, tuyệt đối không dùng đen thuần `#000000`.
* **Neutral Light / Border (`Muted Cream / Hairline` - `rgba(147, 5, 0, 0.08)` / `#EFE7D3`):** Đường viền card mờ 1px và vệt phân cách mảnh tinh tế.

### 1.2. Kiểu Chữ Biên Tập (Editorial Typography Stack)
* **Display & Headings (H1, H2, H3):** Serif Biên Tập (`Playfair Display`, `Instrument Serif`) uốn lượn nghệ thuật, sang trọng.
* **Body & UI Elements:** Humanist Sans-serif (`Plus Jakarta Sans`, `Inter`), nét chữ mảnh-vừa, độ giãn dòng rộng thoáng (`leading-relaxed` / `line-height: 1.6 - 1.8`).
* **Eyebrow / Overline:** Nhãn phụ phía trên tiêu đề viết hoa nhẹ (`uppercase`), letter-spacing giãn nhẹ (`tracking-widest` / `+0.08em`).

### 1.3. Hình Khối & Bóng Đổ (Organic Geometry & Ambient Shadows)
* **Bo góc mềm mại (Large Radii):** Bo góc lớn (`16px - 32px` / `rounded-2xl`, `rounded-3xl`) cho card, modal và khung chat window. Nút bấm và nhãn status dùng dạng viên nhộng mềm (`rounded-full` / `pill shape`).
* **Bóng đổ tàng hình (Ambient Diffused Shadows):** Độ mờ lớn (`blur > 24px`), độ trong suốt cực thấp (`opacity: 4% - 8%`), hòa hợp tự nhiên vào nền bơ kem.
* **Chuyển động êm ái (Motion Tone):** Dynamic transition `300ms - 500ms` (`cubic-bezier(0.25, 1, 0.5, 1)`), hiệu ứng hover card phóng to cực nhẹ (`scale(1.015)`).

---

## 2. 🎯 Mục tiêu & Phạm vi (Goals & Scope)

### 2.1. Mục tiêu Cốt lõi
* **Trang chủ Marketing Landing Page (`LandingPage.jsx`)**: Trang giới thiệu phong cách biên tập cao cấp cho chuỗi PetHome trước khi đăng nhập. Bao gồm Banner Hero giới thiệu Trợ lý CSKH AI 24/7, Khối tính năng nổi bật nền xanh `#95BBEA`, Danh mục sản phẩm tiêu biểu bối cảnh Still-life, Chính sách đổi trả/freeship, và Nút bấm CTA đỏ `#930500` dẫn sang Đăng ký / Đăng nhập / Chat ngay.
* **Xác thực Khách hàng (`pages/auth/`)**: Màn hình Đăng ký (`CustomerRegister.jsx`) và Đăng nhập (`CustomerLogin.jsx`) trên nền kem `#FFF8E7` với card bo tròn `rounded-3xl`, form validation real-time, xử lý thông báo lỗi (email trùng, sai mật khẩu, tài khoản bị tạm khóa 15 phút).
* **Bàn Chat & Lịch sử Hội thoại (`pages/customer/ChatPage.jsx`)**:
  - Thanh Sidebar màu kem/bơ chứa danh sách phiên trò chuyện cũ, nhãn viên nhộng pill badges (`BOT`, `WAITING_HUMAN`, `HUMAN`, `CLOSED`).
  - Nút "Bắt đầu cuộc trò chuyện mới" khởi tạo phiên chat với lời chào tự động của AI Bot và các viên nhộng gợi ý câu hỏi (`SuggestionButtons.jsx`).
  - Tải phân đoạn Lazy Loading (50 tin nhắn gần nhất) khi cuộn lên trên.
* **Tích hợp Luồng Gõ chữ SSE & Trích dẫn RAG (`components/chat/`)**:
  - Bong bóng tin nhắn với hiệu ứng gõ chữ thời gian thực (token-by-token).
  - Popover/Drawer (`CitationsDrawer.jsx`) hiển thị trích dẫn tài liệu gốc (tên PDF, trang, điều khoản, snippet text).
  - Khóa ô nhập liệu khi phiên `CLOSED` và hiển thị dải thông báo khi `WAITING_HUMAN`.

### 2.2. Ngoài phạm vi (Out of Scope)
* Giao diện Bàn làm việc của Nhân viên CSKH (Khối 3: `LiveConsolePage.jsx`).
* Giao diện Bảng quản lý tiến độ Kanban và SLA Engine (Khối 4: `KanbanPage.jsx`).
* Giao diện Cấu hình AI Rules và Báo cáo Thống kê (Khối 2 & 4).

---

## 3. 🏗️ Kiến trúc Kỹ thuật & Luồng Dữ liệu Frontend

### 3.1. Cấu trúc Component & Data Flow
```text
[App.jsx] (React Router / Layout Provider - Canvas #FFF8E7)
   │
   ├── [LandingPage.jsx] (Trang chủ Marketing - Style Editorial Calm)
   │       ├── Editorial Hero Banner (Phông Serif, CTA Đỏ Sangria #930500)
   │       ├── Feature Cards Grid (Nền Xanh Pastel #95BBEA, Bo Góc rounded-3xl)
   │       └── Product Showcase & Pill CTA Buttons
   │
   ├── [CustomerAuth Pages] (CustomerLogin.jsx / CustomerRegister.jsx)
   │       └── Card bo tròn rounded-3xl, viền mist 1px ──► authService.js ──► Save JWT in AuthContext
   │
   └── [ChatPage.jsx] (Giao diện Chat Khách hàng - Stylised UI)
           ├── [Sidebar / ConversationList] (Màu bơ sáng, Pill Badges) ──► chatService.getConversations()
           │       └── [NewChatButton] (Pill CTA Sangria Red) ──────────► chatService.createConversation()
           │
           └── [ChatWindow.jsx]
                   ├── [MessageList.jsx] ───► chatService.getMessages(limit=50)
                   │       ├── [MessageItem.jsx] (SSE Streaming Token-by-Token, Bong bóng kem/xanh)
                   │       └── [CitationsDrawer.jsx] (Drawer trích dẫn RAG bo góc mềm)
                   │
                   ├── [StatusBanner.jsx] (WAITING_HUMAN / CLOSED warning pill banner)
                   └── [ChatInput.jsx] ─────► useSSEChat() ──► [POST /api/chat/stream]
```

---

## 4. 📂 Touchpoints (Danh sách Tệp Tác động)

### 4.1. Các Tệp Tạo Mới & Cấu Hình Design Tokens
* `code/frontend/src/index.css`: Cấu hình Google Fonts (`Playfair Display`, `Plus Jakarta Sans`), variables màu sắc CSS (`--color-canvas: #FFF8E7`, `--color-primary-accent: #930500`, `--color-secondary-block: #95BBEA`, `--color-neutral-dark: #2B2523`, `--color-muted-border: #EFE7D3`).
* `code/frontend/src/utils/constants.js`: Khai báo hằng số API URL, Enum Mode, Enum Status, Suggestion Prompts.
* `code/frontend/src/utils/formatters.js`: Định dạng tiền VNĐ (`145.000đ`), định dạng ngày giờ (`DD/MM/YYYY HH:mm`).
* `code/frontend/src/services/api.js`: Khởi tạo Axios Instance với Interceptor tự động gán Bearer Token.
* `code/frontend/src/services/authService.js`: Gọi API register, login, get current user (`/api/auth/customer/*`).
* `code/frontend/src/services/chatService.js`: Gọi API lấy danh sách phiên, mở phiên mới, lấy 50 tin nhắn, đóng phiên (`/api/conversations/*`).
* `code/frontend/src/context/AuthContext.jsx`: State quản lý thông tin khách hàng, JWT token, login/logout functions.
* `code/frontend/src/hooks/useAuth.js`: Custom Hook dùng AuthContext nhanh.
* `code/frontend/src/hooks/useSSEChat.js`: Custom Hook xử lý fetch SSE Stream token-by-token.
* `code/frontend/src/components/common/Button.jsx`: Component Nút bấm chuẩn hóa Design System (Pill shape `rounded-full`, Primary Red `#930500`, Secondary Blue `#95BBEA`, Ghost Outline).
* `code/frontend/src/components/common/Input.jsx`: Component Ô nhập liệu bo góc `rounded-2xl`, viền mờ `rgba(147, 5, 0, 0.08)`.
* `code/frontend/src/components/common/Modal.jsx`: Component Hộp thoại Popup Modal bo góc `rounded-3xl` với hiệu ứng diffused shadow.
* `code/frontend/src/components/common/Badge.jsx`: Component Nhãn viên nhộng pill status (BOT, WAITING_HUMAN, CLOSED).
* `code/frontend/src/components/common/LoadingSpinner.jsx`: Component Icon chờ nạp dữ liệu tông đỏ rượu/xanh mờ.
* `code/frontend/src/components/chat/MessageItem.jsx`: Bong bóng chat (User: Nền bơ đậm/đỏ rượu nhẹ; Bot: Nền xanh pastel `#95BBEA` hoặc bơ sáng `#FFF8E7`) kèm hiệu ứng gõ từng từ.
* `code/frontend/src/components/chat/MessageList.jsx`: Khung chứa tin nhắn & cuộn tự động / lazy loading.
* `code/frontend/src/components/chat/CitationsDrawer.jsx`: Drawer xem chi tiết trích dẫn tài liệu bo góc `rounded-3xl`.
* `code/frontend/src/components/chat/SuggestionButtons.jsx`: Các nút dạng viên nhộng pill chips gợi ý câu hỏi nhanh.
* `code/frontend/src/components/chat/ChatWindow.jsx`: Khung hội thoại chính ghép nối tin nhắn & ô nhập trên nền bơ `#FFF8E7`.
* `code/frontend/src/pages/customer/LandingPage.jsx`: Trang chủ Marketing phong cách Editorial Calm giới thiệu PetHome & CSKH AI.
* `code/frontend/src/pages/auth/CustomerLogin.jsx`: Trang Đăng nhập Khách hàng phong cách organic minimalism.
* `code/frontend/src/pages/auth/CustomerRegister.jsx`: Trang Đăng ký Tài khoản Khách hàng.
* `code/frontend/src/pages/customer/ChatPage.jsx`: Màn hình Chat tổng thể (Sidebar màu bơ sáng + ChatWindow).

### 4.2. Các Tệp Cập Nhật
* `code/frontend/src/App.jsx`: Điều phối Navigation & bọc Provider Wrappers.

---

## 5. 📝 Implementation Checklist (Danh Sách Bước Thực Thi Chi Tiết)

### Giai Đoạn 1: Tiện ích, Design System Tokens & API Services
1. [ ] Cập nhật `code/frontend/src/index.css`: Cấu hình Google Fonts (`Playfair Display`, `Plus Jakarta Sans`), định nghĩa CSS custom properties cho Canvas `#FFF8E7`, Accent `#930500`, Secondary `#95BBEA`, Neutral Dark `#2B2523`, viền `#EFE7D3`.
2. [ ] Tạo `code/frontend/src/utils/constants.js`: Định nghĩa Base URL (`http://localhost:8000`), Enums `MODE`, `CONVERSATION_STATUS`, các gợi ý câu hỏi mẫu.
3. [ ] Tạo `code/frontend/src/utils/formatters.js`: Hàm `formatVND(amount)`, `formatDateTime(isoStr)`, `formatTimeAgo(isoStr)`.
4. [ ] Tạo `code/frontend/src/services/api.js`: Cấu hình Axios instance với Interceptors đọc JWT từ localStorage và gán Header `Authorization: Bearer <token>`.
5. [ ] Tạo `code/frontend/src/services/authService.js`: Viết các hàm `registerCustomer(data)`, `loginCustomer(data)`, `getMe()`.
6. [ ] Tạo `code/frontend/src/services/chatService.js`: Viết các hàm `getConversations()`, `createConversation()`, `getMessages(conversationId, limit, beforeId)`, `closeConversation(conversationId)`.
7. [ ] Tạo `code/frontend/src/context/AuthContext.jsx` & `code/frontend/src/hooks/useAuth.js`: Quản lý `user`, `token`, `isLoggedIn`, hàm `login()`, `logout()`.

### Giai Đoạn 2: UI Components Dùng Chung (Editorial Style) & Custom Hooks
8. [ ] Tạo `code/frontend/src/components/common/Button.jsx`, `Input.jsx`, `Badge.jsx`, `Modal.jsx`, `LoadingSpinner.jsx`: Chuẩn hóa 100% hình khối bo tròn `rounded-full` / `rounded-3xl`, bóng mờ diffused shadow, màu sắc `#930500` và `#95BBEA`.
9. [ ] Tạo Custom Hook `code/frontend/src/hooks/useSSEChat.js`: Xử lý gửi tin nhắn tới `/api/chat/stream`, đọc stream token-by-token từ `response.body.getReader()`, lưu trạng thái `isStreaming`, `streamedContent`, `citations`.

### Giai Đoạn 3: Trang Chủ Marketing Landing Page (Editorial Calm & Organic Minimalism)
10. [ ] Tạo `code/frontend/src/pages/customer/LandingPage.jsx`:
    - **Header/Navbar**: Logo PetHome, font Serif, nút "Đăng nhập", "Đăng ký" và "Trợ lý AI 24/7" dạng viên nhộng pill.
    - **Hero Section**: Tiêu đề Serif lớn "Chuỗi Cửa Hàng Đồ Dùng Thú Cưng PetHome & Trợ Lý CSKH AI 24/7", nền bơ `#FFF8E7`, nút CTA nổi bật màu đỏ rượu `#930500`.
    - **Features Grid**: 4 khối tính năng mảng nền xanh pastel `#95BBEA` bo góc `rounded-3xl` (Tra cứu tồn kho real-time, Tư vấn đổi trả/freeship, Giám sát cảm xúc, Trích dẫn nguồn tài liệu).
    - **Product Showcase**: Khối hình ảnh sản phẩm phong cách Still-life studio, bóng đổ mờ tự nhiên.
    - **Footer**: Thông tin chuỗi cửa hàng, thiết kế tối giản thư thái.

### Giai Đoạn 4: Màn Hình Đăng Ký & Đăng Nhập Khách Hàng
11. [ ] Tạo `code/frontend/src/pages/auth/CustomerRegister.jsx`: Form đăng ký nằm trong card kem/bơ bo góc `rounded-3xl` với validation real-time (Họ tên, Email, Mật khẩu >= 8 ký tự, SĐT). Báo lỗi trùng email.
12. [ ] Tạo `code/frontend/src/pages/auth/CustomerLogin.jsx`: Form đăng nhập với email & mật khẩu. Xử lý báo lỗi sai thông tin và cảnh báo tài khoản bị khóa 15 phút (423 Locked).

### Giai Đoạn 5: Components Chat & Màn Hình ChatPage Tổng Thể
13. [ ] Tạo `code/frontend/src/components/chat/CitationsDrawer.jsx`: Drawer / Popup bo góc `rounded-3xl` hiển thị danh sách trích dẫn nguồn tài liệu RAG.
14. [ ] Tạo `code/frontend/src/components/chat/SuggestionButtons.jsx`: Các nút viên nhộng pill chips gợi ý câu hỏi mẫu.
15. [ ] Tạo `code/frontend/src/components/chat/MessageItem.jsx` & `MessageList.jsx`: Bong bóng chat mềm mại, hiệu ứng gõ chữ thời gian thực, nút "Xem trích dẫn", cuộn tự động / lazy loading 50 tin nhắn cũ.
16. [ ] Tạo `code/frontend/src/components/chat/ChatWindow.jsx`: Khung chat ghép nối tin nhắn, dải thông báo trạng thái (`WAITING_HUMAN`, `CLOSED`), ô nhập văn bản và nút gửi.
17. [ ] Tạo `code/frontend/src/pages/customer/ChatPage.jsx`: Màn hình Chat hoàn chỉnh kết hợp Sidebar danh sách phiên chat cũ và Khung ChatWindow.
18. [ ] Cập nhật `code/frontend/src/App.jsx`: Điều phối Navigation giữa Landing Page, Auth Pages, và Chat Page.

---

## 6. 🎯 Acceptance Criteria (Tiêu Chuẩn Nghiệm Thu)

| Mã AC | Tiêu Chuẩn Nghiệm Thu | Phương Pháp Chứng Minh | SPEC Ref |
| :--- | :--- | :--- | :--- |
| **AC-FE-1.0** | Trang chủ Marketing Landing Page hiển thị chuẩn ngôn ngữ Editorial Calm (Nền kem `#FFF8E7`, phông Serif, CTA Đỏ `#930500`, Block xanh `#95BBEA`). | Manual / E2E Test `LandingPage.test.jsx` | SPEC US-1.0 |
| **AC-FE-1.1** | Form Đăng ký validate dữ liệu máy khách và đăng ký thành công; Form Đăng nhập báo lỗi khi sai mật khẩu hoặc bị khóa 15p (423 Locked). | Manual / E2E Test `Auth.test.jsx` | SPEC US-1.1 (AC-1, AC-2) |
| **AC-FE-1.2** | Màn hình ChatPage hiển thị Sidebar với danh sách các phiên cũ, nhãn trạng thái viên nhộng pill badges và đoạn tóm tắt tin nhắn cuối. | Manual / E2E Test `Sidebar.test.jsx` | SPEC US-1.2 (AC-3) |
| **AC-FE-1.3** | Bấm "Bắt đầu cuộc trò chuyện mới" tạo phiên chat `BOT` và nhận lời chào mừng tự động kèm nút gợi ý viên nhộng. | Manual / E2E Test `NewChat.test.jsx` | SPEC US-1.2 (AC-4) |
| **AC-FE-1.4** | Cuộn lên đầu danh sách tin nhắn tải thêm 50 tin nhắn cũ hơn (Lazy Loading). | Manual / E2E Test `LazyLoad.test.jsx` | SPEC US-1.2 (AC-5) |
| **AC-FE-1.5** | Gửi tin nhắn kích hoạt luồng SSE Stream `/api/chat/stream`, câu trả lời gõ từng từ thời gian thực; bấm nút "Xem trích dẫn" mở Pop-up trích đoạn tài liệu gốc. | Manual / E2E Test `SSEStream.test.jsx` | SPEC US-1.3 (AC-6, AC-7) |
| **AC-FE-1.6** | Phiên `CLOSED` khóa ô nhập liệu và báo dải thông báo xám; Phiên `WAITING_HUMAN` hiển thị dải thông báo cam. | Manual / E2E Test `SessionMode.test.jsx` | SPEC US-1.2 (AC-8) |

---

## 7. 💥 Blast Radius & Security Safeguards

* **Blast Radius**: Toàn bộ thay đổi nằm gói gọn trong `code/frontend/src/` và `code/frontend/public/`.
* **Bảo mật Frontend**:
  - Không lưu mật khẩu thô trong State hay localStorage.
  - JWT Access Token được lưu an toàn trong localStorage và gán tự động vào Header qua Axios Interceptor.
  - Xóa Token và chuyển trạng thái về chưa đăng nhập khi nhận HTTP 401 từ Server.

---

## 8. 🛡️ Test Infra Improvement Notes
(none identified yet)

---

## 9. 🔄 Resume and Execution Handoff

* **Tệp Kế Hoạch**: `process/features/customer-assistant/active/customer-services_16-09-26/customer-services_PLAN_16-09-26.md`
* **Trạng thái**: Đã nghiệm thu Validate Contract (Gate: PASS), chuẩn hóa 100% Design System Editorial Calm, sẵn sàng triển khai mã nguồn Frontend.

---

## Validate Contract

Status: PASS
Date: 16-09-26
date: 2026-09-16
generated-by: outer-pvl

Parallel strategy: sequential
Rationale: 7/7 signals favor sequential execution due to clear layered dependency chain (CSS Tokens/Utils/Services -> Context/Hooks -> Marketing Page -> Auth Pages -> Chat Components -> Chat Page).

Test gates:

| criterion id | behavior | strategy | proving test | gap-resolution |
|---|---|---|---|---|
| AC-FE-1.0 | Editorial Marketing Landing Page render hero, features, CTA buttons | Fully-Automated | `src/pages/customer/LandingPage.test.jsx` | B |
| AC-FE-1.1 | Customer Auth Forms validation & lockout alerts | Fully-Automated | `src/pages/auth/Auth.test.jsx` | B |
| AC-FE-1.2 | Sidebar Conversation List with snippet & mode badges | Fully-Automated | `src/components/chat/Sidebar.test.jsx` | B |
| AC-FE-1.3 | Create New Chat with Auto Greeting & Suggestion Chips | Fully-Automated | `src/components/chat/NewChat.test.jsx` | B |
| AC-FE-1.4 | Message History 50-limit Lazy Load on scroll | Fully-Automated | `src/components/chat/LazyLoad.test.jsx` | B |
| AC-FE-1.5 | SSE Token Stream Real-time Typing & Citations Drawer | Fully-Automated | `src/components/chat/SSEStream.test.jsx` | B |
| AC-FE-1.6 | CLOSED & WAITING_HUMAN Mode Warning Banners | Fully-Automated | `src/components/chat/SessionMode.test.jsx` | B |

Legacy line form:
- landing_page: [Fully-automated: npm run test src/pages/customer/LandingPage.test.jsx]
- auth_ui: [Fully-automated: npm run test src/pages/auth/Auth.test.jsx]
- chat_ui: [Fully-automated: npm run test src/components/chat/SSEStream.test.jsx]

Dimension findings:
- Infra fit: PASS — Cấu trúc React 18, Vite, Tailwind CSS, Editorial Design Tokens (`#FFF8E7`, `#930500`, `#95BBEA`), Axios Services & Context API hoàn toàn khớp với kiến trúc hệ thống.
- Test coverage: PASS — Bao phủ 100% các tiêu chí SPEC cho Trang chủ Marketing, Auth, Chatbot và RAG SSE stream.
- Breaking changes: PASS — Bổ sung các components & pages giao diện người dùng mới (Additive).
- Security surface: PASS — Axios Interceptor tự động đính kèm Bearer JWT Token, tự xóa token khi 401, không lưu mật khẩu thô.

Open gaps: none

What this coverage does NOT prove:
- Mức độ hiển thị chuẩn xác trên các thiết bị di động có màn hình quá nhỏ (<320px).

Gate: PASS
Accepted by: user (requested plan)

## Autonomous Goal Block

TARGET: Triển khai hoàn chỉnh giao diện Frontend cho Khối 1 và Trang chủ Marketing theo checklist trong customer-services_PLAN_16-09-26.md.
PER-PHASE LOOP: Research -> Innovate -> Plan -> Validate -> Execute -> Review
HARD STOPS: Không làm gián đoạn mã nguồn Backend; dừng lại nếu kiểm thử giao diện thất bại.
SAFETY: Luôn kiểm tra tính hợp lệ của token; không lưu thông tin nhạy cảm vào State tĩnh.
TEST GATES: automated
VALIDATE CONTRACT: customer-services_PLAN_16-09-26.md
START: Step 1 of Implementation Checklist

