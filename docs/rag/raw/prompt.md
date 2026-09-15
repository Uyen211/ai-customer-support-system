Trong docs\dataset-rag.md hãy chia thành 2 luồng dữ liệu:
Nhánh 1 (Dữ liệu quan hệ - SQL): Khối JSON PRODUCT (10 sản phẩm) phải bóc tách ra để nạp trực tiếp vào bảng products bằng câu lệnh INSERT thông thường, không cần tạo vector embedding cho toàn bộ JSON này. Và cái metadata của cái product cũng tách ra.
Nhánh 2 (Dữ liệu phi cấu trúc - Vector): Toàn bộ nội dung Chính sách (1, 2, 3) và khối EMBEDDING_CONTENT của sản phẩm cần tiền xử lý văn bản để đưa vào bảng knowledge_chunks.  

Dữ liệu đưa vào embedding tiếp theo cần Làm sạch nhiễu định dạng:
1. Khử ký hiệu LaTeX: File thô chứa các mũi tên toán học như $\rightarrow$. 
Cần replace thành dấu -> hoặc từ "dẫn đến", "sẽ" để bộ tokenizer tiếng Việt xử lý tự nhiên nhất.  
2. Chuẩn hóa khoảng trắng & ngắt dòng: Loại bỏ các chuỗi ngắt dòng dư thừa (\n\n\n), giữ lại cấu trúc đoạn văn rõ ràng.

ví dụ metadata cho chính sách:
{
  "document_name": "Chinh_sach_doi_tra_PET-CS-002.md",
  "metadata": {
    "doc_type": "POLICY",
    "policy_code": "PET-CS-002",
    "section": "3.3",
    "title": "Hàng hư hỏng do vận chuyển",
    "parent_content": "..."
  }
}


---

**2. Chiến lược phân tách Cặp Parent - Child (Chunking Strategy)**

**A. Đối với Tri thức Sản phẩm (`EMBEDDING_CONTENT` - 10 sản phẩm)**

* **Parent Chunk (1 chunk/sản phẩm):**
* *Nội dung:* Giữ nguyên toàn bộ đoạn `EMBEDDING_CONTENT` gốc (~200 – 240 từ) bao gồm thông số kỹ thuật, cách dùng, lưu ý và kênh mua Zalo OA/Fanpage.


* *Mục đích:* Làm ngữ cảnh hoàn chỉnh đưa vào prompt cho LLM, không qua mô hình embedding.




* **Child Chunks (Tạo 2 child chunks ngắn từ mỗi Parent):**
* *Child 1 (Đặc tính cốt lõi):* Trích xuất thông tin đối tượng thú cưng, độ tuổi, thành phần và công dụng chính (độ dài: ~60 – 80 từ).


* *Child 2 (Vấn đề & Câu hỏi tìm kiếm):* Trích xuất phần giải quyết vấn đề (búi lông, rụng lông, phân hôi, cắn phá) và các câu hỏi mẫu người dùng hay hỏi (độ dài: ~60 – 90 từ).


* *Xử lý:* Cả 2 child chunks đều được đưa qua `dangvantuan/vietnamese-embedding` để sinh vector 768 chiều.



**B. Đối với Tài liệu Chính sách (Chính sách 1, 2, 3)**

* **Parent Chunk (Theo từng nhóm điều khoản lớn):**
* Gom toàn bộ nội dung của một phần lớn (Ví dụ: toàn bộ Mục 3 "Các trường hợp được đổi trả" gồm từ 3.1 đến 3.5, hoặc toàn bộ Mục 5 "Phí vận chuyển và điều kiện freeship").




* **Child Chunks (Theo từng quy định chi tiết hoặc từng dòng bảng):**
* Tách từng tiểu mục độc lập: Mục 3.1 (Lỗi NSX), Mục 3.3 (Hàng vỡ do ship), Mục 3.5 (Khách đổi ý).


* Với các bảng cước phí: Chuyển từng hàng dữ liệu thành 1 câu tự nhiên ngắn gọn để làm 1 child chunk.


* Gắn thêm tiền tố ngữ cảnh (Context Header) vào đầu mỗi child: `[Chính sách Đổi trả - Mục 3.3 Hàng hư hỏng do vận chuyển]: Khách cần quay video...`.


(parrent chunk sẽ được lưu trong metadata cùng vs các thông tin khác.)
