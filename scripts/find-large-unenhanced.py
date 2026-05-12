"""Find scrapbook scans >= 4000x4000 that have not been enhance-transcribed."""
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SCANS = ROOT / 'scans'

prefix_map = [
    (re.compile(r'^Album Memories 01_(\d{3})\.JPG$', re.I), 1),
    (re.compile(r'^Family book_(\d{3})\.JPG$',       re.I), 2),
    (re.compile(r'^Photo Memories 01_(\d{3})\.JPG$', re.I), 3),
]


def enhanced(book, page):
    p = ROOT / 'src' / 'books' / f'book-{book:03d}' / 'pages' / f'{page:03d}.md'
    if not p.exists():
        return None
    try:
        return 'transcription_pass: enhanced' in p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return None


results = {b: {'total': 0, 'large': 0, 'enh': 0, 'unenh': 0} for b in (1, 2, 3)}
unenh_list = []

for path in sorted(SCANS.iterdir()):
    if not path.is_file():
        continue
    book = page = None
    for rx, b in prefix_map:
        m = rx.match(path.name)
        if m:
            book, page = b, int(m.group(1))
            break
    if book is None:
        continue
    results[book]['total'] += 1
    try:
        with Image.open(path) as im:
            w, h = im.size
    except Exception:
        continue
    if w >= 4000 and h >= 4000:
        results[book]['large'] += 1
        eh = enhanced(book, page)
        if eh is True:
            results[book]['enh'] += 1
        else:
            results[book]['unenh'] += 1
            unenh_list.append((book, page, w, h))

print('=== Per-book ===')
for b in (1, 2, 3):
    v = results[b]
    print(f'book-{b:03d}: total={v["total"]:4d}  large(>=4000x4000)={v["large"]:4d}  '
          f'enhanced={v["enh"]:4d}  large+unenhanced={v["unenh"]:4d}')

tot_large = sum(v['large'] for v in results.values())
tot_enh = sum(v['enh'] for v in results.values())
tot_unenh = sum(v['unenh'] for v in results.values())
print()
print('=== Totals ===')
print(f'Large scans (>=4000x4000): {tot_large}')
print(f'  Already enhanced:        {tot_enh}')
print(f'  Large + unenhanced:      {tot_unenh}')
print()
print(f'=== First 20 large unenhanced (in page order) ===')
for b, p, w, h in unenh_list[:20]:
    print(f'  book-{b:03d}/p{p:03d}  {w}x{h}')

print()
print(f'=== Top 20 large unenhanced (sorted by pixel area, biggest first) ===')
by_area = sorted(unenh_list, key=lambda t: t[2] * t[3], reverse=True)
for b, p, w, h in by_area[:20]:
    mp = (w * h) / 1_000_000
    print(f'  book-{b:03d}/p{p:03d}  {w}x{h}  ({mp:.1f} MP)')
