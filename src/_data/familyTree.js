// Data for the hand-laid family tree at /family-tree/.
//
// People are keyed by an `id`; `parents` and `spouse` reference other
// people's ids. The Eleventy build step at the bottom of the file walks
// the people and emits `lines` — marriage lines as straight strokes
// between portrait pairs, parent → child lines as soft quadratic Béziers
// from the parents' midpoint down to the child's portrait top.
//
// Each person has:
//   name       — full given name (used on the card and as the canonical label)
//   nickname   — optional; rendered in quotes on its own caption line
//   dates      — life-span string ("1888–1973" or "?–1975")
//   note       — optional one-line descriptor for the caption foot
//   photo      — optional /books/.../portrait/PPP-id.jpg path
//   photoLink  — optional album-page URL the portrait card links to
//   x, y, tilt — hand-tuned layout coordinates
//   parents    — optional [id, id] pair
//   spouse     — optional id

const VIEW_W = 2800;
const VIEW_H = 2200;

// Row Y-coordinates per generation. Each generation row is ~360px tall
// (200 for the card + caption block + ~160 vertical breathing room for
// the connecting lines).
const ROW = {
  gen_minus_3: 200,   // Christopher the emigrant + Catherine Pritchard
  gen_minus_2: 560,   // Christopher 2nd + Elizabeth Porcher Stoney
  gen_minus_1: 920,   // Dr. Christopher 3rd + Susan Milliken Barker
  gen_0:       1280,  // Amy's grandparents (Walker side + SGFS Sr. & Minnie)
  gen_1:       1640,  // Amy + Jamie
  gen_2:       2000,  // Walker children + spouses
};

const people = [
  // ─── Generation −3: the emigrant ─────────────────────────────────
  {
    id: "emigrant",
    name: "Christopher FitzSimons",
    nickname: "the emigrant",
    dates: "1762–1825",
    note: "of Dundalk, Co. Louth, Ireland; Charleston merchant",
    photo: "/books/book-001/images/portrait/002-emigrant.jpg",
    photoLink: "/books/book-001/002/",
    spouse: "catherine_pritchard",
    x: 1000, y: ROW.gen_minus_3, tilt: -1.5,
  },
  {
    id: "catherine_pritchard",
    name: "Catherine Pritchard",
    dates: "1772–1841",
    note: "of Hobcaw shipyard, Christ Church Parish",
    photo: "/books/book-001/images/portrait/002-catherine_pritchard.jpg",
    photoLink: "/books/book-001/002/",
    spouse: "emigrant",
    x: 1180, y: ROW.gen_minus_3, tilt: 2,
  },

  // ─── Generation −2 ───────────────────────────────────────────────
  {
    id: "christopher_2nd",
    name: "Christopher FitzSimons",
    nickname: "Christopher 2nd",
    dates: "1802–1832",
    note: "died age 30 at Lexington, SC",
    parents: ["emigrant", "catherine_pritchard"],
    spouse: "elizabeth_porcher_stoney",
    x: 1000, y: ROW.gen_minus_2, tilt: 1,
  },
  {
    id: "elizabeth_porcher_stoney",
    name: "Elizabeth Porcher Stoney",
    dates: "1806–1873",
    note: "of the Stoney–Gaillard line",
    spouse: "christopher_2nd",
    x: 1180, y: ROW.gen_minus_2, tilt: -2,
  },

  // ─── Generation −1 ───────────────────────────────────────────────
  {
    id: "christopher_3rd",
    name: "Dr. Christopher FitzSimons",
    nickname: "Christopher 3rd",
    dates: "1828–1866",
    note: "killed in the May 1866 Cooper River tornado at Moss Grove",
    photo: "/books/book-001/images/portrait/271-christopher_3rd.jpg",
    photoLink: "/books/book-001/271/",
    parents: ["christopher_2nd", "elizabeth_porcher_stoney"],
    spouse: "susan_milliken_barker",
    x: 1000, y: ROW.gen_minus_1, tilt: -1.5,
  },
  {
    id: "susan_milliken_barker",
    name: "Susan Milliken Barker",
    dates: "1827–1900",
    note: "of Charleston; widowed at 39 with seven children",
    photo: "/books/book-001/images/portrait/271-susan_milliken_barker.jpg",
    photoLink: "/books/book-001/271/",
    spouse: "christopher_3rd",
    x: 1180, y: ROW.gen_minus_1, tilt: 2,
  },

  // ─── Generation 0: Amy's grandparents ────────────────────────────
  {
    id: "samuel_cadwaller",
    name: "Samuel Cadwaller Walker",
    dates: "1842–1923",
    note: "of Winchester, VA; later Havre, MT",
    spouse: "emma_dee_pickens",
    x: 230, y: ROW.gen_0, tilt: -2,
  },
  {
    id: "emma_dee_pickens",
    name: "Emma Dee Pickens",
    dates: "1856–1933",
    note: "of Gnatty Creek, Barbour Co., WV",
    spouse: "samuel_cadwaller",
    x: 410, y: ROW.gen_0, tilt: 1.5,
  },
  // ── SGFS Sr.'s elder brother, "Kit", and his wife ──
  {
    id: "kit",
    name: "Christopher FitzSimons Jr.",
    nickname: "Kit",
    dates: "1856–1925",
    note: "cottonseed-oil pioneer, Columbia, SC",
    photo: "/books/book-001/images/portrait/311-kit.jpg",
    photoLink: "/books/book-001/311/",
    parents: ["christopher_3rd", "susan_milliken_barker"],
    spouse: "frances_motte_huger",
    x: 620, y: ROW.gen_0, tilt: -1,
  },
  {
    id: "frances_motte_huger",
    name: "Frances Motte Huger",
    dates: "1863–1937",
    note: "of Columbia, SC",
    photo: "/books/book-001/images/portrait/311-frances_motte_huger.jpg",
    photoLink: "/books/book-001/311/",
    spouse: "kit",
    x: 800, y: ROW.gen_0, tilt: 2,
  },

  // ── SGFS Sr. + Minnie (Amy's parents) ──
  {
    id: "sgfs_sr",
    name: "Samuel Gaillard FitzSimons Sr.",
    dates: "1856–1930",
    note: "of Mount Hope plantation, Edisto River",
    photo: "/books/book-001/images/portrait/312-sgfs_sr.jpg",
    photoLink: "/books/book-001/312/",
    parents: ["christopher_3rd", "susan_milliken_barker"],
    spouse: "minnie",
    x: 1000, y: ROW.gen_0, tilt: -1.5,
  },
  {
    id: "minnie",
    name: "Mary Anne Perry FitzSimons",
    nickname: "Minnie",
    dates: "1859–1934",
    note: "of Charleston",
    photo: "/books/book-001/images/portrait/312-minnie.jpg",
    photoLink: "/books/book-001/312/",
    spouse: "sgfs_sr",
    x: 1180, y: ROW.gen_0, tilt: 2,
  },

  // ── SGFS Sr.'s siblings (Amy's paternal aunts & uncles) ──
  {
    id: "theodore_stoney_fs",
    name: "Theodore Stoney FitzSimons",
    nickname: "Uncle Tote",
    dates: "1858–1944",
    parents: ["christopher_3rd", "susan_milliken_barker"],
    spouse: "sabina_mccrady",
    x: 1380, y: ROW.gen_0, tilt: 1,
  },
  {
    id: "sabina_mccrady",
    name: "Sabina Lynch McCrady",
    dates: "?–?",
    spouse: "theodore_stoney_fs",
    x: 1560, y: ROW.gen_0, tilt: -1.5,
  },
  {
    id: "seaman",
    name: "Seaman Sinkler FitzSimons",
    dates: "?–?",
    photo: "/books/book-001/images/portrait/441-seaman.jpg",
    photoLink: "/books/book-001/441/",
    parents: ["christopher_3rd", "susan_milliken_barker"],
    spouse: "henrietta_gaillard",
    x: 1760, y: ROW.gen_0, tilt: -2,
  },
  {
    id: "henrietta_gaillard",
    name: "Henrietta Gaillard",
    dates: "?–1917",
    note: "d. 17 Dec 1917",
    photo: "/books/book-001/images/portrait/441-henrietta_gaillard.jpg",
    photoLink: "/books/book-001/441/",
    spouse: "seaman",
    x: 1940, y: ROW.gen_0, tilt: 1.5,
  },
  {
    id: "w_huger_fs",
    name: "William Huger FitzSimons",
    dates: "1861–1939",
    parents: ["christopher_3rd", "susan_milliken_barker"],
    spouse: "annie_cain",
    x: 2140, y: ROW.gen_0, tilt: 1.5,
  },
  {
    id: "annie_cain",
    name: "Annie Cain",
    dates: "?–?",
    spouse: "w_huger_fs",
    x: 2320, y: ROW.gen_0, tilt: -2,
  },
  {
    id: "ellen_milliken_fs",
    name: "Ellen Milliken FitzSimons",
    nickname: "Aunt Ellen",
    dates: "1862–1953",
    note: "Charleston Library Society librarian, 50 years",
    parents: ["christopher_3rd", "susan_milliken_barker"],
    x: 2500, y: ROW.gen_0, tilt: -1,
  },
  {
    id: "gaillie_fs",
    name: "Gaillard Stoney FitzSimons",
    nickname: "Gaillie",
    dates: "?–?",
    note: "of Spartanburg, SC",
    parents: ["christopher_3rd", "susan_milliken_barker"],
    x: 2640, y: ROW.gen_0, tilt: 2,
  },

  // ─── Generation 1: Amy + Jamie ───────────────────────────────────
  {
    id: "jpw_sr",
    name: "James Pickens Walker Sr.",
    nickname: "Jamie / Puck",
    dates: "1883–1960",
    note: "Atlantic Coast Line Railroad",
    photo: "/books/book-002/images/portrait/057-jpw_sr.jpg",
    photoLink: "/books/book-002/057/",
    parents: ["samuel_cadwaller", "emma_dee_pickens"],
    spouse: "amy",
    x: 600, y: ROW.gen_1, tilt: -2,
  },
  {
    id: "amy",
    name: "Amy Ann Perry FitzSimons",
    nickname: "Amy",
    dates: "1888–1973",
    note: "the compiler of this album",
    photo: "/books/book-002/images/portrait/047-amy.jpg",
    photoLink: "/books/book-002/047/",
    parents: ["sgfs_sr", "minnie"],
    spouse: "jpw_sr",
    x: 800, y: ROW.gen_1, tilt: 1.5,
  },

  // ─── Generation 2: Walker children + spouses ─────────────────────
  {
    id: "buzzie",
    name: "Amy Perry Walker",
    nickname: "Buzzie",
    dates: "1910–1911",
    note: "died at fifteen months",
    parents: ["jpw_sr", "amy"],
    x: 180, y: ROW.gen_2, tilt: -1,
  },
  {
    id: "bo",
    name: "James Pickens Walker Jr.",
    nickname: "Bo",
    dates: "1912–1969",
    note: "Medical Corps captain, WWII",
    photo: "/books/book-002/images/portrait/169-bo.jpg",
    photoLink: "/books/book-002/169/",
    parents: ["jpw_sr", "amy"],
    spouse: "ann_knight",
    x: 430, y: ROW.gen_2, tilt: 1,
  },
  {
    id: "ann_knight",
    name: "Ann Seymour Knight",
    dates: "c. 1918–2010",
    note: "later Mrs. Morton E. Lord",
    spouse: "bo",
    x: 590, y: ROW.gen_2, tilt: -1,
  },
  {
    id: "dee",
    name: "Emma Dee Walker Corbell",
    nickname: "Dee",
    dates: "1915–1959",
    parents: ["jpw_sr", "amy"],
    spouse: "robert_corbell",
    x: 800, y: ROW.gen_2, tilt: -1.5,
  },
  {
    id: "robert_corbell",
    name: "Dr. Robert Lawrence Corbell Jr.",
    dates: "?–1960",
    note: "82nd Airborne battalion surgeon",
    spouse: "dee",
    x: 960, y: ROW.gen_2, tilt: 2,
  },
  {
    id: "mary_ann",
    name: "Mary Ann Walker McEwan",
    dates: "1918–1975",
    note: "Hunter's grandmother",
    photo: "/books/book-002/images/portrait/087-mary_ann.jpg",
    photoLink: "/books/book-002/087/",
    parents: ["jpw_sr", "amy"],
    spouse: "oswald",
    x: 1170, y: ROW.gen_2, tilt: 1,
  },
  {
    id: "oswald",
    name: "Oswald Beverley McEwan",
    nickname: "Bo",
    dates: "1913–1995",
    note: "U.S. Army, Field Artillery",
    photo: "/books/book-002/images/portrait/181-oswald.jpg",
    photoLink: "/books/book-002/181/",
    spouse: "mary_ann",
    x: 1330, y: ROW.gen_2, tilt: -2,
  },
];

// ─── Compute connecting lines ──────────────────────────────────────
const positions = Object.fromEntries(people.map(p => [p.id, { x: p.x, y: p.y }]));

const lines = [];
const seenMarriages = new Set();

for (const p of people) {
  if (p.spouse && positions[p.spouse]) {
    const key = [p.id, p.spouse].sort().join("|");
    if (!seenMarriages.has(key)) {
      seenMarriages.add(key);
      const sp = positions[p.spouse];
      lines.push({
        type: "marriage",
        x1: Math.min(p.x, sp.x) + 84, y1: p.y + 100,
        x2: Math.max(p.x, sp.x) - 84, y2: sp.y + 100,
      });
    }
  }

  if (p.parents && p.parents.length === 2) {
    const a = positions[p.parents[0]];
    const b = positions[p.parents[1]];
    if (a && b) {
      lines.push({
        type: "descent",
        midX: (a.x + b.x) / 2,
        midY: (a.y + b.y) / 2 + 100,
        childX: p.x,
        childY: p.y - 100,
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
