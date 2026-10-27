# Codex handoff: picture book V41, page 5 dust and the 11 × 8.5 in print edition

Status: `SUPPORTING_CURRENT` work order for Codex, published 2026-10-26.
V41 is not started. Claude wrote this handoff and made no images; Codex
builds every image.

**Task:** first finish and publish V40, the wider page 2 arrival you are
building on the owner's instruction. Then build V41 in two parts with a stop
between them:

1. Make page 5's dust easier to see, and publish a review build.
2. Once the owner has accepted the illustrations, make the 11 × 8.5 in print
   edition.

- **Repository:** `Ebonyks/mermaid-roshan-reef`.
- **Branch:** `codex/mermaid-roshan-picture-book`.
- **Start from:** the published V40 commit. V40 changes only page 2, so the
  references pinned here at V39
  (`f55c094cfde2c1722eb210c74f85b868a4158ce9`) stay valid for every other
  page.
- **Part 1 package:** `books/chapter_one/landscape/revisions/v41_final_review/`.
- **Part 2 package:** `books/chapter_one/landscape/revisions/v41_print_11x8_5/`.

## Read in this order

1. This file.
2. [AUDIT.md](AUDIT.md): the page-by-page audit of V39 and the accepted
   defaults.
3. The standing rules in the
   [2026-10-19 decision record](../2026-10-18_v34_audit_fixes/OWNER_DECISION_2026-10-19.md)
   and the
   [character standards](../2026-10-18_v34_audit_fixes/CHARACTER_CONSISTENCY_2026-10-19.md).
   The decision record's print plan is made concrete below.
4. The [V38 work order](../2026-10-25_v38_audit_fixes/README.md); its "Rules
   that still bind" carry over unchanged.
5. The book's binding rules in [DESIGN_LANGUAGE.md](../../DESIGN_LANGUAGE.md)
   and DL-ASSET-08 in `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`.

If two documents disagree, this file wins for V41, except that the owner's
direct V40 instruction governs page 2's content. After that come the
2026-10-19 decision record, the character standards, the V38 work order and
the audit. The book's design language and DL-ASSET-08 bind all of them.

## Owner decision (2026-10-26)

After reading the V39 audit, the owner wrote: "Write the V40 Codex work order
using your suggested defaults: an 11-inch-wide trim (Q1), rebuild page 2 from
its source layers (Q2), stronger page 5 dust (Q3), and no third page 9
attempt (Q4)."

This work order is numbered V41 because V40 was already in progress for
page 2 when it was written.

| # | Decision | Where |
| --- | --- | --- |
| Q1 | An 11-inch-wide trim. This work order uses 11 × 8.5 in (US Letter landscape). It is the standard size, and it leaves the original art 23 pt (0.32 in) inside the trim at top and bottom; 11 × 8 in would leave 5 pt. If the owner meant 11 × 8 in, see "If the trim is 11 × 8 in". | Part 2 |
| Q2 | Rebuild page 2 from its source layers. The owner has since given Codex a more specific instruction: wider, no otter, and Pearl Castle shown close by. V40 implements it, and that instruction wins over the audit's suggestions for page 2. Part 2 adds what page 2 needs for print. | V40, P5 |
| Q3 | Make page 5's dust easier to see. | B1 |
| Q4 | No third attempt at the page 9 drawing. V37's drawing is enlarged about 1.1 times in the print edition, and A9 closes as not needed at this trim. | B2, P6 |

This decision authorizes:

- one bounded local edit, the page 5 dust (B1);
- the print-edition steps in Part 2.

The 2026-10-19 rule stands: nothing is enlarged for print until the owner
accepts the illustrations. Nothing here authorizes a full-scene redraw, a
change to the words, game or runtime work, or a release step.

## Rules that still bind

The [V38 work order's rules](../2026-10-25_v38_audit_fixes/README.md#rules-that-still-bind)
apply unchanged:

- source art only (DL-ASSET-08);
- keep originals, with every derivative recorded;
- the character standards;
- the bank rules (BK-BG-08, BK-BG-11);
- the book's 34 pages and its page-turn reveals;
- two takes per brief;
- no game, runtime, `dev`, `master` or release work.

Coordinates use the book's 504 × 360 point grid, origin bottom-left, as
`book.json` and `page_provenance.json` do. Source pixels are measured from the
top-left of the named file.

## Part 1: V41 review build (14 × 10 in)

### B1: page 5 dust (Q3)

**Now:**

- The dust is `books/chapter_one/landscape/revisions/v38_audit_fixes/art/door_dust_attempt4_rgba.png`.
- It is shown through four polygons, at opacity 0.7, over the door cutout
  `books/chapter_one/landscape/revisions/v34_editorial_polish/art/door_cutout_repair_attempt1.png`
  (1100 × 1429 px, placed at 163 × 225 pt).
- Its visible cores are about 86–89 × 43–45 px, beside a door handle of about
  69 × 34 px.
- On the page the wisps cover a strip about 0.9 × 0.1 in at 7 × 5 in. They
  average 1.44:1 contrast with the door beneath, too faint for a child to spot
  unprompted.

**Change:**

- Make each wisp about twice as tall (cores about 86–90 × 86–90 px).
- Raise the opacity to about 0.9, and lighten the lavender-grey slightly,
  taking the colour from dusty Grand Puff in
  `books/chapter_one/landscape/art/language_v26/puff_unwell.png`.
- Let one wisp spill forward over the front edge of the top red step, so the
  dust reads as drifting out from under the door.
- Keep the dust soft and shapeless: no eyes, spirals, pearls or star, so
  nothing gives Puff away.
- Keep it inside the door cutout's contour, or as small separate cutouts
  touching it; never a rectangle.

**Accept when:**

- Measured as the pixels that differ from V37's page 5 (as in the V39 audit),
  the dust covers a strip at least 0.2 in tall at 7 × 5 in. It also averages
  at least 2:1 contrast with what lies beneath (V39: 0.11 in and 1.44:1).
- A reader notices it at 7 × 5 in without anyone pointing.
- Nothing outside the dust changes, and the cutout shows no halo or
  rectangular backing.

### B2: page 9 (Q4)

- No change. V37's drawing stays (A9 held in V38 and V39).
- Record A9 as closed: at the 11-inch-wide trim it needs only about 1.1 times
  (see P6).

### Deliver Part 1, then stop

1. Package V41's review build the way V39 was packaged, with a before-and-after
   of page 5 against V40, and publish it (see "Delivery").
2. **Stop.** The owner reviews the whole book, including V40's page 2 and
   V41's page 5, and accepts the illustrations. One review covers both.
3. Do not start Part 2 until the owner says so.

## Part 2: print edition, 11 × 8.5 in

### P1: page geometry

| Item | Value |
| --- | --- |
| Trim | 11 × 8.5 in (792 × 612 pt), landscape |
| Bleed | 0.125 in (9 pt) on every edge |
| PDF boxes | MediaBox and BleedBox `[0 0 810 630]`, TrimBox `[9 9 801 621]` |
| Raster per page at 300 ppi | 3375 × 2625 px |
| Scale from the 504 × 360 grid | s = 11/7 = 1.5714 |
| Position mapping (points) | x′ = 9 + 1.5714·x, y′ = 32.14 + 1.5714·y |
| Where the original art sits | x′ 9–801, y′ 32.14–597.86 |

The mapping keeps every caption and cutout in the same place relative to the
art. The original art fills the trim's width and sits 23.14 pt inside its top
and bottom.

### P2: extend every page

- **Full-art pages:**
  - Add 9 pt on the left and right (the bleed) and 32.14 pt at the top and
    bottom (9 pt of bleed plus 23.14 pt inside the trim).
  - Outpaint the extensions as painted continuation: sky, ceiling or wall
    above; floor, grass or water below.
  - Never crop the original art.
  - For 1484 × 1060 px art, that is about 17 px on each side and 60 px at the
    top and bottom, at native size.
- **Cutout pages:**
  - Extend the blue stationery's wash by the same margins; its dotted bubble
    border stays where it is.
  - Continue the two bottom banks down to the new bottom edge, with nothing
    in the banks moving.
  - Cutouts keep their positions through the mapping.
- **Covers:** extend the same way as full-art pages. Page 2 has its own
  method (P5).

### P3: enlarge once, with one tool

- **Order:** extend each page at its native size first, then enlarge the whole
  extended canvas once to 3375 × 2625 px. For 1484 px art that is about 2.2
  times, and the added areas and the original then match.
- **Cutouts:** enlarge each one with the same tool to its placed print size,
  keeping clean alpha with no halo.
- **One tool:** use one recorded enlarging tool and one set of settings for
  the whole book.
- **Check at 100%:** compare faces, eyes, hands, tails and line work against
  the 14 × 10 in review, and reject any result that changes identity.
- **Records:** keep every original, and record every hash.

### P4: typography

Scale every size, outline and halo width by 1.5714, and map every position
with P1's formula.

| Use | Review size | Print size |
| --- | --- | --- |
| Story captions and the rear-cover copy | 20 pt | 31.4 pt |
| Page 21's two speech balloons | 18 pt | 28.3 pt |
| Cover title, line 1 | 30 pt | 47.1 pt |
| Cover title, line 2 | 22 pt | 34.6 pt |
| Cover subtitle | 13 pt | 20.4 pt |

The story-text inset becomes 37.7 pt from the trim's left and right edges,
and at least 60.9 pt from its top and bottom. The cover's inset becomes
28.3 pt.

### P5: page 2 at print size

- **Recompose, don't enlarge the flat picture.** Rebuild page 2 at print size
  from V40's own layers instead of enlarging its flattened composite.
- **Background:**
  - V40's 2867 × 2048 px crop of the Sky Lagoon panorama (its x 1250–4117)
    becomes the 3300 × 2357 px art area, about 1.15 times.
  - Take the left and right bleed from the panorama itself, which continues
    past V40's crop.
  - Outpaint only the top and bottom: about 116 px of sky above and grass
    below at the panorama's scale.
- **Plane:**
  - V40's plane is cut from the 720p video frame 396: 444 × 242 px, shown at
    940 × 512 px. At print size it would need about 2.4 times.
  - The game's picture of the same plane at the same angle,
    `assets/sprites/sky_lagoon/sky_lagoon_plane_v5_hd_grade.png`
    (775 × 360 px), needs only about 1.4 times, but it is drawn in flight
    without landing gear.
  - Use that picture at V40's exact position and size, and add the landing
    gear from frame 396 as a small local patch.
  - If the join shows at 100%, keep V40's video plane, enlarge it once with
    the book's tool, and record why.
- **Other pieces:**
  - The castle needs about 1.12 times and the slide about 1.15 times.
  - The swing frame and seat print smaller than their sources.
- **Accept when:** page 2 matches V40's approved layout, with no visible join.

### P6: page 9

V37's drawing (`books/chapter_one/landscape/revisions/v36_next_draft/art/w3b_attempt2.png`,
1181 × 1316 px used) prints at 1287 × 1434 px, about 1.09 times. Make no new
drawing.

### P7: checks

- **Safe zone:** keep faces, hands, tails, the main action and all text at
  least 0.25 in (18 pt) inside the trim.
  - Vertically the original art already sits 23.14 pt inside.
  - Horizontally, anything within 11.5 pt of the left or right edge of the
    504-pt grid falls in the outer 0.25 in.
  - List every page where a face, hand or tail falls there; check the cover's
    left fin and story 1's hair first.
- **Contrast:**
  - Re-run V39's composed caption check on the print composition.
  - Expect V39's 79 PASS, 7 OUTLINE_REQUIRED and 0 FAIL, with the cover
    subtitle counted as two lines.
  - Fix any FAIL.
- **Resolution:** every raster reaches 300 ppi at its placed size; report the
  lowest.
- **Joins:** no visible join at any extension or patch at 100%.
- **Identity:** faces, eyes, hands, tails and line work match the 14 × 10 in
  review at 100%.

### P8: files

- **Interior PDF:**
  - Stories 1–32 in order: 32 pages, each with P1's boxes.
  - Story 1 is the first page, a right-hand page.
  - Fonts embedded, and no added blank pages.
- **Covers:**
  - Front and rear as separate 810 × 630 pt pages with the same boxes.
  - A printer's cover wrap (back, spine and front in one file) depends on
    its spine width for 32 pages, so build it once a printer is chosen.
- **Colour:** keep RGB, and convert only to a chosen printer's profile.
- **Screen PDF:** one of 25 MB or less, for reading on screen.

**Accept when:**

- Every page carries the right boxes.
- Every raster reaches 300 ppi.
- The contrast check shows 0 FAIL.
- No join is visible and no identity has changed.
- Text and key detail sit inside the safe zone.

The owner's physical test print stays open; it is not Codex's to close.

## If the trim is 11 × 8 in

- **Boxes:** MediaBox and BleedBox `[0 0 810 594]`, TrimBox `[9 9 801 585]`.
- **Mapping:** y′ = 14.14 + 1.5714·y, so the extension is 14.14 pt at the top
  and bottom.
- **Safe zone:** the original art then sits only 5.14 pt inside the trim, so
  check every page's top and bottom 8.2 pt of the 504 × 360 grid for faces,
  hands, tails and text.
- **Everything else:** unchanged.

## Delivery

For each part:

1. **Package:** follow the V39 package. Include:
   - a README and revision scope;
   - generation evidence, with every prompt, reference hash and take,
     including rejected ones;
   - the derivative art and a before-and-after review;
   - verification, page provenance, caption contrast and the manifest;
   - the PDFs, with the lossless master split into exact parts if over
     100 MiB.
2. **Book records:** update `book.json`, the book `README.md`,
   `PAGE_PLAN.md`, `REVIEW.md` and `STORY_COMPREHENSION_AUDIT.md`.
3. **Design language:** add a "V41 owner decision (2026-10-26)" section to
   `DESIGN_LANGUAGE.md` that quotes the decision above and links this packet.
4. **Licences and ledger:** add an `ASSET_LICENSES.md` line for every new
   derivative and an impact record under `design/audit_impacts/`. Add ledger
   rows marking the newest README current and the previous one historical.
5. **Checks:** run the V39 package's checks adapted to V41, then:
   - `python -X utf8 -B tools/audit_document_authority.py`;
   - `python -X utf8 -B tools/audit_development.py --base auto`;
   - `python -X utf8 -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development`.
6. **Publish:** push to `codex/mermaid-roshan-picture-book`. Then verify the
   manifest and every file it lists over anonymous HTTPS from the exact
   commit, as V39's `verify_remote.py` does.

## Report back

- One line per item, B1–B2 and P1–P8: done, held or blocked, with evidence
  paths.
- The caption-check counts beside V39's (79 PASS, 7 OUTLINE_REQUIRED, 0 FAIL).
- The lowest ppi in the print edition, and the enlargement factor each page
  used.
- The remote verification receipt: commit, manifest SHA-256, check time and
  access mode.
- Every gap recorded instead of invented, with its reason.
- What stays open:
  - the owner's acceptance of the illustrations, between the parts;
  - a physical test print;
  - a child reading;
  - a speech-language review.

## Files in this packet

| File | Contents |
| --- | --- |
| `README.md` | This work order. |
| `AUDIT.md` | The page-by-page audit of V39 and the accepted defaults. |
| `MANIFEST.json` | Every file this handoff needs: repository path, role, size and SHA-256. |
