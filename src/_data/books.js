// Per-book display metadata. Keyed by the `book` value in each page's
// frontmatter. Templates use this to render labels for each volume so the
// book number is the only thing pages need to know about.
module.exports = {
  1: {
    label: "Volume 1",
    title: "Album of Memories, Book 1",
    unit: "page",
  },
  2: {
    label: "Volume 2",
    title: "Album of Memories, Book 2",
    unit: "page",
  },
  3: {
    label: "Keepsakes",
    title: "Photo Memories",
    unit: "item",
  },
  4: {
    label: "Appendix",
    title: "Appendix & Supporting Documents",
    unit: "document",
  },
};
