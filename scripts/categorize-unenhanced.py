"""List remaining unenhanced pages grouped by their primary content_type.

Reads the find-large-unenhanced output (>= 2000x2000) and joins each page's
frontmatter to surface which document types still need an enhanced pass.

Usage:
    py scripts/categorize-unenhanced.py
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter_content_types(md_path: Path) -> list[str]:
    if not md_path.exists():
        return []
    text = md_path.read_text(encoding='utf-8', errors='replace')
    # Match the frontmatter block only
    m = re.match(r'^---\r?\n(.+?)\r?\n---', text, re.DOTALL)
    if not m:
        return []
    fm = m.group(1)
    # Find content_types: block (YAML list)
    types_m = re.search(r'(?m)^content_types:\s*\r?\n((?:[ \t]+-[^\n]*\r?\n?)+)', fm)
    if not types_m:
        return []
    block = types_m.group(1)
    items = []
    for line in block.splitlines():
        s = line.strip()
        if s.startswith('-'):
            items.append(s.lstrip('- ').strip().strip('"\''))
    return items


def main():
    # Get the list of unenhanced pages from find-large-unenhanced
    result = subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'find-large-unenhanced.py'), '--min-px', '2000'],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    lines = (result.stdout + result.stderr).splitlines()

    # The script doesn't print all pages — only first 20 + top 30. We need our own
    # walk over every md file to find unenhanced ones.
    pages = []
    for book_dir in sorted((ROOT / 'src' / 'books').glob('book-*')):
        book = book_dir.name  # e.g. "book-001"
        for md in sorted((book_dir / 'pages').glob('*.md')):
            text = md.read_text(encoding='utf-8', errors='replace')
            if 'transcription_pass: enhanced' in text:
                continue
            # Only include pages where transcribed: true (handwritten content)
            if 'transcribed: true' not in text:
                continue
            pages.append((book, md.stem, md))

    print(f"Total unenhanced + transcribed pages: {len(pages)}")
    print()

    # Group by primary content_type
    by_type: dict[str, list[str]] = {}
    no_types: list[str] = []
    for book, stem, md in pages:
        types = parse_frontmatter_content_types(md)
        if not types:
            no_types.append(f"{book}/{stem}")
            continue
        # Use the first content_type as primary; also track all
        for t in types:
            by_type.setdefault(t, []).append(f"{book}/{stem}")

    print("=== By content_type ===")
    for t, ps in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
        print(f"  {len(ps):3d}  {t}")
        for p in ps:
            print(f"        {p}")
    if no_types:
        print(f"\n  {len(no_types):3d}  (no content_types field)")
        for p in no_types:
            print(f"        {p}")


if __name__ == '__main__':
    main()
