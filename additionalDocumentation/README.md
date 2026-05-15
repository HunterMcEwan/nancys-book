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

### From a JPG source (FamilySearch image, etc.)

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

### From a PDF source (newspapers.com download, NDNP, etc.)

PDFs are preferred for newspaper material because they preserve the
issue / page / archive-URL metadata bundled by the source. Drop the
PDF in this directory under its native name, then rasterize the
relevant article region:

1. First find the article location by rasterizing the whole page:
   ```
   py scripts/pdf-to-web-image.py `
     additionalDocumentation\<archive-name>.pdf `
     tmp_enh\b4p<NNN>_full.jpg --dpi 200
   ```
2. Open `tmp_enh/b4p<NNN>_full.jpg`, eyeball the article's bounding
   box as fractions of the page (x0,y0,x1,y1 from 0–1). Iterate the
   `--crop` flag until the rendered crop is tight on the article
   text. Drop the result into `src/books/book-004/images/web/`:
   ```
   py scripts/pdf-to-web-image.py `
     additionalDocumentation\<archive-name>.pdf `
     src\books\book-004\images\web\<NNN>.jpg `
     --dpi 300 --crop "x0,y0,x1,y1"
   ```
3. Generate the thumbnail: `py scripts/make-thumbnails.py 4`
4. Write `src/books/book-004/pages/<NNN>.md`. Always cite both the
   newspapers.com / Chronicling-America URL **and** the source PDF
   filename so future readers can recover the full-page context.

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
| `image.jpg`             | Inventory Bk, pp. 302-303 | book-004/009 — Inventory of William Valentine of Charleston (1790), with Christopher Fitzsimons named Executor — also contains unrelated inventories of Joseph Harvey (Oct 1790) and Robert Smith |
| `The_Charleston_Mercury_1825_08_06_3.pdf` | Charleston Mercury, 6 Aug 1825 p.3 | book-004/010 — Obituary tribute to Christopher Fitzsimons the emigrant (signed "W. G. R."); first contemporary confirmation of his service in the SC State Legislature and his War-of-1812 fortification donation |
| `The_Charleston_Daily_Courier_1866_05_19_2.pdf` | Charleston Daily Courier, 19 May 1866 p.2 | book-004/011 — "Fatal Tornado" news brief on the death of Dr. Christopher Fitzsimons at Moss Grove plantation; the primary printed source for the family hand-copy on book-001/p279 |
| `service-ndnp-scu-...-1866051901-0361.pdf` | Charleston Daily News, 19 May 1866 p.5 (NDNP / LCCN sn84026994) | book-004/012 — Independent Daily News notice of the same tornado event; adds time-of-day ("about 1 P.M.") and distance ("about 25 miles from Charleston") not in the Courier account |
| `The_Watchman_and_Southron_1925_10_10_6.pdf` | Watchman and Southron (Sumter), 10 Oct 1925 p.6 | book-004/013 — Obit of Christopher "Kit" FitzSimmons Jr. (the cottonseed-oil pioneer of Columbia); preserves the headline and lede missing from the album clipping on book-001/p308 — pins exact death date 7 Oct 1925 5 P.M. at 1117 Barnwell St, Columbia |
| `The_State_1937_11_15_16.pdf` | The State (Columbia), 15 Nov 1937 p.16 | book-004/014 — Brief obit of Frances Motte Huger FitzSimons (Kit's widow); pins death to 14 Nov 1937 2 A.M. at 1724 Gervais St, Columbia; identifies a previously-unrecorded Huger sister "Mrs. H. V. Sampson of Cincinnati" |
