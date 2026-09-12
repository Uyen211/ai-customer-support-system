# 💻 Mã Nguồn Hệ thống Trợ lý Trực ca CSKH AI (`code/`)

Thư mục `code/` chứa toàn bộ mã nguồn ứng dụng bao gồm **Backend**, **Frontend**, cấu hình **Docker Compose** và môi trường **.env**.

---

## 📁 Cấu trúc Thư mục Mã nguồn (`code/`)

Cấu trúc thư mục cha `code/` và các thành phần bên trong:

```text
code/
├── 📁 backend/                # FastAPI Application & Background Workers
│   ├── 📁 app/
│   │   ├── 📁 common/         # Models SQLAlchemy (9 bảng DB) & WebSocket Handlers
│   │   ├── 📁 core/           # Configs, DB Engine Supabase & Redis Connection
│   │   ├── 📁 modules/        # 4 Khối chức năng (RAG Customer, Ticket Auto-Triage, Human Live Agent, SLA Dispatcher)
│   │   ├── 📁 workers/        # SLA Monitoring & Ticket Dispatching Async Workers
│   │   └── 📄 main.py         # Entrypoint khởi tạo FastAPI Server
│   ├── 📄 .dockerignore       # Bỏ qua virtual environment và cache khi build image
│   ├── 📄 Dockerfile          # Dockerfile khởi chạy Uvicorn Backend Server
│   └── 📄 requirements.txt    # Danh sách thư viện Python
│
├── 📁 frontend/               # React + Vite Single Page Application
│   ├── 📁 src/
│   │   ├── 📄 App.jsx         # Giao diện giới thiệu & Trải nghiệm Trực quan 4 Khối Chức năng
│   │   ├── 📄 index.css       # Tailwind CSS v4 Setup & Wildcard Override Font Tiếng Việt
│   │   └── 📄 main.jsx        # Entrypoint React 18 Render
│   ├── 📄 Dockerfile          # Dockerfile khởi chạy Vite Frontend Server (Port 5173)
│   ├── 📄 vite.config.js      # Cấu hình Host '0.0.0.0' cho kết nối Docker
│   ├── 📄 tailwind.config.js  # Cấu hình Tailwind CSS
│   └── 📄 package.json        # Dependencies Node.js
│
├── 📄 .env                    # Biến môi trường (Supabase DATABASE_URL, REDIS_URL, OPENAI_API_KEY)
└── 📄 docker-compose.yml      # Cấu hình chạy 3 container (cs_backend, cs_frontend, cs_redis)
```

---

## 🚀 Hướng dẫn Chạy Ứng dụng

### 🔹 Cách 1: Khởi chạy bằng Docker Compose (Khuyên dùng)
```bash
# Di chuyển vào thư mục code
cd code

# Khởi tạo & Chạy ngầm 3 container
docker compose up --build -d

# Xem log các container
docker compose logs -f

# Dừng tất cả container
docker compose down
```

### 🔹 Cách 2: Khởi chạy Thủ công (Local Development)

#### 1. Backend:
```bash
cd code/backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. Frontend:
```bash
cd code/frontend
npm install
npm run dev
```

---

## 🔗 Liên kết Nhanh

- 🏠 [Về README Gốc của Dự án](../README.md)
- ⚙️ [Chi tiết Cài đặt & Khởi chạy](../docs/setup.md)
- 📐 [Phân tích Hệ thống & Cơ sở Dữ liệu](../docs/phantichhethong.md)
