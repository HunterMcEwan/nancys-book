# Fitz Simons Family Archive

A digital archive of two family scrapbooks documenting the Fitz Simons family
of Charleston, S.C. — emigrants from Dundalk, Ireland, with connections to the
Hampton, Hammond, Pritchard, Stoney, and Gaillard families of South Carolina.

This repository contains scanned images of the original albums alongside
transcribed text of the handwritten material. The site is built with
[Eleventy](https://www.11ty.dev/) and deployed as a static site.

---

## Quick start

```bash
# Install dependencies (Node 22 required — verified on Cloudflare Pages)
npm install

# Run the local dev server (auto-rebuilds on save)
npm run dev
# → opens at http://localhost:8080

# Build the production site into _site/
npm run build
```

---

## How the archive is organized

```
src/books/
├── book-01/
│   ├── book-01.json        ← book metadata (title, dates, etc.)
│   ├── images/web/         ← optimized images for the website
│   │   ├── 001.jpg
│   │   ├── 002.jpg
│   │   └── ...
│   └── pages/              ← one Markdown file per scanned page
│       ├── 001.md
│       ├── 002.md
│       └── ...
└── book-02/
    └── (same structure)
```

**One image = one page = one Markdown file.** The Markdown file holds the
transcription plus metadata (people mentioned, places, dates). The site
auto-generates indexes from this metadata.

### Original (archival) scans

The 4000+ pixel original scans are **not** stored in this Git repository — they're
too large and they're irreplaceable. Keep them on:

- An external drive (primary)
- A cloud backup (Backblaze B2 is ~$6/year for this volume, or any other
  cloud storage you trust)

The `images/web/` folder holds web-optimized versions (~1800px wide, ~300KB)
generated from the originals using the script in `scripts/`.

---

## Adding a new transcribed page

1. **Place the optimized image** at `src/books/book-XX/images/web/NNN.jpg`
2. **Create the transcription file** at `src/books/book-XX/pages/NNN.md`:

   ```markdown
   ---
   title: "Memorandum of the Fitz Simons Family"
   book: 1
   page: 3
   image: 003.jpg
   date_range: "1762–1873"
   people:
     - Christopher Fitz Simons (the emigrant)
     - Catherine Pritchard
   places:
     - Dundalk, Ireland
     - Charleston, SC
   content_types:
     - family tree
     - memorandum
   transcribed: true
   notes: ""
   ---

   # Your transcription here

   Use Markdown. Reference people with `[[double brackets]]` to auto-link
   to their person page (this transforms during build).
   ```

3. **Commit and push** — the site rebuilds automatically on Cloudflare Pages.

See `docs/transcription-style-guide.md` for conventions on handling marginalia,
uncertain readings, struck-through text, etc.

---

## The image optimization script

To convert original scans into web-ready images:

```bash
# Requires ImageMagick (brew install imagemagick / apt install imagemagick)
./scripts/optimize-images.sh /path/to/original/scans src/books/book-01/images/web
```

This resizes to 1800px max dimension, sets quality to 85%, strips EXIF
metadata, and uses progressive encoding for faster loading.

---

## Deploying to Cloudflare Pages

1. Push this repository to GitHub
2. In Cloudflare Pages, connect your GitHub account and select this repo
3. Set the build configuration:
   - **Build command:** `npm run build`
   - **Build output directory:** `_site`
   - **Node version:** `22` (set as environment variable `NODE_VERSION`)
4. Deploy. You'll get a URL like `fitzsimons-archive.pages.dev`
5. (Optional) Add a custom domain in Cloudflare Pages settings (~$12/year
   if you register one through Cloudflare)

GitHub Pages also works — just enable Pages in repo settings and point it
at the `_site` folder built by GitHub Actions. Sample workflow in
`.github/workflows/deploy.yml`.

---

## The master spreadsheet

`data/master-index.csv` is the human-readable master index of every image in
the archive. It's redundant with the Markdown frontmatter but useful for:

- Quick searches in Excel/Numbers/Google Sheets
- Tracking transcription progress
- Working with relatives who don't want to clone a Git repo

Update it whenever you add a new transcription. (A future enhancement could
auto-generate it from the Markdown files.)

---

## Adding search later

When you're ready, [Pagefind](https://pagefind.app/) drops in cleanly:

```bash
npm install -D pagefind
# add to package.json scripts:
#   "build": "eleventy && pagefind --site _site"
```

Then add `<div id="search"></div>` plus the Pagefind UI script to your base
layout. No backend, no API keys, no cost — it indexes the static site at
build time.

---

## License

Family content (transcriptions, images): all rights reserved by the family.
Site code: MIT.
