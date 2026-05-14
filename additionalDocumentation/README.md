# additionalDocumentation

Source scans for documents that sit alongside the bound albums but are
not part of them — wills, deeds, news clippings, and other archival
material that the albums reference but do not themselves contain.

Each item here is the unprocessed source image (typically downloaded
from a public archive such as FamilySearch); the web-optimised copies
served from the site live under `src/books/book-004/images/web/` and
are regenerable from these originals via
`scripts/make-web-image.ps1`.

The site presents these as the "Appendix" volume (`book-004`). To add
a new supporting document:

1. Drop the source scan here as `<archive-id>.jpg` (or whatever the
   archive's stable identifier is).
2. Generate the web image:
   ```
   .\scripts\make-web-image.ps1 `
     -Source 'additionalDocumentation\<archive-id>.jpg' `
     -Destination 'src\books\book-004\images\web\<NNN>.jpg'
   ```
3. Generate the thumbnail: `py scripts/make-thumbnails.py 4`
4. Write `src/books/book-004/pages/<NNN>.md` with a transcription,
   frontmatter, and source credit at the foot.

## Current contents

| File                    | Source page              | Site document                            |
| ----------------------- | ------------------------ | ---------------------------------------- |
| `939L-JXS1-PB.jpg`      | Will Book A, p. 198      | book-004/001 — Will of Christopher Fitz Simons (the emigrant's uncle, 1782) — body |
| `939L-JXS1-B7.jpg`      | Will Book A, p. 199      | book-004/002 — Will of Christopher Fitz Simons — closing, witnesses, probate |
| `939L-J49B-9M.jpg`      | Will Book B, p. 963      | book-004/003 — Will of Paul Pritchard (1791) — body opens |
| `939L-J49B-FM.jpg`      | Will Book B, p. 964      | book-004/004 — Will of Paul Pritchard — bequests to children |
| `939L-J49B-G2.jpg`      | Will Book B, p. 965      | book-004/005 — Will of Paul Pritchard — pecuniary legacies and partnership clauses |
| `939L-J49Y-KX.jpg`      | Will Book B, p. 966      | book-004/006 — Will of Paul Pritchard — closing, witnesses, probate |
| `939L-JLSM-7L.jpg`      | Will Book G, p. 1130     | book-004/007 — Will of Christopher Fitzsimons (2nd, 1831) — single page, naming Elizabeth Porcher Fitzsimons sole executrix |
| `939L-JXSZ-WY.jpg`      | Will Book H, p. 834      | book-004/008 — Will of John Stoney (1838) — single page, naming wife Elizabeth and sons P. G. and C. F. Stoney executors |
