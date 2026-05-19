# Transcription Style Guide

Conventions for transcribing the FitzSimons family scrapbooks. Following these
keeps the archive consistent and makes the result genuinely useful for
researchers and family.

## Core principle

**Fidelity to the original, with light editorial help for the modern reader.**
Preserve the writer's spelling, punctuation, and abbreviations. Add only the
typographic conventions a reader needs (italicizing where the original was
clearly emphatic, structuring with headings where the original used spatial
layout).

## Markup conventions

| Convention             | Used for                                            | Example                                        |
| ---------------------- | --------------------------------------------------- | ---------------------------------------------- |
| `[uncertain]`          | A word the transcriber can read but isn't sure of   | "the [Saunderville] road"                       |
| `[illegible]`          | A word that cannot be read at all                   | "buried in [illegible] churchyard"              |
| `*[editorial note]*`   | Anything inserted by the transcriber                | `*[The inscription continues off the page.]*`   |
| `*italic*`             | Words underlined or emphasized in the original      | He said *"They were very nice people."*         |
| `**bold**`             | Names, dates, headings on the original page         | **Christopher Fitz Simons**                    |
| `> blockquote`         | Quoted material — letters, inscriptions, clippings  | See gravestone inscriptions                     |
| `~~strikethrough~~`    | Text struck through in the original                 | "received as her dower" *(struck through)*      |
| `\[bracketed text]`    | Text supplied by the transcriber to fill a gap      | "A purer and more perfect spirit \[never] animated" |

## Spelling and grammar

- **Preserve** original spellings, even archaic or inconsistent ones (*née* vs. *nee*; *Sandersville* vs. *Sandersville*; *Fitz Simons* vs. *FitzSimons* — the family used both).
- **Preserve** punctuation and capitalization where possible. Exception: replace double dashes (`--`) with em dashes (`—`) and straight quotes with curly quotes.
- **Preserve** abbreviations as written (*Esq.*, *Col.*, *Gov.*, *S.C.*, *Ga.*).

## Names

- **In metadata** (frontmatter `people:`, `title:`, `notes:`, and modern editorial prose): standardize the surname as `FitzSimons` — one word, capital S. This is the modern conventional form; using it consistently in metadata lets the People index aggregate references regardless of how each individual scribe spelled the name. Use the fullest form with parenthetical disambiguators where needed:
  - `Christopher FitzSimons (the emigrant)`
  - `Christopher FitzSimons (2nd)`
  - `Catherine FitzSimons (Mrs. Hammond)` — to distinguish from her mother
- **In body transcription text**: reproduce the spelling the writer used (the family wrote both `Fitz Simons` and `FitzSimons`; the original page is the authority).
- For married women, list both maiden and married names in metadata where known: *Catherine Pritchard*, *Mrs. Hammond née FitzSimons*.

## Decoding the compiler's hand — Amy FitzSimons

Most of the handwritten content in these albums is in the hand of **Amy Ann
Perry FitzSimons** (1888–1973), the compiler. Two of her letterforms cause
frequent, predictable misreads. When you see one of these "ghost letters,"
re-read in context before transcribing:

### Capital **D** that looks like **H**

Amy's capital D often leaves its top loop unclosed — the upper-right curve
sweeps over without quite meeting the descending stroke. To a modern eye
that sees a vertical stroke with a separate top curve, it reads as **H**.
This is the single most common misread in the album and it always changes
meaning materially. Confirmed instances so far:

- **Dad** → mistranscribed as **Had** (her father, Samuel Gaillard
  FitzSimons Sr.; appears on virtually every memoir page)
- **Dunkin** Perry FitzSimons → **Hunkin** / **Hunter Perry** (her
  infant brother who died on her 7th birthday; cf. book-001 p630)
- **Dee** Walker (Emma Dee Walker Corbell, her middle daughter) →
  **Ilee** (the H form here was further mistranscribed as Il)
- **Duncan** Wragg → **Hunkin** (1881 letterhead, p339)

When the cursive *could* be H but the context wants a D-word (a
relative's known nickname, "Dad," "Dear," a date, a place), trust
context and write the D form. If you're keeping a `*[uncertain]*`
annotation, prefer the D reading.

### Other recurring patterns

- "Kit" (the family nickname for Christopher) is sometimes misread as
  "Hit." Kit is *always* the right reading — he is Amy's paternal uncle
  Christopher FitzSimons Jr. (1856–1925).
- Long-tailed lowercase **s** at the end of a word (especially in
  proper nouns) can read as an ornamented **g** or **y**.

### When you fix one of these, fix it — don't comment on it

The transcription is what the reader sees. If you detect a D-cursive
misread on an already-transcribed page, **edit the body** to the correct
reading; do not leave the misread in place and explain it in the AI Notes
panel. (A reader-facing note saying *"'Had' here is a misread of cursive
D"* is a bug — the correct form is to write *"Dad"* in the body and say
nothing.) Editorial annotation belongs on genuine ambiguities, not on
errors the transcriber has already resolved.

## Dates

- Use `date_range` in frontmatter, formatted as `YYYY` or `YYYY–YYYY` (en-dash, not hyphen).
- In body text, reproduce dates as written.

## Places

- In metadata, use a consistent form: `City, State` for U.S.; `City, Country` for international.
- "Plantation" or "burial ground" names go before the location: `Hobcaw, Christ Church Parish, SC`.

## Content types

Use these tags in the `content_types:` frontmatter field — these are the categories that surface in the metadata sidebar:

- `family tree` — pedigree charts
- `memorandum` — narrative family history
- `letter` — correspondence
- `envelope` — pasted-in addressed envelopes
- `newspaper clipping` — pasted clippings
- `inscription` — gravestone or monument text
- `photograph` — pasted photographs
- `obituary`
- `marriage notice`
- `family anecdote` — recorded oral history
- `recipe`
- `legal document`
- `epigraph` — an inscribed quotation, often a frontispiece or section opener
- `ephemera` — anything else (calling cards, programs, receipts, etc.)

## Blank or untranscribed pages

If a page has no text to transcribe (a blank album page, or a photograph
without caption), still create the `.md` file with `transcribed: false` and a
brief note in the body:

```markdown
---
title: "Photograph: unidentified woman, undated"
page: 47
image: 047.jpg
transcribed: false
content_types:
  - photograph
notes: "Unidentified. Possibly a FitzSimons or Walker descendant. Tintype, ca. 1880s."
---

*This page contains no transcribable text. See notes.*
```

This keeps the archive complete — every scanned page has a corresponding
entry, even when there's nothing written to read.

## Keep methodology out of user-facing content

The `notes:` field and body annotations are shown to readers of the published
site. State findings directly. Don't narrate the transcription process or
which pass produced what — readers don't know what "phase 1", "phase 2",
"enhanced pass", "first pass", or "on re-read" mean, and shouldn't have to.

- **Bad:** *"Phase-2 enhanced pass confirmed the captions; no corrections required."*
- **Good:** Just write the cleanest current rendering and let the page speak.
- **Bad:** *"Phase-1 had 'Lydia C. Bullard'; corrected to 'Lydia C. Gaillard' on the enhanced pass."*
- **Good:** *"The recipient is **Lydia C. Gaillard**."*

If a discrepancy is worth surfacing because the page itself records both
readings, frame it editorially ("the source's '30th' conflicts with the dates
on the same line"), not as a pass-to-pass diff. Save methodology, dates, and
pass-name framing for commit messages, `data/enhanced-pages.csv`, and
`FAMILY-NOTES.md`.

## When in doubt

Err toward **including more context in editorial notes** rather than less.
Future readers — including descendants generations from now — will appreciate
knowing why an envelope was kept, who a person was, or what a place reference
meant.
