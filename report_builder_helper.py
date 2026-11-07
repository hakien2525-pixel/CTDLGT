import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_report_document(docx_path):
    doc = docx.Document()

    # 1. Page setup: A4, Margins: Top 3.0cm, Bottom 2.0cm, Left 3.0cm, Right 2.0cm, Header 1.0cm, Footer 1.2cm
    for s in doc.sections:
        s.page_width = Inches(8.267)   # 21.0 cm
        s.page_height = Inches(11.692) # 29.7 cm
        s.top_margin = Inches(1.181)    # 3.0 cm
        s.bottom_margin = Inches(0.787) # 2.0 cm
        s.left_margin = Inches(1.181)   # 3.0 cm
        s.right_margin = Inches(0.787)  # 2.0 cm
        s.header_distance = Inches(0.394) # 1.0 cm
        s.footer_distance = Inches(0.472) # 1.2 cm

    # 2. Configure docDefaults and styles to Times New Roman 100%
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(11)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.0
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.space_after = Pt(3)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.first_line_indent = Inches(0.197) # 0.5 cm

    # Set rFonts and sz for Normal style
    rPr = normal_style.element.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>')
    rPr.append(rFonts)
    sz_xml = parse_xml(f'<w:sz {nsdecls("w")} w:val="22"/>')
    szCs_xml = parse_xml(f'<w:szCs {nsdecls("w")} w:val="22"/>')
    rPr.append(sz_xml)
    rPr.append(szCs_xml)

    # Configure Headings
    for level, sz in [(1, 14), (2, 12), (3, 11)]:
        h_style = styles[f'Heading {level}']
        h_font = h_style.font
        h_font.name = 'Times New Roman'
        h_font.size = Pt(sz)
        h_font.bold = True
        h_font.color.rgb = RGBColor(0, 0, 0)
        h_style.paragraph_format.line_spacing = 1.0
        h_style.paragraph_format.space_before = Pt(6)
        h_style.paragraph_format.space_after = Pt(6)
        h_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        h_style.paragraph_format.first_line_indent = Inches(0)
        hrPr = h_style.element.get_or_add_rPr()
        hrFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>')
        hrPr.append(hrFonts)

    return doc

print("Setup helper updated.")
