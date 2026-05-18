// Data for the hand-laid family tree at /family-tree/.
//
// The layout coordinates here are deliberately hand-tuned per person so the
// tree composes as a scrapbook-page artifact rather than an evenly-spaced
// org chart. Photo paths point at the existing 400px-max-edge thumbnails;
// in a later pass we'll generate proper portrait crops per person.
//
// People are keyed by an `id`; `parents` and `spouse` reference other
// people's ids. The Eleventy build step at the bottom computes the
// connecting lines (marriage + parent-child) so the template only has to
// iterate, never to look anything up.

const VIEW_W = 1500;
const VIEW_H = 1080;

const people = [
  // ─── Generation 1: Amy's grandparents (Walker side) ──────────────
  {
    id: "samuel_cadwaller",
    name: "Samuel Cadwaller Walker",
    short: "Sam'l C. Walker",
    dates: "1842–1923",
    note: "of Winchester, VA; later Havre, MT",
    spouse: "emma_dee_pickens",
    x: 230, y: 170, tilt: -2,
  },
  {
    id: "emma_dee_pickens",
    name: "Emma Dee Pickens",
    short: "Emma Dee",
    dates: "1856–1933",
    note: "of Gnatty Creek, Barbour Co., WV",
    spouse: "samuel_cadwaller",
    x: 400, y: 170, tilt: 1.5,
  },

  // ─── Generation 1: Amy's grandparents (FitzSimons / Perry side) ──
  {
    id: "sgfs_sr",
    name: "Samuel Gaillard FitzSimons Sr.",
    short: "S. G. FitzSimons Sr.",
    dates: "1856–1930",
    note: "of Mount Hope plantation, Edisto River",
    spouse: "minnie",
    x: 1000, y: 170, tilt: -1.5,
  },
  {
    id: "minnie",
    name: "Mary Anne Perry FitzSimons",
    short: "Minnie / Mam'mie",
    dates: "1859–1934",
    photo: "/books/book-002/images/thumb/026.jpg",
    photoLink: "/books/book-002/026/",
    spouse: "sgfs_sr",
    x: 1170, y: 170, tilt: 2,
  },

  // ─── Generation 2: Amy + Jamie ───────────────────────────────────
  {
    id: "jpw_sr",
    name: "James Pickens Walker Sr.",
    short: "Jamie / Puck",
    dates: "1883–1960",
    note: "Atlantic Coast Line Railroad",
    photo: "/books/book-002/images/thumb/057.jpg",
    photoLink: "/books/book-002/057/",
    spouse: "amy",
    x: 600, y: 540, tilt: -2,
  },
  {
    id: "amy",
    name: "Amy Ann Perry FitzSimons",
    short: "Amy",
    dates: "1888–1973",
    note: "the compiler of this album",
    photo: "/books/book-002/images/thumb/047.jpg",
    photoLink: "/books/book-002/047/",
    spouse: "jpw_sr",
    x: 800, y: 540, tilt: 1.5,
  },

  // ─── Generation 3: Walker children + their spouses ───────────────
  {
    id: "buzzie",
    name: "Amy Perry \"Buzzie\" Walker",
    short: "Buzzie",
    dates: "1910–1911",
    note: "died at fifteen months",
    parents: ["jpw_sr", "amy"],
    x: 180, y: 880, tilt: -1,
  },
  {
    id: "bo",
    name: "James Pickens Walker Jr.",
    short: "Bo",
    dates: "1912–1969",
    note: "Medical Corps captain, WWII",
    photo: "/books/book-002/images/thumb/169.jpg",
    photoLink: "/books/book-002/169/",
    parents: ["jpw_sr", "amy"],
    spouse: "ann_knight",
    x: 430, y: 880, tilt: 1,
  },
  {
    id: "ann_knight",
    name: "Ann Seymour Knight",
    short: "Ann Knight",
    dates: "c. 1918–2010",
    note: "m. Bo June 1941; later Mrs. M. E. Lord",
    spouse: "bo",
    x: 580, y: 880, tilt: -1,
  },
  {
    id: "dee",
    name: "Emma Dee Walker Corbell",
    short: "Dee",
    dates: "1915–1959",
    parents: ["jpw_sr", "amy"],
    spouse: "robert_corbell",
    x: 800, y: 880, tilt: -1.5,
  },
  {
    id: "robert_corbell",
    name: "Dr. Robert Lawrence Corbell Jr.",
    short: "Dr. Corbell",
    dates: "?–1960",
    note: "82nd Airborne battalion surgeon",
    photo: "/books/book-002/images/thumb/192.jpg",
    photoLink: "/books/book-002/192/",
    spouse: "dee",
    x: 950, y: 880, tilt: 2,
  },
  {
    id: "mary_ann",
    name: "Mary Ann Walker McEwan",
    short: "Mary Ann",
    dates: "?–1975",
    note: "Hunter's grandmother",
    parents: ["jpw_sr", "amy"],
    spouse: "oswald",
    x: 1170, y: 880, tilt: 1,
  },
  {
    id: "oswald",
    name: "Oswald Beverley McEwan",
    short: "Lt. Col. McEwan",
    dates: "?–?",
    note: "U.S. Army, Field Artillery",
    photo: "/books/book-002/images/thumb/181.jpg",
    photoLink: "/books/book-002/181/",
    spouse: "mary_ann",
    x: 1320, y: 880, tilt: -2,
  },
];

// Wire up "Amy's parents" and "JPW Sr.'s parents" by adding the parents field
// to the gen-2 entries (kept separate above for readability).
for (const p of people) {
  if (p.id === "jpw_sr") p.parents = ["samuel_cadwaller", "emma_dee_pickens"];
  if (p.id === "amy") p.parents = ["sgfs_sr", "minnie"];
}

// ─── Compute connecting lines ──────────────────────────────────────
const positions = Object.fromEntries(people.map(p => [p.id, { x: p.x, y: p.y }]));

const lines = [];
const seenMarriages = new Set();

for (const p of people) {
  // Marriage: horizontal line through the bottom of both portraits.
  if (p.spouse && positions[p.spouse]) {
    const key = [p.id, p.spouse].sort().join("|");
    if (!seenMarriages.has(key)) {
      seenMarriages.add(key);
      const sp = positions[p.spouse];
      lines.push({
        type: "marriage",
        x1: Math.min(p.x, sp.x) + 60, y1: p.y + 90,
        x2: Math.max(p.x, sp.x) - 60, y2: sp.y + 90,
      });
    }
  }

  // Parent-child: a soft elbow from the midpoint between parents down to the
  // child's portrait top. Rendered as a quadratic Bézier with a control point
  // placed midway down, so the line reads as a hand-drawn descent rather than
  // an engineering rule.
  if (p.parents && p.parents.length === 2) {
    const [aId, bId] = p.parents;
    const a = positions[aId];
    const b = positions[bId];
    if (a && b) {
      const midX = (a.x + b.x) / 2;
      const midY = (a.y + b.y) / 2 + 90;
      const childTop = { x: p.x, y: p.y - 90 };
      lines.push({
        type: "descent",
        midX, midY,
        childX: childTop.x, childY: childTop.y,
      });
    }
  }
}

module.exports = {
  viewW: VIEW_W,
  viewH: VIEW_H,
  people,
  lines,
};
