import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
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

def build_chapter2(doc):
    add_heading_1(doc, "CHƯƠNG 2. CƠ SỞ LÝ THUYẾT THUẬT TOÁN")

    # 2.1
    add_heading_2(doc, "2.1. Đồ thị và cách biểu diễn")
    add_body_paragraph(doc, "Trong lý thuyết đồ thị và khoa học máy tính, hai phương pháp biểu diễn đồ thị phổ biến nhất là ma trận kề (adjacency matrix) và danh sách kề (adjacency list). Ma trận kề sử dụng một mảng hai chiều kích thước V × V, trong đó phần tử tại vị trí hàng u và cột v lưu trữ trọng số của cung nối từ u đến v, hoặc nhận giá trị vô cùng nếu không tồn tại cạnh nối trực tiếp. Phương pháp này có ưu điểm cho phép kiểm tra sự tồn tại của một cung bất kỳ trong thời gian hằng số O(1), song nhược điểm chí mạng là đòi hỏi không gian bộ nhớ cố định O(V²), bất kể số lượng cạnh thực tế nhiều hay ít.")
    add_body_paragraph(doc, "Ngược lại, danh sách kề biểu diễn đồ thị bằng một mảng gồm V phần tử, trong đó mỗi phần tử chứa con trỏ trỏ đến đầu một danh sách liên kết đơn lưu trữ tập hợp các đỉnh kề trực tiếp cùng thuộc tính trọng số tương ứng. Tổng bộ nhớ tiêu thụ của danh sách kề chỉ tỷ lệ thuận với số lượng đỉnh và số lượng cung thực tế là O(V + E). Trong các mạng lưới giao thông đường bộ đô thị, đồ thị luôn mang bản chất thưa rõ rệt khi mỗi nút giao thông thông thường chỉ kết nối từ 2 đến 4 tuyến đường rẽ, dẫn đến số cạnh xấp xỉ tuyến tính với số đỉnh E xấp xỉ k·V với k <= 4. Với quy mô 20.000 đỉnh, ma trận kề đòi hỏi bảng 400 triệu ô nhớ gây lãng phí nghiêm trọng, trong khi danh sách kề chỉ yêu cầu khoảng 100.000 phần tử liên kết, do đó danh sách kề là sự lựa chọn tối ưu tuyệt đối cho đồ án.")

    # 2.2
    add_heading_2(doc, "2.2. Hàng đợi ưu tiên và Min-Heap")
    add_body_paragraph(doc, "Hàng đợi ưu tiên (priority queue) là cấu trúc dữ liệu trừu tượng quản lý tập hợp các phần tử có gắn kèm khóa độ ưu tiên, hỗ trợ trích xuất phần tử có khóa nhỏ nhất một cách hiệu quả. Min-Heap là một hiện thực kinh điển của hàng đợi ưu tiên dưới dạng cây nhị phân gần đầy đủ (nearly complete binary tree), thỏa mãn tính chất đống: khóa của mỗi nút cha luôn nhỏ hơn hoặc bằng khóa của hai nút con tương ứng. Cấu trúc này được lưu trữ liên tục trên một mảng một chiều tuyến tính mà không cần cấp phát con trỏ động, giúp tiết kiệm bộ nhớ và tối ưu hóa bộ nhớ đệm CPU.")
    add_body_paragraph(doc, "Với quy ước chỉ số mảng bắt đầu từ 0, mối quan hệ phân cấp giữa chỉ số nút cha và các nút con được xác định hoàn toàn thông qua các công thức số học nguyên:")

    # Eq 2, 3, 4
    eq_parent = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>parent(i) = </m:t></m:r>'
        r'<m:d><m:dPr><m:begChr m:val="⌊"/><m:endChr m:val="⌋"/></m:dPr><m:e>'
        r'<m:f><m:fPr/><m:num><m:r><m:t>i - 1</m:t></m:r></m:num><m:den><m:r><m:t>2</m:t></m:r></m:den></m:f>'
        r'</m:e></m:d>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_parent, "(2)")

    eq_left = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>left_child(i) = 2i + 1</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_left, "(3)")

    eq_right = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>right_child(i) = 2i + 2</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_right, "(4)")

    add_body_paragraph(doc, "Thao tác chèn một phần tử mới insert(priority, item) được thực hiện bằng cách bổ sung phần tử vào cuối mảng rồi kích hoạt thủ tục vun lên sift-up. Thao tác trích xuất đỉnh nhỏ nhất pop_min() lấy phần tử gốc tại chỉ số 0, đưa phần tử cuối cùng lên thay thế gốc và kích hoạt thủ tục vun xuống sift-down để tái lập bất biến đống. Vì cây nhị phân gần đầy đủ chứa n phần tử có chiều cao h được chặn trên bởi h = floor(log2(n)), số lượng phép tráo đổi nút trong quá trình vun lên hoặc vun xuống dọc theo một đường đi từ gốc tới lá không bao giờ vượt quá chiều cao cây, chứng minh độ phức tạp thời gian của cả hai thao tác đều đạt O(log n).")
    add_body_paragraph(doc, "Trong thuật toán tìm đường đi ngắn nhất, khi một tuyến đường tốt hơn tới đỉnh v được phát hiện, ta cần cập nhật giảm khoảng cách của đỉnh v trong hàng đợi ưu tiên, thao tác này được gọi là decrease-key. Nếu sử dụng heap tiêu chuẩn, việc định vị đỉnh v trong heap đòi hỏi quét tuyến tính toàn bộ mảng mất thời gian O(n), làm suy thoái độ phức tạp của thuật toán Dijkstra lên O(V²). Để giải quyết triệt để vấn đề này, đề tài cài đặt IndexedMinHeap tích hợp một mảng vị trí pos[] kích thước V, trong đó pos[v] lưu trữ chính xác chỉ số vị trí hiện tại của đỉnh v trong mảng heap, cho phép tra cứu tọa độ đỉnh trong O(1) và thực hiện vun lên sift-up trong O(log V). Cách tiếp cận này vượt trội hoàn toàn so với kỹ thuật chèn trùng nút (lazy deletion) vốn làm kích thước heap phình to lên O(E) phần tử và tiêu tốn thêm thời gian xử lý các bản ghi rác.")

    # 2.3
    add_heading_2(doc, "2.3. Thuật toán Dijkstra")
    add_body_paragraph(doc, "Thuật toán Dijkstra do nhà khoa học máy tính Edsger W. Dijkstra đề xuất năm 1959 là thuật toán tham lam kinh điển giải quyết bài toán đường đi ngắn nhất từ một nguồn đơn trên đồ thị có trọng số không âm. Thuật toán duy trì một mảng khoảng cách ước lượng dist[v] cho mọi đỉnh v, khởi tạo dist[s] = 0 cho đỉnh xuất phát s và dist[v] = vô cực cho tất cả các đỉnh còn lại. Tại mỗi bước lặp, thuật toán trích xuất đỉnh u có giá trị dist[u] nhỏ nhất trong số các đỉnh chưa hoàn tất, chốt đỉnh u là tối ưu, sau đó thực hiện thao tác nới lỏng (relaxation) trên tất cả các cung đi ra (u, v) theo công thức toán học:")

    # Eq (5)
    eq_relax = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>dist[v] ← min(dist[v], dist[u] + w</m:t></m:r>'
        r'<m:sSub><m:sSubPr/><m:e><m:r><m:t>eff</m:t></m:r></m:e><m:sub><m:r><m:t>(u,v)</m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t>)</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_relax, "(5)")

    add_body_paragraph(doc, "Tính đúng đắn của thuật toán Dijkstra được chứng minh chặt chẽ bằng phương pháp quy nạp toán học dựa trên bất biến vòng lặp: tại thời điểm một đỉnh u bất kỳ được trích xuất ra khỏi hàng đợi ưu tiên, giá trị dist[u] đã đạt tới khoảng cách ngắn nhất tuyệt đối delta(s, u). Cơ sở quy nạp đúng tại bước khởi tạo khi đỉnh s được lấy ra đầu tiên với dist[s] = 0. Giả sử bất biến đúng cho tập hợp các đỉnh đã chốt S. Khi chọn đỉnh kế tiếp u không thuộc S có dist[u] nhỏ nhất, giả sử phản chứng tồn tại một đường đi thực tế P nối s tới u có tổng chiều dài ngắn hơn dist[u]. Khi đó đường đi P phải rời tập S tại một cung nào đó (x, y) với x thuộc S và y chưa thuộc S. Vì x đã được chốt tối ưu và đã nới lỏng cạnh (x, y), ta có dist[y] <= chiều dài đoạn đường từ s đến y trên P. Do trọng số mọi cung đều không âm, chiều dài từ s đến y không vượt quá chiều dài toàn bộ đường đi P, dẫn tới dist[y] <= length(P) < dist[u]. Tuy nhiên điều này mâu thuẫn trực tiếp với quy tắc chọn đỉnh tham lam rằng u là đỉnh chưa chốt có dist nhỏ nhất trong hàng đợi ưu tiên, chứng tỏ không thể tồn tại đường đi P nào ngắn hơn dist[u].")
    add_body_paragraph(doc, "Về mặt độ phức tạp tính toán, thuật toán thực hiện chính xác V lần thao tác trích xuất đỉnh pop_min() và nhiều nhất E lần thao tác nới lỏng cạnh dẫn đến thao tác giảm khóa decrease_key() trên IndexedMinHeap. Do mỗi thao tác trên heap nhị phân có chi phí thời gian O(log V), tổng thời gian thực thi của thuật toán đạt mức chặn tiệm cận O((V + E) log V).")
    add_body_paragraph(doc, "Giả thiết trọng số không âm đóng vai trò sinh tử đối với tính đúng đắn của phép chứng minh quy nạp nói trên. Khi xuất hiện cạnh mang trọng số âm, một đường đi vòng qua đỉnh khác có thể tạo ra tổng chi phí nhỏ hơn khoảng cách của đỉnh đã chốt, khiến bất biến bị phá vỡ hoàn toàn. Ví dụ, xét đồ thị ba đỉnh gồm cung (A, B) có trọng số 3, cung (A, C) có trọng số 5 và cung (C, B) có trọng số âm bằng -4. Thuật toán Dijkstra sẽ tham lam chốt đỉnh B ngay từ bước đầu với khoảng cách dist[B] = 3 vì 3 < 5. Tuy nhiên, đường đi thực tế A -> C -> B lại có tổng chi phí bằng 5 + (-4) = 1, nhỏ hơn 3, chứng minh tính đúng đắn bị phá hỏng hoàn toàn khi tồn tại trọng số âm.")

    # 2.4
    add_heading_2(doc, "2.4. Thuật toán A* và tính Admissible của Heuristic")
    add_body_paragraph(doc, "Thuật toán A* do Peter Hart, Nils Nilsson và Bertram Raphael công bố năm 1968 là thuật toán tìm kiếm theo thông tin (informed search) mở rộng từ Dijkstra nhằm định hướng không gian tìm kiếm về phía đỉnh mục tiêu t. Thuật toán đánh giá độ ưu tiên của mỗi đỉnh n thông qua hàm mục tiêu tổng hợp f(n) kết hợp giữa chi phí đã tích lũy và chi phí ước lượng tương lai:")

    # Eq (6)
    eq_fn = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>f(n) = g(n) + h(n)</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_fn, "(6)")

    add_body_paragraph(doc, "Trong đó g(n) biểu diễn chi phí thực tế nhỏ nhất từ đỉnh xuất phát s đến đỉnh n đã tìm được, còn h(n) là hàm heuristic đánh giá khoảng cách ước lượng từ đỉnh n đến đỉnh đích t. Trên bản đồ tọa độ phẳng, hàm heuristic tự nhiên nhất là khoảng cách đường chim bay Euclid giữa hai điểm tọa độ. Khoảng cách Euclid luôn là cận dưới toán học của quãng đường thực tế vì đường thẳng luôn là khoảng cách ngắn nhất giữa hai điểm trong không gian phẳng.")
    add_body_paragraph(doc, "Một hàm heuristic h(n) được gọi là chấp nhận được (admissible) nếu với mọi đỉnh n, giá trị ước lượng h(n) không bao giờ vượt quá khoảng cách ngắn nhất thực tế h*(n) từ n đến đỉnh đích t, tức thỏa mãn:")

    # Eq (7)
    eq_admissible = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>0 ≤ h(n) ≤ h*(n),   ∀n ∈ V</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_admissible, "(7)")

    add_body_paragraph(doc, "Hàm heuristic h(n) được gọi là nhất quán (consistent hay monotone) nếu với mọi cung (u, v) trên đồ thị, giá trị ước lượng thỏa mãn bất đẳng thức tam giác:")

    # Eq (8)
    eq_consistent = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>h(u) ≤ w</m:t></m:r>'
        r'<m:sSub><m:sSubPr/><m:e><m:r><m:t>eff</m:t></m:r></m:e><m:sub><m:r><m:t>(u,v)</m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t> + h(v),   h(t) = 0</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_consistent, "(8)")

    add_body_paragraph(doc, "Khi hàm heuristic thỏa mãn tính nhất quán, giá trị hàm f(n) luôn đơn điệu không giảm dọc theo mọi đường đi hợp lệ. Khi một đỉnh u được trích xuất ra khỏi hàng đợi ưu tiên, giá trị g(u) được đảm bảo đã đạt mức chi phí tối ưu tuyệt đối mà không bao giờ cần phải mở lại (re-open) đỉnh đó, giúp thuật toán A* bảo toàn trọn vẹn kết quả đường đi ngắn nhất hoàn toàn trùng khớp với thuật toán Dijkstra. Bản thân thuật toán Dijkstra thực chất chính là một trường hợp đặc biệt của thuật toán A* khi hàm heuristic h(n) = 0 với mọi đỉnh n.")
    add_body_paragraph(doc, "Trong các hệ thống bản đồ cho phép người dùng tự do chỉnh sửa hoặc nhập trọng số cạnh thủ công, có thể xảy ra trường hợp trọng số cơ sở của một cung nhỏ hơn khoảng cách hình học Euclid giữa hai đầu mút của nó. Nếu giữ nguyên khoảng cách Euclid thuần túy làm hàm đánh giá, hàm heuristic sẽ vượt trần khoảng cách thực tế và đánh mất tính admissible, dẫn đến nguy cơ A* đưa ra lộ trình sai lệch. Để triệt tiêu hoàn toàn rủi ro này, chương trình tự động tính toán một hệ số tỷ lệ co giãn an toàn h_scale theo công thức cực tiểu hóa trên toàn bộ tập cung của đồ thị:")

    # Eq (9)
    eq_h_scale = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>h_scale = max</m:t></m:r>'
        r'<m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>'
        r'<m:r><m:t>0,  min</m:t></m:r>'
        r'<m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>'
        r'<m:r><m:t>1.0,  min</m:t></m:r>'
        r'<m:sSub><m:sSubPr/><m:e><m:r><m:t></m:t></m:r></m:e><m:sub><m:r><m:t>(u,v)∈E, d_E &gt; 0</m:t></m:r></m:sub></m:sSub>'
        r'<m:f><m:fPr/><m:num><m:r><m:t>w(u,v)</m:t></m:r></m:num><m:den><m:r><m:t>d</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>Euclid</m:t></m:r></m:e><m:sub><m:r><m:t>(u,v)</m:t></m:r></m:sub></m:sSub></m:den></m:f>'
        r'</m:e></m:d>'
        r'</m:e></m:d>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_h_scale, "(9)")

    add_body_paragraph(doc, "Nhờ có hệ số h_scale, hàm heuristic h(n) = h_scale × d_Euclid(n, t) luôn được bảo đảm là một cận dưới chặt chẽ của quãng đường thực tế trong mọi tình huống. Tuy nhiên, thuật toán A* không phải lúc nào cũng mang lại lợi thế vượt trội. Trong các đồ thị dạng mê cung có nhiều vật cản hoặc đồ thị có hàm heuristic quá yếu (h_scale xấp xỉ 0), vector hướng đi hình học bị cản trở bởi các ngõ cụt buộc thuật toán phải quay lui liên tục, khi đó số lượng đỉnh duyệt của A* sẽ tương đương với Dijkstra nhưng tổng thời gian chạy thực tế có thể lớn hơn do phải tốn thêm chi phí tính toán căn bậc hai cho mỗi lân cận.")

    # 2.5
    add_heading_2(doc, "2.5. Các cấu trúc phụ trợ và thuật toán số học")
    add_body_paragraph(doc, "Nhằm đảm bảo tôn chỉ không phụ thuộc vào thư viện ngoài, hệ thống đã tự xây dựng ba cấu trúc và giải thuật số học phụ trợ thiết yếu. Cấu trúc thứ nhất là bảng băm CustomHashTable sử dụng hàm băm DJB2 do Daniel J. Bernstein đề xuất kết hợp kỹ thuật giải quyết xung đột bằng phương pháp dò tuyến tính (linear probing). Hàm băm DJB2 khởi tạo giá trị băm h = 5381 và liên tục nhân với 33 kết hợp cộng mã ký tự tiếp theo:")

    # Eq (10)
    eq_djb2 = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>hash</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t> = (hash</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>i-1</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t> × 33 + c</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>i</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t>) mod Capacity</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_djb2, "(10)")

    add_body_paragraph(doc, "Để kiểm soát xung đột khi bảng băm đầy dần, bảng băm tự động giám sát hệ số tải alpha = size / capacity. Khi alpha >= 0.5, hàm _rehash() được kích hoạt để mở rộng kích thước mảng lên capacity mới = 2 × capacity cũ + 1 và băm lại toàn bộ các khóa hiện có. Nhờ kiểm soát hệ số tải dưới ngưỡng 0.5, độ phức tạp trung bình cho các thao tác tra cứu, thêm và kiểm tra tồn tại luôn được duy trì ở mức O(1), trong khi trường hợp xấu nhất khi toàn bộ các khóa rơi vào cùng một chuỗi cụm là O(n).")
    add_body_paragraph(doc, "Cấu trúc thứ hai là ngăn xếp CustomStack hoạt động theo cơ chế Vào sau - Ra trước (LIFO). Ngăn xếp đóng vai trò tối quan trọng trong việc phục hồi đường đi tối ưu: mảng prev[] của thuật toán Dijkstra và A* lưu vết chỉ số đỉnh cha đi trước, do đó quá trình truy vết ngược từ đỉnh đích t về đỉnh xuất phát s sẽ thu được thứ tự các đỉnh bị đảo ngược. Bằng cách đẩy lần lượt các đỉnh vào CustomStack và sau đó rút tuần tự ra danh sách, lộ trình hoàn chỉnh từ điểm xuất phát đến điểm kết thúc được phục hồi chính xác trong độ phức tạp thời gian tuyến tính O(V).")
    add_body_paragraph(doc, "Thuật toán số học thứ ba là phép tính căn bậc hai số thực sqrt_newton phục vụ tính khoảng cách Euclid mà không sử dụng hàm thư viện math.sqrt. Giải thuật áp dụng phương pháp lặp tiếp tuyến Newton-Raphson để giải phương trình f(x) = x² - S = 0 với S là bình phương khoảng cách, thông qua công thức lặp hồi quy:")

    # Eq (11)
    eq_newton = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>x</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>n+1</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t> = </m:t></m:r>'
        r'<m:f><m:fPr/><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>2</m:t></m:r></m:den></m:f>'
        r'<m:d><m:dPr><m:begChr m:val="("/><m:endChr m:val=")"/></m:dPr><m:e>'
        r'<m:r><m:t>x</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>n</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t> + </m:t></m:r>'
        r'<m:f><m:fPr/><m:num><m:r><m:t>S</m:t></m:r></m:num><m:den><m:r><m:t>x</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>n</m:t></m:r></m:e><m:sub><m:r><m:t></m:t></m:r></m:sub></m:sSub></m:den></m:f>'
        r'</m:e></m:d>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_newton, "(11)")

    add_body_paragraph(doc, "Vòng lặp kết thúc khi độ chênh lệch tuyệt đối giữa hai bước lặp liên tiếp đạt ngưỡng dung sai |x_n+1 - x_n| < 10^(-7). Nhờ đặc tính hội tụ bậc hai (quadratic convergence) của phương pháp Newton-Raphson khi số lượng chữ số có nghĩa chính xác tăng gấp đôi sau mỗi bước lặp, thuật toán đạt độ chính xác tương đương kiểu số thực kép chỉ sau khoảng 5 đến 7 phép lặp, đảm bảo tính toán siêu nhanh và tin cậy tuyệt đối.")

print("Chapter 2 builder defined.")
