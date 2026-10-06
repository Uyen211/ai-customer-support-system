# HƯỚNG DẪN CHI TIẾT TRÌNH BÀY NỘI DUNG KIỂM THỬ HỘP TRẮNG (WHITE-BOX TESTING)

Tài liệu dưới đây được tinh gọn theo đúng các bài tập và biểu mẫu trong giáo trình, loại bỏ các cột không cần thiết và giữ các bảng biểu tập trung trực tiếp vào: **Đường đi, Đầu vào và Đầu ra**.

---

## 1. Kiểm thử dòng điều khiển (Control Flow Testing)

### 1.1. Mã nguồn đơn vị kiểm thử (Source Code & Numbering)

* **Phương pháp trình bày:** Khối mã nguồn (Code Block) hoàn chỉnh của hàm kiểm thử.
* **Quy tắc cốt lõi:**
  * Đánh số thứ tự tuần tự từng dòng lệnh (1, 2, 3...).
  * Số thứ tự này được dùng làm tên định danh của các đỉnh trên đồ thị dòng điều khiển.

### 1.2. Xây dựng đồ thị dòng điều khiển (Control Flow Graph - CFG)

* **Phương pháp trình bày:** Vẽ hình ảnh đồ thị có hướng.
  * Đỉnh: Biểu diễn câu lệnh hoặc khối lệnh tuần tự.
  * Cạnh có hướng: Biểu diễn luồng điều khiển, các nhánh rẽ gắn nhãn `True` (Đúng) hoặc `False` (Sai).
* **Quy tắc cốt lõi:**
  * **Đồ thị cho độ đo C1, C2:** Biểu thức logic phức hợp (có toán tử AND `&&`, OR `||`) có thể để chung trong một đỉnh điều kiện.
  * **Đồ thị cho độ đo C3:** Bắt buộc tách từng điều kiện con thành phần thành từng đỉnh quyết định riêng lẻ để kiểm tra nhánh Đúng/Sai của từng điều kiện con.

### 1.3. Sinh đường đi và ca kiểm thử theo các độ đo bao phủ

#### A. Sinh đường đi và ca kiểm thử với độ đo C1 (Statement Coverage)

* **Quy tắc cốt lõi:** Mọi câu lệnh trong chương trình đều phải được thực thi ít nhất một lần. Chọn tập đường đi ngắn nhất phủ kín toàn bộ các đỉnh.
* **Bảng biểu trình bày:**

| TT / ID | Đường đi (Test Path) | Đầu vào (Inputs) | Đầu ra (Output) |
| --- | --- | --- | --- |
| **TC_C1_01** | 1; 2; 3 | *Dữ liệu chạy vào nhánh đầu* | *Kết quả trả về tương ứng* |
| **TC_C1_02** | 1; 2; 4; 5; 6; 7; 8 | *Dữ liệu chạy qua các dòng còn lại* | *Kết quả trả về tương ứng* |

#### B. Sinh đường đi và ca kiểm thử với độ đo C2 (Branch Coverage)

* **Quy tắc cốt lõi:** Mỗi điểm quyết định (rẽ nhánh) phải được duyệt qua cả hai nhánh Đúng (True) và Sai (False) ít nhất một lần.
* **Bảng biểu trình bày:**

| TT / ID | Điểm quyết định phủ (True/False) | Đường đi (Test Path) | Đầu vào (Inputs) | Đầu ra (Output) |
| --- | --- | --- | --- | --- |
| **TC_C2_01** | Đỉnh 2: True | 1; 2; 3 | *Dữ liệu thỏa mãn điều kiện tại 2* | *Giá trị trả về* |
| **TC_C2_02** | Đỉnh 2: False; Đỉnh 5: True | 1; 2; 4; 5; 6; 7; 8 | *Dữ liệu sai tại 2, đúng tại 5* | *Giá trị trả về* |
| **TC_C2_03** | Đỉnh 2: False; Đỉnh 5: False | 1; 2; 4; 5; 7; 8 | *Dữ liệu sai tại 2, sai tại 5* | *Giá trị trả về / Báo lỗi* |

#### C. Sinh đường đi và ca kiểm thử với độ đo C3 (Condition Coverage - Áp dụng khi có điều kiện phức hợp)

* **Quy tắc cốt lõi:** Mỗi điều kiện con trong biểu thức điều kiện phức hợp đều phải nhận cả hai giá trị Đúng (True) và Sai (False) ít nhất một lần.
* **Bảng biểu trình bày:**

| TT / ID | Trạng thái các điều kiện con | Đường đi (Test Path) | Đầu vào (Inputs) | Đầu ra (Output) |
| --- | --- | --- | --- | --- |
| **TC_C3_01** | Điều kiện 1: T, Điều kiện 2: T | 1; 2; 4; 5; 6; 7; 8 | *Bộ dữ liệu làm cả 2 điều kiện Đúng* | *Giá trị trả về* |
| **TC_C3_02** | Điều kiện 1: T, Điều kiện 2: F | ... | *Bộ dữ liệu làm ĐK 1 Đúng, ĐK 2 Sai* | *Giá trị trả về* |
| **TC_C3_03** | Điều kiện 1: F, Điều kiện 2: T | ... | *Bộ dữ liệu làm ĐK 1 Sai, ĐK 2 Đúng* | *Giá trị trả về* |
| **TC_C3_04** | Điều kiện 1: F, Điều kiện 2: F | ... | *Bộ dữ liệu làm cả 2 điều kiện Sai* | *Giá trị trả về* |

#### D. Kiểm thử cấu trúc lặp (Loop Testing - Áp dụng nếu hàm có vòng lặp While / Do-While / For)

* **Quy tắc cốt lõi:** Lập bảng ca kiểm thử theo các số lần lặp biên: 0 lần, 1 lần, 2 lần, $k$ lần (điển hình), $n-1$ lần, $n$ lần (tối đa), và $n+1$ lần (vượt ngưỡng).
* **Bảng biểu trình bày:**

| TT / ID | Số lần lặp | Đầu vào (Inputs) | Đầu ra (Output) |
| --- | --- | --- | --- |
| **TC_LOOP_0** | 0 lần | *Mảng rỗng hoặc phần tử dừng ngay vị trí đầu* | *Kết quả khi không chạy vòng lặp* |
| **TC_LOOP_1** | 1 lần | *Dữ liệu thỏa mãn đúng 1 lần lặp* | *Kết quả sau 1 lần lặp* |
| **TC_LOOP_2** | 2 lần | *Dữ liệu thỏa mãn 2 lần lặp* | *Kết quả sau 2 lần lặp* |
| **TC_LOOP_K** | $k$ lần (ví dụ $k=5$) | *Dữ liệu thỏa mãn $k$ lần lặp* | *Kết quả sau $k$ lần lặp* |
| **TC_LOOP_N-1** | $n - 1$ lần | *Dữ liệu thỏa mãn $n-1$ lần lặp* | *Kết quả sau $n-1$ lần lặp* |
| **TC_LOOP_N** | $n$ lần | *Dữ liệu đạt ngưỡng tối đa $n$ lần lặp* | *Kết quả sau $n$ lần lặp* |
| **TC_LOOP_N+1** | $n + 1$ lần | *Dữ liệu vượt quá kích thước $n$* | *Báo lỗi / Dừng lặp* |

---

## 2. Kiểm thử dòng dữ liệu (Data Flow Testing)

### 2.1. Liệt kê các câu lệnh ứng với các khái niệm của biến

* **Quy tắc cốt lõi:**
  * `def`: Câu lệnh gán hoặc khởi tạo giá trị cho biến.
  * `c-use`: Câu lệnh sử dụng biến để tính toán biểu thức hoặc trả về giá trị.
  * `p-use`: Biến được sử dụng trong các biểu thức điều kiện logic (rẽ nhánh hoặc lặp).
* **Bảng biểu trình bày:**

| Tên biến | Dòng lệnh định nghĩa (`def`) | Dòng lệnh dùng tính toán (`c-use`) | Cạnh/Dòng lệnh dùng điều kiện (`p-use`) |
| --- | --- | --- | --- |
| **Biến X** | Dòng 1, Dòng 4 | Dòng 5, Dòng 7 | Cạnh (3, 4), Cạnh (3, 7) |
| **Biến Y** | Dòng 2 | Dòng 5 | Cạnh (4, 5) |

### 2.2. Vẽ đồ thị dòng dữ liệu (Data Flow Graph - DFG)

* **Phương pháp trình bày:** Vẽ hình ảnh đồ thị có hướng.
  * Đỉnh: Là các câu lệnh gán (`def`) hoặc tính toán (`c-use`). Đỉnh bắt đầu là nơi nhận tham số, đỉnh kết thúc là lệnh kết thúc hàm.
  * Cạnh: Gắn kèm biểu thức điều kiện và danh sách các biến tham gia kiểm tra điều kiện (`p-use`).

### 2.3. Xác định các đường đi hoàn chỉnh cơ bản (Complete-paths)

* **Quy tắc cốt lõi:** Complete-path là đường đi có đỉnh đầu là điểm bắt đầu và đỉnh cuối là điểm kết thúc của đồ thị dòng dữ liệu.
* **Bảng biểu trình bày:**

| Mã đường đi | Danh sách các đỉnh tuần tự (Complete-path) |
| --- | --- |
| **CP_01** | Đỉnh 1 $\rightarrow$ Đỉnh 2 $\rightarrow$ Đỉnh 3 $\rightarrow$ Đỉnh 7 $\rightarrow$ Đỉnh 9 $\rightarrow$ Đỉnh 10 |
| **CP_02** | Đỉnh 1 $\rightarrow$ Đỉnh 2 $\rightarrow$ Đỉnh 3 $\rightarrow$ Đỉnh 4 $\rightarrow$ Đỉnh 5 $\rightarrow$ Đỉnh 6 $\rightarrow$ Đỉnh 3 $\rightarrow$ Đỉnh 7 $\rightarrow$ Đỉnh 10 |

### 2.4. Sinh đường đi và ca kiểm thử theo các tiêu chí độ đo dòng dữ liệu

* **Quy tắc cốt lõi:**
  * **All-defs:** Từ mỗi điểm `def` của biến, chọn Complete-path chứa đường dẫn sạch định nghĩa (Def-clear path) đến ít nhất một nơi sử dụng (`c-use` hoặc `p-use`).
  * **All-c-uses:** Từ mỗi điểm `def`, chọn Complete-path bao phủ đường dẫn sạch định nghĩa đến **tất cả** các đỉnh sử dụng tính toán (`c-use`) của biến đó.
  * **All-p-uses:** Từ mỗi điểm `def`, chọn Complete-path bao phủ đường dẫn sạch định nghĩa đến **tất cả** các cạnh sử dụng điều kiện (`p-use`) của biến đó.
  * **Xác định đầu vào:** Lấy các biểu thức điều kiện nằm trên các cạnh của đường đi Complete-path đã chọn, giải biểu thức để ra bộ dữ liệu đầu vào.
* **Bảng biểu trình bày:**

| TT / ID | Độ đo áp dụng & Biến xét | Đường đi lựa chọn (Complete-path) | Đầu vào (Inputs) | Đầu ra (Output) |
| --- | --- | --- | --- | --- |
| **TC_DF_01** | All-defs (Biến `tv`) | 1; 2; 3; 4; 5; 6; 3; 7; 9; 10 | `val = [1, -999]`, `AS = 2` | `1.0` |
| **TC_DF_02** | All-c-uses (Biến `ti`) | 1; 2; 3; 4; 5; 6; 3; 7; 8; 10 | `val = [0, -999]`, `AS = 2` | `-999` |
| **TC_DF_03** | All-p-uses (Biến `tv`) | 1; 2; 3; 7; 8; 10 | `val = [-999]`, `AS = 0` | `-999` |


---