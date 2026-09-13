# 🏢 Hệ thống Trợ lý Trực ca CSKH AI & Giám sát Vận hành Tự động

> Hệ thống Trực ca CSKH kết hợp Trí tuệ Nhân tạo (AI Agent) và Cảm xúc Con người (Human-in-the-Loop), hỗ trợ doanh nghiệp tự động hóa phân loại Ticket, tra cứu RAG với Supabase `pgvector`, quản lý SLA real-time và can thiệp trực ca live cho Nhân viên CSKH.

---

## 📁 Cấu trúc Thư mục Dự án (Project Directory Structure)

Cấu trúc tổng thể của thư mục dự án gốc (`project/`):

```text
project/
├── 📁 .claude/                    # Cấu hình AI Assistant (Skills, Agents & Guidelines)
│   ├── 📁 agents/                 # Agent profiles & chuyên gia hỗ trợ (VC UI/UX Designer...)
│   ├── 📁 skills/                 # Skill guides & bộ quy chuẩn lập trình / thiết kế
│   └── 📄 settings.json           # Cấu hình thiết lập AI Environment
│
├── 📁 code/                       # Mã nguồn ứng dụng (Full-stack Codebase)
│   ├── 📁 backend/                # Server FastAPI, AI Engine, Worker & Services
│   │   ├── 📁 app/                # Core logic, modules & workers
│   │   ├── 📄 Dockerfile          # Dockerfile build backend container
│   │   └── 📄 requirements.txt    # Thư viện Python (FastAPI, Supabase, Redis...)
│   ├── 📁 frontend/               # Single Page Application (React + Vite)
│   │   ├── 📁 src/                # Giao diện UI, Components & Styling
│   │   ├── 📄 Dockerfile          # Dockerfile build frontend container
│   │   ├── 📄 vite.config.js      # Cấu hình Vite Dev/Production Server
│   │   └── 📄 package.json        # Thư viện Node.js (React, Tailwind CSS v4...)
│   ├── 📄 .env                    # Biến môi trường hệ thống (Supabase DSN, Redis, API Keys)
│   ├── 📄 docker-compose.yml      # Cấu hình khởi chạy toàn bộ 3 dịch vụ qua 1 lệnh
│   └── 📄 README.md               # Hướng dẫn chi tiết thư mục code
│
├── 📁 docs/                       # Thư mục Tài liệu Dự án (Đã phân loại 3 phần)
│   ├── 📁 overview/               # Tài liệu Phân tích, Tổng quan & Setup
│   │   ├── 📄 gioithieuduan.md    # Tổng quan dự án, 4 khối chức năng & Use Cases
│   │   ├── 📄 phantichhethong.md  # Phân tích kỹ thuật chi tiết, ERD & Sequence Diagrams
│   │   ├── 📄 setup.md            # Hướng dẫn chi tiết Cài đặt, Khởi chạy & Tắt hệ thống
│   │   └── 📄 design_pattern.md   # Quy chuẩn Visual Language & Design Tokens
│   ├── 📁 database/               # Cấu trúc CSDL & DDL SQL
│   │   └── 📄 sql.md              # Câu lệnh DDL khởi tạo Schema PostgreSQL / Supabase
│   └── 📁 rag/                    # Bộ dữ liệu Chatbot RAG (Raw & Processed)
│       ├── 📁 raw/                # Dữ liệu thô (dataset-rag.md, prompt.md)
│       └── 📁 processed/          # Dữ liệu đã làm sạch & bóc tách (knowledge_chunks_prepared.json, insert_products.sql...)
│
└── 📄 README.md                   # Tài liệu tổng quan dự án (File hiện tại)
```

> [!IMPORTANT]
> **Quy tắc Kiến trúc Codebase (Architecture Rule)**:
> Toàn bộ phần mã nguồn (source code) chính để xây dựng, vận hành và khởi chạy hệ thống/phần mềm nằm **duy nhất trong thư mục [`code/`](file:///d:/Study/TLU/kiemthu/project/code/)** (bao gồm `code/backend/`, `code/frontend/`, `code/docker-compose.yml`, `code/.env`). Các thư mục khác (như `docs/`) chỉ dùng cho mục đích lưu trữ tài liệu phân tích, hướng dẫn, sơ đồ CSDL, dữ liệu thô và các artifact dữ liệu RAG tiền xử lý.

---

## 🛠️ Công nghệ Sử dụng (Tech Stack)

- **Backend**: FastAPI (Python 3.11), SQLAlchemy ORM, Uvicorn, WebSockets / SSE.
- **AI & Vector DB**: Supabase PostgreSQL + Extension `pgvector` (bảng `knowledge_chunks` với HNSW Index `vector_cosine_ops`), OpenAI / BGE Embeddings.
- **Event Driven & Cache**: Redis Queue & PubSub.
- **Frontend**: React 18, Vite, Tailwind CSS v4, Lucide Icons, Modern Vietnamese Typography (`Be Vietnam Pro` / `Plus Jakarta Sans`).
- **DevOps**: Docker, Docker Compose.

---

## 🚀 Khởi chạy Nhanh (Quick Start)

Yêu cầu: Đã cài đặt **Docker Desktop** và **Git**.

### 1. Khởi chạy 1 Lệnh qua Docker (Khuyên dùng)
```bash
cd code
docker compose up --build -d
```

- **Frontend (Giao diện UI)**: [http://localhost:5173](http://localhost:5173)
- **Backend (API Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redis Server**: `localhost:6379`

### 2. Dừng Hệ thống
```bash
cd code
docker compose down
```

---

## 📖 Tài liệu Tham khảo Chi tiết

- 📘 [Tài liệu Giới thiệu Dự án](file:///d:/Study/TLU/kiemthu/project/docs/overview/gioithieuduan.md)
- 📐 [Tài liệu Phân tích & Thiết kế Hệ thống](file:///d:/Study/TLU/kiemthu/project/docs/overview/phantichhethong.md)
- ⚙️ [Hướng dẫn Setup & Thao tác Vận hành](file:///d:/Study/TLU/kiemthu/project/docs/overview/setup.md)
- 🎨 [Quy chuẩn Thiết kế Giao diện UI/UX](file:///d:/Study/TLU/kiemthu/project/docs/overview/design_pattern.md)
- 🗄️ [Tài liệu Cơ sở Dữ liệu & SQL](file:///d:/Study/TLU/kiemthu/project/docs/database/sql.md)
- 🤖 [Tập Dữ liệu RAG & Tiền xử lý](file:///d:/Study/TLU/kiemthu/project/docs/rag/processed/README_prepared_data.md)
- 💻 [Hướng dẫn Mã nguồn Codebase](file:///d:/Study/TLU/kiemthu/project/code/README.md)
