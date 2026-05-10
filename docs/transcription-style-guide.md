# Transcription Style Guide

Conventions for transcribing the Fitz Simons family scrapbooks. Following these
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

- Use the **fullest form** of a name in metadata, with parenthetical disambiguators where needed:
  - `Christopher Fitz Simons (the emigrant)`
  - `Christopher Fitz Simons (2nd)`
  - `Catherine Fitz Simons (Mrs. Hammond)` — to distinguish from her mother
- In the body text, reproduce the form the writer used.
- For married women, list both maiden and married names where known: *Catherine Pritchard*, *Mrs. Hammond née Fitz Simons*.

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
notes: "Unidentified. Possibly a Fitz Simons or Walker descendant. Tintype, ca. 1880s."
---

*This page contains no transcribable text. See notes.*
```

This keeps the archive complete — every scanned page has a corresponding
entry, even when there's nothing written to read.

## When in doubt

Err toward **including more context in editorial notes** rather than less.
Future readers — including descendants generations from now — will appreciate
knowing why an envelope was kept, who a person was, or what a place reference
meant.
