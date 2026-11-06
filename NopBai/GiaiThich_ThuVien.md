# BÁO CÁO GIẢI THÍCH SỬ DỤNG THƯ VIỆN & CÔNG CỤ
**Học phần:** Cấu trúc Dữ liệu và Giải thuật  
**Đề tài 5:** Hệ Thống Tìm Đường Đi Ngắn Nhất Trên Bản Đồ (Dijkstra & A*)  
**Đơn vị:** Khoa Công nghệ Thông tin - Trường Đại học Lạc Hồng  

---

## 1. NGUYÊN TẮC CỐT LÕI: "CODE CHAY" 100% (ZERO LIBRARIES CHO PHẦN THUẬT TOÁN)
Đồ án tuân thủ nghiêm ngặt chuẩn mực học thuật của môn học: **Không sử dụng bất kỳ thư viện ngoài hay cấu trúc dựng sẵn nào của ngôn ngữ** cho toàn bộ phần lõi tính toán.

### Bảng đối chiếu các cấu trúc dữ liệu và giải thuật tự cài đặt:
| Cấu trúc / Giải thuật | Thư viện cấm dùng | File tự cài đặt trong đồ án | Độ phức tạp lý thuyết | Ghi chú kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **Hàng đợi ưu tiên** | `heapq`, `queue.PriorityQueue` | `src/cautruc/minheap.py` | Thêm: $O(\log V)$, Giảm khóa: $O(\log V)$, Lấy min: $O(\log V)$ | Min-Heap có mảng chỉ mục vị trí `pos[]` để `decrease_key` trong $O(\log V)$ |
| **Bảng băm ánh xạ** | `dict` (dùng làm hash table lõi) | `src/cautruc/hashtable.py` | Chèn: $O(1)$, Tra cứu: $O(1)$ | Tự cài bảng băm Linear Probing với giải thuật băm chuỗi kinh điển **djb2** |
| **Ngăn xếp phục hồi** | `collections.deque` | `src/cautruc/stack.py` | Push: $O(1)$, Pop: $O(1)$ | Tự cài ngăn xếp mảng động phục vụ đảo ngược lộ trình truy vết từ `prev[]` |
| **Hàng đợi FIFO** | `queue.Queue`, `deque` | `src/cautruc/queue_.py` | Push: $O(1)$, Pop: $O(1)$ | Tự cài hàng đợi 2 con trỏ phục vụ giải thuật BFS |
| **Đồ thị thành phố** | `networkx`, `scipy.sparse` | `src/cautruc/graph.py` | Duyệt kề: $O(\text{deg}(u))$ | Danh sách kề tự cài với nút liên kết `AdjListNode`, lưu tọa độ km thực |
| **Giải thuật Dijkstra** | `networkx.dijkstra_path` | `src/thuattoan/dijkstra.py` | $O((V + E) \log V)$ | Dijkstra nguồn đơn và điểm-đến-điểm dừng sớm khi chạm đích |
| **Giải thuật A\*** | `networkx.astar_path` | `src/thuattoan/astar.py` | $O((V + E) \log V)$ | Heuristic Euclid chuẩn hóa tỉ lệ $h\_scale$ bảo đảm tính Admissible |
| **Kiểm tra liên thông** | `networkx.is_connected` | `src/thuattoan/lienthong.py` | $O(V + E)$ | BFS lan truyền kiểm tra đồ thị liên thông an toàn |
| **Sắp xếp chi phí** | `list.sort()`, `sorted()` | `src/thuattoan/sapxep_timkiem.py`| $O(N \log N)$ | Quicksort phân hoạch Lomuto tự cài đặt thủ công |
| **Căn bậc hai** | `math.sqrt` | `src/tienich/toan.py` | $O(\log(1/\epsilon))$ | Xấp xỉ tiếp tuyến Newton-Raphson với sai số $\epsilon = 10^{-7}$ |
| **Sinh số ngẫu nhiên** | `random` (cho benchmark) | `src/tienich/sinhdothi.py` | $O(1)$ | Bộ sinh số tuyến tính đồng dư LCG tự cài có seed cố định tái lập được |
| **Phân tích cú pháp JSON**| `import json` (phần lõi) | `src/tienich/dulieu.py` | $O(N)$ | Bộ Parser và Serializer chuỗi JSON viết bằng thuật toán duyệt ký tự thuần |

---

## 2. DANH SÁCH THƯ VIỆN HỖ TRỢ ĐƯỢC PHÉP SỬ DỤNG
Các thư viện dưới đây chỉ được dùng cho mục đích phụ trợ ngoại vi (hệ thống, đo đạc đồng hồ phần cứng, định dạng kiểu dữ liệu):

| Thư viện | Phiên bản / Nguồn | File sử dụng | Mục đích sử dụng | Có tham gia tính toán đường đi không? |
| :--- | :--- | :--- | :--- | :--- |
| `time` | Có sẵn trong Python Standard Library | `src/tienich/dohieunang.py` | Sử dụng hàm `time.perf_counter()` để đo thời gian CPU thực thi giải thuật | **KHÔNG** (Chỉ đo thời gian hệ thống) |
| `dataclasses` | Có sẵn trong Python (>= 3.7) | `src/thuattoan/duongdi.py` | Khai báo lớp dữ liệu chuẩn `KetQuaTimDuong` giúp code rõ ràng, có type hint | **KHÔNG** (Chỉ cấu trúc hóa dữ liệu trả về) |
| `typing` | Có sẵn trong Python Standard Library | Hầu hết các file `src/` | Khai báo Type Hints (`List`, `Tuple`, `Optional`, `Any`) phục vụ kiểm tra kiểu | **KHÔNG** (Chỉ phục vụ cú pháp) |
| `sys`, `os` | Có sẵn trong Python Standard Library | `src/main.py`, `test/*` | Điều hướng đường dẫn thư mục `sys.path` để chạy module không bị lỗi import | **KHÔNG** (Chỉ phục vụ môi trường) |

---

## 3. CÂU HỎI VẤN ĐÁP THƯỜNG GẶP KHI BẢO VỆ ĐỒ ÁN

### Câu 1: Tại sao nhóm phải tự cài đặt Indexed Min-Heap có mảng `pos[]` thay vì dùng `heapq` của Python?
* **Trả lời:**
  - Thư viện `heapq` trong Python là Min-Heap chuẩn nhưng **không hỗ trợ hàm `decrease_key` (giảm khóa) trực tiếp**. Trong thuật toán Dijkstra và A*, khi nới lỏng một cạnh (relax), nếu tìm thấy một cung đường ngắn hơn đến đỉnh $v$, ta cần cập nhật khoảng cách của $v$ trong Heap.
  - Nếu không có mảng chỉ mục `pos[]`, ta buộc phải tìm kiếm đỉnh $v$ mất thời gian tuyến tính $O(V)$, làm độ phức tạp tổng thể bị suy biến thành $O(V^2)$.
  - Nhờ tự cài đặt mảng vị trí `pos[v]` lưu vị trí chỉ số hiện tại của đỉnh $v$ trong cây Heap, thao tác `decrease_key` được thực hiện bằng cách hoán vị ngược lên gốc (`_sift_up`) chỉ mất đúng **$O(\log V)$**, đưa toàn bộ giải thuật về độ phức tạp tối ưu **$O((V + E) \log V)$**.

### Câu 2: Làm thế nào nhóm đảm bảo hàm Heuristic của A* luôn Admissible và Consistent?
* **Trả lời:**
  - Điều kiện tiên quyết để A* tìm ra đường đi ngắn nhất tối ưu tuyệt đối (không bị chệch so với Dijkstra) là hàm heuristic $h(n)$ phải có tính **Admissible**: $h(n) \le d^*(n)$ (ước lượng không bao giờ vượt quá khoảng cách thực).
  - Vì tọa độ các đỉnh tính theo đường chim bay (Euclid), nhưng khoảng cách đường bộ thực tế $w$ có thể gấp khúc hoặc có hệ số khác nhau, nhóm đã cài đặt thuật toán tự động tính hệ số co giãn:
    $$h\_scale = \min\left(1.0, \min_{(u,v) \in E} \frac{\text{Trọng số thực } w(u,v)}{\text{Khoảng cách Euclid}(u,v)}\right)$$
  - Khi nhân Euclid với $h\_scale$, hàm $h(n)$ đảm bảo luôn là chặn dưới của khoảng cách thực tế trên mọi nhánh đi, do đó A* bảo đảm tính đúng đắn 100% tương đương Dijkstra trên mọi trường hợp thử nghiệm.

### Câu 3: Khi đồ thị bị mất liên thông, hệ thống xử lý như thế nào để tránh vòng lặp vô tận hoặc crash?
* **Trả lời:**
  - Trong Min-Heap, các đỉnh không liên thông với đỉnh xuất phát sẽ luôn giữ giá trị khoảng cách ban đầu là `inf`.
  - Vòng lặp `while not heap.is_empty()` chỉ trích xuất các đỉnh có thể tới được. Khi heap hết phần tử mà đỉnh đích $v_{end}$ vẫn có `dist[v_{end}] == inf`, thuật toán lập tức dừng lại an toàn, đóng gói kết quả với cờ `success = False` và thông báo `"Không có đường đi giữa hai địa điểm"`. Chương trình không bao giờ bị crash hay rơi vào vòng lặp vô tận.
