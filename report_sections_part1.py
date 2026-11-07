import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

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

def build_cover_page(doc):
    # Header institution
    p_inst = doc.add_paragraph()
    p_inst.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    p_inst.paragraph_format.first_line_indent = Inches(0)
    r = p_inst.add_run("TRƯỜNG ĐẠI HỌC LẠC HỒNG\nKHOA CÔNG NGHỆ THÔNG TIN")
    apply_run_font(r, "Times New Roman", 13, bold=True)

    # Sub-department
    p_line = doc.add_paragraph()
    p_line.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(0)
    p_line.paragraph_format.space_after = Pt(40)
    p_line.paragraph_format.first_line_indent = Inches(0)
    r_line = p_line.add_run("------------------------------------")
    apply_run_font(r_line, "Times New Roman", 11, bold=True)

    # Report title
    p_rep = doc.add_paragraph()
    p_rep.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_before = Pt(20)
    p_rep.paragraph_format.space_after = Pt(8)
    p_rep.paragraph_format.first_line_indent = Inches(0)
    r_rep = p_rep.add_run("BÁO CÁO ĐỒ ÁN CUỐI KỲ\nHỌC PHẦN: CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT")
    apply_run_font(r_rep, "Times New Roman", 15, bold=True)

    # Topic title (<= 20 words)
    p_topic = doc.add_paragraph()
    p_topic.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(14)
    p_topic.paragraph_format.space_after = Pt(18)
    p_topic.paragraph_format.first_line_indent = Inches(0)
    r_topic = p_topic.add_run("ĐỀ TÀI: TÌM ĐƯỜNG ĐI NGẮN NHẤT TRÊN BẢN ĐỒ BẰNG THUẬT TOÁN DIJKSTRA VÀ A*")
    apply_run_font(r_topic, "Times New Roman", 16, bold=True, color_rgb=(29, 78, 216))

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(50)
    p_sub.paragraph_format.first_line_indent = Inches(0)
    r_sub = p_sub.add_run("Cài đặt thuần cấu trúc Min-Heap có mảng chỉ mục, Bảng băm DJB2 và thực nghiệm đa quy mô")
    apply_run_font(r_sub, "Times New Roman", 11, italic=True)

    # Student info block
    p_info = doc.add_paragraph()
    p_info.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.space_before = Pt(40)
    p_info.paragraph_format.space_after = Pt(40)
    p_info.paragraph_format.left_indent = Inches(1.5)
    p_info.paragraph_format.first_line_indent = Inches(0)
    p_info.paragraph_format.line_spacing = 1.15
    info_text = (
        "Giảng viên hướng dẫn: ThS. Đoàn Thiện Minh\n"
        "Sinh viên thực hiện:\n"
        "  1. Nguyễn Hoàng Anh  - MSSV: 125000977 (Nhóm trưởng)\n"
        "  2. Hà Văn Kiên        - MSSV: 125000399\n"
        "  3. Trần Quang Huy     - MSSV: 125001825\n"
        "  4. Hoàng Minh Phát    - MSSV: 125001323\n"
        "Lớp: 25CT111"
    )
    r_info = p_info.add_run(info_text)
    apply_run_font(r_info, "Times New Roman", 11)

    # Location & Date
    p_loc = doc.add_paragraph()
    p_loc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_loc.paragraph_format.space_before = Pt(30)
    p_loc.paragraph_format.space_after = Pt(0)
    p_loc.paragraph_format.first_line_indent = Inches(0)
    r_loc = p_loc.add_run("Đồng Nai, tháng 11 năm 2026")
    apply_run_font(r_loc, "Times New Roman", 11, italic=True)

    doc.add_page_break()

def build_pledge_page(doc):
    add_heading_1(doc, "LỜI CAM ĐOAN")
    add_body_paragraph(doc, "Chúng em xin cam đoan toàn bộ nội dung công trình nghiên cứu và báo cáo đồ án này là kết quả lao động học thuật trung thực của tập thể nhóm dưới sự chỉ dẫn của giảng viên phụ trách học phần Cấu trúc Dữ liệu và Giải thuật. Mọi số liệu thực nghiệm, bảng số đo benchmark, biểu đồ và mã nguồn cài đặt trình bày trong tài liệu này đều được trích xuất từ quá trình chạy thực tế trên máy tính thử nghiệm, không qua bất kỳ hình thức can thiệp chỉnh sửa số liệu hay ngụy tạo kết quả.")
    add_body_paragraph(doc, "Nhóm cam kết không sao chép nguyên văn, không chiếm dụng mã nguồn hay bài viết của bất kỳ cá nhân, đồ án khóa trước hay tài liệu trực tuyến nào mà không thực hiện trích dẫn khoa học minh bạch. Tất cả các cấu trúc dữ liệu nền tảng gồm Hàng đợi ưu tiên Min-Heap có mảng chỉ vị pos[], Bảng băm đóng dò tuyến tính giải quyết xung đột, Ngăn xếp truy vết và Hàng đợi kiểm tra liên thông đều được nhóm tự tay thiết kế và lập trình thuần túy mà không sử dụng bất kỳ thư viện hỗ trợ cấu trúc dữ liệu dựng sẵn nào.")
    add_body_paragraph(doc, "Nếu có bất kỳ sự sai lệch hoặc vi phạm quy chế liêm chính học thuật nào bị phát hiện, toàn thể các thành viên trong nhóm xin chịu hoàn toàn trách nhiệm trước Hội đồng thẩm định và Quy định xử lý kỷ luật học vụ của Trường Đại học Lạc Hồng.")

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(20)
    p_sig.paragraph_format.space_after = Pt(0)
    p_sig.paragraph_format.first_line_indent = Inches(0)
    r_sig = p_sig.add_run("Đồng Nai, ngày 06 tháng 11 năm 2026\nĐại diện nhóm sinh viên thực hiện\n(Ký và ghi rõ họ tên)\n\n\n\nNguyễn Hoàng Anh")
    apply_run_font(r_sig, "Times New Roman", 11, italic=True)

    doc.add_page_break()

def build_toc_placeholders(doc):
    add_heading_1(doc, "MỤC LỤC")
    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.first_line_indent = Inches(0)
    p_toc.paragraph_format.line_spacing = 1.0
    p_toc.paragraph_format.space_after = Pt(3)
    # Add TOC field
    fldSimple = parse_xml(r'<w:fldSimple %s w:instr="TOC \o &quot;1-3&quot; \h \z \u"/>' % nsdecls('w'))
    p_toc._p.append(fldSimple)
    doc.add_page_break()

    add_heading_1(doc, "DANH MỤC HÌNH VẼ")
    p_tof = doc.add_paragraph()
    p_tof.paragraph_format.first_line_indent = Inches(0)
    p_tof.paragraph_format.line_spacing = 1.0
    p_tof.paragraph_format.space_after = Pt(3)
    fldSimple_f = parse_xml(r'<w:fldSimple %s w:instr="TOC \c &quot;Hình&quot; \h \z"/>' % nsdecls('w'))
    p_tof._p.append(fldSimple_f)
    doc.add_page_break()

    add_heading_1(doc, "DANH MỤC BẢNG BIỂU")
    p_tot = doc.add_paragraph()
    p_tot.paragraph_format.first_line_indent = Inches(0)
    p_tot.paragraph_format.line_spacing = 1.0
    p_tot.paragraph_format.space_after = Pt(3)
    fldSimple_t = parse_xml(r'<w:fldSimple %s w:instr="TOC \c &quot;Bảng&quot; \h \z"/>' % nsdecls('w'))
    p_tot._p.append(fldSimple_t)
    doc.add_page_break()

print("Page templates defined.")
