"""Remove the easy 'Phase-2 enhanced pass confirmed ...; no corrections required'
boilerplate from notes fields and body content of page .md files.

This handles the mechanical, no-content-loss cases. Anything ambiguous is left
alone — those go to a follow-up manual / agent pass.

Usage:
    py scripts/strip-methodology-leakage.py            # dry run, print what would change
    py scripts/strip-methodology-leakage.py --write    # actually modify files
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Patterns we can strip safely. Each is a tuple (description, regex, replacement).
PATTERNS = [
    # Pattern A1: trailing sentence in notes — "Phase-2 enhanced pass confirmed X; no corrections required."
    (
        "trailing 'Phase-N enhanced pass confirmed X; no corrections required' clause",
        re.compile(
            r"(?:\s+)?Phase[-\s]?\d\s+(?:enhanced\s+)?pass\s+(?:confirmed|verified|reviewed)[^.\"\n]*?;?\s*no\s+(?:corrections?|changes|word[-\s]level\s+corrections?|name\s+or\s+date\s+corrections?|substantive\s+changes?)\s+(?:required|needed|made|found)\.?",
            re.IGNORECASE,
        ),
        "",
    ),
    # Pattern A2: standalone tail — "Phase-2 enhanced pass: no corrections."
    (
        "trailing 'Phase-N enhanced pass: no corrections' clause",
        re.compile(
            r"(?:\s+)?Phase[-\s]?\d\s+(?:enhanced\s+)?pass\s*:\s*no\s+(?:corrections?|changes)\.?",
            re.IGNORECASE,
        ),
        "",
    ),
    # Pattern A3: "Enhanced pass confirmed X; no corrections required."
    (
        "trailing 'Enhanced pass confirmed X; no corrections required' clause",
        re.compile(
            r"(?:\s+)?Enhanced\s+(?:transcription\s+)?(?:pass|re[-\s]?read|reading)\s+(?:confirmed|verified)[^.\"\n]*?;?\s*no\s+(?:corrections?|changes|word[-\s]level\s+corrections?)\s+(?:required|needed|made|found)\.?",
            re.IGNORECASE,
        ),
        "",
    ),
    # Pattern A4: leading phrase in editorial bracket — "*[Phase 2 enhanced pass: " -> "*["
    (
        "leading 'Phase N enhanced pass:' inside editorial bracket",
        re.compile(
            r"\*\[Phase[-\s]?\d\s+(?:enhanced\s+)?(?:pass|re[-\s]?read|reading)\s*:\s*",
            re.IGNORECASE,
        ),
        "*[",
    ),
    # Pattern A5: leading phrase "Phase 2 enhanced pass: " in body text
    (
        "leading 'Phase N enhanced pass:' in body text",
        re.compile(
            r"^Phase[-\s]?\d\s+(?:enhanced\s+)?(?:pass|re[-\s]?read|reading)\s*:\s*",
            re.IGNORECASE | re.MULTILINE,
        ),
        "",
    ),
]


def process_file(p: Path, write: bool = False) -> tuple[int, list[str]]:
    """Return (number_of_substitutions, list_of_pattern_descriptions_applied).

    Only modifies the file when at least one leakage pattern actually fired.
    Post-cleanup (doubled-space collapse, repeated periods) is applied only
    to lines that contained a stripped pattern, so we don't churn unrelated
    files with cosmetic whitespace changes.
    """
    text = p.read_text(encoding="utf-8")
    applied: list[str] = []
    new_text = text
    for desc, regex, replacement in PATTERNS:
        candidate, n = regex.subn(replacement, new_text)
        if n > 0:
            applied.append(f"{desc} (x{n})")
            new_text = candidate
    if not applied:
        return (0, [])
    # Only run cleanup on lines that changed, to avoid churning unrelated content.
    old_lines = text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    if len(old_lines) == len(new_lines):
        cleaned: list[str] = []
        for old, new in zip(old_lines, new_lines):
            if old == new:
                cleaned.append(new)
                continue
            polished = re.sub(r" {2,}", " ", new)
            polished = re.sub(r"\.\s*\.+", ".", polished)
            cleaned.append(polished)
        new_text = "".join(cleaned)
    if write and new_text != text:
        p.write_text(new_text, encoding="utf-8", newline="\n")
    return (sum(1 for _ in applied), applied)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Actually modify files")
    args = ap.parse_args()

    base = ROOT / "src" / "books"
    changed = 0
    total_subs = 0
    for md in sorted(base.glob("book-*/pages/*.md")):
        n, applied = process_file(md, write=args.write)
        if n:
            changed += 1
            total_subs += n
            rel = md.relative_to(ROOT).as_posix()
            print(f"{rel}: {n} pattern(s) — {', '.join(applied)}")

    print()
    print(f"Files changed: {changed}")
    print(f"Total pattern substitutions: {total_subs}")
    print(f"Mode: {'WRITE' if args.write else 'DRY RUN — re-run with --write to apply'}")


if __name__ == "__main__":
    main()
