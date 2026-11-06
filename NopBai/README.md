# ĐỒ ÁN MÔN HỌC: CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT
## ĐỀ TÀI 5: HỆ THỐNG TÌM ĐƯỜNG ĐI NGẮN NHẤT TRÊN BẢN ĐỒ (DIJKSTRA & A*)
**Trường Đại học Lạc Hồng - Khoa Công nghệ Thông tin**  
**Quy tắc:** Code chay thuần túy 100% (Zero Libraries) cho toàn bộ cấu trúc dữ liệu và giải thuật.

---

## 1. CẤU TRÚC THƯ MỤC DỰ ÁN SAU TÁI CẤU TRÚC (REFACTORED)

```text
NopBai/
│
├── BaoCao_DoAn_CuoiKy_DeTai5.docx  <-- Báo cáo thuyết minh Word học thuật hoàn chỉnh
├── BaoCao_ThuyetTrinh_DeTai5.pptx  <-- Slide PowerPoint báo cáo bảo vệ
├── GiaiThich_ThuVien.md            <-- Tài liệu giải trình thư viện & bộ câu hỏi vấn đáp
├── VideoScript.md                  <-- Kịch bản quay video demo (8-12 phút)
├── README.md                       <-- Hướng dẫn vận hành hệ thống
│
├── src/                            <-- Mã nguồn Python tái cấu trúc thành các module độc lập
│   ├── main.py                     (Điểm vào chính: điều phối menu console, không chứa thuật toán)
│   ├── route_finder.py             (Lớp tương thích ngược đảm bảo mọi mã cũ hoạt động bình thường)
│   ├── cautruc/                    (Các cấu trúc dữ liệu tự cài đặt thủ công)
│   │   ├── minheap.py              - IndexedMinHeap: Hàng đợi ưu tiên có mảng vị trí pos[]
│   │   ├── hashtable.py            - CustomHashTable: Bảng băm djb2 Linear Probing
│   │   ├── stack.py                - CustomStack: Ngăn xếp phục vụ đảo ngược lộ trình
│   │   ├── queue_.py               - CustomQueue: Hàng đợi FIFO phục vụ BFS
│   │   └── graph.py                - AdjListNode, CityMapGraph: Đồ thị danh sách kề tọa độ km
│   ├── thuattoan/                  (Các thuật toán cốt lõi)
│   │   ├── dijkstra.py             - dijkstra_shortest_path: Nguồn đơn & điểm tới điểm
│   │   ├── astar.py                - astar_shortest_path: Heuristic Euclid Admissible
│   │   ├── duongdi.py              - KetQuaTimDuong (dataclass), phục hồi lộ trình
│   │   ├── lienthong.py            - kiem_tra_lien_thong_bfs: BFS kiểm tra liên thông
│   │   └── sapxep_timkiem.py       - Quicksort & Binary Search tự cài
│   ├── tienich/                    (Công cụ toán học, dữ liệu và đo đạc)
│   │   ├── toan.py                 - tinh_can_bac_hai_newton, tinh_khoang_cach_euclid
│   │   ├── dulieu.py               - Bộ sinh và đọc JSON thuần, bản đồ mẫu 15 nút
│   │   ├── sinhdothi.py            - Sinh lưới km, sinh đồ thị ngẫu nhiên liên thông (LCG seed)
│   │   └── dohieunang.py           - Đo thời gian lặp lặp loại bỏ warmup, benchmark
│   └── giaodien/                   (Giao diện dòng lệnh tách biệt)
│       ├── menu.py                 - Các hàm chức năng menu riêng biệt
│       ├── nhaplieu.py             - Nhập liệu an toàn (số nguyên, số thực, tên đỉnh)
│       └── hienthi.py              - In bảng so sánh học thuật, in chi tiết lộ trình
│
├── web/                            <-- Ứng dụng Web mô phỏng trực quan (Mở chạy ngay)
│   ├── index.html                  (Giao diện HTML5 thuần, Map View & Benchmark View)
│   ├── style.css                   (CSS hiện đại, hiệu ứng sinh động)
│   ├── graph_core.js               (Lõi cấu trúc dữ liệu & thuật toán JS thuần)
│   └── app.js                      (Điều phối sự kiện chuột, Zoom/Pan Canvas, kẹt xe động)
│
├── test/                           <-- Hệ thống kiểm thử tự động toàn diện
│   ├── test_cautruc.py             (Kiểm thử Heap, Hash Table, Stack, Queue)
│   ├── test_thuattoan.py           (Kiểm thử tính đúng đắn, 1 chiều, kẹt xe, >= 200 cặp ngẫu nhiên)
│   ├── test_hieunang.py            (Kiểm thử stress-test quy mô lớn: 100 đến 20.000 đỉnh)
│   ├── test_suite.py               (Bộ test tổng 26 Test Cases gốc)
│   ├── chay_tat_ca.py              (Runner thực thi toàn bộ và xuất báo cáo)
│   └── test_results.csv            (File kết quả kiểm thử định dạng CSV)
│
└── hinh/                           <-- Hình ảnh kiến trúc hệ thống, sơ đồ khối & biểu đồ
    ├── hinh_1_1_tien_do_gantt.png
    ├── hinh_3_1_kien_truc_he_thong.png
    ├── hinh_3_2_luu_do_thuat_toan.png
    ├── hinh_4_1_ban_do_6_nut.png
    └── hinh_4_2_bieu_do_so_sanh.png
```

---

## 2. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

### A. Chạy ứng dụng Web mô phỏng trực quan:
* Không cần cài đặt bất kỳ server web nào (Apache, Nginx, Node.js).
* Chỉ cần **nhấp đúp chuột vào file `web/index.html`** hoặc mở bằng trình duyệt (Google Chrome, Microsoft Edge, Firefox, Cốc Cốc).

### B. Chạy ứng dụng Console Python:
* Mở terminal tại thư mục `NopBai` và thực hiện một trong hai cách:
  ```bash
  python -m src.main
  # hoặc
  python src/main.py
  ```

### C. Chạy bộ kiểm thử tự động:
* Chạy toàn bộ các bộ test mô-đun hóa và stress test đến 20.000 đỉnh:
  ```bash
  python test/chay_tat_ca.py
  ```
* Chạy riêng lẻ từng bộ kiểm thử:
  ```bash
  python test/test_cautruc.py
  python test/test_thuattoan.py
  python test/test_hieunang.py
  ```
