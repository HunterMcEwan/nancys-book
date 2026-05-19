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
    # All face crops below target the SVG card aperture aspect ratio
    # of 140/172 ≈ 0.81 (w/h), so the displayed image isn't sliced at
    # top/bottom. Face is vertically centered where the source photo
    # allows it.

    # James Pickens Walker Sr. — cabinet card, 1900 Rockville Academy
    # (b002/p057); tight on the oval portrait, dropping the matte.
    (2,  57, "jpw_sr",           370, 505, 480, 590),
    # Bo Walker (James Pickens Walker Jr.) — WWII Army officer
    # vignette portrait (b002/p169); cap + face + collar, face centered.
    (2, 169, "bo",               260, 171, 600, 738),
    # Oswald Beverley McEwan — WWII Army officer portrait (b002/p181);
    # the photo's left edge sits at source x ~ 350 on a lined notebook
    # page, so we crop tight on cap-brim + face to avoid showing the
    # notebook's blue rules.
    (2, 181, "oswald",           350, 290, 540, 664),
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
    (1, 271, "christopher_3rd",    50,  60, 450, 510),
    # Susan Milliken Barker FitzSimons — oval portrait in white cap, b001/p271 (upper-right)
    (1, 271, "susan_milliken_barker", 1280, 30, 460, 540),
    # Christopher "Kit" FitzSimons Jr. — moustachioed bust, b001/p311 (upper-left)
    (1, 311, "kit",                  20,  50, 540, 720),
    # Frances Motte Huger — Hennies of Columbia cabinet card, b001/p311
    # (upper-right). Tight on her face/upper body — the original
    # cabinet card shows her holding a grandchild on her lap, but the
    # tree card just wants Frances herself.
    (1, 311, "frances_motte_huger", 1320, 50, 320, 380),
    # Seaman Sinkler FitzSimons — bearded cabinet card, b001/p441 (upper-left)
    (1, 441, "seaman",                20,  30, 580, 820),
    # Henrietta Gaillard FitzSimons (with young daughter) — b001/p441 (upper-right)
    (1, 441, "henrietta_gaillard",   1150, 30, 600, 820),
    # Amy Perry FitzSimons as a child with a stringed instrument — b001/p392 (top-left tall portrait)
    (1, 392, "amy_child",             80, 270, 290, 420),
    # Amy Perry "Buzzie" Walker — infant photo, b001/p392 (lower-left)
    (1, 392, "buzzie",                30, 820, 250, 290),
    # James Pickens "Bo" Walker Jr. — Savannah High School portrait, b001/p393 (top-centre)
    (1, 393, "bo_school",            650, 160, 460, 660),
    # Emma Dee "Dee" Walker — Savannah High School portrait, b001/p393 (top-left)
    (1, 393, "dee_school",           160, 130, 460, 660),
    # Mary Ann Walker — Savannah High School portrait, b001/p393 (top-right)
    (1, 393, "mary_ann_school",     1240, 130, 480, 660),

    # ── Dr. Christopher 3rd's seven children — the 1890s adult group
    # portrait pasted on book-001/p272 (lower photo). We crop the four
    # for whom we don't already have a dedicated cabinet card: Theodore
    # Stoney "Tote" (back-left), Ellen Milliken (back-centre, the only
    # daughter — unmarried, Charleston Library Society librarian),
    # William Huger (back-right), and Gaillard Stoney "Gaillie"
    # (front-left). The remaining three (Kit, SGFS Sr., Seaman Sinkler)
    # already have sharper solo cabinet-card crops elsewhere.
    (1, 272, "theodore_stoney_fs",   216, 1000, 220, 290),
    (1, 272, "ellen_milliken_fs",    461, 1020, 220, 290),
    (1, 272, "w_huger_fs",           696, 1020, 220, 290),
    (1, 272, "gaillie_fs",            81, 1160, 220, 290),

    # ── Amy's FitzSimons first cousins (children of her father's
    # siblings). Each crop is hand-tuned per source page. Several of
    # these cousins appear only in tipped-in studio portraits or news
    # clippings on densely-laid pages, so crops are conservative —
    # widen rather than tighten if a face gets clipped.

    # Christopher FitzSimons 5th (b. 1892) — small oval boy portrait
    # in middle-centre of book-001/p304.
    (1, 304, "christopher_5th",      785,  820, 200, 260),
    # Nathalie Heyward (m. Christopher 5th) — profile head-and-shoulders,
    # middle-right of p304.
    (1, 304, "nathalie_heyward",    1260,  460, 220, 300),

    # William Huger + Annie Cain children — three oval portraits in
    # mid-row of book-001/p487 (in caption order L→R: Cain, W. Huger
    # Jr., Sam the aviator), plus Marguerite and Reginald below.
    (1, 487, "cain_fs",              820,  560, 220, 280),
    (1, 487, "huger_jr_fs",          1090, 560, 220, 280),
    (1, 487, "sam_aviator_fs",      1420,  680, 200, 260),
    (1, 487, "marguerite_fs",        610,  980, 220, 320),
    (1, 487, "reginald_fs",          970, 1240, 220, 260),

    # Seaman + Henrietta's only child Christopher (b. 1888, d. Waycross
    # GA 1898 in his 11th year). Cabinet portrait in dark mat, lower
    # centre of book-001/p441.
    (1, 441, "christopher_seaman_son", 730, 930, 260, 340),

    # Theodore Stoney's children — John McCrady (Navy uniform, WWI)
    # and Louisa de Berniere ("Louiza F.S." in the album hand), both
    # on book-001/p443.
    (1, 443, "louisa_de_burian_fs",   80,   90, 220, 280),
    (1, 443, "john_mccrady_fs",      125,  635, 220, 270),
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
