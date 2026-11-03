# Codex handoff: picture book V38 audit fixes

Status: `SUPPORTING_CURRENT` work order for Codex, published 2026-10-25.
V38 is not started. Claude wrote this handoff and made no images; Codex
builds every image.

**Task:** build V38 of "Mermaid Roshan and the Hidden Rainbow", the
chapter-one picture book, by fixing what the V37 audit found.

- **Repository:** `Ebonyks/mermaid-roshan-reef`.
- **Branch:** `codex/mermaid-roshan-picture-book`.
- **Start from:** V37 at commit `eb405fe45edbcc37b59bebebba475de445cffb58`.
- **Build the package in:** `books/chapter_one/landscape/revisions/v38_audit_fixes/`.

## Read in this order

1. This file.
2. [AUDIT.md](AUDIT.md): the page-by-page audit of V37 and the accepted
   defaults.
3. The standing rules in
   [OWNER_DECISION_2026-10-19.md](../2026-10-18_v34_audit_fixes/OWNER_DECISION_2026-10-19.md)
   and
   [CHARACTER_CONSISTENCY_2026-10-19.md](../2026-10-18_v34_audit_fixes/CHARACTER_CONSISTENCY_2026-10-19.md).
   These are the final manuscript, rear-cover rules and character standards,
   all still in force.
4. The book's binding rules in [DESIGN_LANGUAGE.md](../../DESIGN_LANGUAGE.md)
   and DL-ASSET-08 in `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`.

If two documents disagree, this file wins for V38. Next come the 2026-10-19
decision record, then the character standards, then the audit. The book's
design language and DL-ASSET-08 bind all of them.

## Owner decision (2026-10-25)

After reading the V37 audit, the owner wrote: "Write the V38 Codex handoff
for the V37 audit fixes, using your suggested defaults for Q1-Q6; leave Q7
(final trim) open."

| # | Accepted default | Work item |
| --- | --- | --- |
| Q1 | Bring back the hidden Lamma on the rear cover: a tiny head peeking from the far doorway, added with a local patch. | A6 |
| Q2 | Keep page 25's sofa, with the cloth instead of popcorn. | No change |
| Q3 | Show a little more of the problem on the rear cover: one cobweb in an upper corner and a few more dust drifts, keeping the scene inviting. | A7 |
| Q4 | Show page 5's sniffle with faint lavender dust motes drifting from under the door. Roshan stays off the page. | A8 |
| Q5 | Remake the page 9 drawing at print size now, before the print step. | A9 |
| Q6 | Keep "Whoosh!" on both 14 and 15 unless it sounds repetitive in the owner's read-aloud. | No change |
| Q7 | Final trim: open. Do not start the print edition. | None |

This acceptance authorizes three small additions, each a bounded local edit
inside existing art: the rear Lamma (A6), the rear cobweb and dust (A7), and
page 5's dust motes (A8). None of them is a new scene, a new pose or a story
change. A9 continues the 2026-10-19 approval of the page 9 drawing (W3b) at a
higher resolution. Nothing here authorizes a full-scene redraw, a change to
the words, a game or runtime change, or a release step.

## Rules that still bind

- **Source art (DL-ASSET-08):** work from existing art with crops, cutouts,
  layout and local inpainting or outpainting only. Record a missing moment as
  a gap; never invent one.
- **Originals:** keep them. Save every derivative separately with its
  polygon, source hash and output hash. Never edit the protected originals in
  `assets/book/`, `assets/audio/voices/` or `assets/characters/friends/`.
- **Characters:** every character must match
  [the character standards](../2026-10-18_v34_audit_fixes/CHARACTER_CONSISTENCY_2026-10-19.md#character-standards).
  Bind `assets/characters/roshan_25d/roshan_base.png` for Roshan, with
  rounded ears, the standard rainbow ponytail and the small gold tiara.
- **Banks:** banks hold only little puffs (BK-BG-11). Each object plays one
  role per page (BK-BG-08). Bank props sit in the bottom 15%, each at most
  12% of page width and height, and the central gap stays empty.
- **Book shape:** 34 pages; story 1 on a right-hand page; page-turn reveals
  at 13 to 14, 23 to 24 and 27 to 28. The final manuscript's words stay
  exactly as they are; only the line breaks in A1 and A3 change.
- **Process:** start with two takes per brief, and if neither passes, find
  out why before trying again. A visible join fails. Keep every take,
  selected or rejected, with its prompt and references.
- **Scope:** no game, runtime, `dev`, `master` or release work.

Coordinates below use the book's 504 × 360 point grid, origin bottom-left,
as `book.json` and `page_provenance.json` do; the 14 × 10 in review PDF is
exactly twice that. Source pixels are measured from the top-left of the named
file.

## Work items

Every page and cover not named here stays exactly as V37 made it.

### A1: page 22 line breaks (text only)

- Set the caption to three hand-broken lines:
  "In the art room, Roshan put / the paints in their places. / Then she
  scrubbed the table. Scrub, scrub!"
- At 20 pt they measure 241.4, 221.8 and 372.4 pt of the 440 pt box. Keep
  the box, position and colour.
- **Accept when:** no line holds a single word, and the words match the
  manuscript.

### A2: page 16, one caption in one colour

- Remove the per-line colours. Set all three lines navy, keeping the light
  halo and 1 pt outline the caption already has.
- Use even 26 pt spacing with baselines at 110, 84 and 58 pt: the block
  moves up and line 3 closes its 20 pt gap.
- Measured on the page's source art (it has no local repaints):

  | Line | Typical | Worst | Verdict |
  | --- | --- | --- | --- |
  | 1 | 6.2 | 3.4 | PASS |
  | 2 | 6.2 | 3.7 | PASS |
  | 3 | 4.3 | 3.3 | OUTLINE_REQUIRED |

  The halo already on the caption meets line 3's outline requirement.
- Check at 100% that line 1 doesn't cover Rumi's fins or the splash ring
  around her tail. If it does, keep one colour and use a bounded
  caption-area repaint like V37's on pages 7 and 14, then re-run the gate.
- **Accept when:** the caption reads as one block in one colour, with even
  spacing and no FAIL line.

### A3: page 18 line breaks (text only)

- Set the caption to three hand-broken lines:
  "Chirp, chirp! / “Someone in the playroom / needs help!” said Roshan."
- At 20 pt they measure 104.4, 235.6 and 221.0 pt of the 310 pt box. Keep
  the box, position, white colour and outline.
- **Accept when:** "needs help" stays on one line, and the gate passes.

### A4: front cover subtitle

- Set "A Pearl Castle friendship story" in two lines at 13 pt navy:
  "A Pearl Castle" over "friendship story".
- Right-align both lines to x 428.2 pt, the right edge of
  "and the Hidden Rainbow". Put the baselines at 262 and 246 pt.
- Measured on the V37 cover:

  | Line | Spans (pt) | Typical | Worst |
  | --- | --- | --- | --- |
  | A Pearl Castle | 349.0 to 428.2 | 8.8 | 6.4 |
  | friendship story | 338.0 to 428.2 | 8.4 | 6.6 |

- Roshan's ponytail colour ends at about x 281 to 286 pt beside the title,
  so the subtitle clears her hair by about 50 pt.
- **Accept when:**
  - no hair, tiara or character pixel lies within 10 pt of either line;
  - both lines pass the gate;
  - the subtitle sits inside the 18 pt cover inset.

### A5: page 9 bank, one plug only

- Page 9's stationery background is
  `books/chapter_one/landscape/revisions/v29_polish/art/bank08_tiny.png`;
  only page 9 uses it.
- On its right bank, replace the plug and chain, left of the rolled towel,
  with a small shell-shaped pail of clean pale-aqua water with a few bubbles.
  It answers Roshan's draining on 9 and hints at the clean water on 10.
- Keep the rolled towel, the shells and the left bank's little puff and duck.
- Draw the pail in the book's outlined watercolour bank style, grounded with
  the bank's sand contact and a narrow shadow.
- **Accept when:**
  - no plug or chain appears in either bank;
  - the bank rules hold;
  - the new prop shows no rectangular patch edge at 100%.

### A6: rear cover Lamma (Q1)

- The rear art is
  `books/chapter_one/landscape/revisions/v36_rear_composition_20261021/rear_scene_attempt1.png`
  (1484 × 1060), with V37's hair patch
  `books/chapter_one/landscape/revisions/v37_consistency_20261022/art/rear_hair_attempt1.png`.
- Add a tiny Lamma head peeking around the left curtain of the central
  arched doorway, the far doorway with purple curtains and a blue corridor.
  Place it low, near the corridor floor, at about source x 540 to 585 and
  y 540 to 600. It should be about the height of Roshan's hand.
- Match the canonical lamb: white plush with a pale face, lashes and pink
  cheeks.
- References:
  - `assets/sprites/stuffie_studio/lamma.png`, the canonical lamb;
  - `books/chapter_one/landscape/revisions/v29_polish/art/lamma09.png`, the
    page 10 cameo;
  - `books/chapter_one/landscape/revisions/v33_story_covers/art/rear_lamma.png`,
    an earlier rear cameo.
- Use a local patch only. The curtain, corridor light, Roshan, the duster,
  the little puff and the copy stay unchanged.
- **Accept when:**
  - a careful look finds the Lamma, but it doesn't pull the eye from Roshan;
  - the book holds two silent Lamma sightings again (page 10 and the rear);
  - nothing in the text points to them.

### A7: rear cover dust and cobweb (Q3)

- On the same rear art, add one cobweb in the upper-right corner, at about
  source x 1380 to 1484 and y 0 to 110. Draw it thin, pale and soft like the
  book's existing cobwebs on pages 4, 18 and 26, clear of the wall lamp and
  the banner.
- Add 3 to 5 more soft grey dust drifts on the red carpet and along its
  edges. Match the existing small tufts, and favour the lower half so they
  read at print size.
- Keep the hall bright and inviting: no darkening, no grime, nothing behind
  the copy.
- **Accept when:**
  - a child can point to dust and a cobweb;
  - the copy still passes the gate;
  - pixels outside the edited areas are unchanged.

### A8: page 5 dust motes (Q4)

- Page 5's foreground is the door cutout
  `books/chapter_one/landscape/revisions/v34_editorial_polish/art/door_cutout_repair_attempt1.png`
  (1100 × 1429).
- Add 3 to 5 faint lavender-grey dust motes drifting out from under the shut
  door, where it meets the top red step. Make each mote between the size of
  the door's gold handle and twice that.
- Take their colour from dusty Grand Puff in
  `books/chapter_one/landscape/art/language_v26/puff_unwell.png`. Draw soft,
  irregular puffs of dust: no eyes, spirals, pearls or star, so nothing
  reveals Puff.
- Keep the motes inside one complete cutout contour with the door, or as
  small separate cutouts touching it; never a rectangle.
- Roshan stays off this page, and the listening little puff and closed books
  in the banks stay.
- **Accept when:** the motes read as dust coming from behind the door at
  7 × 5 in, and the cutout shows no halo or rectangular backing.

### A9: page 9 drawing at print size (Q5)

- The selected V36 take is
  `books/chapter_one/landscape/revisions/v36_next_draft/art/w3b_attempt2.png`,
  1181 × 1332 px. Its prompt and references are in
  `books/chapter_one/landscape/revisions/v36_next_draft/generation_evidence.json`.
- Make the same drawing at least 1,800 px tall for the Roshan-and-tub group.
  Prefer a native generation with the selected take as the reference;
  plain upscaling is the fallback.
- Keep the same pose, composition, tub, brush, chain, drain swirl, green
  streaks and identity.
- Two takes. If neither holds the pose and identity, keep V37's cutout,
  record the reason, and leave it to the print-edition upscale.
- **Accept when:**
  - it is at least 1,800 px tall;
  - it passes every check on the
    [2026-10-19 W3b list](../2026-10-18_v34_audit_fixes/OWNER_DECISION_2026-10-19.md#page-9-drawing-w3b),
    including the rounded ear and exactly two arms;
  - side by side at 100% with the V37 cutout, nothing has changed except
    detail.

### A10: the caption gate

- Use V37's composed method, from
  `books/chapter_one/landscape/revisions/v37_consistency_20261022/verify_revision.py`:
  measure on the final composed page without the text, including local
  repaints, and exclude the stroke.
- The 2026-10-18 `caption_contrast.py` no longer serves as the gate, because
  it ignores local repaints.
- V37's result is 79 PASS, 6 OUTLINE_REQUIRED and 0 FAIL of 85 lines. V38
  should come to 86 lines, since the cover subtitle becomes two.
- **Accept when:** 0 FAIL, and every OUTLINE_REQUIRED line has an outline or
  halo. Report the counts beside V37's.

## Deliberately unchanged

- **Page 25:** the sofa and cloth stay (Q2).
- **Pages 14 and 15:** "Whoosh!" stays on both (Q6), unless the owner later
  asks for "Splash!" on 15.
- **Pages 3 and 23:** the captions stay where they are. Page 3's sits where
  V33 had it and passes. Page 23's already has a light halo, and no position
  inside the margins clears both the frieze and the chains at 20 pt.
- **C14:** Daddy's hair stays as it is (optional).
- **Print edition:** do not start it until the owner names a trim (Q7). The
  2026-10-19 print plan stays as written.

## Delivery

1. Package V38 the way V37 was packaged:
   - a README and revision scope;
   - generation jobs and evidence, with every prompt, reference hash and
     take;
   - the derivative art;
   - a before-and-after review of every changed page against V37;
   - `complete/` with the 34 proofs, the lossless master (split into exact
     parts if over 100 MiB), an email PDF of 25 MB or less, the reader,
     verification, page provenance, print pagination and the composed
     caption contrast.
2. Update `book.json`, the book `README.md`, `PAGE_PLAN.md` (new line breaks
   on 18 and 22), `REVIEW.md` and `STORY_COMPREHENSION_AUDIT.md`.
3. Add a "V38 owner decision (2026-10-25)" section to `DESIGN_LANGUAGE.md`
   that quotes the decision above and links this packet.
4. Add an `ASSET_LICENSES.md` line for every new derivative, an impact record
   under `design/audit_impacts/`, and ledger rows marking the V38 README
   current and the V37 README historical.
5. Run V37's checks adapted to V38:
   - `verify_revision.py`;
   - `audit_book.py` routed to V38 with V37 as the baseline;
   - the email-export check and the composed caption gate;
   - `python -X utf8 -B tools/audit_document_authority.py`;
   - `python -X utf8 -B tools/audit_development.py --base auto`;
   - `python -X utf8 -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development`.
6. Push to `codex/mermaid-roshan-picture-book`, then verify the V38 manifest
   and every file it lists over anonymous HTTPS from the exact commit, as
   V37's `verify_remote.py` does.

## Report back

- One line per item, A1–A10: done, held or blocked, with evidence paths.
- The caption gate counts beside V37's (79 PASS, 6 OUTLINE_REQUIRED, 0 FAIL).
- The remote verification receipt: commit, manifest SHA-256, check time and
  access mode.
- Every gap recorded instead of invented, with its reason.
- What stays open: owner acceptance of the illustrations, a child reading,
  a speech-language review, the final trim and a physical test print.

## Files in this packet

| File | Contents |
| --- | --- |
| `README.md` | This work order. |
| `AUDIT.md` | The page-by-page audit of V37 and the accepted defaults. |
| `MANIFEST.json` | Every file this handoff needs: repository path, role, size and SHA-256. |
