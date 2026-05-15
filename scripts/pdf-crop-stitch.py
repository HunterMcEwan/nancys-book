#!/usr/bin/env python3
"""
Crop one or more rectangular regions from a PDF page and stitch them
vertically into a single web-ready JPEG. Use this when a newspaper
article spans a column break and the bounding rectangle would include
unrelated content from neighboring columns.

Usage:
  py scripts/pdf-crop-stitch.py <pdf> <dest.jpg> \
      --crops "x0,y0,x1,y1;x0,y0,x1,y1[;...]" \
      [--page N] [--dpi N] [--max-dim N] [--quality N] [--gap N]

Crops are joined top-to-bottom in the order given, with a thin white
gap (default 16px in final-image scale) between them. Each crop is
normalised to the page (fractions 0-1).

Example: stitch the bottom of column 1 to the top of column 2 of a
single newspaper page:
  py scripts/pdf-crop-stitch.py source.pdf out.jpg \
      --crops "0.34,0.86,0.51,0.94;0.495,0.05,0.65,0.18"
"""
import argparse
import sys
from pathlib import Path

import fitz
from PIL import Image


def crop_page(page: fitz.Page, mat: fitz.Matrix, frac: str) -> Image.Image:
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    x0, y0, x1, y1 = (float(v) for v in frac.split(","))
    w, h = img.size
    return img.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("pdf")
    ap.add_argument("dest")
    ap.add_argument("--crops", required=True, help="semicolon-separated x0,y0,x1,y1 specs")
    ap.add_argument("--page", type=int, default=1)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--max-dim", type=int, default=1800)
    ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--gap", type=int, default=16, help="vertical gap between crops")
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"error: {pdf_path} not found", file=sys.stderr)
        return 1

    doc = fitz.open(pdf_path)
    page = doc[args.page - 1]
    mat = fitz.Matrix(args.dpi / 72, args.dpi / 72)

    parts = [crop_page(page, mat, c.strip()) for c in args.crops.split(";") if c.strip()]
    if not parts:
        print("error: no crops given", file=sys.stderr)
        return 1

    target_w = max(p.width for p in parts)
    parts = [
        p if p.width == target_w
        else p.resize((target_w, int(p.height * target_w / p.width)), Image.LANCZOS)
        for p in parts
    ]
    total_h = sum(p.height for p in parts) + args.gap * (len(parts) - 1)
    canvas = Image.new("RGB", (target_w, total_h), "white")
    y = 0
    for p in parts:
        canvas.paste(p, (0, y))
        y += p.height + args.gap

    if max(canvas.size) > args.max_dim:
        ratio = args.max_dim / max(canvas.size)
        canvas = canvas.resize(
            (int(canvas.width * ratio), int(canvas.height * ratio)),
            Image.LANCZOS,
        )

    dest = Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "JPEG", quality=args.quality, optimize=True)

    src_mb = pdf_path.stat().st_size / (1024 * 1024)
    dst_kb = dest.stat().st_size / 1024
    print(
        f"{pdf_path} (p{args.page}, {src_mb:.2f} MB) -> {dest} "
        f"({dst_kb:.0f} KB, {canvas.size[0]}x{canvas.size[1]}, "
        f"{len(parts)} crops stitched)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
