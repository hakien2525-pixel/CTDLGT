import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from report_builder_helper import create_report_document
from report_sections_part1 import build_cover_page, build_pledge_page, build_toc_placeholders
from report_sections_part2 import build_intro_and_chapter1
from report_sections_part3 import build_chapter2
from report_sections_part4 import build_chapter3
from report_sections_part5 import build_chapter4
from report_sections_part6 import build_chapter5_and_end

def generate_complete_report(output_path):
    print(f"Bắt đầu xây dựng tài liệu báo cáo học thuật: {output_path}")
    doc = create_report_document(output_path)

    # 1. Trang bìa
    build_cover_page(doc)

    # 2. Lời cam đoan
    build_pledge_page(doc)

    # 3. Mục lục, Danh mục hình, Danh mục bảng
    build_toc_placeholders(doc)

    # 4. Lời mở đầu & Chương 1
    build_intro_and_chapter1(doc)

    # 5. Chương 2: Cơ sở lý thuyết
    build_chapter2(doc)

    # 6. Chương 3: Thiết kế và cài đặt
    build_chapter3(doc)

    # 7. Chương 4: Minh họa bản đồ mẫu
    build_chapter4(doc)

    # 8. Chương 5, Kết luận, Tài liệu tham khảo, Phụ lục
    build_chapter5_and_end(doc)

    # Setup page numbering in footer (section 2 onwards)
    # Configure footers with page number
    for s_idx, s in enumerate(doc.sections):
        footer = s.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        p_ft.paragraph_format.first_line_indent = Inches(0)
        p_ft.paragraph_format.space_before = Pt(0)
        p_ft.paragraph_format.space_after = Pt(0)
        # Add PAGE field
        fldSimple_p = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        p_ft._p.append(fldSimple_p)

    doc.save(output_path)
    print(f"Đã lưu thành công tệp DOCX tại: {output_path}")

if __name__ == "__main__":
    out_file = os.path.abspath("NopBai/BaoCao_DoAn_CuoiKy_DeTai5.docx")
    generate_complete_report(out_file)
