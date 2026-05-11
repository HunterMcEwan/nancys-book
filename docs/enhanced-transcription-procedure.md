# Enhanced transcription procedure

The first transcription pass (phase 1) produced one Markdown page per
scrapbook scan with the vision LLM reading the full-page image. That pass
works well on letters and large-script ink, but on dense, faded, or
multi-region pages it produced two kinds of error:

1. **Illegibility gaps** — `[illegible]` and `[uncertain]` markers where
   the model couldn't read the cursive at the effective resolution the
   vision pipeline received.
2. **Hallucinated content** — when faint cursive was filled with
   plausible-but-incorrect period prose. For example, page 026 originally
   carried a multi-paragraph "U.S. Senate / John C. Calhoun" career
   narrative for John Stoney that did not exist on the page; the cursive
   actually described a Charleston merchant's death and an 1821
   newspaper obituary for his father.

The enhanced procedure addresses both. It re-reads candidate pages at
much higher effective resolution by **cropping** them into structural
regions, **enhancing** each crop, and **re-transcribing** each region
with rich context.

## Why cropping matters more than image filters

Claude's vision pipeline server-side downsamples submitted images to a
fixed long-edge ceiling (≈2576 px on the Opus high-res tier). A full
scrapbook page at ~10 inches wide ends up at ~157 effective ppi after
that downsample — at the edge of legibility for fine cursive. The same
ink at the same submitted resolution, cropped to one column, hits
≈300–400 ppi. Cropping is the largest single lever.

Image filters that classical OCR depends on — binarization (Otsu,
Sauvola), aggressive CLAHE, forced grayscale, deskewing — tend to
**hurt** vision-LLM accuracy, because they strip tonal information the
ViT encoder uses. The only filters worth applying after cropping are:

- **Lanczos resize** to the model's long-edge cap.
- **Background flatten** (divide by Gaussian-blurred copy) to neutralize
  yellowing without binarizing.
- **Mild blue-channel weighting** when brown ink is on cream paper —
  brown ink contrasts strongest in the blue channel.

The script `scripts/enhance-crop.py` implements this pipeline.

## When to apply the enhanced procedure

A page is a candidate if **all** of:

- `transcribed: true` (the first pass attempted it),
- the content is handwritten or mixed (typeface pages don't benefit;
  the scan itself is the canonical record), and
- the body contains a non-trivial number of `[illegible]` / `[uncertain]`
  / `[word?]` markers (≥3, or any single dense cluster).

Cross-written pages (two layers of writing at perpendicular angles —
e.g. pages 092, 095, 097) are a separate, harder problem and **not
addressed by this procedure**; cropping and contrast don't separate
overlapping ink layers. Note: the cross-written cluster is NOT
contiguous — pages 093 and 094 are in poor condition but are NOT
cross-written, and are valid candidates for this procedure.

To find candidates, see `data/repass-candidates.json` (regenerate with
the scoring script if pages have changed). To track what has already
been done, see `data/enhanced-pages.csv`.

## The four-step procedure

For each candidate page:

### 1. Layout detection (one vision call)

Pass the full scan to a vision LLM and ask for **structural text
regions**, not specific illegible clusters. Region boundaries are
visually well-defined (paper edges, photo borders, column gutters,
blank gaps) and the model gives reliable coarse coordinates. Cluster
bboxes are too fine-grained and tend to land 50–300 px off, often
crossing column boundaries.

Output schema (JSON):

```json
[
  {
    "region_id": "left_column",
    "description": "left column — pencil cursive narrative",
    "x": 80, "y": 900, "w": 1020, "h": 2800,
    "writing_type": "pencil cursive on cream paper",
    "expected_content": "biographical narrative beginning '…'"
  }
]
```

Aim for **3–6 regions per page**. They should tile the page without
overlap. Exclude photographs and obvious decorative elements from the
text-region bboxes.

### 2. Crop and enhance (one Python call per region)

```
py scripts/enhance-crop.py <src.jpg> <out.png> <x> <y> <w> <h>
```

The script:

- Crops the requested region.
- Lanczos-resizes so the long edge is 2576 px (the Opus high-res cap).
- Applies background flatten via Gaussian-blur division.
- Applies mild blue-channel weighting.
- Saves as PNG.

### 3. Re-transcribe each region (one vision call per region, parallelizable)

Pass each enhanced crop to a fresh vision subagent with **rich context**
extracted from the page's existing frontmatter and a few historical
anchors. The prompt should include:

- Page title, date range, document type.
- The `people:` and `places:` lists from frontmatter (proper-name
  anchors for letterform recognition).
- A short list of likely historical figures and events from the era —
  these act as a sanity check ("if the model claims this person served
  on a Senate committee, but the historical record places their death
  before that body existed, the reading is wrong").
- **The existing draft transcription for that region**, framed
  explicitly as a draft to be corrected — not an answer to confirm.
- Instructions to flag corrections inline using `previous ⇒ corrected`,
  and to **prefer `[illegible]` over a guess** when genuinely unsure.
  Accuracy over coverage.

Have each subagent write its output to a file rather than echo it into
chat (keeps chat context lean; allows parallelism).

### 4. Consolidate into the page's `.md`

Merge the four region transcriptions back into a single `body`,
preserving the original sectional structure (`## Top center`,
`## Left column`, etc.). Update the frontmatter where the new pass
corrected dates, names, or places. Add the marker:

```yaml
transcription_pass: enhanced
```

Then append a row to `data/enhanced-pages.csv` recording the page, the
date the enhanced pass was run, and a one-line note on the most
significant corrections found (this is searchable history when we
later want to know whether a given page has been revised).

## Cost

Per page: roughly 5 vision calls (1 layout + 4 regions) and 100k–200k
tokens. Parallelize the 4 region calls. Page 026 (a dense 3-column
genealogy page) ran with one outlier subagent taking 129 tool calls;
the other three averaged ~30. The outlier was caused by over-iteration
on the chart's structural reconstruction — adding a turn cap to the
subagent prompt is recommended.

## What the procedure does NOT solve

- **Cross-written pages** (two ink layers at right angles): cropping
  and contrast don't separate overlapping strokes. Skipped.
- **Marginalia in the wrong region**: the layout pass tiles the page
  into rectangles, but marginal notes sometimes straddle two regions.
  The re-transcription will catch and report this; consolidation
  requires manual judgment about where the marginalia belongs in the
  final body.
- **Genuinely lost ink**: where paper has foxed badly enough that the
  ink is physically gone, no preprocessing recovers it. The procedure
  reduces over-confident hallucination but cannot conjure absent
  signal.

## Provenance

Procedure developed and validated on page 026 (Stoney–Gaillard family
memorandum). The first run uncovered substantive errors in the
original transcription — wrong birth years (off by ~42), wrong family
name (`Guilland` for `Gaillard`), a fabricated Senate career, a
fabricated plantation name (`Mont Repose` for `Montpellier`, the
family's actual French town of origin), and a missed genealogical
climax (the chart resolves on the compiler herself, **Amy Perry
FitzSimons b. 1888 m. James Pickens Walker**). See
`data/enhanced-pages.csv` for a running log.
