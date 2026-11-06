# KỊCH BẢN VIDEO BÁO CÁO NGHIỆM THU ĐỒ ÁN CUỐI KỲ
## ĐỀ TÀI 5: HỆ THỐNG TÌM ĐƯỜNG ĐI NGẮN NHẤT TRÊN BẢN ĐỒ (DIJKSTRA & A*)
**Học phần:** Cấu trúc Dữ liệu và Giải thuật  
**Đơn vị:** Trường Đại học Lạc Hồng - Khoa Công nghệ Thông tin  
**Nhóm sinh viên thực hiện (Nhóm 4):**
1. **Nguyễn Hoàng Anh (Nhóm trưởng)** - MSSV: 125000977
2. **Hà Văn Kiên** - MSSV: 125000399
3. **Trần Quang Huy** - MSSV: 125001825
4. **Hoàng Minh Phát** - MSSV: 125001323

**Thời lượng dự kiến:** 10 phút (Trong khung 8 - 12 phút chuẩn học thuật).

---

### PHÂN BỔ THỜI GIAN VÀ CẢNH QUAY (TIMELINE & SCREENPLAY)

#### PHẦN 1: MỞ ĐẦU & GIỚI THIỆU TỔNG QUAN (00:00 - 01:30)
* **Người trình bày:** Nguyễn Hoàng Anh (Nhóm trưởng)
* **Cảnh quay:**
  - `[00:00 - 00:30]` Toàn cảnh Slide 1 (Tiêu đề đồ án, tên trường Đại học Lạc Hồng, danh sách thành viên nhóm).
  - `[00:30 - 01:30]` Chuyển sang Slide 2 & 3: Trình bày bài toán thực tế, 5 yêu cầu đề bài F01 - F05.
* **Lời thoại chi tiết:**
  > *"Kính chào Thầy Cô và các bạn. Em là Nguyễn Hoàng Anh, đại diện Nhóm 4 lớp 25CT111 Khoa Công nghệ Thông tin, Trường Đại học Lạc Hồng. Hôm nay nhóm em xin phép được báo cáo nghiệm thu đồ án môn Cấu trúc Dữ liệu và Giải thuật với Đề tài số 5: 'Hệ thống Tìm đường đi Ngắn nhất trên Bản đồ Thành phố ứng dụng thuật toán Dijkstra và A*'.*  
  > *Bài toán đặt ra là mô phỏng hệ thống giao thông đô thị dưới dạng đồ thị có trọng số, hỗ trợ tìm kiếm tuyến đường tối ưu giữa các địa điểm, đồng thời mở rộng thuật toán A* với hàm Heuristic khoảng cách Euclid để tăng tốc độ tìm kiếm và mô phỏng phản ứng đổi đường khi xảy ra kẹt xe động."*

---

#### PHẦN 2: THIẾT KẾ CẤU TRÚC DỮ LIỆU & GIẢI THUẬT THUẦN (01:30 - 03:30)
* **Người trình bày:** Hà Văn Kiên
* **Cảnh quay:**
  - `[01:30 - 02:15]` Mở file mã nguồn `src/route_finder.py` trên VS Code (dòng 58 - 145: giải thích lớp `IndexedMinHeap`).
  - `[02:15 - 03:00]` Cuộn xuống dòng 150 - 240: giải thích `AdjListNode`, `CityMapGraph` và bảng băm `CustomHashTable`.
  - `[03:00 - 03:30]` Mở Slide 4 & 5 chiếu lưu đồ thuật toán Dijkstra và A*.
* **Lời thoại chi tiết:**
  > *"Chào Thầy Cô, em là Hà Văn Kiên. Để tuân thủ đúng nguyên tắc 'code thuần chay 100%' không phụ thuộc vào bất kỳ thư viện ngoài hay module có sẵn nào của ngôn ngữ, nhóm em đã tự thiết kế toàn bộ các cấu trúc dữ liệu cốt lõi:*  
  > *1. Tại dòng 58 của file `route_finder.py`, nhóm em tự cài đặt hàng đợi ưu tiên `IndexedMinHeap` với mảng chỉ số vị trí `pos[]`. Nhờ đó, thao tác `decrease_key` khi nới lỏng cạnh được thực hiện tối ưu trong độ phức tạp O(log V) thay vì phải đẩy trùng lặp phần tử.*  
  > *2. Đồ thị thành phố được biểu diễn bằng Danh sách kề với cấu trúc Danh sách liên kết đơn `AdjListNode`, hỗ trợ đầy đủ đường một chiều, hai chiều và lưu trữ tọa độ Descartes (x, y).*  
  > *3. Thuật toán Dijkstra tìm kiếm vết dầu loang theo khoảng cách tích lũy g(v), trong khi thuật toán A* kết hợp hàm Heuristic h(n) tính khoảng cách đường chim bay Euclidean bằng phương pháp lặp số Newton-Raphson thuần túy để dẫn hướng trực tiếp về đích."*

---

#### PHẦN 3: DEMO ỨNG DỤNG WEB MÔ PHỎNG TRỰC QUAN (03:30 - 06:30)
* **Người trình bày:** Trần Quang Huy
* **Cảnh quay:**
  - `[03:30 - 04:30]` Mở trình duyệt Web chạy file `web/index.html`. Giới thiệu giao diện Canvas bản đồ 15 giao lộ mẫu.
  - `[04:30 - 05:15]` Thao tác chọn Start (`N1_VongXoayBenTre`) và End (`N15_CangGiaoNhanHang`). Nhấn "So Sánh Cả Hai".
  - `[05:15 - 05:50]` Chạy hoạt ảnh Step-by-Step (Tự chạy, tạm dừng, lùi bước), chỉ vào bảng `dist[]`, `prev[]` và các đỉnh đổi màu.
  - `[05:50 - 06:30]` Thao tác chọn cạnh kẹt xe, kéo thanh trượt hệ số $k = 3.0$, chỉ ra màu đỏ của tuyến đường và hệ thống tự động bẻ lộ trình tối ưu mới.
* **Lời thoại chi tiết:**
  > *"Em là Trần Quang Huy. Em xin phép trình diễn giao diện tương tác trực quan trên nền tảng Web thuần không dùng thư viện ngoài.*  
  > *Trên màn hình là bản đồ thành phố mẫu gồm 15 nút giao lộ và 24 tuyến đường. Khi chúng ta chọn điểm đầu N1 và điểm cuối N15 rồi bấm 'So Sánh Cả Hai':*  
  > *- Cả Dijkstra và A* đều tìm ra chính xác lộ trình tối ưu dài 102.0 km.*  
  > *- Tuy nhiên, Thầy Cô có thể quan sát trên biểu đồ cột và bảng số liệu: Thuật toán Dijkstra phải duyệt qua 13 nút, trong khi thuật toán A* chỉ cần duyệt 8 nút (tiết kiệm hơn 38% không gian tìm kiếm).*  
  > *Tiếp theo, khi em click vào cung đường nối giữa N10 và N15 rồi tăng thanh trượt kẹt xe lên 3.0x, cung đường lập tức chuyển sang màu đỏ cảnh báo. Hệ thống tính toán lại ngay lập tức và tự động chuyển hướng xe sang trục đường N14 để né điểm nghẽn."*

---

#### PHẦN 4: CHẠY TERMINAL & KIỂM THỬ TỰ ĐỘNG STRESS TEST (06:30 - 08:30)
* **Người trình bày:** Hoàng Minh Phát
* **Cảnh quay:**
  - `[06:30 - 07:15]` Mở Terminal PowerShell, chạy lệnh `python src/main.py`. Thao tác menu chọn chức năng 1, 2, 3.
  - `[07:15 - 08:30]` Chạy lệnh `python test/test_suite.py`. Quay màn hình toàn bộ 22 ca kiểm thử PASS 100%, đặc biệt là các ca Stress Test quy mô lớn 100, 1.000, 5.000 và 20.000 đỉnh. Mở file `test/test_results.csv`.
* **Lời thoại chi tiết:**
  > *"Em là Hoàng Minh Phát. Em xin phép trình diễn chương trình dòng lệnh Console và bộ kiểm thử tự động toàn diện.*  
  > *Trong menu Console của `main.py`, người dùng có thể dễ dàng quản lý đồ thị, tra cứu khoảng cách Dijkstra nguồn đơn và cập nhật tham số giao thông thời gian thực.*  
  > *Đặc biệt, để khẳng định độ tin cậy và sự bền vững của thuật toán, nhóm đã xây dựng bộ kiểm thử tự động trong `test_suite.py` với 22 Test Cases. Kết quả kiểm thử đạt 100% PASS:*  
  > *- Kiểm thử xử lý biên: đồ thị mất liên thông báo lỗi an toàn, từ chối trọng số âm, xử lý điểm đầu trùng điểm cuối.*  
  > *- Kiểm thử quy mô lớn: Trên đồ thị lưới 20.000 đỉnh và gần 80.000 cung đường, thuật toán giải quyết bài toán tìm đường chỉ trong khoảng 0.12 giây, chứng minh cấu trúc Indexed Min-Heap tự cài đặt đạt độ phức tạp O((V + E) log V) vô cùng chính xác."*

---

#### PHẦN 5: TỔNG KẾT & KẾT LUẬN (08:30 - 10:00)
* **Người trình bày:** Nguyễn Hoàng Anh (Nhóm trưởng)
* **Cảnh quay:**
  - `[08:30 - 09:30]` Chiếu Slide 11 & 12 (Bảng đánh giá đóng góp thành viên, kết luận đồ án).
  - `[09:30 - 10:00]` Chiếu Slide cuối (Lời cảm ơn Thầy Cô phản biện và phiên Hỏi & Đáp).
* **Lời thoại chi tiết:**
  > *"Kính thưa Thầy Cô, qua quá trình nghiên cứu và thực hiện đề tài, nhóm em đã hoàn thành trọn vẹn 100% các yêu cầu từ lý thuyết thuật toán, lập trình thực nghiệm thuần túy đến mô phỏng giao diện người dùng.*  
  > *Đồ án đã giúp từng thành viên trong nhóm hiểu sâu sắc bản chất vận hành của các cấu trúc dữ liệu nâng cao như Min-Heap, Bảng băm và ứng dụng thực tiễn của giải thuật đồ thị trong đời sống.*  
  > *Nhóm 4 xin chân thành cảm ơn sự hướng dẫn tận tình của Quý Thầy Cô bộ môn Cấu trúc Dữ liệu và Giải thuật. Nhóm em rất mong nhận được những nhận xét và góp ý quý báu để đồ án ngày càng hoàn thiện hơn. Em xin chân thành cảm ơn!"*

---

### CHECKLIST CÁC PHÂN CẢNH QUAY MÀN HÌNH (SCREEN RECORDING CHECKLIST)
- [ ] **Cảnh 1:** Trình chiếu Slide PowerPoint từ Slide 1 đến Slide 5 (Đầy đủ tiêu đề ĐH Lạc Hồng, mục tiêu, lưu đồ).
- [ ] **Cảnh 2:** Quay cận cảnh mã nguồn file `src/route_finder.py` (Lớp `IndexedMinHeap` và hàm `sqrt_newton`).
- [ ] **Cảnh 3:** Mở file `web/index.html` trên trình duyệt Chrome/Edge, phóng to màn hình 100%.
- [ ] **Cảnh 4:** Thao tác chọn điểm trên Web và click nút "So Sánh Cả Hai" để thấy lộ trình tím và biểu đồ cột.
- [ ] **Cảnh 5:** Nhấn nút "Tự Chạy" trên Web để ghi lại chuyển động của các đỉnh đổi màu từng bước.
- [ ] **Cảnh 6:** Kéo thanh trượt kẹt xe $k = 3.0$ trên một tuyến đường để ghi lại việc bẻ hướng lộ trình.
- [ ] **Cảnh 7:** Mở Terminal và gõ lệnh chạy `python src/main.py`.
- [ ] **Cảnh 8:** Gõ lệnh chạy `python test/test_suite.py` để xuất hiện dòng `TONG KET KIEM THU: 22/22 TEST CASES PASS (100.0%)`.
- [ ] **Cảnh 9:** Mở file `test/test_results.csv` bằng Excel để minh chứng dữ liệu kiểm thử thực tế.
- [ ] **Cảnh 10:** Trình chiếu Slide kết luận và bảng phân công đóng góp thành viên.
