"""Find scrapbook scans above a pixel-area threshold that have not been phase-2 transcribed.

Reads `data/enhanced-pages.csv` to identify pages with status='enhanced' or any
'deferred-*' status — both are excluded from the queue. Pages whose md frontmatter
has `transcription_pass: enhanced` are also excluded (in case the CSV lags).

Usage:
    py scripts/find-large-unenhanced.py                 # default 4000x4000 threshold
    py scripts/find-large-unenhanced.py --min-px 3000   # use 3000x3000 threshold
"""
import argparse
import csv
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SCANS = ROOT / 'scans'
CSV_PATH = ROOT / 'data' / 'enhanced-pages.csv'

prefix_map = [
    (re.compile(r'^Album Memories 01_(\d{3})\.JPG$', re.I), 1),
    (re.compile(r'^Family book_(\d{3})\.JPG$',       re.I), 2),
    (re.compile(r'^Photo Memories 01_(\d{3})\.JPG$', re.I), 3),
]


def load_status_map():
    """Return {(book, page): status} from the CSV. Any status excludes the page from the queue."""
    status = {}
    if not CSV_PATH.exists():
        return status
    with CSV_PATH.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            page_id = row['page']  # e.g. "book-001/071"
            m = re.match(r'book-(\d{3})/(\d{3})', page_id)
            if m:
                status[(int(m.group(1)), int(m.group(2)))] = row.get('status', 'enhanced')
    return status


def md_enhanced(book, page):
    p = ROOT / 'src' / 'books' / f'book-{book:03d}' / 'pages' / f'{page:03d}.md'
    if not p.exists():
        return None
    try:
        return 'transcription_pass: enhanced' in p.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min-px', type=int, default=4000,
                    help='Minimum width AND height in pixels (default: 4000)')
    args = ap.parse_args()

    status_map = load_status_map()

    results = {b: {'total': 0, 'large': 0, 'enh': 0, 'def': 0, 'unenh': 0} for b in (1, 2, 3)}
    unenh_list = []
    deferred_list = []

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
        if w < args.min_px or h < args.min_px:
            continue
        results[book]['large'] += 1

        csv_status = status_map.get((book, page))
        is_enh = csv_status == 'enhanced' or md_enhanced(book, page) is True
        is_deferred = csv_status and csv_status.startswith('deferred')

        if is_enh:
            results[book]['enh'] += 1
        elif is_deferred:
            results[book]['def'] += 1
            deferred_list.append((book, page, w, h, csv_status))
        else:
            results[book]['unenh'] += 1
            unenh_list.append((book, page, w, h))

    print(f'=== Per-book (threshold: {args.min_px} x {args.min_px} px) ===')
    for b in (1, 2, 3):
        v = results[b]
        print(f'book-{b:03d}: total={v["total"]:4d}  large={v["large"]:4d}  '
              f'enhanced={v["enh"]:4d}  deferred={v["def"]:4d}  unenhanced={v["unenh"]:4d}')

    tot_large = sum(v['large'] for v in results.values())
    tot_enh = sum(v['enh'] for v in results.values())
    tot_def = sum(v['def'] for v in results.values())
    tot_unenh = sum(v['unenh'] for v in results.values())
    print()
    print('=== Totals ===')
    print(f'Large scans (>= {args.min_px}x{args.min_px} px): {tot_large}')
    print(f'  Enhanced:                                       {tot_enh}')
    print(f'  Deferred:                                       {tot_def}')
    print(f'  Unenhanced (eligible for next batch):           {tot_unenh}')

    print()
    print('=== First 20 large+unenhanced (in page order) ===')
    for b, p, w, h in unenh_list[:20]:
        print(f'  book-{b:03d}/p{p:03d}  {w}x{h}')

    print()
    print('=== Top 30 large+unenhanced (sorted by pixel area, biggest first) ===')
    by_area = sorted(unenh_list, key=lambda t: t[2] * t[3], reverse=True)
    for b, p, w, h in by_area[:30]:
        mp = (w * h) / 1_000_000
        print(f'  book-{b:03d}/p{p:03d}  {w}x{h}  ({mp:.1f} MP)')

    if deferred_list:
        print()
        print(f'=== Deferred ({len(deferred_list)}) ===')
        for b, p, w, h, st in deferred_list:
            print(f'  book-{b:03d}/p{p:03d}  {w}x{h}  ({st})')


if __name__ == '__main__':
    main()
