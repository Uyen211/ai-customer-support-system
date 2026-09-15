# HƯỚNG DẪN DÀNH CHO NGƯỜI MỚI: SETUP & VẬN HÀNH DỰ ÁN

Tài liệu này hướng dẫn chi tiết từng bước cho thành viên mới khi tải mã nguồn dự án về: từ khâu **khởi tạo lần đầu tiên**, **cách bật hệ thống hàng ngày**, **cách tắt hệ thống** đến **cách kiểm tra và xử lý sự cố**.

---

## ⚙️ YÊU CẦU TIỀN ĐỀ (PREREQUISITES)

Trước khi bắt đầu, máy tính của bạn cần được cài đặt sẵn:
1. **Docker Desktop** (Đã bật và đang chạy dịch vụ Docker engine).
2. **Git** (Để clone dự án) hoặc file nén mã nguồn dự án.

---

## 🚀 1. LẦN ĐẦU TIÊN KHI MỚI TẢI DỰ ÁN VỀ (FIRST-TIME SETUP)

### **Bước 1: Mở thư mục mã nguồn**
Mở giao diện dòng lệnh (Terminal / Command Prompt / PowerShell) và di chuyển vào thư mục `code/`:
```bash
cd code
```

### **Bước 2: Tạo file biến môi trường `.env`**
Tạo một file tên là **`.env`** nằm trực tiếp bên trong thư mục `code/` (nếu chưa có) và dán nội dung cấu hình kết nối như sau:

```env
# Kết nối CSDL Supabase PostgreSQL
DATABASE_URL="postgresql+psycopg2://postgres.xxxx:your-password@aws-0-ap-northeast-1.pooler.supabase.com:6543/postgres"

# Kết nối Hàng đợi Redis
REDIS_URL=redis://localhost:6379/0

# API Key cho LLM Engine (OpenAI / Gemini API)
OPENAI_API_KEY=your-openai-api-key-here
```
*(Lưu ý: Thay `your-password` và `your-openai-api-key-here` bằng thông tin chính xác do Nhóm trưởng cung cấp).*

### **Bước 3: Khởi chạy & Build toàn bộ hệ thống qua Docker**
Tại thư mục `code/`, chạy duy nhất lệnh sau:
```bash
docker compose up --build -d
```

* **Hiện tượng diễn ra:**
  - Ở lần đầu tiên, Docker sẽ tự động tải các hình ảnh (images) của **Redis**, **Python 3.11** và **Node 20**.
  - Docker sẽ tự động cài đặt 100% tất cả các thư viện Backend trong `requirements.txt` và Frontend trong `package.json`.
  - Quá trình này mất khoảng **1 - 2 phút**.
  - Kết quả hiển thị `Healthy / Created / Started` cho cả 3 container (`cs_redis`, `cs_backend`, `cs_frontend`) là bạn đã setup thành công!

---

## 🔌 2. NHỮNG LẦN SAU: CÁCH BẬT VÀ TẮT HỆ THỐNG HÀNG NGÀY

Sau lần đầu tiên đã build thành công, những lần sau khi mở máy làm việc bạn thực hiện như sau:

### 🟢 **CÁCH BẬT HỆ THỐNG (START)**
Mở Terminal tại thư mục `code/` và chạy lệnh:
```bash
cd code
docker compose up -d
```
*(Chỉ mất **3-5 giây** để toàn bộ 3 dịch vụ bật lên hoàn toàn mà không cần build lại).*

---

### 🔴 **CÁCH TẮT HỆ THỐNG (STOP)**
Khi làm việc xong hoặc muốn giải phóng bộ nhớ RAM cho máy tính, mở Terminal tại thư mục `code/` và chạy:
```bash
cd code
docker compose down
```
*(Tất cả container dịch vụ sẽ được dừng và dọn dẹp an toàn).*

---

## 🌐 3. ĐỊA CHỈ TRUY CẬP HỆ THỐNG

Sau khi bật hệ thống thành công, bạn mở trình duyệt web và truy cập theo các đường dẫn:

| Phân hệ | Đường dẫn (URL) | Mô tả |
| --- | --- | --- |
| **Frontend Web App** | [`http://localhost:5173`](http://localhost:5173) | Màn hình Chat Khách hàng, Bàn làm việc Nhân viên & Bảng Kanban |
| **Backend API Docs** | [`http://localhost:8000/docs`](http://localhost:8000/docs) | Giao diện Swagger UI kiểm thử tất cả các API của FastAPI |
| **API Health Check** | [`http://localhost:8000/health`](http://localhost:8000/health) | Kiểm tra trạng thái hoạt động của Backend (`{"status":"healthy"}`) |

---

## 🔍 4. CÁCH KIỂM TRA TRẠNG THÁI & XỬ LÝ SỰ CỐ (LOGS & TROUBLESHOOTING)

### **Xem danh sách các container đang chạy:**
```bash
docker compose ps
```

### **Xem nhật ký (Logs) của các dịch vụ khi gặp lỗi:**
* Xem log Backend FastAPI:
  ```bash
  docker compose logs -f backend
  ```
* Xem log Frontend React:
  ```bash
  docker compose logs -f frontend
  ```
* Xem log Redis:
  ```bash
  docker compose logs -f redis
  ```

### **Nếu bạn thay đổi mã nguồn Backend hoặc cài thêm thư viện mới:**
Chạy lại lệnh build lại container:
```bash
docker compose up --build -d
```

---

## 🛠️ 5. DÀNH CHO LẬP TRÌNH VIÊN CẦN CODE TRỰC TIẾP (LOCAL DEV MODE)

Nếu bạn muốn chỉnh sửa code trực tiếp trên máy và cần tính năng Hot-Reload (sửa code đâu tự đổi giao diện/API đó) mà không qua Docker Container:

1. **Bật duy nhất Redis Container bằng Docker:**
   ```bash
   cd code
   docker compose up -d redis
   ```
2. **Khởi chạy Backend trên máy Local:**
   ```bash
   cd code/backend
   # Trên Windows:
   venv\Scripts\activate
   # Khởi chạy server API dev:
   uvicorn app.main:app --reload --port 8000
   ```
3. **Khởi chạy Frontend trên máy Local (Mở Terminal khác):**
   ```bash
   cd code/frontend
   npm run dev
   ```
