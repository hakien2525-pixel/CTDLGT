import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx_formatting_tools import (
    apply_run_font,
    add_body_paragraph,
    add_heading_1,
    add_heading_2,
    add_heading_3,
    add_code_block,
    add_equation_numbered,
    add_caption_figure,
    add_caption_table,
    format_table
)

def build_chapter3(doc):
    add_heading_1(doc, "CHƯƠNG 3. THIẾT KẾ VÀ CÀI ĐẶT HỆ THỐNG")
    add_body_paragraph(doc, "Hệ thống tìm đường đi ngắn nhất được thiết kế theo kiến trúc hướng đối tượng mô-đun hóa cao, phân định rõ ràng giữa các cấu trúc dữ liệu nền tảng, các giải thuật điều hướng cốt lõi và hệ thống giao tiếp người dùng. Toàn bộ các lớp và hàm được đặt tên tường minh, đúng chuẩn quy ước kỹ thuật và được cài đặt thuần túy tại thư mục mã nguồn NopBai/src/.")

    # 3.1
    add_heading_2(doc, "3.1. Các lớp cấu trúc dữ liệu nền tảng")
    add_body_paragraph(doc, "Lớp CustomHashTable (trong file src/cautruc/hashtable.py) quản lý ánh xạ hai chiều giữa chuỗi định danh địa điểm (tên giao lộ) và chỉ số số nguyên đại diện trong đồ thị. Bảng băm lưu trữ hai mảng song song self.keys và self.values cùng biến đếm self.size. Khi thêm một cặp khóa - giá trị bằng phương thức put(khoa, gia_tri), thuật toán tính chỉ số băm qua DJB2 và thực hiện dò tuyến tính. Nếu hệ số tải vượt ngưỡng 50%, phương thức _rehash() tự động nhân đôi kích thước bảng và băm lại toàn bộ dữ liệu, duy trì độ phức tạp trung bình O(1) cho phương thức get(khoa) và contains(khoa).")
    add_body_paragraph(doc, "Lớp IndexedMinHeap (trong file src/cautruc/minheap.py) cài đặt hàng đợi ưu tiên có mảng định vị chỉ số. Dữ liệu đống được lưu trong self.heap dưới dạng danh sách các cặp (priority, item), kết hợp mảng self.pos có kích thước cố định bằng capacity đỉnh. Thao tác insert(priority, item) thêm phần tử vào cuối đống, ghi nhận vị trí vào self.pos và kích hoạt _sift_up(). Thao tác decrease_key(item, new_priority) sử dụng mảng self.pos để định vị ngay lập tức vị trí phần tử trong O(1), cập nhật độ ưu tiên mới và thực hiện vun lên đống trong O(log V). Thao tác pop_min() lấy phần tử gốc nhỏ nhất, hoán vị phần tử cuối lên thay thế và thực hiện _sift_down() trong O(log V). Mọi thao tác đều được theo dõi bằng bộ đếm self.heap_ops phục vụ đánh giá thực nghiệm.")

    # Trích mã IndexedMinHeap
    code_heap = [
        "def decrease_key(self, item: int, new_priority: float) -> None:",
        "    self.heap_ops += 1",
        "    idx = self.pos[item]",
        "    if idx != -1 and new_priority < self.heap[idx][0]:",
        "        self.heap[idx] = (new_priority, item)",
        "        self._sift_up(idx)",
        "",
        "def pop_min(self) -> Tuple[Optional[float], Optional[int]]:",
        "    self.heap_ops += 1",
        "    if not self.heap: return None, None",
        "    min_prio, min_item = self.heap[0]",
        "    self.pos[min_item] = -1",
        "    last_prio, last_item = self.heap.pop()",
        "    if self.heap:",
        "        self.heap[0] = (last_prio, last_item)",
        "        self.pos[last_item] = 0",
        "        self._sift_down(0)",
        "    return min_prio, min_item"
    ]
    add_code_block(doc, code_heap)
    add_body_paragraph(doc, "Đoạn mã trên minh họa sự phối hợp nhịp nhàng giữa mảng pos[] và mảng heap[]. Trong decrease_key, việc tra cứu trực tiếp vị trí idx = self.pos[item] giúp triệt tiêu hoàn toàn thao tác duyệt mảng tốn kém O(n). Trong pop_min, việc xóa gốc và cập nhật lại chỉ số pos[last_item] = 0 trước khi thực hiện sift-down đảm bảo tính toàn vẹn địa chỉ của mọi nút trong đống.")

    # Image diagram heap
    p_img_heap = doc.add_paragraph()
    p_img_heap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img_heap.paragraph_format.first_line_indent = Inches(0)
    p_img_heap.add_run().add_picture("NopBai/hinh_moi/so_do_minheap_pos.png", width=Inches(5.8))
    add_caption_figure(doc, "Hình 3.1. Sơ đồ cơ chế quản lý con trỏ và mảng định vị vị trí hai chiều trong IndexedMinHeap")

    add_body_paragraph(doc, "Lớp CustomStack (trong file src/cautruc/stack.py) và CustomQueue (trong file src/cautruc/queue_.py) cung cấp các thao tác cơ bản phục vụ điều hướng. CustomStack cài đặt push, pop và to_list() trong O(1) mỗi thao tác, dùng để đảo chiều mảng dấu vết prev[] nhằm phục hồi đường đi từ điểm xuất phát tới điểm đích. CustomQueue sử dụng kỹ thuật mảng hai con trỏ quản lý chỉ số head trong O(1) thời gian trích xuất, phục vụ thuật toán duyệt theo chiều rộng BFS kiểm tra tính liên thông của mạng lưới đường bộ.")

    # 3.2
    add_heading_2(doc, "3.2. Cấu trúc đồ thị CityMapGraph")
    add_body_paragraph(doc, "Lớp CityMapGraph (trong file src/cautruc/graph.py) là trung tâm biểu diễn mạng lưới giao thông đô thị. Mỗi tuyến đường đi ra từ một nút được đóng gói trong một đối tượng AdjListNode gồm chỉ số đích target_idx, trọng số cơ sở base_weight, hệ số kẹt xe traffic_factor, cờ báo một chiều is_oneway và con trỏ next liên kết tới cung tiếp theo. Phương thức get_effective_weight() trả về tích số giữa trọng số cơ sở và hệ số kẹt xe.")
    add_body_paragraph(doc, "Lớp CityMapGraph duy trì danh sách tên đỉnh self.node_names, danh sách tọa độ phẳng self.node_coords lưu cặp (x, y) bằng ki-lô-mét, bảng băm tra cứu self.node_lookup và mảng danh sách kề self.adj. Phương thức add_node(name, x, y) đăng ký đỉnh mới hoặc cập nhật tọa độ hình học nếu đỉnh đã tồn tại. Phương thức add_edge(u_name, v_name, base_weight, traffic_factor, is_oneway) kiểm tra tính hợp lệ của trọng số cơ sở (từ chối trọng số âm), thêm cung thuận e = (u, v) và tự động thêm cung nghịch e = (v, u) nếu cung là đường hai chiều.")
    add_body_paragraph(doc, "Phương thức update_traffic(u_name, v_name, traffic_factor) tiếp nhận hệ số kẹt xe k, kiểm tra điều kiện k >= 1.0 và cập nhật hệ số trên cung đường tương ứng. Phương thức compute_admissible_h_scale() quét qua toàn bộ các cung trên đồ thị để tính tỷ số nhỏ nhất giữa trọng số cơ sở và khoảng cách Euclid, đảm bảo tính admissible tuyệt đối cho hàm heuristic của thuật toán A*.")

    # 3.3
    add_heading_2(doc, "3.3. Cài đặt thuật toán Dijkstra và A*")
    add_body_paragraph(doc, "Hàm dijkstra_shortest_path (trong file src/thuattoan/dijkstra.py) tiếp nhận đối tượng CityMapGraph cùng tên đỉnh xuất phát và đỉnh đích tùy chọn. Hàm khởi tạo mảng dist[] bằng vô cực, dist[start_idx] = 0 và đưa (0, start_idx) vào IndexedMinHeap. Vòng lặp chính liên tục rút đỉnh u có khoảng cách nhỏ nhất, kiểm tra cờ visited[u] để tránh duyệt lặp, và dừng sớm ngay khi u trùng với end_idx. Quá trình nới lỏng duyệt danh sách liên kết của đỉnh u, tính new_dist = dist[u] + w_eff, cập nhật mảng dist[v], mảng prev[v] và gọi decrease_key hoặc insert trên heap. Kết quả trả về được đóng gói chuẩn hóa trong đối tượng KetQuaTimDuong.")

    # Flowchart Dijkstra
    p_img_dijk = doc.add_paragraph()
    p_img_dijk.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img_dijk.paragraph_format.first_line_indent = Inches(0)
    p_img_dijk.add_run().add_picture("NopBai/hinh_moi/luu_do_dijkstra.png", width=Inches(5.0))
    add_caption_figure(doc, "Hình 3.2. Lưu đồ giải thuật tìm đường đi ngắn nhất Dijkstra có cơ chế dừng sớm khi gặp đích")

    add_body_paragraph(doc, "Hàm astar_shortest_path (trong file src/thuattoan/astar.py) thực hiện tìm đường có định hướng bằng hàm heuristic Euclid. Hàm tự động gọi dothi.compute_admissible_h_scale() để xác định hệ số co giãn an toàn h_scale trước khi khởi tạo hàm đánh giá heuristic. Hai mảng g_score[] và f_score[] được quản lý song song, trong đó f_score[v] = g_score[v] + h(v) được dùng làm khóa sắp xếp trong IndexedMinHeap. Khi duyệt cung (u, v), nếu chi phí tạm thời tent_g = g_score[u] + w_eff nhỏ hơn g_score[v], thuật toán cập nhật g_score[v], tính lại f_score[v] và kích hoạt decrease_key trên heap.")

    # Flowchart A*
    p_img_astar = doc.add_paragraph()
    p_img_astar.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img_astar.paragraph_format.first_line_indent = Inches(0)
    p_img_astar.add_run().add_picture("NopBai/hinh_moi/luu_do_astar.png", width=Inches(5.0))
    add_caption_figure(doc, "Hình 3.3. Lưu đồ giải thuật tìm kiếm tối ưu A* kết hợp hàm Heuristic Euclid Admissible")

    # 3.4
    add_heading_2(doc, "3.4. Xử lý các trường hợp biên và điều kiện bất thường")
    add_body_paragraph(doc, "Hệ thống được thiết kế phòng thủ chặt chẽ nhằm xử lý an toàn mọi tình huống biên có thể phát sinh trong quá trình vận hành thực tế. Đối với trường hợp điểm bắt đầu trùng điểm kết thúc (start == end), cả Dijkstra và A* đều phát hiện tức thời tại khâu kiểm tra đầu vào, trả về lộ trình gồm duy nhất một đỉnh với tổng chi phí bằng 0.0, số đỉnh duyệt bằng 1 và số thao tác heap bằng 1 mà không cần kích hoạt vòng lặp chính. Đối với trường hợp truy vấn đỉnh không tồn tại, hàm tra cứu bảng băm trả về None và hệ thống phát sinh thông báo lỗi rõ ràng, trả về KetQuaTimDuong với cờ success = False mà không gây sập chương trình.")
    add_body_paragraph(doc, "Đối với trường hợp đồ thị mất liên thông khi không tồn tại bất kỳ đường đi nào kết nối từ điểm xuất phát đến điểm đích, giá trị khoảng cách tại đích dist[end_idx] vẫn giữ nguyên giá trị vô cực sau khi hàng đợi ưu tiên đã vét cạn toàn bộ thành phần liên thông chứa đỉnh nguồn. Khi đó hệ thống phát hiện dist == inf và trả về thông báo an toàn báo hiệu hai địa điểm không thể kết nối. Đối với các dữ liệu đầu vào không hợp lệ như thêm cạnh có trọng số âm hoặc cập nhật hệ số kẹt xe k < 1.0, các hàm kiểm soát add_edge và update_traffic lập tức từ chối và gửi thông điệp cảnh báo, bảo toàn trọn vẹn mô hình vật lý và tính đúng đắn toán học của hệ thống.")

print("Chapter 3 builder defined.")
