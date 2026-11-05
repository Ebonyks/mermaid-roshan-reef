# Start here: picture book V36

Status: `SUPPORTING_CURRENT` entry point for Codex, published 2026-10-21.
V36 is not started. Claude wrote this handoff and made no images; Codex
builds every image.

**Task:** build V36 of "Mermaid Roshan and the Hidden Rainbow", the
chapter-one picture book, on branch `codex/mermaid-roshan-picture-book` in
`Ebonyks/mermaid-roshan-reef`. Start from V34 at commit
`4f65c502beabb38bb3365920005e2e6f90ea13f0`; its art and controls are
unchanged since. Build the package in
`books/chapter_one/landscape/revisions/v36_next_draft/`.

## Read in this order

1. This file.
2. [OWNER_DECISION_2026-10-19.md](OWNER_DECISION_2026-10-19.md): what
   governs V36. It covers the reconciliation with V34, the final 32-page
   manuscript, rear cover A, the page 9 drawing (W3b), Roshan's ears (Q6),
   the character decisions and the larger print edition.
3. [CHARACTER_CONSISTENCY_2026-10-19.md](CHARACTER_CONSISTENCY_2026-10-19.md):
   the standard for each character, fixes C1–C14 and a page checklist.
4. [README.md](README.md): the detailed specifications for work items
   W1–W17. W14 and W16 are replaced.
5. [AUDIT.md](AUDIT.md): background, the page-by-page audit of V33.
6. The book's binding rules in
   [DESIGN_LANGUAGE.md](../../DESIGN_LANGUAGE.md), including BK-BG-11 (only
   little puffs in the banks) and the 2026-10-19 owner sections, and
   DL-ASSET-08 in `design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md`.

If two documents disagree, the decision record wins, then the character
addendum, then the README, then the audit. The book's design language and
DL-ASSET-08 bind all of them.

## Owner decisions in force

| Date | Decision | Where |
| --- | --- | --- |
| 2026-10-18 | Accept every audit default, Q1–Q14 | [README](README.md#owner-decision-2026-10-18), [AUDIT](AUDIT.md#open-questions-and-accepted-defaults) |
| 2026-10-19 | This handoff governs V36: its 14 changed captions win, V34 wording stays elsewhere, the rear cover is spoiler-free, and the print step suits a larger book | [Decision record](OWNER_DECISION_2026-10-19.md#the-decision) |
| 2026-10-19 | Rear cover A: Roshan and Daddy at the castle doorway | [Rear cover](OWNER_DECISION_2026-10-19.md#rear-cover) |
| 2026-10-19 | W3b approved: one new page 9 cutout | [Page 9 drawing](OWNER_DECISION_2026-10-19.md#page-9-drawing-w3b) |
| 2026-10-19 | Roshan's ears are rounded | [Ears](OWNER_DECISION_2026-10-19.md#roshans-ears-q6) |
| 2026-10-19 | One standard rainbow lock for Roshan; character-only edits allowed on the locked cover and stories 28–29 | [Character consistency](CHARACTER_CONSISTENCY_2026-10-19.md#owner-decisions-2026-10-19) |
| Open | Final trim: 11 × 8, 11 × 8.5 or 14 × 11 in | Ask at step 10; not needed earlier |

## Build order

| Step | Do | Where it is specified | Accept when |
| --- | --- | --- | --- |
| 1 | Set up the V36 package from V34 at `4f65c502` and record that baseline. | This file | The package folder exists and names its baseline. |
| 2 | Restore the handoff page order and set every caption to the final manuscript. Story 4 is the dusty hall. Story 5 is the shut-door page, reusing V34's door cutout and its listening little-puff bank. Story 23 is the route-light hall again, and stories 6–32 take V33's numbering. | [Reconciliation](OWNER_DECISION_2026-10-19.md#reconciliation-with-codexs-v34) (W1, W2), [Final manuscript](OWNER_DECISION_2026-10-19.md#final-manuscript) | 34 pages; story 1 on a right-hand page; reveals 23 to 24 and 27 to 28 across page turns; every caption matches the table exactly. |
| 3 | Carry over V34's results where the reconciliation table says keep (W3a, W4, W5, W7, W9, W10, W11, story 31). Do W8's resting sponge on story 22 and W15's subtitle and doorway light. Retry W17's dust and shadow on stories 3 and 4 with a seam-free method. | [Reconciliation](OWNER_DECISION_2026-10-19.md#reconciliation-with-codexs-v34) and the matching [README](README.md#work-items) items | Each item's own acceptance line. |
| 4 | Build the new page 9 cutout (W3b). | [Page 9 drawing](OWNER_DECISION_2026-10-19.md#page-9-drawing-w3b) | Its acceptance list, including the rounded ear. |
| 5 | Make character fixes C1–C14, with the rounded ear (Q6) as C3. Build story 3 and rear cover A from one corrected derivative. | [Fix list](CHARACTER_CONSISTENCY_2026-10-19.md#fix-list), [Method](CHARACTER_CONSISTENCY_2026-10-19.md#method-for-every-fix) | The method's checks; any visible join is recorded as a gap and shown to the owner. |
| 6 | Make rear cover A from the corrected story 3 derivative. | [Rear cover](OWNER_DECISION_2026-10-19.md#rear-cover) | Its copy passes the contrast gate and the tiny Lamma shows. |
| 7 | Apply the caption system (W6) and run the contrast gate. | [README W6](README.md#w6-one-caption-system-and-the-contrast-gate-q9), [caption_contrast.py](caption_contrast.py) | Zero FAIL lines; every OUTLINE_REQUIRED line uses the heavier outline. |
| 8 | Render the 14 × 10 in review proofs, a lossless master and an email PDF of 25 MB or less. Review every changed page natively against the character standards. Check spreads 8–9, 19–20 and 24–25, and the run 26–29, side by side, and add a before-and-after view against V34. | [Character standards](CHARACTER_CONSISTENCY_2026-10-19.md#character-standards) | Every changed page reviewed; review notes saved in the package. |
| 9 | Deliver the review package (see "Delivery" below), then report back. | This file | Pushed, verified over anonymous HTTPS, reported. |
| 10 | Stop. The owner reviews the V36 illustrations and picks the final trim. Do not upscale before this. | [Print edition](OWNER_DECISION_2026-10-19.md#print-edition-replaces-w16) | The owner accepts the illustrations and names a trim. |
| 11 | Later and separately: make the print edition. | [Print edition](OWNER_DECISION_2026-10-19.md#print-edition-replaces-w16) | Its acceptance list, ending with a physical test print. |

## Rules for every step

- DL-ASSET-08: work from existing frames with crops, cutouts, layout and
  local inpainting or outpainting. No full-scene redraw. The W3b cutout is
  the only new piece of art. Record a missing moment as a gap; never invent
  one.
- Never edit protected originals in `assets/book/`, `assets/audio/voices/`
  or `assets/characters/friends/`; use them as references only. Baby Eagle's
  original is in `assets/book/`.
- Keep originals. Save every derivative separately with its polygon, source
  hash and output hash, and keep rejected takes as evidence.
- Start with two takes per brief; if neither passes, find out why before
  trying again. A visible join fails.
- No game, runtime, `dev`, `master` or release work.

## Delivery

- Add an `ASSET_LICENSES.md` line for every new derivative, and keep the
  prompts, references and every take in the package's generation evidence.
- Write the V36 README, revision scope, verification, page provenance,
  print pagination and print dummy, following the V34 package.
- Update `book.json`, the book `README.md`, `PAGE_PLAN.md`, `REVIEW.md` and
  `STORY_COMPREHENSION_AUDIT.md`. Add an impact record under
  `design/audit_impacts/`. Add ledger rows marking the V36 README current
  and the V34 README historical.
- Run the V34 package's checks: `verify_revision.py`, `audit_book.py`
  against V34, the email-export check and the caption gate. Then run
  `python -X utf8 -B tools/audit_document_authority.py`,
  `python -X utf8 -B tools/audit_development.py --base auto` and
  `python -X utf8 -B -m unittest tools.tests.test_audit_document_authority tools.tests.test_audit_development`.
- Push to `codex/mermaid-roshan-picture-book`. Verify the V36 manifest and
  every file it lists over anonymous HTTPS from the exact commit, as V34's
  `verify_remote.py` does.

## Report back

- One line per build step and per work item (W1–W17 and C1–C14): done, held
  or blocked, with evidence paths.
- V36's caption gate counts beside V33's source-layer baseline (11 FAIL,
  5 OUTLINE_REQUIRED, 61 PASS) and V34's composed-art result (0 FAIL,
  7 OUTLINE_REQUIRED, 68 PASS).
- The remote verification receipt: commit, manifest SHA-256, check time and
  access mode.
- Every gap recorded instead of invented, with its reason.
- What stays open: owner acceptance, a child reading, a speech-language
  review and a physical test print.

## Everything in this handoff

[MANIFEST.json](MANIFEST.json) lists every file this handoff needs, with
its repository path, role, size and SHA-256 of the committed bytes. It
covers these documents, the book's rules and controls, the reference art,
every V34 render input, the 34 V34 proofs and the rear cover A proposal.

| File | Contents |
| --- | --- |
| `START_HERE.md` | This entry point. |
| `OWNER_DECISION_2026-10-19.md` | The governing owner decisions and the final manuscript. |
| `CHARACTER_CONSISTENCY_2026-10-19.md` | Character standards and fixes C1–C14. |
| `README.md` | Work items W1–W17 and their specifications. |
| `AUDIT.md` | The page-by-page audit of V33. |
| `references.json` | SHA-256 of the V33 sources and proofs named in the README. |
| `caption_contrast.py` | The numbers-only caption contrast gate; it writes no images. |
| `caption_contrast_v33.tsv` | The V33 baseline, 77 caption lines. |
| `MANIFEST.json` | Every file the handoff needs, hashed. |
