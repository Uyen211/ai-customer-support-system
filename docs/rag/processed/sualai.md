Dưới đây là kết quả rà soát chi tiết cho file `knowledge_chunks_prepared_2.json` dựa trên yêu cầu kiểm tra độ dài token và các lỗi dữ liệu còn tồn đọng.

---

### 1. Kiểm tra độ dài Token so với ngữ cảnh mô hình (Trần 256 tokens)

Mô hình `dangvantuan/vietnamese-embedding` sử dụng tokenizer gốc RoBERTa/PhoBERT (tỷ lệ trung bình: **1 từ tiếng Việt $\approx$ 1.2 – 1.4 tokens**). Ngưỡng an toàn tối đa cho văn bản là **$\le$ 180 từ** (tương đương ~220–240 tokens, chừa biên cho token đặc biệt).

* **Đa số các chunk chính sách:** Rất an toàn, chỉ dài từ 30 đến 90 từ (khoảng 40 – 120 tokens).


* **3 CHUNK BỊ VƯỢT TRẦN HOẶC CHẠM NGƯỠNG NGUY HIỂM:**

| Chunk bị dài | Số từ thực tế | Ước tính Tokens | Đánh giá rủi ro |
| --- | --- | --- | --- |
| **Mục 1 - PET-CS-004** (Quy trình 5 bước mua hàng online)

 | **172 từ** | **~245 – 260 tokens** | **RẤT NGUY HIỂM / VƯỢT TRẦN:** Bị cắt cụt ở Bước 5 (Thanh toán & Vận đơn).

 |
| **Mục 5.1 - PET-CS-003** (Bảng phí ship toàn bộ)

 | **148 từ** | **~210 – 225 tokens** | **CHẠM NGƯỠNG BÁO ĐỘNG:** Đầy số và ký tự ghép, dễ bị tokenizer chẻ nhỏ vượt 256 tokens.

 |
| **Child 2 - Royal Canin Indoor 2KG** (`PROBLEM_SOLVING_FAQS`)

 | **198 từ** | **~270 – 290 tokens** | **CHẮC CHẮN TRÀN TRẦN (>256):** Bị mất toàn bộ danh sách câu hỏi tìm kiếm ở cuối.

 |

**Cách khắc phục:**

1. **Với Child 2 - Royal Canin Indoor 2KG (`PROBLEM_SOLVING_FAQS`):** Đoạn này bạn đang lặp lại gần như nguyên xi cả liều lượng ăn và bảo quản. Hãy tinh gọn lại đúng trọng tâm vấn đề và câu hỏi tìm kiếm:


> `"[Sản phẩm Thức ăn hạt Royal Canin Indoor cho mèo trưởng thành 2kg (CAT-ROYAL-INDOOR-2KG) - Giải quyết vấn đề & Tình huống tìm kiếm]: Giải quyết tình trạng tiêu hóa chậm, phân hôi, béo phì và nôn búi lông ở mèo nuôi nhà. Bổ sung chất xơ psyllium đào thải búi lông qua phân và omega 3-6 giảm rụng lông. Đặt mua qua Zalo OA hoặc Fanpage PetHome. Thường tìm kiếm: thức ăn cho mèo nuôi chung cư, mèo bị búi lông nên ăn gì, mèo ít vận động bị mập, hạt giúp mèo giảm hôi phân, Royal Canin Indoor có tốt không."`
> 
> *(Giảm từ 198 từ xuống còn 82 từ $\rightarrow$ cực kỳ an toàn, chỉ ~110 tokens)*.
> 
> 


2. **Với Mục 1 - PET-CS-004 (Quy trình mua hàng):** Cắt bỏ các câu dẫn rườm rà ở đầu, chỉ giữ cốt lõi 5 bước:
> `"[Hướng dẫn Mua hàng và Thanh toán (PET-CS-004) - Mục 1 Quy trình mua hàng online]: Quy trình 5 bước đặt hàng qua Zalo OA PetHome Việt Nam (zalo.me/pethome.official - Zalo 0988.123.456) hoặc Fanpage PetHome: Bước 1: Nhắn tin liên hệ. Bước 2: Nhân viên tư vấn kích cỡ, loại thức ăn. Bước 3: Cung cấp tên, số điện thoại, địa chỉ nhận hàng. Bước 4: Nhận bản tóm tắt đơn (mã PHxxxx, tiền hàng, phí ship, voucher) và nhắn Xác nhận hoặc OK. Bước 5: Chọn thanh toán COD hoặc quét QR chuyển khoản, nhận mã vận đơn theo dõi."`
> 
> *(Giảm từ 172 từ xuống còn 94 từ $\rightarrow$ ~130 tokens)*.
> 
> 



---

### 2. Các lỗi dữ liệu & Logic nghiệp vụ còn sót lại

* **VẪN THIẾU CHUNK "CẢNH BÁO GIẢ MẠO & SỐ TÀI KHOẢN" (Mục 4 - PET-CS-004):** File `knowledge_chunks_prepared_2.json` vẫn chưa có chunk Mục 4 này. Cần bổ sung ngay chunk thông tin PetHome **chưa có website, không có hotline 1900**, chỉ dùng STK Vietcombank `0123456789`.


* **Lỗi câu cụt ở 4 sản phẩm (`PROBLEM_SOLVING_FAQS`):**
* **Trụ cào Trixie (`CAT-TRIXIE-SCRATCHER-L`):** Chunk 2 bắt đầu bằng: *"Trụ được bọc bằng dây thừng sisal... Nhắn tin chốt đơn... Người dùng tìm kiếm..."* $\rightarrow$ Bị cụt mất vế chỉ rõ *"Trụ cào giúp chống cào sofa, rèm cửa"*.


* **Pate Whiskas (`CAT-WHISKAS-PATE-12GX12`):** Chunk 2 chỉ vỏn vẹn: *"Pate mềm mịn... Chốt đơn giao hàng nhanh qua Zalo... Người dùng tìm kiếm..."* $\rightarrow$ Thiếu thông tin quan trọng nhất là *"dành cho mèo lười uống nước, kén ăn, hỗ trợ sỏi thận/tiết niệu"*.


* **Thức ăn Vẹt (`BIRD-VERSELE-LAGA-PARROT-1KG`):** Chunk 2 chỉ lặp lại thành phần hạt, thiếu thông tin loài vẹt phù hợp (*Cockatiel, Lovebird, Sun Conure*).


* **Máy cho ăn PetKit (`DOG-PETKIT-FEEDER-6L`):** Chunk 2 chỉ có: *"Bình chứa 6L... Cài đặt qua App... Người dùng tìm kiếm..."* $\rightarrow$ Bị thiếu ngữ cảnh tìm kiếm chính: *"phù hợp cho chủ bận đi làm cả ngày hoặc đi công tác xa"*.




* **Dấu chấm câu bị biến mất ở tên thành phố:**
* Tại Mục 4 và Mục 5.1 của `Chinh_sach_van_chuyen_PET-CS-003.md`: Regex làm sạch biến dấu ba chấm `...` thành dấu chấm lẻ đặt sát chữ:
* Hiện tại: `Cần Thơ.)`, `Cần Giờ.)`, `Đà Nẵng.)`.


* Nên sửa lại: `Cần Thơ...)`, `Cần Giờ...)`, `Đà Nẵng...)` hoặc bỏ hẳn dấu chấm lơ lửng này để thành `Cần Thơ, Hải Phòng...`.







---

Chỉ cần rút gọn 2 chunk bị dài (Royal Canin Indoor và Quy trình mua hàng), bổ sung thêm chunk Mục 4 Cảnh báo giả mạo, và viết thêm 1 câu công dụng vào 4 chunk sản phẩm trên là toàn bộ dataset đạt chuẩn an toàn 100% cho mô hình `dangvantuan/vietnamese-embedding`.