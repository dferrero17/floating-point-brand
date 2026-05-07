# print — alt 06 (longitude card) + letterhead

Press-ready PDF/X-1a:2001 of the alt 06 longitude card (85 × 55 mm trim, 3 mm bleed) and a DOCX letterhead.

## deliverables

- `alt-06-x1a.pdf` — final PDF/X-1a:2001 business card. 91 × 61 mm media (85 × 55 trim + 3 mm bleed), CMYK, fonts subset-embedded, crop and registration marks. Send to the printer.
- `alt-06.pdf` — intermediate weasyprint output (RGB, with crop marks); useful for screen review.
- `letterhead.docx` — A4 letterhead template. Header has the wordmark and return address, body is empty (with a date / salutation / signoff scaffold), footer carries the company tax line.

## regenerate

```bash
pip install weasyprint python-docx
apt install ghostscript libreoffice-writer
python3 build.py             # → alt-06.pdf, alt-06-x1a.pdf
python3 letterhead-build.py  # → letterhead.docx
```

`build.py` reads the embedded fonts and the `<symbol id="wordmark">` from `../index.html`, so any change to the brand book's typography or wordmark flows through.

## card layout

- **front** — full-bleed paper, wordmark centred at 55 mm wide
- **back** — name + role in upper-left, wordmark mini in upper-right, longitude axis centred (dot at aveiro = −8.654°, end labels −10° and −8°), `floating point` in mono caps above the dot, `aveiro · −8.654°` below, contact rows pinned to the bottom

## letterhead layout

- **header** — wordmark left (~34 mm wide), return address right (mono, fog colour, right-aligned)
- **body** — `yyyy · mm · dd` date placeholder, `dear [name],` salutation, empty paragraphs, `yours,` then `daniel.` as a starting closing
- **footer** — three columns, mono caps in fog: company entity · tax line · page number

Replace `[name]`, the date, and the body text with your own when writing a letter.

## printer notes

- 350 gsm cotton recommended for the card (per the brand book), 80–100 gsm uncoated for the letterhead
- 3 mm bleed included on the card, crop and registration marks present in the bleed area
- Card output intent: generic CMYK (ghostscript `default_cmyk.icc`). Replace with your printer's preferred ICC (e.g. FOGRA39, GRACoL) by editing `PDFX_def_x1a.ps` and re-running.
- Letterhead body uses Inter (regular for body, semi-bold for the closing name). Mono runs are JetBrains Mono. If those aren't installed on the editing machine, Word will substitute — install both for fidelity.
