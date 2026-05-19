"""
Draw current PORTRAITS crop rectangles onto each source page so I can
verify by eye whether each box is over the intended face. Outputs go to
tmp_preview/*.jpg.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("portraits", ROOT / "scripts" / "family-tree-portraits.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Group by page so we can overlay all boxes for a page in one preview.
by_page: dict[tuple[int, int], list] = {}
for spec_entry in mod.PORTRAITS:
    book, page, pid, x, y, w, h = spec_entry
    by_page.setdefault((book, page), []).append((pid, x, y, w, h))

out_dir = ROOT / "tmp_preview"
out_dir.mkdir(exist_ok=True)

try:
    font = ImageFont.truetype("arial.ttf", 28)
except Exception:
    font = ImageFont.load_default()

for (book, page), boxes in by_page.items():
    src = ROOT / "src" / "books" / f"book-{book:03d}" / "images" / "web" / f"{page:03d}.jpg"
    if not src.exists():
        continue
    im = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(im)
    for pid, x, y, w, h in boxes:
        draw.rectangle((x, y, x + w, y + h), outline=(255, 0, 0), width=5)
        draw.text((x + 6, y + 6), pid, fill=(255, 0, 0), font=font)
    dst = out_dir / f"b{book:03d}_p{page:03d}_preview.jpg"
    im.thumbnail((1400, 1400), Image.LANCZOS)
    im.save(dst, "JPEG", quality=82)
    print(f"  {dst.relative_to(ROOT)}")
