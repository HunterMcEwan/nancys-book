"""
Crop portrait-rectangle regions out of the existing web-sized scrapbook
images for use in the family tree at /family-tree/.

The web images live at src/books/book-NNN/images/web/PPP.jpg at 1800px max
edge; the cropped portraits are written to a sibling directory
src/books/book-NNN/images/portrait/PPP-id.jpg at a target size of ~360px
wide (sharp at the family-tree's 120px display size with retina headroom).

Coordinates here are eyeballed from the source web images viewed during
the family-tree build. They're hand-tuned per portrait and worth a second
pass once the tree's visual style is settled.

Usage:
  py scripts/family-tree-portraits.py            # rebuild everything
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent

# Each entry: (book, page, person_id, x, y, w, h) in source web-image
# coordinates. The output is saved to
#   src/books/book-N/images/portrait/PAGE-PERSON_ID.jpg
PORTRAITS = [
    # Amy Ann Perry FitzSimons — oval studio portrait, 1905 (b002/p047)
    (2,  47, "amy",              430, 290, 600, 770),
    # James Pickens Walker Sr. — cabinet card, 1900 Rockville Academy (b002/p057)
    (2,  57, "jpw_sr",           300, 320, 680, 870),
    # Bo Walker — WWII Medical Corps captain (b002/p169)
    (2, 169, "bo",               320, 200, 900, 1100),
    # Oswald Beverley McEwan — Army officer portrait (b002/p181)
    (2, 181, "oswald",           280, 130, 750, 950),
    # Mary Ann Walker — vignette studio portrait c. 1920 ("about 2") (b002/p087)
    (2,  87, "mary_ann",         760, 1180, 520, 540),
    # Samuel Gaillard FitzSimons Sr. — oval bust portrait (b001/p312, upper-center)
    (1, 312, "sgfs_sr",          400,  20, 480, 560),
    # Mary Anne Perry "Minnie" — cabinet card (b001/p312, upper-right)
    (1, 312, "minnie",           890,  10, 470, 590),
    # Christopher FitzSimons the emigrant — painted portrait, b001/p002 (left)
    (1,   2, "emigrant",          110, 250, 740, 900),
    # Catherine Pritchard FitzSimons — painted portrait with her daughter, b001/p002 (right)
    # Cropped to her face / upper body; the daughter in her lap shows
    # at the lower edge.
    (1,   2, "catherine_pritchard", 920, 250, 680, 720),
    # Dr. Christopher FitzSimons 3rd — bearded oval bust portrait, b001/p271 (upper-left)
    (1, 271, "christopher_3rd",    50,  30, 480, 540),
    # Susan Milliken Barker FitzSimons — oval portrait in white cap, b001/p271 (upper-right)
    (1, 271, "susan_milliken_barker", 1280, 30, 460, 540),
    # Christopher "Kit" FitzSimons Jr. — moustachioed bust, b001/p311 (upper-left)
    (1, 311, "kit",                  20,  50, 540, 720),
    # Frances Motte Huger — Henneby's of Columbia cabinet card, b001/p311 (upper-right)
    (1, 311, "frances_motte_huger", 1170, 50, 560, 720),
    # Seaman Sinkler FitzSimons — bearded cabinet card, b001/p441 (upper-left)
    (1, 441, "seaman",                20,  30, 580, 820),
    # Henrietta Gaillard FitzSimons (with young daughter) — b001/p441 (upper-right)
    (1, 441, "henrietta_gaillard",   1150, 30, 600, 820),
    # Amy Perry FitzSimons as a child with a stringed instrument — b001/p392 (top-left tall portrait)
    (1, 392, "amy_child",             80, 270, 290, 420),
    # Amy Perry "Buzzie" Walker — infant photo, b001/p392 (lower-left)
    (1, 392, "buzzie",                30, 820, 250, 290),
    # James Pickens "Bo" Walker Jr. — Savannah High School portrait, b001/p393 (top-centre)
    (1, 393, "bo_school",            610,  60, 460, 660),
    # Emma Dee "Dee" Walker — Savannah High School portrait, b001/p393 (top-left)
    (1, 393, "dee_school",           150,  60, 460, 660),
    # Mary Ann Walker — Savannah High School portrait, b001/p393 (top-right)
    (1, 393, "mary_ann_school",     1140,  60, 480, 660),
]


def crop_one(book: int, page: int, person_id: str, x: int, y: int, w: int, h: int) -> tuple[Path, tuple[int, int]]:
    book_dir = ROOT / "src" / "books" / f"book-{book:03d}"
    src_path = book_dir / "images" / "web" / f"{page:03d}.jpg"
    if not src_path.exists():
        raise SystemExit(f"missing source: {src_path}")
    im = Image.open(src_path).convert("RGB")
    sw, sh = im.size
    # Clamp the crop box to the image bounds.
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(sw, x + w)
    y1 = min(sh, y + h)
    cropped = im.crop((x0, y0, x1, y1))
    # Resize so the long edge is 360px — sharp at the tree's 120px display
    # with retina headroom, small enough to keep the page light.
    cw, ch = cropped.size
    if max(cw, ch) > 360:
        scale = 360 / max(cw, ch)
        cropped = cropped.resize((round(cw * scale), round(ch * scale)), Image.LANCZOS)
    dst_dir = book_dir / "images" / "portrait"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / f"{page:03d}-{person_id}.jpg"
    cropped.save(dst_path, "JPEG", quality=82, optimize=True, progressive=True)
    return dst_path, cropped.size


def main() -> int:
    for spec in PORTRAITS:
        dst, size = crop_one(*spec)
        print(f"  {dst.relative_to(ROOT)}  ({size[0]}x{size[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
