module.exports = {
  title: "The FitzSimons Family Archive",
  subtitle: "Two scrapbooks of the FitzSimons family of Charleston, S.C.",
  description:
    "A digital archive of family memoranda, letters, photographs, and clippings " +
    "documenting the FitzSimons family — emigrants from Dundalk, Ireland, " +
    "with branches into the Hampton, Hammond, Pritchard, Stoney, and Gaillard " +
    "families of South Carolina.",
  // Update this when you set up a custom domain
  url: "https://nancys-book.goodhunter.workers.dev",
  // Public URL of the Cloudflare R2 bucket holding the 4000px archival
  // originals (no trailing slash). Per-page originals live at:
  //   <originalsUrl>/book-NNN/NNN.jpg
  // Leave empty to fall back to the local web-optimized image for the
  // "Open full size" link. Set after creating the R2 bucket.
  originalsUrl: "",
  // Used in the footer
  attribution: "Compiled and transcribed by the family.",
  buildYear: new Date().getFullYear(),
};
