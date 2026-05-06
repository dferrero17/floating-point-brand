# print — alt 06 (longitude card)

Press-ready PDF/X-1a:2001 of the alt 06 longitude card, 85 × 55 mm trim with 3 mm bleed.

## deliverables

- `alt-06-x1a.pdf` — final PDF/X-1a:2001, 91 × 61 mm media (85 × 55 trim + 3 mm bleed), CMYK, fonts subset-embedded, crop and registration marks. Send this to the printer.
- `alt-06.pdf` — intermediate weasyprint output (RGB, with crop marks); useful for screen review.

## regenerate

```bash
pip install weasyprint
apt install ghostscript
python3 build.py
```

The build script reads embedded fonts and the `<symbol id="wordmark">` from `../index.html`, so any change to the brand book's typography or wordmark flows through.

## layout

- **front** — full-bleed paper, wordmark centred at 55 mm wide
- **back** — name + role in upper-left, wordmark mini in upper-right, longitude axis centred (dot at aveiro = −8.654°, end labels −10° and −8°), `floating point` in mono caps above the dot, `aveiro · −8.654°` below, contact rows pinned to the bottom

## printer notes

- 350 gsm cotton recommended (per the brand book)
- 3 mm bleed included on all sides
- Crop and registration marks present in the bleed area
- Output intent: generic CMYK (ghostscript `default_cmyk.icc`). Replace with your printer's preferred ICC (e.g. FOGRA39, GRACoL) by editing `PDFX_def_x1a.ps` and re-running.
