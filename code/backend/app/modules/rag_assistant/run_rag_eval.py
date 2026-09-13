"""
Script tạo Embedding cho 62 Child Chunks và Đánh giá 7 Test Cases RAG.
- Mô hình: dangvantuan/vietnamese-embedding (768 dimensions)
- File đầu vào: docs/rag/processed/knowledge_chunks_prepared.json
- File vector lưu ngoài: docs/rag/processed/embedded_chunks.json
- File test cases: docs/rag/raw/test.md
"""

import os
import json
import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from embedder import VietnameseEmbedder

# Xác định đường dẫn thư mục gốc project chứa thư mục 'docs'
current_dir = os.path.abspath(__file__)
BASE_DIR = None
while current_dir != os.path.dirname(current_dir):
    if os.path.exists(os.path.join(current_dir, "docs")):
        BASE_DIR = current_dir
        break
    current_dir = os.path.dirname(current_dir)

if not BASE_DIR:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

CHUNKS_FILE = os.path.join(BASE_DIR, "docs", "rag", "processed", "knowledge_chunks_prepared.json")
EMBEDDED_OUTPUT_FILE = os.path.join(BASE_DIR, "docs", "rag", "processed", "embedded_chunks.json")
EVAL_RESULT_FILE = os.path.join(BASE_DIR, "docs", "rag", "processed", "test_evaluation_results.md")

TEST_CASES = [
    {
        "id": 1,
        "group": "Chính sách Đổi trả (PET-CS-002)",
        "query": "Hàng mua về bị vỡ hỏng trong lúc vận chuyển thì phải làm thế nào?",
        "expected_keywords": ["3.3", "vận chuyển", "hư hỏng", "video"],
        "expected_code": "PET-CS-002"
    },
    {
        "id": 2,
        "group": "Chính sách Đổi trả (PET-CS-002)",
        "query": "Tôi không thích mùi của gói pate này nữa, shop có cho đổi trả không?",
        "expected_keywords": ["4", "không được đổi trả", "lý do", "thẩm mỹ", "3.5"],
        "expected_code": "PET-CS-002"
    },
    {
        "id": 3,
        "group": "Chính sách Vận chuyển & Phí ship (PET-CS-003)",
        "query": "Tôi ở Biên Hòa thì đặt hàng mấy ngày nhận được và phí ship ra sao?",
        "expected_keywords": ["2", "5.1", "Biên Hòa", "Nhóm B"],
        "expected_code": "PET-CS-003"
    },
    {
        "id": 4,
        "group": "Chính sách Vận chuyển & Phí ship (PET-CS-003)",
        "query": "Đơn hàng ở TP.HCM bao nhiêu tiền thì được miễn phí ship?",
        "expected_keywords": ["5.2", "Freeship", "300.000", "TP. Hồ Chí Minh"],
        "expected_code": "PET-CS-003"
    },
    {
        "id": 5,
        "group": "Tri thức Sản phẩm (Product Chunks)",
        "query": "Mèo nhà tôi nuôi chung cư hay bị nôn ra búi lông thì ăn loại hạt nào?",
        "expected_sku": "CAT-ROYAL-INDOOR-2KG",
        "expected_keywords": ["Royal Canin Indoor", "búi lông"]
    },
    {
        "id": 6,
        "group": "Tri thức Sản phẩm (Product Chunks)",
        "query": "Chó nhà hay cắn phá giày dép đồ đạc thì mua đồ chơi gì chịu lực tốt?",
        "expected_sku": "DOG-KONG-CLASSIC-M",
        "expected_keywords": ["Kong Classic", "cắn phá"]
    },
    {
        "id": 7,
        "group": "Cảnh báo & Kênh liên hệ (PET-CS-004)",
        "query": "Shop có website chính thức nào không hay chuyển khoản vào số tài khoản nào?",
        "expected_keywords": ["4", "CẢNH BÁO", "chưa có website", "0123456789"],
        "expected_code": "PET-CS-004"
    }
]

def run_evaluation():
    print("=" * 80)
    print("🚀 BẮT ĐẦU CHƯƠNG TRÌNH EMBEDDING & ĐÁNH GIÁ THỬ NGHIỆM RAG")
    print("=" * 80)

    # 1. Đọc dữ liệu 62 chunks
    if not os.path.exists(CHUNKS_FILE):
        print(f"❌ Không tìm thấy file dữ liệu: {CHUNKS_FILE}")
        return

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"📦 Đã nạp thành công {len(chunks)} Child Chunks từ file prepared.")

    # 2. Khởi tạo Mô hình Embedder & Tạo vector
    embedder = VietnameseEmbedder("dangvantuan/vietnamese-embedding")
    embedded_chunks = embedder.embed_chunks(chunks)

    # 3. Ghi file vector ra đĩa (không ghi DB)
    with open(EMBEDDED_OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(embedded_chunks, f, ensure_ascii=False, indent=2)

    print(f"💾 Đã lưu file Embedded Chunks ra: {EMBEDDED_OUTPUT_FILE}")
    print(f"   Kích thước vector mẫu: {len(embedded_chunks[0]['embedding'])} dimensions.")

    # 4. Đánh giá 7 Test Cases
    doc_vectors = np.array([c["embedding"] for c in embedded_chunks])

    eval_summary = []
    print("\n" + "=" * 80)
    print("📊 ĐÁNH GIÁ CHẤT LƯỢNG TRUY VẤN (RETRIEVAL EVALUATION - COSINE SIMILARITY)")
    print("=" * 80)

    top1_pass_count = 0
    top3_pass_count = 0

    for tc in TEST_CASES:
        q_text = tc["query"]
        q_vec = embedder.embed_text(q_text)
        
        # Tính Cosine Similarity
        sims = cosine_similarity([q_vec], doc_vectors)[0]
        
        # Lấy Top 3 chỉ số cao nhất
        top_indices = np.argsort(sims)[::-1][:3]
        
        top_results = []
        for rank, idx in enumerate(top_indices, 1):
            chunk = embedded_chunks[idx]
            score = float(sims[idx])
            top_results.append({
                "rank": rank,
                "score": score,
                "document_name": chunk.get("document_name"),
                "content": chunk.get("content"),
                "metadata": chunk.get("metadata")
            })

        top1 = top_results[0]
        
        # Kiểm tra điều kiện khớp
        is_top1_pass = False
        is_top3_pass = False

        expected_code = tc.get("expected_code")
        expected_sku = tc.get("expected_sku")

        for res in top_results:
            meta = res["metadata"]
            if expected_code and meta.get("policy_code") == expected_code:
                # Kiểm tra section hoặc title
                if any(kw.lower() in res["content"].lower() for kw in tc.get("expected_keywords", [])):
                    if res["rank"] == 1:
                        is_top1_pass = True
                    is_top3_pass = True
            elif expected_sku and meta.get("sku") == expected_sku:
                if res["rank"] == 1:
                    is_top1_pass = True
                is_top3_pass = True

        if is_top1_pass:
            top1_pass_count += 1
        if is_top3_pass:
            top3_pass_count += 1

        eval_summary.append({
            "test_case": tc,
            "top1_pass": is_top1_pass,
            "top3_pass": is_top3_pass,
            "top_results": top_results
        })

        # In log trực quan
        status_str = "✅ TOP 1 MATCH" if is_top1_pass else ("⚠️ TOP 3 MATCH" if is_top3_pass else "❌ MISMATCH")
        print(f"\n[Test #{tc['id']}] {tc['group']}")
        print(f"❓ Câu hỏi: \"{q_text}\"")
        print(f"🎯 Kết quả: {status_str}")
        print(f"   Top 1 (Score: {top1['score']:.4f}): {top1['content'][:120]}...")

    print("\n" + "=" * 80)
    print("📈 TỔNG KẾT ĐÁNH GIÁ")
    print(f"-> Đạt Top 1 Accuracy: {top1_pass_count}/{len(TEST_CASES)} ({top1_pass_count/len(TEST_CASES)*100:.1f}%)")
    print(f"-> Đạt Top 3 Recall:   {top3_pass_count}/{len(TEST_CASES)} ({top3_pass_count/len(TEST_CASES)*100:.1f}%)")
    print("=" * 80)

    # 5. Xuất Báo cáo Markdown
    with open(EVAL_RESULT_FILE, "w", encoding="utf-8") as f:
        f.write("# Báo Cáo Đánh Giá Chất Lượng Truy Vấn Vector RAG\n\n")
        f.write(f"- **Mô hình Embedding**: `dangvantuan/vietnamese-embedding` (768 dims)\n")
        f.write(f"- **Tổng số Chunks**: {len(chunks)}\n")
        f.write(f"- **Top-1 Accuracy**: {top1_pass_count}/{len(TEST_CASES)} ({top1_pass_count/len(TEST_CASES)*100:.1f}%)\n")
        f.write(f"- **Top-3 Recall**: {top3_pass_count}/{len(TEST_CASES)} ({top3_pass_count/len(TEST_CASES)*100:.1f}%)\n\n")
        f.write("---\n\n## Chi Tiết Kết Quả 7 Test Cases\n\n")

        for item in eval_summary:
            tc = item["test_case"]
            status = "✅ PASS (Top 1)" if item["top1_pass"] else ("⚠️ PASS (Top 3)" if item["top3_pass"] else "❌ FAIL")
            f.write(f"### Test #{tc['id']}: {tc['group']} - {status}\n")
            f.write(f"- **Câu hỏi**: *\"{tc['query']}\"*\n")
            f.write(f"- **Kỳ vọng**: {tc.get('expected_code', '')} {tc.get('expected_sku', '')} {tc.get('expected_keywords', [])}\n\n")
            f.write("| Rank | Score | Content Snippet |\n|---|---|---|\n")
            for r in item["top_results"]:
                content_sub = r["content"].replace("\n", " ")[:150] + "..."
                f.write(f"| Top {r['rank']} | {r['score']:.4f} | {content_sub} |\n")
            f.write("\n---\n\n")

    print(f"📝 Đã xuất báo cáo chi tiết ra: {EVAL_RESULT_FILE}")

if __name__ == "__main__":
    run_evaluation()
