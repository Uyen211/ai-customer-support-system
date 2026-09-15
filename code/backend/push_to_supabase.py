"""
Script nạp Dữ liệu Sản phẩm (11 items) + RAG Vector Chunks (62 items) vào Supabase DB.
Đặt tại: code/backend/push_to_supabase.py
"""

import os
import sys
import json
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

# Nạp file .env từ code/.env
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(BACKEND_DIR))
ENV_PATH = os.path.join(PROJECT_ROOT, "code", ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
elif os.path.exists(os.path.join(BACKEND_DIR, ".env")):
    load_dotenv(os.path.join(BACKEND_DIR, ".env"))
else:
    load_dotenv()

# Lấy connection string
DB_URL = os.getenv("DIRECT_URL") or os.getenv("DATABASE_URL")
if not DB_URL:
    print("❌ Không tìm thấy DATABASE_URL hoặc DIRECT_URL trong file .env!")
    sys.exit(1)

# Chuyển đổi định dạng SQLAlchemy URL nếu cần (postgresql+psycopg2:// -> postgresql://)
if DB_URL.startswith("postgresql+psycopg2://"):
    DB_URL = DB_URL.replace("postgresql+psycopg2://", "postgresql://")

# Đường dẫn file dữ liệu
PRODUCTS_FILE = os.path.join(PROJECT_ROOT, "docs", "rag", "processed", "products_relational.json")
PREPARED_CHUNKS_FILE = os.path.join(PROJECT_ROOT, "docs", "rag", "processed", "knowledge_chunks_prepared.json")
EMBEDDED_CHUNKS_FILE = os.path.join(PROJECT_ROOT, "docs", "rag", "processed", "embedded_chunks.json")

def push_data():
    print("=" * 80)
    print("🚀 NẠP DỮ LIỆU SẢN PHẨM & RAG VECTOR CHUNKS VÀO SUPABASE DB")
    print("=" * 80)

    # 1. Đọc dữ liệu file JSON
    if not os.path.exists(PRODUCTS_FILE):
        print(f"❌ Không tìm thấy file sản phẩm tại: {PRODUCTS_FILE}")
        return

    with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)

    if os.path.exists(EMBEDDED_CHUNKS_FILE):
        with open(EMBEDDED_CHUNKS_FILE, "r", encoding="utf-8") as f:
            embedded_chunks = json.load(f)
    elif os.path.exists(PREPARED_CHUNKS_FILE):
        print("ℹ️ File embedded_chunks.json đã được dọn dẹp. Tiến hành nhúng vector tự động từ knowledge_chunks_prepared.json...")
        sys.path.append(os.path.join(BACKEND_DIR, "app", "modules", "rag_assistant"))
        from embedder import VietnameseEmbedder
        
        with open(PREPARED_CHUNKS_FILE, "r", encoding="utf-8") as f:
            chunks = json.load(f)
            
        embedder = VietnameseEmbedder("dangvantuan/vietnamese-embedding")
        embedded_chunks = embedder.embed_chunks(chunks)
    else:
        print(f"❌ Không tìm thấy file RAG chunks tại: {PREPARED_CHUNKS_FILE}")
        return

    print(f"📦 Đã chuẩn bị thành công: {len(products)} sản phẩm & {len(embedded_chunks)} RAG vector chunks.")

    # 2. Kết nối tới Supabase PostgreSQL
    print(f"🔌 Đang kết nối tới Supabase Database...")
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    print("✅ Kết nối Supabase thành công!")

    # 3. Nạp 11 sản phẩm vào bảng `products`
    print("\n📥 [1/2] Đang nạp 11 sản phẩm vào bảng 'products'...")
    prod_tuples = []
    for p in products:
        prod_tuples.append((
            p.get("sku"),
            p.get("name"),
            p.get("category"),
            p.get("pet_type"),
            p.get("price"),
            p.get("sale_price"),
            p.get("stock_quantity", 0),
            p.get("status", "IN_STOCK"),
            json.dumps(p.get("attributes", {}), ensure_ascii=False),
            p.get("description")
        ))

    insert_prod_query = """
    INSERT INTO products (sku, name, category, pet_type, price, sale_price, stock_quantity, status, attributes, description)
    VALUES %s
    ON CONFLICT (sku) DO UPDATE SET
        name = EXCLUDED.name,
        category = EXCLUDED.category,
        pet_type = EXCLUDED.pet_type,
        price = EXCLUDED.price,
        sale_price = EXCLUDED.sale_price,
        stock_quantity = EXCLUDED.stock_quantity,
        status = EXCLUDED.status,
        attributes = EXCLUDED.attributes,
        description = EXCLUDED.description,
        updated_at = NOW();
    """
    execute_values(cursor, insert_prod_query, prod_tuples)
    print(f"✅ Đã nạp/cập nhật thành công {len(products)} sản phẩm vào bảng 'products'!")

    # 4. Nạp 62 Vector Chunks vào bảng `knowledge_chunks`
    print("\n📥 [2/2] Đang nạp 62 RAG Vector Chunks (768 dims) vào bảng 'knowledge_chunks'...")
    
    # Xóa chunks cũ nếu nạp lại để tránh lặp bản ghi
    cursor.execute("TRUNCATE TABLE knowledge_chunks;")

    chunk_tuples = []
    for c in embedded_chunks:
        emb_str = "[" + ",".join(map(str, c["embedding"])) + "]"
        chunk_tuples.append((
            c.get("document_name"),
            c.get("content"),
            emb_str,
            json.dumps(c.get("metadata", {}), ensure_ascii=False)
        ))

    insert_chunk_query = """
    INSERT INTO knowledge_chunks (document_name, content, embedding, metadata)
    VALUES %s;
    """
    execute_values(cursor, insert_chunk_query, chunk_tuples)
    print(f"✅ Đã nạp thành công {len(embedded_chunks)} vector chunks vào bảng 'knowledge_chunks'!")

    # 5. Đối soát số lượng và chạy thử Vector Search trên Supabase DB
    print("\n" + "=" * 80)
    print("📊 ĐỐI SOÁT DỮ LIỆU & THỬ TRUY VẤN VECTOR SEARCH TRÊN SUPABASE")
    print("=" * 80)

    cursor.execute("SELECT COUNT(*) FROM products;")
    prod_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM knowledge_chunks;")
    chunk_count = cursor.fetchone()[0]

    print(f"-> Tổng số dòng trong bảng 'products':        {prod_count} (Kỳ vọng: 11)")
    print(f"-> Tổng số dòng trong bảng 'knowledge_chunks': {chunk_count} (Kỳ vọng: 62)")

    # Thử 1 câu vector search mẫu
    sample_chunk = embedded_chunks[0]
    sample_emb_str = "[" + ",".join(map(str, sample_chunk["embedding"])) + "]"

    cursor.execute("""
    SELECT document_name, metadata->>'title' AS title, 1 - (embedding <=> %s::vector) AS similarity
    FROM knowledge_chunks
    ORDER BY embedding <=> %s::vector ASC
    LIMIT 3;
    """, (sample_emb_str, sample_emb_str))

    results = cursor.fetchall()
    print("\n🔍 Thử nghiệm Vector Search (Cosine Similarity) Top 3 trên Supabase:")
    for rank, r in enumerate(results, 1):
        print(f"   Top {rank} | Similarity: {r[2]:.4f} | Document: {r[0]} | Title: {r[1]}")

    cursor.close()
    conn.close()

    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH PUSH DỮ LIỆU LÊN SUPABASE THÀNH CÔNG (100%)!")
    print("=" * 80)

if __name__ == "__main__":
    push_data()
