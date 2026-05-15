#!/usr/bin/env python3
"""
Rasterize a page of a PDF to a web-ready JPEG, optionally cropping to a
sub-region. Built for the appendix workflow (book-004) where source
PDFs from newspapers.com / NDNP live in additionalDocumentation/ and we
need a cropped, web-sized JPG for site display.

Requires: PyMuPDF (`pip install pymupdf`) and Pillow.

Usage:
  py scripts/pdf-to-web-image.py <pdf> <dest.jpg>
    [--page N]                  # 1-based page number (default 1)
    [--dpi N]                   # rasterization DPI before crop (default 200)
    [--crop x0,y0,x1,y1]        # fractions 0-1 of the rasterized page
    [--max-dim N]               # max width/height of final JPG (default 1800)
    [--quality N]               # JPEG quality (default 85)

Crop coordinates are *fractions of the rasterized page* (0.0-1.0). To
find them, run once without --crop, view the output, eyeball the box.

The script preserves the source PDF in place; only the destination JPG
is produced.
"""
import argparse
import sys
from pathlib import Path

import fitz
from PIL import Image


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("pdf")
    ap.add_argument("dest")
    ap.add_argument("--page", type=int, default=1, help="1-based page number")
    ap.add_argument("--dpi", type=int, default=200, help="rasterization DPI")
    ap.add_argument("--crop", help="x0,y0,x1,y1 fractions 0-1 of the page")
    ap.add_argument("--max-dim", type=int, default=1800)
    ap.add_argument("--quality", type=int, default=85)
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"error: {pdf_path} not found", file=sys.stderr)
        return 1

    doc = fitz.open(pdf_path)
    if args.page < 1 or args.page > doc.page_count:
        print(
            f"error: --page {args.page} out of range (PDF has "
            f"{doc.page_count} page(s))",
            file=sys.stderr,
        )
        return 1
    page = doc[args.page - 1]
    mat = fitz.Matrix(args.dpi / 72, args.dpi / 72)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    if args.crop:
        try:
            x0, y0, x1, y1 = (float(v) for v in args.crop.split(","))
        except ValueError:
            print("error: --crop must be 4 comma-separated floats", file=sys.stderr)
            return 1
        w, h = img.size
        box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
        img = img.crop(box)

    if max(img.size) > args.max_dim:
        ratio = args.max_dim / max(img.size)
        img = img.resize(
            (int(img.width * ratio), int(img.height * ratio)),
            Image.LANCZOS,
        )

    dest = Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=args.quality, optimize=True)

    src_mb = pdf_path.stat().st_size / (1024 * 1024)
    dst_kb = dest.stat().st_size / 1024
    print(
        f"{pdf_path} (p{args.page}, {src_mb:.2f} MB) -> {dest} "
        f"({dst_kb:.0f} KB, {img.size[0]}x{img.size[1]})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
