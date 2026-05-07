#!/usr/bin/env python3
"""Build a DOCX letterhead for floating point.

Produces letterhead.docx — A4, branded header with the wordmark and a
return address block, an empty body, and a colophon footer. Open it,
type the letter, save as a new file.

Run from this directory:
    python3 build.py

Requires: python-docx (pip), and ../assets/floating-wordmark@3x.png
to exist in the repo.
"""
from pathlib import Path

from docx import Document
from docx.shared import Mm, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).parent
WORDMARK_PNG = ROOT.parent / "assets" / "floating-wordmark@3x.png"

# Brand palette
INK       = RGBColor(0x15, 0x14, 0x1A)
INK_SOFT  = RGBColor(0x2A, 0x27, 0x30)
FOG       = RGBColor(0x9A, 0x9A, 0x9E)

INTER_SANS = "Inter"
INTER_FALLBACK = "Helvetica Neue"
MONO = "JetBrains Mono"
MONO_FALLBACK = "Consolas"


def set_run(run, *, font=INTER_SANS, size=Pt(11), bold=False,
            color=INK_SOFT, letter_spacing=None, caps=False):
    run.font.name = font
    run.font.size = size
    run.font.bold = bold
    run.font.color.rgb = color
    # East Asian + complex script font fallback (Word respects rFonts complex)
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts")) or OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), font)
    rFonts.set(qn("w:hAnsi"), font)
    rFonts.set(qn("w:cs"), font)
    if rFonts.getparent() is None:
        rPr.append(rFonts)
    if letter_spacing is not None:
        spacing = OxmlElement("w:spacing")
        spacing.set(qn("w:val"), str(letter_spacing))
        rPr.append(spacing)
    if caps:
        caps_el = OxmlElement("w:caps")
        caps_el.set(qn("w:val"), "true")
        rPr.append(caps_el)


def remove_table_borders(table):
    tbl_pr = table._element.find(qn("w:tblPr")) or OxmlElement("w:tblPr")
    tbl_borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        b = OxmlElement(f"w:{edge}")
        b.set(qn("w:val"), "nil")
        tbl_borders.append(b)
    tbl_pr.append(tbl_borders)


def main():
    doc = Document()

    # A4 page, generous margins
    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.top_margin = Mm(28)
    section.bottom_margin = Mm(24)
    section.left_margin = Mm(24)
    section.right_margin = Mm(24)
    section.header_distance = Mm(12)
    section.footer_distance = Mm(12)

    # ---- HEADER: wordmark left, return address right ----
    header = section.header
    # Use a 2-column borderless table for layout
    htable = header.add_table(rows=1, cols=2, width=Mm(162))
    htable.autofit = False
    htable.columns[0].width = Mm(80)
    htable.columns[1].width = Mm(82)
    remove_table_borders(htable)

    # left cell: wordmark image
    left_cell = htable.cell(0, 0)
    left_cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    p_logo = left_cell.paragraphs[0]
    p_logo.paragraph_format.space_before = Pt(0)
    p_logo.paragraph_format.space_after = Pt(0)
    run_logo = p_logo.add_run()
    run_logo.add_picture(str(WORDMARK_PNG), width=Mm(34))

    # right cell: return address
    right_cell = htable.cell(0, 1)
    right_cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    p_addr = right_cell.paragraphs[0]
    p_addr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_addr.paragraph_format.space_before = Pt(0)
    p_addr.paragraph_format.space_after = Pt(0)
    p_addr.paragraph_format.line_spacing = 1.5

    addr_lines = [
        "floating point lda",
        "rua direita 40",
        "3800-218 aveiro",
        "floatingpoint.pt",
    ]
    for i, line in enumerate(addr_lines):
        run = p_addr.add_run(line)
        set_run(run, font=MONO, size=Pt(8), color=FOG)
        if i < len(addr_lines) - 1:
            p_addr.add_run().add_break()

    # Default style for body text
    style = doc.styles["Normal"]
    style.font.name = INTER_SANS
    style.font.size = Pt(11)
    style.font.color.rgb = INK_SOFT
    pf = style.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.55

    # ---- BODY: date placeholder + space for the letter ----
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(8)
    p_date.paragraph_format.space_after = Pt(20)
    r_date = p_date.add_run("yyyy · mm · dd")
    set_run(r_date, font=MONO, size=Pt(9), color=FOG, letter_spacing=24)

    p_to = doc.add_paragraph()
    p_to.paragraph_format.space_after = Pt(14)
    r_to = p_to.add_run("dear [name],")
    set_run(r_to, font=INTER_SANS, size=Pt(11), color=INK_SOFT)

    for _ in range(3):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(12)
        r = p.add_run(" ")
        set_run(r, font=INTER_SANS, size=Pt(11), color=INK_SOFT)

    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(20)
    p_close.paragraph_format.space_after = Pt(8)
    r_close = p_close.add_run("yours,")
    set_run(r_close, font=INTER_SANS, size=Pt(11), color=INK_SOFT)

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(28)
    r_sig = p_sig.add_run("daniel.")
    set_run(r_sig, font=INTER_SANS, size=Pt(11), bold=True, color=INK)

    # ---- FOOTER: 3 columns, mono small caps, fog ----
    footer = section.footer
    ftable = footer.add_table(rows=1, cols=3, width=Mm(162))
    ftable.autofit = False
    ftable.columns[0].width = Mm(60)
    ftable.columns[1].width = Mm(62)
    ftable.columns[2].width = Mm(40)
    remove_table_borders(ftable)

    foot_left = ftable.cell(0, 0).paragraphs[0]
    foot_left.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = foot_left.add_run("floating point lda")
    set_run(r1, font=MONO, size=Pt(7), color=FOG, letter_spacing=24, caps=True)

    foot_mid = ftable.cell(0, 1).paragraphs[0]
    foot_mid.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = foot_mid.add_run("tax · pt · 514 159 265")
    set_run(r2, font=MONO, size=Pt(7), color=FOG, letter_spacing=24, caps=True)

    foot_right = ftable.cell(0, 2).paragraphs[0]
    foot_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r3 = foot_right.add_run("page 1 / 1")
    set_run(r3, font=MONO, size=Pt(7), color=FOG, letter_spacing=24, caps=True)

    out = ROOT / "letterhead.docx"
    doc.save(out)
    print(f"wrote {out} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
