"""Detect people-list name variants that slugify to the same path.

Eleventy generates one /people/{slug}/ page per unique name string in the
`people:` frontmatter list across all md files. If two distinct strings
slugify identically (e.g. 'Foo (Sr.)' and 'Foo Sr.', or 'née' and 'nee'
that normalize away the diacritic), the build fails with
DuplicatePermalinkOutputError.

Run this before pushing to catch collisions locally:
    py scripts/check-people-slugs.py

Exits 0 if no collisions, 1 if any are found.
"""
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


def slugify(s):
    """Mirror of the Eleventy slugify in .eleventy.js."""
    s = s.lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')


def main():
    root = Path(__file__).resolve().parent.parent / 'src' / 'books'
    slug_to_names = defaultdict(set)
    for md in root.rglob('*.md'):
        in_people = False
        for line in md.read_text(encoding='utf-8', errors='replace').splitlines():
            if line.startswith('people:'):
                in_people = True
                continue
            if in_people:
                m = re.match(r'^\s\s-\s+(.+?)\s*$', line)
                if m:
                    name = m.group(1)
                    # Strip outer YAML quote-wrapping so '"Foo"' and 'Foo' don't
                    # appear as different names (the YAML parser dedupes them).
                    if (len(name) >= 2 and name[0] == name[-1] == '"') or \
                       (len(name) >= 2 and name[0] == name[-1] == "'"):
                        name = name[1:-1]
                    slug_to_names[slugify(name)].add(name)
                elif not line.startswith(' '):
                    in_people = False

    collisions = {s: names for s, names in slug_to_names.items() if len(names) > 1}
    if not collisions:
        print('OK: no people-slug collisions detected.')
        return 0

    print(f'FAIL: {len(collisions)} colliding slug(s):')
    for slug, names in sorted(collisions.items()):
        print(f'  {slug}:')
        for n in sorted(names):
            print(f'    - {n!r}')
    return 1


if __name__ == '__main__':
    sys.exit(main())
