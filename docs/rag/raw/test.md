
### 1. Test nhóm Chính sách Đổi trả (`PET-CS-002`)

* **Câu hỏi 1 (Tìm kiếm ngữ nghĩa - Thay thế từ ngữ):** *"Hàng mua về bị vỡ hỏng trong lúc vận chuyển thì phải làm thế nào?"*
* **Kỳ vọng:** Phải trả về đoạn chunk **Mục 3.3 (Hàng hư hỏng do vận chuyển)** với yêu cầu quay video mở hộp và thông báo trong 48 giờ.




* **Câu hỏi 2 (Tìm kiếm ngữ nghĩa - Suy luận ngược):** *"Tôi không thích mùi của gói pate này nữa, shop có cho đổi trả không?"*
* **Kỳ vọng:** Phải trả về đoạn chunk **Mục 4 (Các trường hợp không được đổi trả)** - *Đổi trả vì lý do thẩm mỹ chủ quan đối với thức ăn, pate* hoặc **Mục 3.5 (Khách đổi ý)**.





### 2. Test nhóm Chính sách Vận chuyển & Phí ship (`PET-CS-003`)

* **Câu hỏi 3 (Tìm kiếm theo dữ liệu bảng/số liệu):** *"Tôi ở Biên Hòa thì đặt hàng mấy ngày nhận được và phí ship ra sao?"*
* **Kỳ vọng:** Phải trả về đoạn chunk **Mục 2 (Khu vực giao hàng - Nhóm B Biên Hòa)** và **Mục 5.1 (Bảng phí ship)**.




* **Câu hỏi 4 (Tìm kiếm điều kiện):** *"Đơn hàng ở TP.HCM bao nhiêu tiền thì được miễn phí ship?"*
* **Kỳ vọng:** Phải trả về chunk **Mục 5.2 (Chính sách Freeship TP.HCM từ 300.000đ)**.





### 3. Test nhóm Tri thức Sản phẩm (Product Chunks)

* **Câu hỏi 5 (Tìm kiếm theo triệu chứng/vấn đề của thú cưng):** *"Mèo nhà tôi nuôi chung cư hay bị nôn ra búi lông thì ăn loại hạt nào?"*
* **Kỳ vọng:** Phải trả về chunk sản phẩm **Thức ăn hạt Royal Canin Indoor 2kg** (`CAT-ROYAL-INDOOR-2KG`).




* **Câu hỏi 6 (Tìm kiếm theo hành vi phá hoại):** *"Chó nhà hay cắn phá giày dép đồ đạc thì mua đồ chơi gì chịu lực tốt?"*
* **Kỳ vọng:** Phải trả về chunk sản phẩm **Đồ chơi Kong Classic size M** (`DOG-KONG-CLASSIC-M`).





### 4. Test nhóm Cảnh báo & Kênh liên hệ (`PET-CS-004`)

* **Câu hỏi 7 (Tìm kiếm thông tin định danh/cảnh báo):** *"Shop có website chính thức nào không hay chuyển khoản vào số tài khoản nào?"*
* **Kỳ vọng:** Phải trả về chunk **Mục 4 (Cảnh báo giả mạo & Kênh hỗ trợ chính thức)** khẳng định chưa có website và dùng STK Vietcombank `0123456789`.

