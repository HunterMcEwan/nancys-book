const markdownIt = require("markdown-it");
const markdownItAttrs = require("markdown-it-attrs");
const markdownItFootnote = require("markdown-it-footnote");

module.exports = function (eleventyConfig) {
  // ─── Markdown setup ────────────────────────────────────────────────
  const md = markdownIt({
    html: true,
    linkify: true,
    typographer: true, // turns -- into em-dash, "" into curly quotes
  })
    .use(markdownItAttrs)
    .use(markdownItFootnote);

  eleventyConfig.setLibrary("md", md);

  // ─── Pass-through copy ─────────────────────────────────────────────
  // Images live alongside their Markdown — copy the whole tree
  eleventyConfig.addPassthroughCopy("src/books/**/images/**");
  eleventyConfig.addPassthroughCopy("src/assets");

  // ─── Collections ───────────────────────────────────────────────────
  // All transcribed pages, sorted by book then page number
  eleventyConfig.addCollection("allPages", (collection) => {
    return collection
      .getFilteredByGlob("src/books/**/pages/*.md")
      .sort((a, b) => {
        if (a.data.book !== b.data.book) return a.data.book - b.data.book;
        return a.data.pageNumber - b.data.pageNumber;
      });
  });

  // Pages grouped by book — used for book index pages
  eleventyConfig.addCollection("pagesByBook", (collection) => {
    const pages = collection.getFilteredByGlob("src/books/**/pages/*.md");
    const grouped = {};
    pages.forEach((p) => {
      const book = p.data.book;
      if (!grouped[book]) grouped[book] = [];
      grouped[book].push(p);
    });
    Object.keys(grouped).forEach((b) => {
      grouped[b].sort((a, b) => a.data.pageNumber - b.data.pageNumber);
    });
    return grouped;
  });

  // Auto-generate a people index from frontmatter
  eleventyConfig.addCollection("people", (collection) => {
    const pages = collection.getFilteredByGlob("src/books/**/pages/*.md");
    const peopleMap = {};
    pages.forEach((page) => {
      const people = page.data.people || [];
      people.forEach((person) => {
        if (!peopleMap[person]) peopleMap[person] = [];
        peopleMap[person].push(page);
      });
    });
    return Object.entries(peopleMap)
      .map(([name, pages]) => ({
        name,
        slug: slugify(name),
        pages: pages.sort((a, b) => {
          if (a.data.book !== b.data.book) return a.data.book - b.data.book;
          return a.data.pageNumber - b.data.pageNumber;
        }),
        count: pages.length,
      }))
      .sort((a, b) => a.name.localeCompare(b.name));
  });

  // Auto-generate a places index from frontmatter
  eleventyConfig.addCollection("places", (collection) => {
    const pages = collection.getFilteredByGlob("src/books/**/pages/*.md");
    const placesMap = {};
    pages.forEach((page) => {
      const places = page.data.places || [];
      places.forEach((place) => {
        if (!placesMap[place]) placesMap[place] = [];
        placesMap[place].push(page);
      });
    });
    return Object.entries(placesMap)
      .map(([name, pages]) => ({
        name,
        slug: slugify(name),
        pages: pages.sort((a, b) => {
          if (a.data.book !== b.data.book) return a.data.book - b.data.book;
          return a.data.pageNumber - b.data.pageNumber;
        }),
        count: pages.length,
      }))
      .sort((a, b) => a.name.localeCompare(b.name));
  });

  // ─── Filters ───────────────────────────────────────────────────────
  eleventyConfig.addFilter("slugify", slugify);

  eleventyConfig.addFilter("padPage", (n) => String(n).padStart(3, "0"));

  // Find the previous page within the same book
  eleventyConfig.addFilter("prevPage", (allPages, currentPageNumber, currentBook) => {
    const sameBook = allPages.filter((p) => p.data.book === currentBook);
    const idx = sameBook.findIndex((p) => p.data.pageNumber === currentPageNumber);
    return idx > 0 ? sameBook[idx - 1] : null;
  });

  // Find the next page within the same book
  eleventyConfig.addFilter("nextPage", (allPages, currentPageNumber, currentBook) => {
    const sameBook = allPages.filter((p) => p.data.book === currentBook);
    const idx = sameBook.findIndex((p) => p.data.pageNumber === currentPageNumber);
    return idx >= 0 && idx < sameBook.length - 1 ? sameBook[idx + 1] : null;
  });

  // Sort a collection by frontmatter `order` field (ascending)
  eleventyConfig.addFilter("sortByOrder", (collection) => {
    return [...collection].sort((a, b) => (a.data.order || 0) - (b.data.order || 0));
  });

  // Format an array of strings as a comma-separated list
  eleventyConfig.addFilter("commaList", (arr) => {
    if (!arr || !arr.length) return "";
    return arr.join(", ");
  });

  // Render a string as Markdown (used for the AI Notes panel on each page,
  // whose source comes from YAML frontmatter and is not auto-rendered).
  eleventyConfig.addFilter("markdown", (str) => {
    if (!str) return "";
    return md.render(String(str));
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    templateFormats: ["md", "njk", "html"],
  };
};

// ─── Helpers ─────────────────────────────────────────────────────────
function slugify(str) {
  return String(str)
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // strip diacritics
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
