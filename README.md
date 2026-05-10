# The FitzSimons Family Archive

A digital archive of two family scrapbooks documenting the FitzSimons family of
Charleston, S.C. — emigrants from Dundalk, Ireland, with branches into the
Hampton, Hammond, Pritchard, Stoney, and Gaillard families of South Carolina.
Scanned pages are presented alongside transcriptions of the handwritten
material.

**Live site:** https://nancys-book.goodhunter.workers.dev/

## Running locally

```bash
npm install      # Node 22
npm run dev      # serves at http://localhost:8080
npm run build    # one-shot build into _site/
```

## How it's hosted

Cloudflare Pages, auto-deployed on every push to `main`. Build configuration
lives in `wrangler.jsonc`. The GitHub Actions workflow at
`.github/workflows/deploy.yml` is a GitHub Pages fallback path; it isn't
currently in use.

## Adding a transcribed page

The site is plain Markdown + Nunjucks under `src/`. The People and Places
indexes are auto-generated from each page's frontmatter at build time — no
database, no CMS.

- [`docs/transcription-style-guide.md`](docs/transcription-style-guide.md) —
  conventions for transcribing handwriting and tagging metadata.
- [`docs/page-template.md`](docs/page-template.md) — frontmatter template for
  a new page.

## Original scans

The 4000-pixel archival scans aren't stored in this repository — they're too
large. They live on an external drive plus a cloud backup. The
`scripts/optimize-images.sh` helper resizes them into web-ready JPEGs for
`src/books/book-NN/images/web/`.

## License

Family content (transcriptions, images): all rights reserved by the family.
Site code: MIT.
