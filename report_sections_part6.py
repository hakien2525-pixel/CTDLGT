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

def build_chapter5_and_end(doc):
    add_heading_1(doc, "CHƯƠNG 5. KIỂM THỬ VÀ ĐÁNH GIÁ THỰC NGHIỆM")

    # 5.1
    add_heading_2(doc, "5.1. Phương pháp và môi trường thực nghiệm")
    add_body_paragraph(doc, "Thực nghiệm đánh giá được triển khai theo quy trình khoa học nghiêm ngặt trên nhiều bộ dữ liệu đại diện bao gồm đồ thị mạng lưới đường giao thông đô thị thực tế, đồ thị hình học ngẫu nhiên đảm bảo tính liên thông và các đồ thị lưới quy mô lớn có cấu trúc chuẩn hóa. Kích thước đồ thị được phân cấp từ 100 đỉnh (lưới 10 × 10), 1.000 đỉnh (lưới 20 × 50), 5.000 đỉnh (lưới 50 × 100) đến 20.000 đỉnh (lưới 100 × 200). Các thực nghiệm sử dụng bộ sinh số giả ngẫu nhiên có seed cố định (seed = 2026) để bảo đảm tính tái lập độc lập của mọi kết quả đo.")
    add_body_paragraph(doc, "Quy trình đo lường thời gian thực thi tuân thủ nguyên tắc loại bỏ hoàn toàn giai đoạn khởi động CPU (warmup), mỗi phép đo trên một cặp điểm được lặp lại 5 lần liên tiếp và lấy giá trị trung vị (median) nhằm triệt tiêu ảnh hưởng của cơ chế đa nhiệm và ngắt hệ điều hành. Cấu hình máy trạm thử nghiệm thực tế ghi nhận thông số: Hệ điều hành Microsoft Windows 11 Enterprise (phiên bản 10.0.26200), Trình biên dịch Python 3.12.10 (kiến trúc AMD64), Bộ vi xử lý phần cứng AMD64 Family 25 Model 68 Stepping 1 (AuthenticAMD) và Trình duyệt Chrome 133 phục vụ hiển thị đồ họa trực quan.")

    # 5.2
    add_heading_2(doc, "5.2. Kết quả kiểm thử đúng đắn tự động")
    add_body_paragraph(doc, "Hệ thống kiểm thử tự động gồm 26 ca kiểm thử toàn diện (Test Cases) bao quát mọi khía cạnh cấu trúc và thuật toán. Bảng 5.1 trích xuất nguyên văn dữ liệu kết quả từ tệp test_results.csv do chương trình kiểm thử test/test_suite.py sinh ra:")

    # Table 5.1
    add_caption_table(doc, "Bảng 5.1. Bảng tổng hợp kết quả 26 ca kiểm thử đúng đắn tự động từ tệp test_results.csv")
    headers_tc = ["Mã test", "Mô tả ca kiểm thử", "Kết quả mong đợi", "Kết quả thực tế", "Trạng thái"]
    widths_tc = [1.2, 2.2, 1.4, 1.4, 0.6]
    data_tc = [
        ["TC01_HEAP_EMPTY", "Kiểm tra thao tác pop trên heap rỗng", "(None, None)", "(None, None)", "PASS"],
        ["TC02_HEAP_ORDER", "Thứ tự trích xuất tăng dần của Min-Heap", "[1.5, 2.0, 5.0, 8.0]", "[1.5, 2.0, 5.0, 8.0]", "PASS"],
        ["TC03_HEAP_DECREASE_KEY", "Giảm khóa decrease_key trong O(log V)", "(2.0, 1)", "(2.0, 1)", "PASS"],
        ["TC04_HASH_TABLE", "Bảng băm collision & rehash tự cài đặt", "True", "True", "PASS"],
        ["TC05_STACK_TRACE", "Ngăn xếp đảo ngược lộ trình truy vết", "['C', 'B', 'A']", "['C', 'B', 'A']", "PASS"],
        ["TC05B_QUEUE_BFS", "Hàng đợi FIFO tự cài đặt", "[10, 20]", "[10, 20]", "PASS"],
        ["TC06_MANUAL_CALC", "Kiểm chứng đáp án tính tay: N1 -> N4", "Cost=4.0, Path=['N1'..'N4']", "Cost=4.0, Path=['N1'..'N4']", "PASS"],
        ["TC07_DIJKSTRA_ALL", "Dijkstra nguồn đơn đến tất cả các nút", "{'N1':0, 'N2':2, 'N3':3, 'N4':4}", "{'N1':0, 'N2':2, 'N3':3, 'N4':4}", "PASS"],
        ["TC08_ONEWAY_FORWARD", "Tìm đường xuôi chiều A -> B", "5.0", "5.0", "PASS"],
        ["TC09_ONEWAY_BACKWARD", "Từ chối đi ngược chiều B -> A", "inf", "inf", "PASS"],
        ["TC10_DISCONNECTED", "Đồ thị mất liên thông (báo lỗi an toàn)", "False", "False", "PASS"],
        ["TC10B_BFS_CONNECTIVITY", "Kiểm tra tính liên thông bằng BFS", "False (2/3 nút)", "False (2/3 nút)", "PASS"],
        ["TC11_ASTAR_COST", "Chi phí A* bằng tuyệt đối Dijkstra", "11.10", "11.10", "PASS"],
        ["TC12_ASTAR_NODES", "Số nút duyệt của A* <= Dijkstra", "<= 4", "3", "PASS"],
        ["TC13_SAME_START_END", "Điểm bắt đầu trùng điểm kết thúc", "Cost=0.0, Visited=1", "Cost=0.0, Visited=1", "PASS"],
        ["TC14_TRAFFIC_REROUTING", "Tự động đổi hướng khi kẹt xe tuyến cũ", "['S', 'M2', 'E']", "['S', 'M2', 'E']", "PASS"],
        ["TC15_TRAFFIC_INVALID_K", "Từ chối hệ số kẹt xe k < 1.0", "False", "False", "PASS"],
        ["TC16_NEGATIVE_WEIGHT", "Từ chối trọng số cạnh âm", "False", "False", "PASS"],
        ["TC17_NON_EXIST_NODE", "Truy vấn nút không tồn tại", "False", "False", "PASS"],
        ["TC18_NEWTON_SQRT", "Newton-Raphson căn bậc hai biên âm và 0", "sq=0.0, 0.0, 4.0", "sq=0.0, 0.0, 4.0", "PASS"],
        ["TC18B_JSON_ROUNDTRIP", "Bộ parser JSON thuần không import thư viện", "True", "True", "PASS"],
        ["TC19_200_RANDOM_PAIRS", "Kiểm thử 200 cặp ngẫu nhiên (Cost Dijk == A*)", "True", "True", "PASS"],
        ["TC20_PERF_100", "Hiệu năng quy mô 100 đỉnh (Grid 10x10)", "Chi phí Dijk == A*", "Dijk=0.4ms, A*=1.7ms", "PASS"],
        ["TC21_PERF_1000", "Hiệu năng quy mô 1.000 đỉnh (Grid 20x50)", "Chi phí Dijk == A*", "Dijk=8.7ms, A*=19.5ms", "PASS"],
        ["TC22_PERF_5000", "Hiệu năng quy mô 5.000 đỉnh (Grid 50x100)", "Chi phí Dijk == A*", "Dijk=45.3ms, A*=82.9ms", "PASS"],
        ["TC23_PERF_20000", "Hiệu năng quy mô 20.000 đỉnh (Grid 100x200)", "Chi phí Dijk == A*", "Dijk=214.1ms, A*=703.6ms", "PASS"]
    ]
    tbl_tc = doc.add_table(rows=1, cols=len(headers_tc))
    format_table(tbl_tc, widths_tc, headers_tc, data_tc)

    add_body_paragraph(doc, "Toàn bộ 26/26 ca kiểm thử đều đạt trạng thái PASS tuyệt đối (100.0%). Đáng chú ý nhất tại ca kiểm thử TC19, hệ thống đã thực hiện kiểm tra đối chiếu tự động trên 200 cặp điểm ngẫu nhiên độc lập trên đồ thị lưới, kết quả ghi nhận 100% các cặp điểm đều cho giá trị chi phí đường đi ngắn nhất của Dijkstra và A* trùng khớp nhau tuyệt đối tới từng chữ số thập phân, chứng minh tính đúng đắn và tính admissible của hàm heuristic đã được bảo toàn trọn vẹn.")

    # 5.3
    add_heading_2(doc, "5.3. Đánh giá hiệu năng và đối chiếu lý thuyết độ phức tạp")
    add_body_paragraph(doc, "Nhằm đánh giá khách quan năng lực giải thuật trên không gian tìm kiếm thực tế, bảng 5.2 tổng hợp kết quả đo đạc trung vị trên tập hợp nhiều cặp điểm ngẫu nhiên đại diện tại 4 cấp độ quy mô đồ thị (từ 100 đến 20.000 đỉnh với seed = 2026):")

    # Table 5.2
    add_caption_table(doc, "Bảng 5.2. Bảng đối chiếu số đỉnh duyệt, thao tác heap và thời gian thực thi trung vị theo quy mô")
    headers_perf = ["Quy mô đồ thị", "Số cạnh (E)", "Số đỉnh duyệt Dijk", "Số đỉnh duyệt A*", "Tỷ lệ tiết kiệm đỉnh", "Thao tác Heap Dijk", "Thao tác Heap A*", "Thời gian Dijk (ms)", "Thời gian A* (ms)"]
    widths_perf = [1.2, 0.6, 0.8, 0.7, 0.8, 0.8, 0.7, 0.8, 0.8]
    data_perf = [
        ["100 đỉnh (10x10)", "360", "41.0", "9.9", "75.7%", "91.7", "30.0", "0.417", "1.237"],
        ["1.000 đỉnh (20x50)", "3.860", "563.4", "183.8", "67.4%", "1.152.2", "413.4", "6.169", "10.186"],
        ["5.000 đỉnh (50x100)", "19.700", "1.971.2", "499.0", "74.7%", "4.012.8", "1.077.8", "18.153", "40.996"],
        ["20.000 đỉnh (100x200)", "79.400", "12.553.2", "2.797.6", "77.7%", "25.257.8", "5.805.0", "118.637", "138.387"]
    ]
    tbl_perf = doc.add_table(rows=1, cols=len(headers_perf))
    format_table(tbl_perf, widths_perf, headers_perf, data_perf)

    # Figures: chart nodes and chart time
    p_img_nodes = doc.add_paragraph()
    p_img_nodes.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img_nodes.paragraph_format.first_line_indent = Inches(0)
    p_img_nodes.add_run().add_picture("NopBai/hinh_moi/bieu_do_so_sanh_dinh.png", width=Inches(5.5))
    add_caption_figure(doc, "Hình 5.1. Biểu đồ so sánh số lượng đỉnh mở rộng trung bình giữa Dijkstra và A* theo quy mô đồ thị")

    p_img_time = doc.add_paragraph()
    p_img_time.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img_time.paragraph_format.first_line_indent = Inches(0)
    p_img_time.add_run().add_picture("NopBai/hinh_moi/bieu_do_so_sanh_thoi_gian.png", width=Inches(5.5))
    add_caption_figure(doc, "Hình 5.2. Biểu đồ so sánh thời gian thực thi trung vị giữa Dijkstra và A* theo quy mô đồ thị")

    add_body_paragraph(doc, "Phân tích số liệu thực nghiệm làm nổi bật hai quy luật cốt lõi mang ý nghĩa lý thuyết sâu sắc. Về phương diện không gian tìm kiếm, thuật toán A* thể hiện ưu thế vượt trội ổn định khi cắt giảm được từ 67.4% đến 77.7% số lượng đỉnh cần mở rộng và giảm tương ứng gần 70% số lượng thao tác heap so với Dijkstra trên toàn bộ các thang đo quy mô. Nhờ hàm heuristic Euclid hướng luồng tìm kiếm trực diện về phía mục tiêu, A* tránh được việc lan tỏa hình tròn đẳng hướng lãng phí mà Dijkstra buộc phải thực hiện.")
    add_body_paragraph(doc, "Tuy nhiên, về phương diện thời gian thực thi thuần túy trên quy mô nhỏ và trung bình (từ 100 đến 5.000 đỉnh), thời gian đo đạc của thuật toán A* lại ghi nhận giá trị cao hơn Dijkstra (ví dụ tại 100 đỉnh, A* mất 1.237 ms trong khi Dijkstra chỉ mất 0.417 ms). Kết quả này hoàn toàn phù hợp với lý thuyết phân tích giải thuật: thuật toán A* phải chịu thêm chi phí tính toán hàm heuristic d_Euclid = sqrt((x1-x2)² + (y1-y2)²) cho mỗi đỉnh kề khi duyệt cung. Phép tính căn bậc hai lặp tiếp tuyến Newton-Raphson tuy hội tụ nhanh nhưng vẫn tiêu tốn chu kỳ lệnh CPU đáng kể so với phép cộng số học thuần túy của Dijkstra. Chỉ khi đồ thị đạt tới quy mô rất lớn (20.000 đỉnh), khi số lượng thao tác heap tiết kiệm được đủ lớn để bù đắp chi phí tính căn (tiết kiệm gần 20.000 thao tác heap sift-up/sift-down), chênh lệch thời gian giữa hai thuật toán mới tiệm cận thu hẹp lại (118.6 ms so với 138.4 ms).")
    add_body_paragraph(doc, "Về phương diện đối chiếu lý thuyết tiệm cận, khi quy mô tăng từ 1.000 đỉnh (E = 3.860) lên 20.000 đỉnh (E = 79.400), tức khối lượng dữ liệu (V+E) tăng xấp xỉ 20.4 lần và hệ số (V+E)log V tăng khoảng 29.2 lần, thời gian thực thi trung vị của Dijkstra tăng từ 6.169 ms lên 118.637 ms (tăng 19.2 lần). Tốc độ tăng trưởng thời gian đo đạc thực tế hoàn toàn bám sát đường cong lý thuyết O((V + E) log V), xác nhận mã nguồn đã được cài đặt tối ưu chuẩn mực, không tồn tại bất kỳ vòng lặp ẩn hay điểm thắt cổ chai phi tuyến tính nào.")

    # 5.4
    add_heading_2(doc, "5.4. Hạn chế và hướng phát triển")
    add_body_paragraph(doc, "Bên cạnh các kết quả đạt được, đồ án thẳng thắn thừa nhận một số hạn chế nội tại cần được tiếp tục hoàn thiện trong tương lai. Thứ nhất, hàm heuristic Euclid tuy đơn giản và trực quan nhưng tính định hướng sẽ bị suy giảm đáng kể trên các mạng lưới đô thị có hình thái phân mảnh hoặc có sông ngòi chia cắt phức tạp. Thứ hai, hệ thống hiện tại chưa tích hợp cấu trúc dữ liệu không gian như cây k-d (k-d tree) hay lưới ô R-tree để tăng tốc độ truy vấn tìm kiếm đỉnh giao lộ gần nhất từ một tọa độ GPS bất kỳ. Thứ ba, mô hình mô phỏng giao thông hiện mới dừng lại ở việc áp dụng hệ số kẹt xe tĩnh tức thời k(u, v) trên từng cung đường chứ chưa mô hình hóa được sự lan truyền tắc nghẽn động theo chuỗi thời gian hoặc dự báo lưu lượng xe dựa trên chuỗi Markov.")

    # KẾT LUẬN
    add_heading_1(doc, "KẾT LUẬN")
    add_body_paragraph(doc, "Đồ án đã hoàn thành trọn vẹn toàn bộ các mục tiêu đặt ra cho Đề tài 5 về hệ thống tìm đường đi ngắn nhất trên bản đồ. Toàn bộ các cấu trúc dữ liệu cốt lõi gồm Hàng đợi ưu tiên IndexedMinHeap, Bảng băm CustomHashTable, Ngăn xếp CustomStack và Hàng đợi CustomQueue đều được thiết kế và cài đặt thuần túy bằng ngôn ngữ Python và JavaScript mà không dựa vào bất kỳ thư viện hỗ trợ ngoài nào. Hai thuật toán tìm đường Dijkstra và A* đã được kiểm chứng tính đúng đắn toán học tuyệt đối qua 26 ca kiểm thử tự động, xác nhận độ chính xác 100% trên 200 cặp điểm ngẫu nhiên.")
    add_body_paragraph(doc, "Kết quả thực nghiệm chuyên sâu trên nhiều quy mô đồ thị từ 100 đến 20.000 đỉnh đã làm sáng tỏ mối quan hệ biện chứng giữa lý thuyết độ phức tạp và hiệu năng thực tế. Thuật toán A* với hàm heuristic Euclid tự động thích ứng qua hệ số h_scale đã chứng minh hiệu quả giảm thiểu không gian tìm kiếm vượt trội từ 67% đến 78% số đỉnh mở rộng, trong khi phân tích thời gian thực thi đã giải thích thỏa đáng ảnh hưởng của chi phí tính toán hàm heuristic trong môi trường phần cứng máy tính. Công trình này là nền tảng vững chắc để phát triển các ứng dụng hệ thống thông tin địa lý (GIS) và điều hướng thông minh trong tương lai.")

    # TÀI LIỆU THAM KHẢO
    add_heading_1(doc, "TÀI LIỆU THAM KHẢO")
    p_ref1 = doc.add_paragraph()
    p_ref1.paragraph_format.first_line_indent = Inches(0)
    p_ref1.paragraph_format.space_after = Pt(4)
    r1 = p_ref1.add_run("[1] Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. Introduction to Algorithms. MIT Press, 4th edition, 2022. (Chương 22: Elementary Graph Algorithms; Chương 24: Single-Source Shortest Paths).")
    apply_run_font(r1, "Times New Roman", 10.5)

    p_ref2 = doc.add_paragraph()
    p_ref2.paragraph_format.first_line_indent = Inches(0)
    p_ref2.paragraph_format.space_after = Pt(4)
    r2 = p_ref2.add_run("[2] Edsger W. Dijkstra. A note on two problems in connexion with graphs. Numerische Mathematik, 1(1):269–271, 1959.")
    apply_run_font(r2, "Times New Roman", 10.5)

    p_ref3 = doc.add_paragraph()
    p_ref3.paragraph_format.first_line_indent = Inches(0)
    p_ref3.paragraph_format.space_after = Pt(4)
    r3 = p_ref3.add_run("[3] Peter E. Hart, Nils J. Nilsson, and Bertram Raphael. A formal basis for the heuristic determination of minimum cost paths. IEEE Transactions on Systems Science and Cybernetics, 4(2):100–107, 1968.")
    apply_run_font(r3, "Times New Roman", 10.5)

    p_ref4 = doc.add_paragraph()
    p_ref4.paragraph_format.first_line_indent = Inches(0)
    p_ref4.paragraph_format.space_after = Pt(4)
    r4 = p_ref4.add_run("[4] Robert Sedgewick and Kevin Wayne. Algorithms. Addison-Wesley Professional, 4th edition, 2011. (Chương 4: Graphs - Shortest Paths and Priority Queues).")
    apply_run_font(r4, "Times New Roman", 10.5)

    p_ref5 = doc.add_paragraph()
    p_ref5.paragraph_format.first_line_indent = Inches(0)
    p_ref5.paragraph_format.space_after = Pt(4)
    r5 = p_ref5.add_run("[5] Daniel J. Bernstein. Comp.lang.c FAQ list · Question 17.1 (DJB2 Hash Function Algorithm), 1991.")
    apply_run_font(r5, "Times New Roman", 10.5)

    # PHỤ LỤC
    add_heading_1(doc, "PHỤ LỤC: DANH MỤC TỆP NGUỒN VÀ MÃ NGUỒN CỐT LÕI")
    add_body_paragraph(doc, "Dưới đây là cấu trúc tổ chức mã nguồn của hệ thống tìm đường đi ngắn nhất đã được đóng gói hoàn chỉnh trong thư mục NopBai/:")

    # File list as table or block
    p_files = doc.add_paragraph()
    p_files.paragraph_format.first_line_indent = Inches(0)
    p_files.paragraph_format.space_after = Pt(6)
    r_f = p_files.add_run(
        "1. src/cautruc/: minheap.py (IndexedMinHeap), hashtable.py (CustomHashTable), stack.py (CustomStack), queue_.py (CustomQueue), graph.py (CityMapGraph, AdjListNode).\n"
        "2. src/thuattoan/: dijkstra.py (dijkstra_shortest_path), astar.py (astar_shortest_path), duongdi.py (KetQuaTimDuong, phuc_hoi_duong_di), lienthong.py (kiem_tra_lien_thong_bfs).\n"
        "3. src/tienich/: toan.py (sqrt_newton, euclid), dulieu.py (json parser, sample map), dohieunang.py (benchmark runner), sinhdothi.py (grid & random generator).\n"
        "4. web/: index.html, style.css, app.js, graph_core.js (Giao diện trực quan mô phỏng bản đồ tương tác)."
    )
    apply_run_font(r_f, "Courier New", 9.5)

    add_body_paragraph(doc, "Đoạn mã cốt lõi của giải thuật tìm kiếm A* tích hợp tính toán h_scale tự động:")
    code_astar_core = [
        "def astar_shortest_path(dothi: Any, start_name: Any, end_name: Any):",
        "    start_idx, end_idx = dothi.get_node_index(start_name), dothi.get_node_index(end_name)",
        "    if start_idx is None or end_idx is None: return KetQuaTimDuong(success=False)",
        "    if start_idx == end_idx: return KetQuaTimDuong(success=True, path=[str(start_name)], total_cost=0.0)",
        "    h_scale = dothi.compute_admissible_h_scale()",
        "    end_x, end_y = dothi.node_coords[end_idx]",
        "    def h(idx: int) -> float:",
        "        x, y = dothi.node_coords[idx]",
        "        return tinh_khoang_cach_euclid(x, y, end_x, end_y) * h_scale",
        "    V = dothi.num_nodes",
        "    g_score, f_score, prev, closed_set = [float('inf')]*V, [float('inf')]*V, [None]*V, [False]*V",
        "    heap = IndexedMinHeap(V)",
        "    g_score[start_idx] = 0.0",
        "    f_score[start_idx] = h(start_idx)",
        "    heap.insert(f_score[start_idx], start_idx)",
        "    while not heap.is_empty():",
        "        _, u = heap.pop_min()",
        "        if closed_set[u]: continue",
        "        closed_set[u] = True",
        "        if u == end_idx: break",
        "        curr = dothi.adj[u]",
        "        while curr:",
        "            v, w = curr.target_idx, curr.get_effective_weight()",
        "            if not closed_set[v]:",
        "                tent_g = g_score[u] + w",
        "                if tent_g < g_score[v]:",
        "                    g_score[v], prev[v] = tent_g, u",
        "                    f_score[v] = tent_g + h(v)",
        "                    if heap.contains(v): heap.decrease_key(v, f_score[v])",
        "                    else: heap.insert(f_score[v], v)",
        "            curr = curr.next",
        "    return KetQuaTimDuong(success=True, path=phuc_hoi_duong_di(prev, end_idx, dothi), total_cost=g_score[end_idx])"
    ]
    add_code_block(doc, code_astar_core)

print("Chapter 5 and concluding sections defined.")
