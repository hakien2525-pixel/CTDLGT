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

def build_intro_and_chapter1(doc):
    # LỜI MỞ ĐẦU
    add_heading_1(doc, "LỜI MỞ ĐẦU")
    add_body_paragraph(doc, "Trong thời đại chuyển đổi số và phát triển đô thị thông minh, nhu cầu tối ưu hóa hành trình di chuyển đóng vai trò then chốt trong việc giảm thiểu tiêu hao nhiên liệu, bảo vệ môi trường và giải tỏa áp lực giao thông đô thị. Bài toán tìm đường đi ngắn nhất trên mạng lưới đường bộ thực tế là một bài toán nền tảng kinh điển của khoa học máy tính, đòi hỏi sự kết hợp chặt chẽ giữa các cấu trúc dữ liệu tiên tiến và các chiến lược giải thuật tối ưu hóa đồ thị.")
    add_body_paragraph(doc, "Mục tiêu trọng tâm của đồ án là thiết kế, cài đặt thuần túy và kiểm chứng thực nghiệm hệ thống tìm đường đi ngắn nhất ứng dụng hai thuật toán nền tảng Dijkstra và A* trên đồ thị có hướng mang trọng số không âm. Toàn bộ hệ thống được xây dựng với nguyên tắc không phụ thuộc vào bất kỳ thư viện ngoài nào đối với các cấu trúc dữ liệu lõi, giúp người học nắm bắt tường tận từ bản chất cấu trúc bộ nhớ, cơ chế quản lý con trỏ, phép toán băm giải quyết xung đột đến kỹ thuật giảm khóa tối ưu trong hàng đợi ưu tiên.")
    add_body_paragraph(doc, "Phạm vi nghiên cứu bao gồm việc mô hình hóa mạng lưới giao thông đô thị dạng đồ thị danh sách kề với tọa độ địa lý chuẩn hóa ki-lô-mét, hỗ trợ các tuyến đường một chiều, hai chiều và mô phỏng hệ số kẹt xe động theo thời gian thực. Bên cạnh đó, đồ án thực hiện đánh giá thực nghiệm toàn diện trên các tập dữ liệu từ bản đồ mẫu đô thị 15 nút đến các đồ thị lưới quy mô lớn đạt ngưỡng 20.000 đỉnh nhằm đối chiếu trực tiếp giữa lý thuyết độ phức tạp tiệm cận và thời gian thực thi đo đạc trên hệ thống phần cứng thực tế.")
    add_body_paragraph(doc, "Bố cục báo cáo được tổ chức thành năm chương chính: Chương 1 trình bày bài toán và mô hình hóa hệ thống; Chương 2 phân tích sâu cơ sở lý thuyết cấu trúc dữ liệu và giải thuật; Chương 3 mô tả kiến trúc thiết kế và giải pháp cài đặt chi tiết kèm mã nguồn; Chương 4 minh họa từng bước chạy thuật toán trên bản đồ thực tế; và Chương 5 tổng kết toàn bộ kiểm thử đúng đắn cùng thực nghiệm benchmark hiệu năng chuyên sâu.")

    # CHƯƠNG 1
    add_heading_1(doc, "CHƯƠNG 1. BÀI TOÁN VÀ MÔ HÌNH HÓA")
    add_body_paragraph(doc, "Bài toán đường đi ngắn nhất trên đồ thị có hướng là bài toán tìm kiếm một chuỗi liên tiếp các cung nối từ đỉnh xuất phát s đến đỉnh đích t sao cho tổng trọng số hiệu dụng tích lũy trên các cung là nhỏ nhất. Trong ngữ cảnh bản đồ giao thông đường bộ, một mạng lưới đường sá được mô hình hóa tự nhiên bằng đồ thị có hướng G = (V, E), trong đó tập đỉnh V biểu diễn tập hợp các giao lộ, bến xe, công viên hoặc các địa điểm trọng yếu, còn tập cung E đại diện cho các tuyến đường kết nối trực tiếp giữa các địa điểm đó. Mỗi cung có hướng e = (u, v) được gán một trọng số cơ sở w(u, v) biểu thị khoảng cách vật lý thực tế được đo lường bằng đơn vị ki-lô-mét.")
    add_body_paragraph(doc, "Để phản ánh chính xác quy hoạch giao thông đô thị hiện đại, hệ thống phân biệt tường minh giữa tuyến đường một chiều và hai chiều. Tuyến đường một chiều từ đỉnh u đến đỉnh v chỉ cho phép phương tiện lưu thông theo chiều thuận e = (u, v), do đó chỉ cung này xuất hiện trong danh sách liên kết kề của đỉnh u mà không có chiều ngược lại. Ngược lại, tuyến đường hai chiều giữa hai đỉnh được mô hình hóa đối xứng bằng hai cung riêng biệt (u, v) và (v, u) có cùng độ dài vật lý cơ sở, cho phép các thuật toán điều hướng dễ dàng xử lý tương thích mà không làm mất tính tổng quát.")
    add_body_paragraph(doc, "Yếu tố biến động giao thông thực tế được trừu tượng hóa thông qua hệ số kẹt xe k >= 1 được gán động cho từng tuyến đường. Khi xảy ra tình trạng ùn tắc tại một đoạn đường cụ thể, trọng số hiệu dụng dùng cho việc tính toán điều hướng được xác định theo nguyên lý tỷ lệ thuận bằng tích số giữa chiều dài cơ sở và hệ số kẹt xe tương ứng:")

    # Equation (1)
    eq_w_eff = (
        r'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        r'<m:r><m:t>w</m:t></m:r><m:sSub><m:sSubPr/><m:e><m:r><m:t>eff</m:t></m:r></m:e><m:sub><m:r><m:t>(u,v)</m:t></m:r></m:sub></m:sSub>'
        r'<m:r><m:t> = w(u,v) × k(u,v),   k(u,v) ≥ 1.0</m:t></m:r>'
        r'</m:oMath>'
    )
    add_equation_numbered(doc, eq_w_eff, "(1)")

    add_body_paragraph(doc, "Hệ số kẹt xe k = 1.0 tương ứng với trạng thái đường thông thoáng lý tưởng khi vận tốc phương tiện đạt mức thiết kế tối đa, trong khi k > 1.0 mô phỏng tình trạng lưu lượng xe tăng cao làm giảm tốc độ hành trình, tương đương với việc gia tăng chi phí thời gian di chuyển trên đoạn đường đó. Giới hạn k >= 1.0 đảm bảo tính nhất quán vật lý vì không có hiện tượng giao thông tự nhiên nào làm thời gian di chuyển giảm xuống dưới ngưỡng vận tốc thiết kế tối đa của cung đường.")
    add_body_paragraph(doc, "Trong mô hình toán học của đề tài, các cạnh mang trọng số âm hoàn toàn bị loại bỏ bởi hai lý do cơ bản. Về mặt vật lý giao thông, quãng đường di chuyển và thời gian tiêu tốn giữa hai địa điểm luôn là các đại lượng thực dương, không thể tồn tại một cung đường mà việc đi qua nó lại làm giảm quãng đường tích lũy trước đó của phương tiện. Về mặt lý thuyết tính toán, sự xuất hiện của cạnh âm sẽ phá vỡ bất biến tham lam nền tảng của thuật toán Dijkstra, đồng thời nếu tồn tại chu trình có tổng trọng số âm thì đường đi ngắn nhất sẽ trở nên không xác định vì phương tiện có thể lặp vô hạn quanh chu trình để chi phí giảm về âm vô cực.")
    add_body_paragraph(doc, "Để đảm bảo đồ án giải quyết trọn vẹn và chuẩn mực yêu cầu học thuật của đề tài, toàn bộ hệ thống được xây dựng nhằm đáp ứng toàn diện năm yêu cầu cốt lõi. Yêu cầu thứ nhất về việc cài đặt thuần cấu trúc dữ liệu không dùng thư viện ngoài được hiện thực hóa bằng việc tự lập trình IndexedMinHeap, CustomHashTable, CustomStack và CustomQueue. Yêu cầu thứ hai về việc cài đặt thuật toán Dijkstra và A* được hiện thực hóa trong hai mô-đun độc lập kèm cơ chế dừng sớm khi chạm đích. Yêu cầu thứ ba về mô phỏng mạng lưới giao thông thực tế được đáp ứng thông qua bản đồ 15 giao lộ có tọa độ hình học, đường một chiều và cập nhật kẹt xe động. Yêu cầu thứ tư về việc xây dựng giao diện trực quan được đáp ứng bằng cả giao diện dòng lệnh phân cấp và ứng dụng web mô phỏng tương tác. Yêu cầu thứ năm về kiểm nghiệm và phân tích hiệu năng được hiện thực hóa bằng bộ kiểm thử tự động 26 ca kiểm thử cùng hệ thống benchmark stress-test đa quy mô từ 100 đến 20.000 đỉnh.")

print("Chapter 1 builder defined.")
