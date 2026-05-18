// Data for the hand-laid family tree at /family-tree/.
//
// People are keyed by an `id`; `parents` and `spouse` reference other
// people's ids. The Eleventy build step at the bottom of the file walks
// the people and emits `lines` — marriage lines as straight strokes
// between portrait pairs, parent → child lines as soft quadratic Béziers
// from the parents' midpoint down to the child's portrait top.

const VIEW_W = 3000;
const VIEW_H = 2400;

const ROW = {
  gen_minus_3:    200,   // Christopher the emigrant + Catherine Pritchard
  gen_minus_2:    560,   // Christopher 2nd + siblings
  gen_minus_1:    920,   // Dr. Christopher 3rd + siblings
  gen_0:         1280,   // Amy's grandparents (Walker side + SGFS Sr. & Minnie + siblings)
  gen_1_cousins: 1530,   // Amy's first cousins on the FitzSimons side (sub-row)
  gen_1:         1800,   // Amy + Jamie + Amy's surviving siblings + spouses
  gen_2:         2160,   // Walker children + spouses
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

  // ─── Generation −2: children of the emigrant ─────────────────────
  // Christopher emigrant + Catherine Pritchard bore 10+ children;
  // four survived to maturity. Christopher 2nd (Amy's direct line) is
  // centered; Ann, Paul, and Catherine fan out either side.
  {
    id: "ann_fs",
    name: "Ann FitzSimons",
    dates: "1794–1833",
    note: "mother of Lt. Gen. Wade Hampton III",
    parents: ["emigrant", "catherine_pritchard"],
    spouse: "wade_hampton_ii",
    x: 200, y: ROW.gen_minus_2, tilt: -2,
  },
  {
    id: "wade_hampton_ii",
    name: "Col. Wade Hampton II",
    dates: "1791–1858",
    note: "m. Ann FitzSimons 1817",
    spouse: "ann_fs",
    x: 380, y: ROW.gen_minus_2, tilt: 1,
  },
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
  {
    id: "paul_emigrant_son",
    name: "Paul FitzSimons",
    dates: "1800–1840",
    note: "founded the Georgia FitzSimons branch",
    parents: ["emigrant", "catherine_pritchard"],
    spouse: "eleanor_nesbit_white",
    x: 1500, y: ROW.gen_minus_2, tilt: -1,
  },
  {
    id: "eleanor_nesbit_white",
    name: "Eleanor Nesbit White",
    dates: "?–?",
    note: "of Augusta, GA",
    spouse: "paul_emigrant_son",
    x: 1680, y: ROW.gen_minus_2, tilt: 2,
  },
  {
    id: "catherine_fs_hammond",
    name: "Catherine FitzSimons",
    dates: "1814–1896",
    note: "of Redcliffe, Beech Island, SC",
    parents: ["emigrant", "catherine_pritchard"],
    spouse: "gov_james_hammond",
    x: 1880, y: ROW.gen_minus_2, tilt: 1.5,
  },
  {
    id: "gov_james_hammond",
    name: "Gov. James H. Hammond",
    dates: "1807–1864",
    note: "S.C. governor & U.S. senator",
    spouse: "catherine_fs_hammond",
    x: 2060, y: ROW.gen_minus_2, tilt: -1.5,
  },

  // ─── Generation −1: children of Christopher 2nd ──────────────────
  // Four surviving children per page 003: Christopher 3rd (the doctor),
  // Peter Gaillard FS, Catherine Ann FS, and Paul FS.
  {
    id: "peter_gaillard_fs",
    name: "Peter Gaillard FitzSimons",
    dates: "?–?",
    note: "of the Stoney–Gaillard line",
    parents: ["christopher_2nd", "elizabeth_porcher_stoney"],
    spouse: "julia_white",
    x: 200, y: ROW.gen_minus_1, tilt: 1.5,
  },
  {
    id: "julia_white",
    name: "Julia White",
    dates: "?–?",
    spouse: "peter_gaillard_fs",
    x: 380, y: ROW.gen_minus_1, tilt: -1,
  },
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
  {
    id: "catherine_ann_fs",
    name: "Catherine Ann FitzSimons",
    dates: "?–?",
    parents: ["christopher_2nd", "elizabeth_porcher_stoney"],
    spouse: "dr_robert_vaux",
    x: 1500, y: ROW.gen_minus_1, tilt: 1,
  },
  {
    id: "dr_robert_vaux",
    name: "Dr. Robert W. Vaux",
    dates: "?–?",
    note: "of Georgetown, SC",
    spouse: "catherine_ann_fs",
    x: 1680, y: ROW.gen_minus_1, tilt: -2,
  },
  {
    id: "paul_fs_gen3",
    name: "Paul FitzSimons",
    dates: "?–?",
    parents: ["christopher_2nd", "elizabeth_porcher_stoney"],
    spouse: "martha_selina_ford",
    x: 1880, y: ROW.gen_minus_1, tilt: -1,
  },
  {
    id: "martha_selina_ford",
    name: "Martha Selina Ford",
    dates: "?–?",
    note: "m. 1857",
    spouse: "paul_fs_gen3",
    x: 2060, y: ROW.gen_minus_1, tilt: 1.5,
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

  // SGFS Sr.'s elder brother "Kit" + wife
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

  // SGFS Sr. + Minnie (Amy's parents)
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

  // Remaining SGFS Sr. siblings (Amy's other paternal aunts & uncles)
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

  // ─── gen_1 sub-row: Amy's first cousins on the FitzSimons side ──
  // Two of Kit's children
  {
    id: "susan_milliken_allison",
    name: "Susan Milliken FitzSimons",
    dates: "?–?",
    note: "m. Dr. James Richard Allison",
    parents: ["kit", "frances_motte_huger"],
    x: 620, y: ROW.gen_1_cousins, tilt: -1,
  },
  {
    id: "christopher_5th",
    name: "Christopher FitzSimons",
    nickname: "Christopher 5th",
    dates: "1892–?",
    note: "m. Nathalie Heyward",
    parents: ["kit", "frances_motte_huger"],
    x: 800, y: ROW.gen_1_cousins, tilt: 1.5,
  },
  // Theodore Stoney's three children
  {
    id: "john_mccrady_fs",
    name: "John McCrady FitzSimons",
    dates: "?–?",
    parents: ["theodore_stoney_fs", "sabina_mccrady"],
    x: 1320, y: ROW.gen_1_cousins, tilt: -1,
  },
  {
    id: "louisa_de_burian_fs",
    name: "Louisa de Burian FitzSimons",
    dates: "?–?",
    parents: ["theodore_stoney_fs", "sabina_mccrady"],
    x: 1470, y: ROW.gen_1_cousins, tilt: 1,
  },
  {
    id: "theodora_lynch_fs",
    name: "Theodora Lynch FitzSimons",
    dates: "?–?",
    parents: ["theodore_stoney_fs", "sabina_mccrady"],
    x: 1620, y: ROW.gen_1_cousins, tilt: -1.5,
  },
  // Seaman + Henrietta's son
  {
    id: "christopher_seaman_son",
    name: "Christopher FitzSimons",
    dates: "1888–1898",
    note: "d. at Waycross, GA, age 10",
    parents: ["seaman", "henrietta_gaillard"],
    x: 1850, y: ROW.gen_1_cousins, tilt: 1,
  },
  // William Huger + Annie Cain's five children
  {
    id: "cain_fs",
    name: "James Cain FitzSimons",
    nickname: "Cain",
    dates: "1889–?",
    parents: ["w_huger_fs", "annie_cain"],
    x: 2010, y: ROW.gen_1_cousins, tilt: -1,
  },
  {
    id: "huger_jr_fs",
    name: "William Huger FitzSimons Jr.",
    dates: "?–?",
    parents: ["w_huger_fs", "annie_cain"],
    x: 2140, y: ROW.gen_1_cousins, tilt: 1,
  },
  {
    id: "sam_aviator_fs",
    name: "Samuel Gaillard FitzSimons",
    nickname: "the WWI aviator",
    dates: "c. 1894–1932",
    note: "founded the Lost Battalion; d. by suicide near Flat Rock",
    parents: ["w_huger_fs", "annie_cain"],
    x: 2270, y: ROW.gen_1_cousins, tilt: -1.5,
  },
  {
    id: "marguerite_fs",
    name: "Marguerite FitzSimons",
    dates: "?–?",
    note: "m. Dr. Robert Pringle",
    parents: ["w_huger_fs", "annie_cain"],
    x: 2400, y: ROW.gen_1_cousins, tilt: 1.5,
  },
  {
    id: "reginald_fs",
    name: "Reginald FitzSimons",
    dates: "?–?",
    parents: ["w_huger_fs", "annie_cain"],
    x: 2530, y: ROW.gen_1_cousins, tilt: -1,
  },

  // ─── Generation 1: Amy + Jamie + Amy's siblings ────────────────
  // Amy and Jamie shifted slightly right of their old position so the
  // descent line from SGFS Sr. + Minnie (midpoint 1090) lands close to
  // Amy, and so Amy's surviving FS siblings can sit just to her right.
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
    x: 700, y: ROW.gen_1, tilt: -2,
  },
  {
    id: "amy",
    name: "Amy Ann Perry FitzSimons",
    nickname: "Amy",
    dates: "1888–1973",
    note: "the compiler of this album",
    photo: "/books/book-001/images/portrait/392-amy_child.jpg",
    photoLink: "/books/book-001/392/",
    parents: ["sgfs_sr", "minnie"],
    spouse: "jpw_sr",
    x: 880, y: ROW.gen_1, tilt: 1.5,
  },
  // Dunkin Perry FitzSimons — Amy's brother who died on her 7th
  // birthday. Rendered as a small commemoration card.
  {
    id: "dunkin_perry_fs",
    name: "Dunkin Perry FitzSimons",
    dates: "1893–1895",
    note: "d. of diphtheria on Amy's 7th birthday",
    parents: ["sgfs_sr", "minnie"],
    x: 1060, y: ROW.gen_1, tilt: -1,
    small: true,
  },
  // Amy's three surviving FS siblings and their spouses
  {
    id: "theodore_barker_fs",
    name: "Theodore Barker FitzSimons",
    dates: "?–1943",
    parents: ["sgfs_sr", "minnie"],
    spouse: "clara_mueller",
    x: 1240, y: ROW.gen_1, tilt: 1,
  },
  {
    id: "clara_mueller",
    name: "Clara Hamilton Mueller",
    dates: "?–?",
    spouse: "theodore_barker_fs",
    x: 1420, y: ROW.gen_1, tilt: -2,
  },
  {
    id: "mary_annie_fs",
    name: "Mary Annie FitzSimons",
    nickname: "Minnie",
    dates: "?–?",
    note: "later Mrs. John Sosnowski of Charleston",
    parents: ["sgfs_sr", "minnie"],
    spouse: "donald_mckay_allston",
    x: 1620, y: ROW.gen_1, tilt: -1,
  },
  {
    id: "donald_mckay_allston",
    name: "Donald McKay Allston",
    dates: "?–?",
    note: "of John's Island, SC",
    spouse: "mary_annie_fs",
    x: 1800, y: ROW.gen_1, tilt: 2,
  },
  {
    id: "sgfs_jr",
    name: "Samuel Gaillard FitzSimons Jr.",
    nickname: "Buck",
    dates: "1904–1961",
    parents: ["sgfs_sr", "minnie"],
    spouse: "mary_hadlock",
    x: 2000, y: ROW.gen_1, tilt: 1.5,
  },
  {
    id: "mary_hadlock",
    name: "Mary Hadlock",
    dates: "?–?",
    note: "m. 24 Jan 1931 at Petersburg, VA",
    spouse: "sgfs_jr",
    x: 2180, y: ROW.gen_1, tilt: -1,
  },

  // ─── Generation 2: Walker children + spouses ─────────────────────
  {
    id: "buzzie",
    name: "Amy Perry Walker",
    nickname: "Buzzie",
    dates: "1910–1911",
    note: "died at fifteen months",
    photo: "/books/book-001/images/portrait/392-buzzie.jpg",
    photoLink: "/books/book-001/392/",
    parents: ["jpw_sr", "amy"],
    x: 260, y: ROW.gen_2, tilt: -1,
  },
  {
    id: "bo",
    name: "James Pickens Walker Jr.",
    nickname: "Bo",
    dates: "1912–1969",
    note: "Medical Corps captain, WWII",
    photo: "/books/book-001/images/portrait/393-bo_school.jpg",
    photoLink: "/books/book-001/393/",
    parents: ["jpw_sr", "amy"],
    spouse: "ann_knight",
    x: 510, y: ROW.gen_2, tilt: 1,
  },
  {
    id: "ann_knight",
    name: "Ann Seymour Knight",
    dates: "c. 1918–2010",
    note: "later Mrs. Morton E. Lord",
    spouse: "bo",
    x: 670, y: ROW.gen_2, tilt: -1,
  },
  {
    id: "dee",
    name: "Emma Dee Walker Corbell",
    nickname: "Dee",
    dates: "1915–1959",
    photo: "/books/book-001/images/portrait/393-dee_school.jpg",
    photoLink: "/books/book-001/393/",
    parents: ["jpw_sr", "amy"],
    spouse: "robert_corbell",
    x: 880, y: ROW.gen_2, tilt: -1.5,
  },
  {
    id: "robert_corbell",
    name: "Dr. Robert Lawrence Corbell Jr.",
    dates: "?–1960",
    note: "82nd Airborne battalion surgeon",
    spouse: "dee",
    x: 1040, y: ROW.gen_2, tilt: 2,
  },
  {
    id: "mary_ann",
    name: "Mary Ann Walker McEwan",
    dates: "1918–1975",
    note: "Hunter's grandmother",
    photo: "/books/book-001/images/portrait/393-mary_ann_school.jpg",
    photoLink: "/books/book-001/393/",
    parents: ["jpw_sr", "amy"],
    spouse: "oswald",
    x: 1240, y: ROW.gen_2, tilt: 1,
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
    x: 1400, y: ROW.gen_2, tilt: -2,
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
