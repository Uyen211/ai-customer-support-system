# Báo Cáo Đánh Giá Chất Lượng Truy Vấn Vector RAG

- **Mô hình Embedding**: `dangvantuan/vietnamese-embedding` (768 dims)
- **Tổng số Chunks**: 62
- **Top-1 Accuracy**: 5/7 (71.4%)
- **Top-3 Recall**: 6/7 (85.7%)

---

## Chi Tiết Kết Quả 7 Test Cases

### Test #1: Chính sách Đổi trả (PET-CS-002) - ✅ PASS (Top 1)
- **Câu hỏi**: *"Hàng mua về bị vỡ hỏng trong lúc vận chuyển thì phải làm thế nào?"*
- **Kỳ vọng**: PET-CS-002  ['3.3', 'vận chuyển', 'hư hỏng', 'video']

| Rank | Score | Content Snippet |
|---|---|---|
| Top 1 | 0.6098 | [Chính sách Đổi trả và Hoàn tiền (PET-CS-002) - Mục 6.1 Các trường hợp được hoàn tiền]: Hàng lỗi do nhà sản xuất mà không còn sản phẩm để đổi. Hàng gi... |
| Top 2 | 0.5107 | [Chính sách Vận chuyển và Giao nhận (PET-CS-003) - Mục 6.2 Hàng hư hỏng / Thất lạc do vận chuyển]: Khách quay video/chụp ảnh hộp hàng móp vỡ và gửi ng... |
| Top 3 | 0.5020 | [Chính sách Đổi trả và Hoàn tiền (PET-CS-002) - Mục 3.3 Hàng hư hỏng do vận chuyển]: Sản phẩm bị móp, vỡ, rách, biến dạng trong quá trình vận chuyển. ... |

---

### Test #2: Chính sách Đổi trả (PET-CS-002) - ✅ PASS (Top 1)
- **Câu hỏi**: *"Tôi không thích mùi của gói pate này nữa, shop có cho đổi trả không?"*
- **Kỳ vọng**: PET-CS-002  ['4', 'không được đổi trả', 'lý do', 'thẩm mỹ', '3.5']

| Rank | Score | Content Snippet |
|---|---|---|
| Top 1 | 0.4222 | [Chính sách Đổi trả và Hoàn tiền (PET-CS-002) - Mục 4 CÁC TRƯỜNG HỢP KHÔNG ĐƯỢC ĐỔI TRẢ]: PetHome từ chối đổi trả trong các trường hợp sau:. Quá thời ... |
| Top 2 | 0.4047 | [Chính sách Đổi trả và Hoàn tiền (PET-CS-002) - Mục 6.3 Mức hoàn tiền]: Hoàn 100% giá trị sản phẩm đã thanh toán. Phí vận chuyển: Hoàn 100% phí ship n... |
| Top 3 | 0.3932 | [Chính sách Đổi trả và Hoàn tiền (PET-CS-002) - Mục 3.3 Hàng hư hỏng do vận chuyển]: Sản phẩm bị móp, vỡ, rách, biến dạng trong quá trình vận chuyển. ... |

---

### Test #3: Chính sách Vận chuyển & Phí ship (PET-CS-003) - ❌ FAIL
- **Câu hỏi**: *"Tôi ở Biên Hòa thì đặt hàng mấy ngày nhận được và phí ship ra sao?"*
- **Kỳ vọng**: PET-CS-003  ['2', '5.1', 'Biên Hòa', 'Nhóm B']

| Rank | Score | Content Snippet |
|---|---|---|
| Top 1 | 0.4680 | [Hướng dẫn Mua hàng và Thanh toán (PET-CS-004) - Mục 2.1 Thanh toán khi nhận hàng (COD)]: Khách hàng trả tiền mặt trực tiếp cho shipper khi nhận được ... |
| Top 2 | 0.4650 | [Hướng dẫn Mua hàng và Thanh toán (PET-CS-004) - Mục 3 QUY ĐỊNH HỦY ĐƠN HÀNG]: Hủy miễn phí: Khi đơn hàng chưa được giao cho bên vận chuyển (thông báo... |
| Top 3 | 0.4630 | [Chính sách Vận chuyển và Giao nhận (PET-CS-003) - Mục 1.3 Nguyên tắc chốt đơn và giao hàng]: Đơn hàng được tư vấn, chốt thông tin (sản phẩm, địa chỉ,... |

---

### Test #4: Chính sách Vận chuyển & Phí ship (PET-CS-003) - ⚠️ PASS (Top 3)
- **Câu hỏi**: *"Đơn hàng ở TP.HCM bao nhiêu tiền thì được miễn phí ship?"*
- **Kỳ vọng**: PET-CS-003  ['5.2', 'Freeship', '300.000', 'TP. Hồ Chí Minh']

| Rank | Score | Content Snippet |
|---|---|---|
| Top 1 | 0.5482 | [Chính sách Vận chuyển và Giao nhận (PET-CS-003) - Mục 5.1a Bảng phí ship tiêu chuẩn (TP.HCM & Nhóm B)]: Cước phí khu vực TP.HCM Nội thành: Đơn dưới 2... |
| Top 2 | 0.5376 | [Chính sách Vận chuyển và Giao nhận (PET-CS-003) - Mục 5.2 Chính sách Miễn phí vận chuyển (Freeship)]: Khu vực TP. Hồ Chí Minh: Miễn phí vận chuyển ch... |
| Top 3 | 0.4879 | [Chính sách Vận chuyển và Giao nhận (PET-CS-003) - Mục 3.1 Các hình thức vận chuyển]: Giao hỏa tốc (Nội thành TP.HCM): Giao nhận trong 2–4 giờ qua Gra... |

---

### Test #5: Tri thức Sản phẩm (Product Chunks) - ✅ PASS (Top 1)
- **Câu hỏi**: *"Mèo nhà tôi nuôi chung cư hay bị nôn ra búi lông thì ăn loại hạt nào?"*
- **Kỳ vọng**:  CAT-ROYAL-INDOOR-2KG ['Royal Canin Indoor', 'búi lông']

| Rank | Score | Content Snippet |
|---|---|---|
| Top 1 | 0.5186 | [Sản phẩm Thức ăn hạt Royal Canin Indoor cho mèo trưởng thành 2kg (CAT-ROYAL-INDOOR-2KG) - Thông tin cốt lõi & Công dụng]: Thức ăn hạt Royal Canin Ind... |
| Top 2 | 0.4806 | [Sản phẩm Thức ăn hạt Royal Canin Indoor cho mèo trưởng thành 2kg (CAT-ROYAL-INDOOR-2KG) - Giải quyết vấn đề & Tình huống tìm kiếm]: Giải quyết tình t... |
| Top 3 | 0.3818 | [Sản phẩm Máy uống nước tự động PetKit Eversweet 2L cho mèo (CAT-PETKIT-FOUNTAIN-2L) - Thông tin cốt lõi & Công dụng]: Máy uống nước tự động PetKit Ev... |

---

### Test #6: Tri thức Sản phẩm (Product Chunks) - ✅ PASS (Top 1)
- **Câu hỏi**: *"Chó nhà hay cắn phá giày dép đồ đạc thì mua đồ chơi gì chịu lực tốt?"*
- **Kỳ vọng**:  DOG-KONG-CLASSIC-M ['Kong Classic', 'cắn phá']

| Rank | Score | Content Snippet |
|---|---|---|
| Top 1 | 0.4922 | [Sản phẩm Đồ chơi Kong Classic size M cho chó (DOG-KONG-CLASSIC-M) - Giải quyết vấn đề & Tình huống tìm kiếm]: Sản phẩm giải quyết các vấn đề như chó ... |
| Top 2 | 0.4778 | [Sản phẩm Đồ chơi Kong Classic size M cho chó (DOG-KONG-CLASSIC-M) - Thông tin cốt lõi & Công dụng]: Đồ chơi Kong Classic size M là sản phẩm dành cho ... |
| Top 3 | 0.3380 | [Sản phẩm Trụ cào móng Trixie cho mèo size L (CAT-TRIXIE-SCRATCHER-L) - Giải quyết vấn đề & Tình huống tìm kiếm]: Sản phẩm giải quyết tình trạng mèo c... |

---

### Test #7: Cảnh báo & Kênh liên hệ (PET-CS-004) - ✅ PASS (Top 1)
- **Câu hỏi**: *"Shop có website chính thức nào không hay chuyển khoản vào số tài khoản nào?"*
- **Kỳ vọng**: PET-CS-004  ['4', 'CẢNH BÁO', 'chưa có website', '0123456789']

| Rank | Score | Content Snippet |
|---|---|---|
| Top 1 | 0.4783 | [Hướng dẫn Mua hàng và Thanh toán (PET-CS-004) - Mục 2.2 Chuyển khoản Ngân hàng (CK trước)]: Khách chuyển khoản trực tiếp vào tài khoản ngân hàng chín... |
| Top 2 | 0.4604 | [Hướng dẫn Mua hàng và Thanh toán (PET-CS-004) - Mục 4 KÊNH HỖ TRỢ VÀ CẢNH BÁO GIẢ MẠO]: CẢNH BÁO QUAN TRỌNG: PetHome chưa có website và không có tổng... |
| Top 3 | 0.4601 | [Hướng dẫn Mua hàng và Thanh toán (PET-CS-004) - Mục 2.3 Ví điện tử (MoMo / ZaloPay / VNPay QR)]: Nhân viên tư vấn sẽ gửi Mã QR Thanh toán động trực t... |

---

