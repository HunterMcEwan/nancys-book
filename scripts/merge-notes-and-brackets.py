#!/usr/bin/env python3
"""
One-time migration: merge trailing italic editorial brackets in page bodies
into the `notes:` frontmatter field.

What it does for each src/books/book-*/pages/*.md page:

1. Read frontmatter and body.
2. Parse the body, walking from the end:
   - Skip blank lines, `---` separators, and lone `*Source: ...*` lines
     (these stay in the body).
   - Collect every trailing italic-bracket paragraph (a paragraph whose
     stripped form starts with `*[` and ends with `]*`).
   - Stop at the first non-bracket, non-source, non-separator paragraph.
3. Drop the collected bracket paragraphs from the body (Source/--- stay).
4. Append the bracket bodies (without the `*[ ... ]*` wrappers) to the
   existing `notes:` value, separated by blank lines.
5. Rewrite the `notes:` field as a YAML block scalar (`notes: |`) so the
   merged content can carry multiple paragraphs cleanly.

INLINE italic brackets that appear in the middle of the body (positional
clarifications like *[best-guess reading]*, *[illegible]*, or
*[Pencilled in red ink:]*) are left untouched.

Idempotent in spirit: running again on already-migrated files finds no
trailing brackets and leaves them alone.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: py -3 -m pip install pyyaml")


ROOT = Path(__file__).resolve().parent.parent
PAGES_GLOB = "src/books/book-*/pages/*.md"


def split_file(text: str) -> tuple[str, str]:
    """Return (frontmatter_text, body_text). Frontmatter excludes the surrounding `---` lines."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("No frontmatter found")
    return m.group(1), m.group(2)


SOURCE_LINE_RE = re.compile(r"^\*[Ss]ource\b.*\*\s*$", re.DOTALL)


def extract_trailing_brackets(body: str) -> tuple[str, list[str]]:
    """
    Walk paragraphs from the end. Pull out trailing italic-bracket
    paragraphs. Return (new_body, extracted_contents_in_doc_order).
    """
    # Preserve the body's leading/trailing whitespace footprint roughly:
    # we split on blank lines and rejoin with '\n\n'.
    paragraphs = re.split(r"\n[ \t]*\n", body.strip("\n"))
    if not paragraphs:
        return body, []

    drop_idx: set[int] = set()
    extracted: list[str] = []

    for i in range(len(paragraphs) - 1, -1, -1):
        s = paragraphs[i].strip()
        if s == "":
            continue
        if s == "---":
            continue
        if SOURCE_LINE_RE.match(s):
            continue
        if s.startswith("*[") and s.endswith("]*"):
            drop_idx.add(i)
            inner = s[2:-2].strip()
            extracted.append(inner)
            continue
        break  # first non-trailing content stops the scan

    if not drop_idx:
        return body, []

    extracted.reverse()  # document order

    kept = [p for i, p in enumerate(paragraphs) if i not in drop_idx]
    # Drop trailing structural-only tails (a lone `---` with nothing after,
    # for instance) — but keep them if a *Source* still follows.
    while kept and kept[-1].strip() == "---":
        kept.pop()

    new_body = "\n\n".join(kept).rstrip() + "\n"
    return new_body, extracted


def find_notes_range(fm_lines: list[str]) -> tuple[int, int] | None:
    """Indices [start, end] (inclusive) of the lines that constitute the notes: field value."""
    start = None
    for i, line in enumerate(fm_lines):
        if re.match(r"^notes\s*:", line):
            start = i
            break
    if start is None:
        return None
    end = start
    for j in range(start + 1, len(fm_lines)):
        line = fm_lines[j]
        # A new top-level YAML key looks like `^[A-Za-z_][\w]*\s*:`
        if re.match(r"^[A-Za-z_][\w]*\s*:", line):
            break
        end = j
    return start, end


def parse_notes_value(fm_text: str) -> str:
    """Use PyYAML to extract the notes value as a Python string, normalizing
    paragraph breaks for the (single) page where notes is a multi-paragraph
    double-quoted scalar (YAML folds the blank line to a lone \\n)."""
    data = yaml.safe_load(fm_text) or {}
    notes = data.get("notes", "") or ""
    # Detect source format: quoted (starts with " or ') vs block-scalar (|, >)
    m = re.search(r"^notes:[ \t]*(\S)", fm_text, re.MULTILINE)
    if m and m.group(1) in ('"', "'"):
        # In a quoted scalar, YAML has already folded blank lines to a
        # single \n. Restore them as paragraph breaks so the merged output
        # renders correctly.
        notes = re.sub(r"(?<!\n)\n(?!\n)", "\n\n", notes)
    return notes


def render_notes_block(text: str) -> str:
    """Render the notes value as a YAML block scalar field (with 2-space indent)."""
    # Preserve internal blank lines; trim outer whitespace.
    content = text.strip("\n").rstrip()
    indented = "\n".join(("  " + line if line else "") for line in content.split("\n"))
    return "notes: |\n" + indented


def transform_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    try:
        fm, body = split_file(text)
    except ValueError:
        return False

    new_body, extracted = extract_trailing_brackets(body)
    if not extracted:
        return False

    current_notes = parse_notes_value(fm)
    pieces = [current_notes.rstrip()] if current_notes.strip() else []
    pieces.extend(extracted)
    merged = "\n\n".join(pieces).strip("\n")

    fm_lines = fm.split("\n")
    rng = find_notes_range(fm_lines)
    if rng is None:
        # No notes: field at all — synthesize one as the last field.
        new_fm = fm.rstrip("\n") + "\n" + render_notes_block(merged)
    else:
        s, e = rng
        new_field = render_notes_block(merged)
        new_fm_lines = fm_lines[:s] + new_field.split("\n") + fm_lines[e + 1:]
        new_fm = "\n".join(new_fm_lines)

    new_text = "---\n" + new_fm.rstrip("\n") + "\n---\n\n" + new_body.lstrip("\n")
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    changed = 0
    total = 0
    for md in sorted(ROOT.glob(PAGES_GLOB)):
        total += 1
        if transform_file(md):
            changed += 1
    print(f"processed {total} pages, modified {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
