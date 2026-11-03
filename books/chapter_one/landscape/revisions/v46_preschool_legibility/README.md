# V46: preschool copy and solid lettering

Status: SUPPORTING_CURRENT review candidate. Responds to the owner's 2026-11-01 text-density and apparent-opacity rejection of V45r02. Publishing is part of this task on `Ebonyks/mermaid-roshan-reef`, branch `codex/mermaid-roshan-picture-book`, this directory. Anonymous exact-revision verification is recorded after publication; local files alone are staging.

[Read the book](complete/READ_BOOK.html) | [Reading PDF](complete/Mermaid_Roshan_Book_V46.pdf) | [Email PDF](complete/Mermaid_Roshan_Book_V46_Email.pdf) | [Exact before/after words](manuscript.json) | [Scope](revision_scope.json) | [Verification](complete/verification.json) | [Independent review](peer_review/final_candidate_review.json) | [Manifest](manifest.json) | [Remote receipt](https://github.com/Ebonyks/mermaid-roshan-reef/blob/codex/mermaid-roshan-picture-book/books/chapter_one/landscape/revisions/v46_preschool_legibility/remote_verification.json).

## What changed

- 509 caption words become 309: 39.3% less text. Maximum 14 caption words/page, plus the unchanged four bubble words.26 story captions change; six already-short captions stay. No held-word pages remain.
- The edit keeps the door/promise, safe bunny exit before draining, Rumi's help/rescue/offer, gentle Eagle rescue/apology, asking friends, shared work and belonging. Pictures carry details that do not need a second explanation. No new plot event or artwork is added. New story facts first drafted in V45 still await owner reading.
- Sniglet,20 logical pt body and18 logical pt bubbles remain. Navy is deeper and both inks receive a restrained0.30logicalpt same-colour strengthening stroke. On art, a separate backing is painted first and fully opaque solid ink goes on top. This fixes the hollow pale-letter effect caused by a dark stroke consuming a thin white face. Earlier paint alpha already defaulted to1; the problem was the visible ink interior, not evidence of a hidden transparency slider.
- All34 entries receive this lettering treatment, including unchanged cover/rear words. All native artwork streams/alpha, placements/crops, page dimensions/order and sources remain.14 uses darker lower water;15 is a single low-water line clearing the entire submerged tail;30 moves into floor quiet space.9 has four compact rows above the faucet.
- Historical renderer behaviour remains behind the no-profile branch. V46 explicitly opts into `v46_solid`, so old controls do not silently acquire a new visual method. No art generation, paid job, voice replacement or game change.

## Preschool editorial basis

The age-four brief is an editorial read-aloud target, not a diagnosis, decodability claim or universal word cap. Already-short opening/reveal pages are not padded. Keep some rich vocabulary, short conversations, playful sounds and feelings. [Colorado Libraries for Early Literacy](https://www.clel.org/early-literacy/storytime/selecting-picture-books/) recommends simple/predictive plots, humor, feelings and friendship for preschoolers. [Illinois Early Learning](https://illinoisearlylearning.org/tipsheets/bookspreschooler/) supports shared picture reading with humor/adventure and friendship/family themes. Neither source supplies this project's numeric word target. [Editorial record](editorial_review.json).

## Page report

| Story | Before words | V46 words | Text/layout |
| --- | --- | --- | --- |
| 1 | 4 | 4 | Words retained; box retained |
| 2 | 11 | 11 | Words retained; box retained |
| 3 | 6 | 6 | Words retained; box retained |
| 4 | 14 | 8 | Revised copy; leading default -> 26 |
| 5 | 23 | 12 | Revised copy; box retained |
| 6 | 16 | 14 | Revised copy; box retained |
| 7 | 20 | 11 | Revised copy; leading default -> 26 |
| 8 | 14 | 9 | Revised copy; box retained |
| 9 | 21 | 11 | Revised copy; box retained |
| 10 | 22 | 13 | Revised copy; leading default -> 26 |
| 11 | 9 | 9 | Revised copy; box retained |
| 12 | 6 | 6 | Words retained; box retained |
| 13 | 6 | 6 | Words retained; box retained |
| 14 | 17 | 5 | Revised copy; x 24 -> 32, y 84 -> 60, width 410 -> 440 |
| 15 | 12 | 8 | Revised copy; y 58 -> 32 |
| 16 | 21 | 10 | Revised copy; leading default -> 26 |
| 17 | 19 | 10 | Revised copy; box retained |
| 18 | 15 | 10 | Revised copy; leading 22 -> 26 |
| 19 | 20 | 12 | Revised copy; leading default -> 26 |
| 20 | 9 | 9 | Words retained; box retained |
| 21 | 15 | 6 | Revised copy; box retained |
| 22 | 25 | 10 | Revised copy; box retained |
| 23 | 22 | 12 | Revised copy; leading default -> 26 |
| 24 | 21 | 10 | Revised copy; box retained |
| 25 | 22 | 12 | Revised copy; box retained |
| 26 | 18 | 14 | Revised copy; leading 20 -> 26 |
| 27 | 12 | 9 | Revised copy; leading default -> 26 |
| 28 | 11 | 9 | Revised copy; leading default -> 26 |
| 29 | 13 | 11 | Revised copy; leading default -> 26 |
| 30 | 22 | 10 | Revised copy; y 110 -> 60, leading default -> 26 |
| 31 | 20 | 13 | Revised copy; leading default -> 26 |
| 32 | 23 | 9 | Revised copy; leading 20 -> 26 |

## Evidence and audit limits

[Actual PDF paint audit](lettering_paint_audit.json) tracks q/Q, graphics-state opacity, paint mode, ink RGB, font size and backing-before-fill on every painted line. [Font/glyph audit](font_glyph_audit.json) checks the actual embedded face's source cmap. The composed-caption contrast gate retains V37/V42 median/worst-decile thresholds, using the actual new ink colours; backing is excluded. Art-only and outside-caption pixel checks, image/alpha byte equality and327 source/font seals cover preservation. The two PDF exports are byte-identical and below 25 MB; there is no destructive email recompression.

[Five focused primary reviews](visual_audits.json) and [independent critique](peer_review/final_candidate_review.json) bind the exact PDFs/proofs. Five lenses are not five separate humans or child tests. The reviewer caught15's submerged-tail collision; rejected proofs/controls and the14contrast failure remain under `audit/`. [Question-card anchors](question_card_anchor_map.json) quote current delivered words; the other branch is untouched. Page 21 retains one top caption and lower apology bubbles; no literal interleaved oral reading order is claimed.

## Still open

Owner reading/illustration acceptance, actual human/child read-aloud, qualified speech-language review, physical test print, V41 Part 2 and doublewide arrival imposition/parity/gutter remain open. V44's inherited island/Sky Lagoon geography and seahorse-forehead continuity findings remain. This is not a whole-book art, print or game acceptance. No dev/master/release operation.

## Rebuild and preservation

Run `build_revision.py`, `make_review_sheets.py`, then `verify_revision.py`; authoring verification can use `--draft` before the final visual record exists, but delivery uses strict mode. `audit_book.py` routes V46 to that strict verifier. The overlay rebuild needs the native V44 PDF, current renderer, editable controls and Sniglet font; those dependencies are in the manifest. Full 327-source validation requires a complete checkout and the source-seal list, not only downloaded PDFs. Current project gates and exact outputs are in `validation_results.json`.

V45r02 and the parallel V45 package remain unchanged. The current baseline control copy and before/after manuscript preserve the prior copy, and the published baseline commit is 116b33fa829f7397e55f70af01be45dc39b3f85b. [V45r02](../v45_story_language_r02_review/README.md) remains historical evidence.
