"""Find user-facing methodology leakage in page .md files.

Scans `src/books/*/pages/*.md` for phrases that narrate the transcription
process (Phase 1/2, enhanced pass, first/second/2nd pass, "on re-read",
etc.) and would confuse a casual reader who doesn't know what those
internal pass-names mean.

Skips the legitimate frontmatter field `transcription_pass:` — that's a
metadata field, not user-facing prose.

Usage:
    py scripts/find-methodology-leakage.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Regexes for leaky phrases. Case-insensitive.
LEAKY = re.compile(
    r"phase[\s\-]?[12]\b"
    r"|phase\s*[12]"
    r"|first[\s\-]?pass\b"
    r"|2nd\s+pass\b"
    r"|second\s+pass\b"
    r"|enhanced\s+(transcription|pass|re[\-\s]?read|crop|reading)"
    r"|on\s+re[\-\s]?read\b"
    r"|methodology\b",
    re.IGNORECASE,
)

# Lines to skip: the transcription_pass: frontmatter field, and the
# enhanced-transcription-procedure / phase2-annotation-guide narrative refs.
SKIP_LINE = re.compile(r"^\s*transcription_pass\s*:", re.IGNORECASE)


def scan_file(p: Path) -> list[tuple[int, str]]:
    matches: list[tuple[int, str]] = []
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return matches
    for i, line in enumerate(text.splitlines(), start=1):
        if SKIP_LINE.search(line):
            continue
        if LEAKY.search(line):
            matches.append((i, line.strip()))
    return matches


def main():
    base = ROOT / "src" / "books"
    by_pattern: dict[str, int] = {}
    files_with_leakage: list[tuple[Path, list[tuple[int, str]]]] = []
    for md in sorted(base.glob("book-*/pages/*.md")):
        m = scan_file(md)
        if m:
            files_with_leakage.append((md, m))
            for _, line in m:
                # bucket by leaky phrase
                hit = LEAKY.search(line)
                if hit:
                    key = hit.group(0).lower()
                    by_pattern[key] = by_pattern.get(key, 0) + 1

    print(f"Files with leakage: {len(files_with_leakage)}")
    print(f"Total lines with leakage: {sum(len(m) for _, m in files_with_leakage)}")
    print()
    print("=== By leaky phrase ===")
    for k, v in sorted(by_pattern.items(), key=lambda kv: -kv[1]):
        print(f"  {v:5d}  {k}")

    print()
    print("=== Sample lines (first 30 files) ===")
    for md, hits in files_with_leakage[:30]:
        rel = md.relative_to(ROOT).as_posix()
        for line_no, line in hits[:3]:
            print(f"  {rel}:{line_no}: {line[:160]}")
        if len(hits) > 3:
            print(f"  ... +{len(hits)-3} more lines")


if __name__ == "__main__":
    main()
