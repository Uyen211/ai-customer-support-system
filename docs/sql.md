-- ====================================================================
-- PHẦN 1: KÍCH HOẠT EXTENSION & XÓA CŨ NẾU TỒN TẠI
-- ====================================================================
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

DROP TABLE IF EXISTS canned_responses CASCADE;
DROP TABLE IF EXISTS tickets CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS ai_rules CASCADE;
DROP TABLE IF EXISTS sla_policies CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ====================================================================
-- PHẦN 2: TẠO CẤU TRÚC 8 BẢNG QUAN HỆ
-- ====================================================================

-- 1. Bảng users (Nhân viên, Quản trị viên)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('ADMIN', 'MANAGER', 'AGENT')),
    status VARCHAR(20) NOT NULL DEFAULT 'OFFLINE' CHECK (status IN ('ONLINE', 'BUSY', 'OFFLINE')),
    skills JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Bảng customers (Khách hàng có tài khoản)
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Bảng conversations (Phiên hội thoại)
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
    assigned_agent_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    mode VARCHAR(20) NOT NULL DEFAULT 'BOT' CHECK (mode IN ('BOT', 'HUMAN', 'WAITING_HUMAN')),
    is_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    last_sentiment VARCHAR(20) NULL CHECK (last_sentiment IN ('POSITIVE', 'NEUTRAL', 'NEGATIVE', 'CRITICAL')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Bảng messages (Tin nhắn hội thoại & Trích dẫn RAG)
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_type VARCHAR(10) NOT NULL CHECK (sender_type IN ('CUSTOMER', 'BOT', 'AGENT')),
    sender_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    citations JSONB NULL,
    sentiment_score NUMERIC(4, 2) NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 5. Bảng sla_policies (Chính sách cam kết xử lý)
CREATE TABLE sla_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    priority VARCHAR(10) NOT NULL UNIQUE CHECK (priority IN ('P1', 'P2', 'P3')),
    resolution_time_minutes INT NOT NULL,
    escalation_notify_to VARCHAR(20) NOT NULL DEFAULT 'MANAGER',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 6. Bảng tickets (Yêu cầu khiếu nại & điều phối công việc)
CREATE TABLE tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    assigned_to UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(10) NOT NULL CHECK (priority IN ('P1', 'P2', 'P3')),
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')),
    summary TEXT NOT NULL,
    ai_metadata JSONB NULL,
    sla_deadline TIMESTAMPTZ NOT NULL,
    sla_breached BOOLEAN NOT NULL DEFAULT FALSE,
    resolved_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 7. Bảng canned_responses (Mẫu phản hồi nhanh)
CREATE TABLE canned_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shortcut VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(150) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_by UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. Bảng ai_rules (Cấu hình ngưỡng cảm xúc & luật mở ticket ngầm)
CREATE TABLE ai_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name VARCHAR(100) NOT NULL,
    sentiment_threshold NUMERIC(4, 2) NOT NULL,
    target_priority VARCHAR(10) NOT NULL CHECK (target_priority IN ('P1', 'P2', 'P3')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ====================================================================
-- PHẦN 3: TẠO CHỈ MỤC (INDEXES)
-- ====================================================================
CREATE INDEX idx_conversations_customer_id ON conversations(customer_id);
CREATE INDEX idx_conversations_flagged ON conversations(is_flagged) WHERE is_flagged = TRUE;
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_tickets_assigned_to ON tickets(assigned_to);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_sla_check ON tickets(sla_deadline, status) WHERE status IN ('PENDING', 'IN_PROGRESS');

-- ====================================================================
-- PHẦN 4: NẠP DỮ LIỆU MOCK (ĐÃ CHUẨN HÓA HEX UUID)
-- ====================================================================

-- 1. Nạp người dùng hệ thống (Mật khẩu text giả lập: '123456')
INSERT INTO users (id, email, password_hash, full_name, role, status, skills) VALUES
('a1111111-1111-1111-1111-111111111111', 'admin@brand.com', '$2b$12$K89K/5X0r6wXF9H8j8bZzeo11x9Xwz4GZ7L9R4/4k1nB2a8mK.Sme', 'Quản trị viên Hệ thống', 'ADMIN', 'ONLINE', '["ALL"]'::jsonb),
('a2222222-2222-2222-2222-222222222222', 'manager@brand.com', '$2b$12$K89K/5X0r6wXF9H8j8bZzeo11x9Xwz4GZ7L9R4/4k1nB2a8mK.Sme', 'Trưởng phòng CSKH', 'MANAGER', 'ONLINE', '["ALL"]'::jsonb),
('a3333333-3333-3333-3333-333333333333', 'agent.an@brand.com', '$2b$12$K89K/5X0r6wXF9H8j8bZzeo11x9Xwz4GZ7L9R4/4k1nB2a8mK.Sme', 'Nguyễn Văn An', 'AGENT', 'ONLINE', '["Đổi trả", "Giao hàng"]'::jsonb),
('a4444444-4444-4444-4444-444444444444', 'agent.binh@brand.com', '$2b$12$K89K/5X0r6wXF9H8j8bZzeo11x9Xwz4GZ7L9R4/4k1nB2a8mK.Sme', 'Trần Thị Bình', 'AGENT', 'BUSY', '["Bảo hành", "Kỹ thuật"]'::jsonb);

-- 2. Nạp khách hàng mẫu
INSERT INTO customers (id, email, password_hash, full_name, phone) VALUES
('c1111111-1111-1111-1111-111111111111', 'khachhang1@gmail.com', '$2b$12$K89K/5X0r6wXF9H8j8bZzeo11x9Xwz4GZ7L9R4/4k1nB2a8mK.Sme', 'Lê Hoàng Nam', '0901234567'),
('c2222222-2222-2222-2222-222222222222', 'khachhang2@gmail.com', '$2b$12$K89K/5X0r6wXF9H8j8bZzeo11x9Xwz4GZ7L9R4/4k1nB2a8mK.Sme', 'Phạm Minh Trang', '0912345678');

-- 3. Cấu hình chính sách SLA (P1: 15 phút, P2: 60 phút, P3: 240 phút)
INSERT INTO sla_policies (priority, resolution_time_minutes, escalation_notify_to) VALUES
('P1', 15, 'MANAGER'),
('P2', 60, 'MANAGER'),
('P3', 240, 'AGENT');

-- 4. Cấu hình quy tắc phát hiện cảm xúc AI
INSERT INTO ai_rules (rule_name, sentiment_threshold, target_priority, is_active) VALUES
('Khủng hoảng - Giận dữ cực độ', -0.75, 'P1', TRUE),
('Khiếu nại - Bất mãn vừa', -0.40, 'P2', TRUE),
('Thắc mắc có thái độ tiêu cực nhẹ', -0.15, 'P3', TRUE);

-- 5. Canned responses (Câu trả lời nhanh cho Agent)
INSERT INTO canned_responses (shortcut, title, content, category, created_by) VALUES
('/xinloi', 'Xin lỗi khách hàng', 'Dạ em chào anh/chị, em rất tiếc vì trải nghiệm không mong muốn vừa qua. Em đã tiếp nhận thông tin và sẽ hỗ trợ xử lý ngay lập tức cho mình ạ.', 'Chăm sóc', 'a2222222-2222-2222-2222-222222222222'),
('/doitra', 'Hướng dẫn đổi trả', 'Dạ anh/chị vui lòng đóng gói hàng nguyên vẹn và gửi về chi nhánh gần nhất theo mã vận đơn bên em cung cấp, bên em sẽ đổi mới trong 24h ạ.', 'Đổi trả', 'a2222222-2222-2222-2222-222222222222');

-- 6. Giả lập phiên trò chuyện (Dùng tiền tố 1000... thay vì d...)
INSERT INTO conversations (id, customer_id, assigned_agent_id, mode, is_flagged, last_sentiment) VALUES
('10000000-0000-0000-0000-000000000001', 'c1111111-1111-1111-1111-111111111111', NULL, 'BOT', FALSE, 'POSITIVE'),
('10000000-0000-0000-0000-000000000002', 'c2222222-2222-2222-2222-222222222222', 'a3333333-3333-3333-3333-333333333333', 'HUMAN', TRUE, 'CRITICAL');

-- 7. Giả lập tin nhắn
INSERT INTO messages (conversation_id, sender_type, sender_id, content, citations, sentiment_score) VALUES
('10000000-0000-0000-0000-000000000001', 'CUSTOMER', NULL, 'Shop cho mình hỏi chính sách đổi trả hàng áp dụng trong mấy ngày vậy?', NULL, 0.20),
('10000000-0000-0000-0000-000000000001', 'BOT', NULL, 'Dạ theo chính sách của shop, quý khách được hỗ trợ đổi sản phẩm miễn phí trong vòng 7 ngày kể từ khi nhận hàng đối với lỗi nhà sản xuất ạ.', '[{"doc_id": "chinh-sach-v1", "chunk_id": "c101", "snippet": "Khách hàng được quyền đổi hàng trong vòng 7 ngày tính từ ngày nhận hàng ghi trên vận đơn."}]'::jsonb, 0.85),
('10000000-0000-0000-0000-000000000002', 'CUSTOMER', NULL, 'Giao hàng trễ 5 ngày rồi mà gọi tổng đài không ai thèm nghe, làm ăn lừa đảo à???', NULL, -0.85),
('10000000-0000-0000-0000-000000000002', 'AGENT', 'a3333333-3333-3333-3333-333333333333', 'Dạ em chào chị Trang, em là An chuyên viên hỗ trợ. Em đã tiếp nhận đơn hàng của chị và đang liên hệ bên kho giục giao ngay trong chiều nay ạ.', NULL, 0.40);

-- 8. Giả lập Ticket (Dùng tiền tố b000... thay vì t...)
INSERT INTO tickets (id, conversation_id, assigned_to, category, priority, status, summary, ai_metadata, sla_deadline, sla_breached) VALUES
('b0000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000002', 'a3333333-3333-3333-3333-333333333333', 'Giao hàng', 'P1', 'IN_PROGRESS', 'Khách hàng bức xúc do giao trễ 5 ngày và không liên hệ được tổng đài hỗ trợ.', '{"sentiment_score": -0.85, "intent": "COMPLAINT", "urgency": "HIGH", "detected_reason": "Trễ đơn nghiêm trọng"}'::jsonb, NOW() + INTERVAL '15 minutes', FALSE);

CREATE EXTENSION IF NOT EXISTS vector;

-- Bảng lưu trữ các đoạn tài liệu RAG
CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Chỉ mục HNSW tối ưu tốc độ tìm kiếm tương đồng Cosine (Cosine Similarity)
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_embedding 
ON knowledge_chunks 
USING hnsw (embedding vector_cosine_ops);

-- 1. Tạo bảng lưu trữ thông tin sản phẩm thú cưng
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(50) UNIQUE NOT NULL,                        -- Mã sản phẩm (VD: CAT-FOOD-ROYAL-2KG)
    name VARCHAR(255) NOT NULL,                             -- Tên sản phẩm
    category VARCHAR(100) NOT NULL,                         -- Thức ăn, Cát vệ sinh, Đồ chơi, Phụ kiện, Thuốc thú y...
    pet_type VARCHAR(50) NOT NULL,                          -- 'DOG', 'CAT', 'BIRD', 'ALL'...
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),       -- Giá bán lẻ hiện tại
    sale_price NUMERIC(12, 2) NULL CHECK (sale_price >= 0), -- Giá khuyến mãi (nếu có)
    stock_quantity INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0), -- Tồn kho thực tế
    status VARCHAR(20) NOT NULL DEFAULT 'IN_STOCK' 
        CHECK (status IN ('IN_STOCK', 'OUT_OF_STOCK', 'DISCONTINUED')),
    
    -- Thuộc tính linh hoạt cho đồ thú cưng: trọng lượng túi, kích cỡ chuồng/vòng cổ, mùi hương cát...
    attributes JSONB NULL,                                  -- VD: {"weight": "2kg", "flavor": "Cá hồi", "size": "M"}
    
    description TEXT NULL,                                  -- Mô tả ngắn hiển thị kèm
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Đánh Index phục vụ bộ lọc nghiệp vụ thông thường
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_pet_type ON products(pet_type);
CREATE INDEX IF NOT EXISTS idx_products_status_stock ON products(status, stock_quantity);
-- GIN Index để query linh hoạt trong thuộc tính JSONB (VD: tìm vị, tìm size)
CREATE INDEX IF NOT EXISTS idx_products_attributes ON products USING gin (attributes);
-- Đánh Index GIN cho metadata để tăng tốc filter các chunk thuộc loại 'PRODUCT'
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_metadata ON knowledge_chunks USING gin (metadata);
