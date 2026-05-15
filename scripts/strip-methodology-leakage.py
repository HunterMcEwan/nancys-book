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
    # Pattern B1: leading "Phase 2: " in editorial bracket (no "enhanced pass")
    (
        "leading 'Phase N:' inside editorial bracket",
        re.compile(r"\*\[Phase[-\s]?\d\s*:\s*", re.IGNORECASE),
        "*[",
    ),
    # Pattern B2: "Phase-2 corrections:" header inside a notes block / line
    (
        "'Phase-N corrections:' heading",
        re.compile(r"Phase[-\s]?\d\s+corrections?\s*:\s*", re.IGNORECASE),
        "",
    ),
    # Pattern B3: inline "(phase-1 fabrication[s])" / "(phase-N reading)" parentheticals
    (
        "parenthetical '(phase-N fabrication/reading/etc.)'",
        re.compile(
            r"\s*\((?:both\s+)?phase[-\s]?\d\s+(?:fabrications?|reading|guess(?:es)?|error(?:s)?|brackets?)\)",
            re.IGNORECASE,
        ),
        "",
    ),
    # Pattern B4: trailing/inline "as Phase 1 stated/had it/etc."
    (
        "inline 'as Phase N stated/had it/read it/has it'",
        re.compile(
            r",?\s+as\s+phase[-\s]?\d\s+(?:stated|had\s+it|read\s+it|has\s+it|did)",
            re.IGNORECASE,
        ),
        "",
    ),
    # Pattern B5: "many phase-1 brackets" → "many uncertain readings"
    (
        "'phase-N brackets' substitution",
        re.compile(r"phase[-\s]?\d\s+brackets", re.IGNORECASE),
        "uncertain readings",
    ),
    # Pattern B6: trailing/inline "the Phase 1 transcription/draft was/is X"
    (
        "'the Phase N transcription is...' phrasing",
        re.compile(
            r"\s*the\s+phase[-\s]?\d\s+(?:transcription|draft|reading)\s+(?:is|was)\s+",
            re.IGNORECASE,
        ),
        " the earlier transcription was ",
    ),
    # Pattern B7: parenthetical "(Phase 1)" / "(Phase-1)" / "(Phase 2)" qualifier
    (
        "bare parenthetical '(Phase N)' qualifier",
        re.compile(r"\s*\(phase[-\s]?\d\)", re.IGNORECASE),
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
    # Cleanup preserves leading whitespace (critical for YAML block scalars
    # where each line carries a fixed indent — collapsing it produces invalid YAML).
    old_lines = text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    if len(old_lines) == len(new_lines):
        cleaned: list[str] = []
        for old, new in zip(old_lines, new_lines):
            if old == new:
                cleaned.append(new)
                continue
            # Split into leading whitespace + body + trailing newline
            m = re.match(r"^(\s*)(.*?)(\r?\n?)$", new, re.DOTALL)
            if m:
                leading, body, trailing = m.group(1), m.group(2), m.group(3)
                body = re.sub(r" {2,}", " ", body)
                body = re.sub(r"\.\s*\.+", ".", body)
                cleaned.append(leading + body + trailing)
            else:
                cleaned.append(new)
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
