#!/usr/bin/env python3
"""Build a print-ready PDF/X-1a:2001 of alt 06 (longitude card).

Reads embedded fonts and the wordmark <symbol> from ../index.html so the
print output stays in lockstep with the brand book. Run from this
directory:

    python3 build.py

Produces:
    alt-06.pdf       — intermediate weasyprint output
    alt-06-x1a.pdf   — PDF/X-1a:2001 final deliverable

Requirements: weasyprint (pip), ghostscript (apt). The PDF/X-1a step
needs an ICC profile at "ISO Coated sb.icc" — symlinked at first run.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
SOURCE_HTML = (ROOT.parent / "index.html").read_text()


def extract_fonts_css(source: str) -> str:
    """Pull the four @font-face blocks (Inter 400/500/600 + JetBrains Mono)."""
    blocks = re.findall(r"@font-face\s*\{[^}]*\}", source, re.DOTALL)
    if len(blocks) < 4:
        raise RuntimeError(f"expected 4 @font-face blocks, found {len(blocks)}")
    return "\n".join(blocks[:4])


def extract_wordmark_inner(source: str) -> str:
    """Pull the inner content of <symbol id="wordmark">…</symbol>."""
    m = re.search(
        r'<symbol\s+id="wordmark"[^>]*>(.*?)</symbol>',
        source,
        re.DOTALL,
    )
    if not m:
        raise RuntimeError("wordmark symbol not found in source")
    return m.group(1)


FONTS_CSS = extract_fonts_css(SOURCE_HTML)
WORDMARK_INNER = extract_wordmark_inner(SOURCE_HTML)


def lockup(width, color="var(--ink)"):
    return (
        f'<svg viewBox="0 0 884.691 290.391" preserveAspectRatio="xMidYMid meet" '
        f'style="color: {color}; width: {width}; display: block;" '
        f'xmlns="http://www.w3.org/2000/svg">{WORDMARK_INNER}</svg>'
    )


def card_template(name, role, addr_label, dot_left_pct, axis_left, axis_right):
    front_lockup = lockup("55mm")
    back_lockup = lockup("18mm")

    # 11 ticks evenly spaced along the 73mm-wide axis interior.
    ticks_html = "".join(
        f'<div class="tick" style="left: calc(6mm + (100% - 12mm) * {i / 10:.4f});"></div>'
        for i in range(11)
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>floating point — business card · alt 06</title>
<style>
{FONTS_CSS}

:root {{
  --paper:    #f5f3ee;
  --fog:      #9a9a9e;
  --ink-soft: #2a2730;
  --ink:      #15141a;
}}

@page {{
  size: 85mm 55mm;
  margin: 0;
  bleed: 3mm;
  marks: crop cross;
}}

* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}

html, body {{
  margin: 0; padding: 0;
  font-family: 'Inter', sans-serif;
  color: var(--ink-soft);
  background: var(--paper);
}}

.page {{
  position: relative;
  width: 85mm; height: 55mm;
  background: var(--paper);
  page-break-after: always;
  overflow: hidden;
}}
.page:last-child {{ page-break-after: auto; }}

/* front */
.front {{ position: relative; width: 100%; height: 100%; }}
.front .lockup-wrap {{
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%, -50%);
}}

/* back */
.back {{ position: relative; width: 100%; height: 100%; padding: 6mm; }}

.back .ident {{
  position: absolute;
  left: 6mm; top: 6mm;
  white-space: nowrap;
}}
.back .ident .name {{
  font-size: 7pt; font-weight: 600;
  color: var(--ink); letter-spacing: -0.01em;
}}
.back .ident .role {{
  font-size: 5.2pt;
  color: var(--fog);
  margin-top: 1pt;
}}
.back .lockup-mini {{
  position: absolute;
  right: 6mm; top: 6mm;
}}

.back .axis {{
  position: absolute;
  left: 6mm; right: 6mm;
  top: 50%; height: 0;
  border-top: 0.25mm solid var(--ink);
}}
.back .tick {{
  position: absolute;
  width: 0.18mm; height: 2mm;
  background: var(--ink-soft);
  top: calc(50% - 1mm);
}}
.back .pt {{
  position: absolute;
  width: 1.6mm; height: 1.6mm;
  border-radius: 50%;
  background: var(--ink);
  top: 50%;
  transform: translate(-50%, -50%);
}}
.back .brand-tag {{
  position: absolute;
  top: calc(50% - 4.8mm);
  transform: translate(-50%, 0);
  font-family: 'JetBrains Mono', monospace;
  font-size: 3.4pt;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--fog);
  white-space: nowrap;
}}
.back .loc {{
  position: absolute;
  top: calc(50% + 2.6mm);
  transform: translate(-50%, 0);
  font-family: 'JetBrains Mono', monospace;
  font-size: 5pt;
  color: var(--fog);
  letter-spacing: 0.04em;
  white-space: nowrap;
}}
.back .end {{
  position: absolute;
  top: calc(50% + 2.6mm);
  font-family: 'JetBrains Mono', monospace;
  font-size: 4.4pt;
  color: var(--fog);
  letter-spacing: 0.04em;
}}
.back .end.l {{ left: 6mm; }}
.back .end.r {{ right: 6mm; }}

.back .contact {{
  position: absolute;
  left: 6mm; right: 6mm;
  bottom: 6mm;
}}
.back .contact .row {{ display: flex; margin-top: 0.6mm; }}
.back .contact .row:first-child {{ margin-top: 0; }}
.back .contact .lab {{
  width: 11mm;
  color: var(--fog);
  font-family: 'JetBrains Mono', monospace;
  font-size: 4pt;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  padding-top: 0.3mm;
}}
.back .contact .val {{
  color: var(--ink);
  font-family: 'JetBrains Mono', monospace;
  font-size: 5pt;
}}
</style>
</head>
<body>

<div class="page">
  <div class="front">
    <div class="lockup-wrap">{front_lockup}</div>
  </div>
</div>

<div class="page">
  <div class="back">
    <div class="ident">
      <div class="name">{name}</div>
      <div class="role">{role}</div>
    </div>
    <div class="lockup-mini">{back_lockup}</div>

    {ticks_html}
    <div class="axis"></div>
    <span class="end l">{axis_left}</span>
    <span class="end r">{axis_right}</span>
    <div class="brand-tag" style="left: {dot_left_pct}%;">floating point</div>
    <div class="pt" style="left: {dot_left_pct}%;"></div>
    <div class="loc" style="left: {dot_left_pct}%;">{addr_label}</div>

    <div class="contact">
      <div class="row"><span class="lab">mail</span><span class="val">daniel@floatingpoint.pt</span></div>
      <div class="row"><span class="lab">tel</span><span class="val">+351 910 887 197</span></div>
    </div>
  </div>
</div>
</body>
</html>
"""


def run_weasyprint(html: str, pdf_path: Path) -> None:
    from weasyprint import HTML
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(pdf_path))


def run_ghostscript_pdfx1a(in_pdf: Path, out_pdf: Path, def_ps: Path) -> None:
    # Ghostscript's -dPDFX path defaults to "ISO Coated sb.icc" in CWD.
    # Symlink default_cmyk.icc there so the PostScript prefix can read it.
    fallback_icc = ROOT / "ISO Coated sb.icc"
    if not fallback_icc.exists():
        fallback_icc.symlink_to("/usr/share/color/icc/ghostscript/default_cmyk.icc")

    cmd = [
        "gs",
        "-dPDFX",
        "-dBATCH",
        "-dNOPAUSE",
        "-dNOSAFER",
        "-dCompatibilityLevel=1.3",
        "-sDEVICE=pdfwrite",
        "-sColorConversionStrategy=CMYK",
        "-dProcessColorModel=/DeviceCMYK",
        "-dEmbedAllFonts=true",
        "-dSubsetFonts=true",
        f"-sOutputFile={out_pdf}",
        str(def_ps),
        str(in_pdf),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)


def main():
    html = card_template(
        name="daniel ferreira",
        role="managing partner",
        addr_label="aveiro · −8.654°",
        dot_left_pct=67.30,
        axis_left="−10°",
        axis_right="−8°",
    )

    intermediate = ROOT / "alt-06.pdf"
    final = ROOT / "alt-06-x1a.pdf"
    def_ps = ROOT / "PDFX_def_x1a.ps"

    run_weasyprint(html, intermediate)
    print(f"weasyprint → {intermediate} ({intermediate.stat().st_size:,} bytes)")
    run_ghostscript_pdfx1a(intermediate, final, def_ps)
    print(f"ghostscript → {final} ({final.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
