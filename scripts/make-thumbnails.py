"""
Generate small thumbnail JPEGs for every page scan, for use on the book
index pages.

Reads from src/books/book-NNN/images/web/*.jpg (the existing 1800px web
images) and writes to src/books/book-NNN/images/thumb/*.jpg at 400px max
edge, quality 75. Idempotent — skips files whose thumbnail already exists
and is newer than the source.

Usage:
  py scripts/make-thumbnails.py            # all books
  py scripts/make-thumbnails.py 1          # just book 1
  py scripts/make-thumbnails.py --force    # regenerate everything

Why 400px max edge / quality 75:
- Browsers render the thumb at ~80-100px wide on the index pages but we
  want enough detail for the user to recognize the page; 400px gives 2x
  the typical render width.
- JPEG quality 75 keeps each thumbnail well under 25KB. 960 thumbnails
  total weight ~10-20MB on disk and in git, which is acceptable.
"""
import sys
import argparse
from pathlib import Path
from PIL import Image


def make_thumb(src: Path, dst: Path, max_edge: int, quality: int) -> tuple[int, int, int]:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    scale = max_edge / max(w, h)
    if scale < 1:
        new_size = (max(1, round(w * scale)), max(1, round(h * scale)))
        im = im.resize(new_size, Image.LANCZOS)
        nw, nh = new_size
    else:
        nw, nh = w, h
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "JPEG", quality=quality, optimize=True, progressive=True)
    return nw, nh, dst.stat().st_size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("book", nargs="?", type=int, help="Book number (1, 2, or 3). Omit for all.")
    ap.add_argument("--max-edge", type=int, default=400)
    ap.add_argument("--quality", type=int, default=75)
    ap.add_argument("--force", action="store_true", help="Regenerate even if dst exists")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    book_filter = f"book-{args.book:03d}" if args.book else None

    generated = 0
    skipped = 0
    total_bytes = 0
    for book_dir in sorted((root / "src" / "books").glob("book-*")):
        if book_filter and book_dir.name != book_filter:
            continue
        web_dir = book_dir / "images" / "web"
        thumb_dir = book_dir / "images" / "thumb"
        if not web_dir.is_dir():
            continue
        for src in sorted(web_dir.glob("*.jpg")):
            dst = thumb_dir / src.name
            if dst.exists() and not args.force:
                if dst.stat().st_mtime >= src.stat().st_mtime:
                    skipped += 1
                    continue
            nw, nh, sz = make_thumb(src, dst, args.max_edge, args.quality)
            generated += 1
            total_bytes += sz
            if generated % 50 == 0:
                print(f"  ... {generated} thumbnails")

    print(f"Generated {generated} thumbnails, skipped {skipped} (up-to-date).")
    if generated > 0:
        avg_kb = total_bytes / generated / 1024
        print(f"Average size: {avg_kb:.1f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
