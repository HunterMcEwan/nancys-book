# Phase 2 annotation guide

Phase 1 produced literal transcriptions of every scrapbook page. **Phase
2 adds brief editorial annotations** that give modern readers historical
and biographical context the page itself doesn't supply.

Annotations are *supplements* to transcription, never corrections of it.
(Corrections live in the enhanced-transcription pass — see
`docs/enhanced-transcription-procedure.md`.)

## Goal

When a reader lands on a page, can they understand what they're looking
at? If "Wade Hampton" appears with no context and the reader is a casual
visitor, a one-sentence editorial line — "Wade Hampton III (1818–1902),
the Confederate cavalry general and later governor of South Carolina,
the eldest son of Ann FitzSimons + Wade Hampton II — is the family's
most prominent kinsman" — turns a name into a person. That's the win.

## When to add an annotation

Add one when at least one of these is true:

- The page references a **major historical figure** (Wade Hampton, J. H.
  Hammond, Francis Marion, Robert Browning, etc.) without identifying
  them as such.
- The page is a **letter or document** whose author / date / addressee
  isn't obvious from the body.
- The page records a **practice, custom, or object** that may be
  unfamiliar to modern readers (e.g., photographing painted portraits;
  refugeeing to upcountry; the Confederate paroles system).
- The page references a **historical event** whose significance isn't
  apparent in the text (battles, epidemics, political moments).
- The page contains a **family connection invisible to a casual reader**
  but established elsewhere in the archive or in `FAMILY-NOTES.md`
  (e.g., "the writer is the compiler's uncle").
- The page contains a **date or place that locates the document
  precisely** in a wider event (e.g., a letter dated two weeks after
  Wade Hampton's Gettysburg wounding).

## When to SKIP

Mark `skip` and explain why if any of these apply:

- **Routine 20th-century personal correspondence** (birthday cards,
  household news, "thanks for the visit") that's self-explanatory.
- The page is **already saturated with editorial notes** from an
  enhanced-transcription pass — adding more would be redundant.
- **Blank pages, simple ephemera, or photographs without text** that
  don't carry historical hooks.
- The page is a **direct continuation** of a previous page whose
  annotation already covers the relevant context.
- Pages where the frontmatter `notes:` field **already supplies** what
  a Phase 2 annotation would add. (In that case, judge: would moving the
  note into the body as an italic-bracket annotation actually help the
  reader? If not, skip.)

Skip generously. Better to leave a page untouched than to add filler.

## Format

The annotation is an **italic-bracket paragraph** appended at the
natural end of the page body, after the last transcribed content:

```markdown
*[The two paintings are likely 19th-century likenesses of Christopher
FitzSimons (1762–1825) and his wife Catherine Pritchard FitzSimons
(1772–1841). Photographing painted portraits and mounting the
photographs into family albums was a common late-nineteenth-century
practice — a way to circulate likenesses of ancestors that otherwise
existed as one-of-a-kind oils.]*
```

Or — if the annotation pertains to a specific passage rather than the
whole page — **interleave** it directly after the relevant block:

```markdown
> Genl. H. was again wounded —

*[Wade Hampton III was wounded three times at Gettysburg, 2–3 July
1863; this letter, dated 16 July 1863, is reacting to the news roughly
two weeks later.]*
```

Use the second form sparingly — it interrupts the original document's
flow. Default to end-of-page.

## Style

- **Third person, editorial voice.** No "I" or "we."
- **Brief.** 1–3 sentences typically. A short paragraph is the
  maximum. If you find yourself writing more than that, you're probably
  trying to cover too much.
- **Present tense for general claims; past tense for historical
  events.** ("Wade Hampton III *is* the family's most prominent
  kinsman. He *was wounded* three times at Gettysburg.")
- **Don't repeat the page.** If the body already says "this is Cousin
  Sam's letter from 1862," don't open with "This is a letter from
  Cousin Sam dated 1862."
- **Don't repeat the frontmatter `notes:` field.** It does its own
  job; the body annotation should add something the notes don't.
- **No speculation about intent.** "The compiler probably wanted to
  honor her mother" is a guess. State facts; let readers infer.
- **Editorial brackets only.** Do not modify the original transcribed
  text inside the annotation. Don't rewrite blockquotes.
- **No methodology metadata in user-facing content.** Anything in the
  `notes:` field or in the body's italic-bracket annotations is shown
  to readers. Don't include phrases like "Phase-2 (2026-05-13):",
  "full-resolution re-read", "rotated re-scan", "crop+rotate", or
  internal pass names — those are implementation details. State the
  finding directly: instead of *"Phase-2 (2026-05-14) margin re-scan
  recovered the full note"*, just say *"The pencilled marginal note
  reads:"* and quote it. Reasoning about how you arrived at the
  reading belongs in the commit message, not on the published page.

## Linking

Wikipedia links are encouraged for **major historical figures or
events** the page mentions, formatted as Markdown links:

```markdown
[Wade Hampton III](https://en.wikipedia.org/wiki/Wade_Hampton_III)
[Battle of Brandy Station](https://en.wikipedia.org/wiki/Battle_of_Brandy_Station)
```

Guidelines:

- One or two links per annotation is plenty; don't paper the page with
  blue.
- Don't link minor names or family members — only figures with their
  own substantive Wikipedia article.
- Don't link to `FAMILY-NOTES.md` or `HISTORICAL-CONTEXT.md` (they're
  gitignored; they'd 404 on the published site).
- For **cross-references within the album**, use plain prose: *"See
  page 003 for the family memorandum that opens this thread."*

## Web search policy

Subagents are **empowered and encouraged to use web search** when
needed. Specifically:

- **Verify any historical claim before stating it.** Don't rely on
  training knowledge alone for dates, biographies, regiment details,
  or place facts.
- **Find the canonical Wikipedia URL** for a figure mentioned in the
  page, when one exists.
- **Resolve ambiguous references** that aren't covered in
  `FAMILY-NOTES.md` or `HISTORICAL-CONTEXT.md`.
- **Discover context** that would enrich the annotation but isn't
  obvious — e.g., what specific yellow-fever outbreak was active in
  Charleston in the year a letter was written.

Accuracy beats coverage. If you can't verify a claim, leave it out.

## Examples

### Good — adds non-obvious context

> *[Photographing painted portraits and mounting the photographs into
> family albums was a common late-nineteenth-century practice — a way
> to circulate likenesses of ancestors that otherwise existed as
> one-of-a-kind oils.]*

### Good — identifies and connects

> *[The writer is **Gaillard Stoney FitzSimons** (likely b. 1860s,
> d. after 1944), one of Dr. Christopher FitzSimons (3rd)'s seven
> children, writing from Hendersonville NC to his niece **Amy
> FitzSimons Walker**. See page 003 for the family tree placing him.]*

### Good — situates a letter in its historical moment

> *[The letter's reference to "Genl. H. ... again wounded" places the
> writing about two weeks after [Wade Hampton III](https://en.wikipedia.org/wiki/Wade_Hampton_III)'s
> wounding at Gettysburg on 3 July 1863.]*

### Good — flags a practice unfamiliar to modern readers

> *[Refugeeing — temporarily relocating with household and enslaved
> labor to upcountry South Carolina or the NC mountains to avoid the
> Union blockade and bombardment of Charleston — was the standard
> Lowcountry gentry response from 1862 onward. **Walhalla**, a
> German-colonization town in Oconee County, was a common destination.]*

### AVOID — repeats the page

> *[The page contains two photographs of family portraits with
> handwritten captions identifying the subjects.]*

The body already says exactly this. The annotation adds nothing.

### AVOID — overlong

> *[Wade Hampton III was born March 28, 1818, in Charleston, son of
> Wade Hampton II and Ann FitzSimons. He was educated at South
> Carolina College, graduated in 1836, and married Margaret Preston in
> 1838. He inherited Millwood, became a state senator in 1858, and
> raised Hampton's Legion in 1861...]*

Too long. The reader doesn't need a biography; they need a hook. One
sentence + a link.

### AVOID — speculation

> *[The compiler probably mounted these two portraits side by side as
> a deliberate evocation of her great-grandparents' founding role in
> the family.]*

We don't know that. Don't put thoughts in the compiler's head.

## Tracking

Append a row to `data/phase2-pages.csv` for every page touched (added,
skipped, or judged already-done):

```
page,date_phase2,status,note
book-001/001,2026-05-11,annotated,"Browning identification; frontispiece convention"
book-001/002,2026-05-11,already_done,"Existing annotation covers Phase 2"
book-001/045,2026-05-11,annotated,"Cabinet card practice; Nathalie Ferguson identification"
book-002/232,2026-05-11,skip,"Routine 1950s family note; no historical hook"
```

Status values:

- `annotated` — annotation added in this pass.
- `skip` — judged no annotation needed; the `note` column says why.
- `already_done` — page already carries substantial editorial
  annotation (typically from the enhanced pass); no change made.

## Procedure summary (for subagents)

For each page in your batch:

1. Read the existing page md.
2. Read FAMILY-NOTES.md and HISTORICAL-CONTEXT.md (once per session,
   not per page).
3. Decide: annotate, skip, or already_done.
4. If annotating: web-search to verify any non-obvious claim; draft a
   1–3 sentence italic-bracket annotation; insert it at the end of the
   body (or interleaved, when justified).
5. Append a row to `data/phase2-pages.csv`.
6. Move to the next page.

Total budget per page: under 2 minutes. If a page is taking longer,
ship a `skip` row and move on — better to revisit later than to over-
invest.
