# Before and after proposals — 30 September 2026

Status: **review samples, not a replacement book**. The owner requested screenshots of the recommended changes. [Open the comparison gallery](PREVIEWS.html), [comparison PDF](BEFORE_AFTER.pdf), or [manifest](manifest.json). The original V27 manuscript, renderer, protected art and accepted rear cover H remain unchanged.

## What is shown

| Story page | Proposed correction |
|---|---|
| 6 | Source-based sink/Roshan action cutout: the held sponge contacts the basin. |
| 8 | One subtle Lamb-a peeking from the towel basket; “dust bunny” replaces “playful pest.” |
| 13 | The removed cup is visibly clear of the seahorse’s mouth and water stream. |
| 15 | Connected hugging figures on blue stationery, with a tiny fountain echo. |
| 18 | Brush contacts the trapping bunny away from Eagle’s face; explicit action verb. |
| 19 | Larger speaking bunnies, central Eagle and smaller rounded native speech balloons. |
| 23 | Quiet wall recess behind shorter text, preserving the foreground art-making action. |
| 26 | Copy-only empathy cue: “Easy, Grand Puff!” |
| 27 | New ceiling extension above the unchanged complete accepted scene. |
| 31 | Roshan addresses the same rainbow Puff seen in the landing, now visibly present. |

Two additional diagrams show the glowing-door/Puff and bubbles/POP reveals on opposite sides of a page turn. They assume story page 1 is a recto. The diagram proposes combining current pages 19–20, shifting later beats, and reserving the freed page for a closing participation beat after these reveals. Inserting that page earlier would cancel the parity gain; the waterfall action should replace its existing page when sourced. It **does not** implement a new pagination or change the 34-page total.

## Art and layout boundaries

- Source inventory preceded generation. The sink action board is draft/reference evidence only; no accepted matching action image was found. The preview combines the existing sink and existing leaning Roshan reference with a bounded hand/tool adaptation.
- Existing book scenes remain the identity, action and staging authority. Generated full-frame edit candidates are not claimed to be pixel-identical outside the requested edit.
- Bath and craft-page changes are clipped to local areas in the native layout. Page 27 exposes only the new upper ceiling; its original lower scene is placed unchanged and uniformly scaled.
- The accepted landing itself is untouched. Puff’s foreground derivative is a generated isolation of that frame, not a claim of exact pixel extraction.
- All new cutouts have actual transparency, no scenic blob or sticker outline. The Rumi cutout’s tiny top hair crest still needs final edge inspection.
- Page 19 is a proposed foreground dialogue composition. Its enlarged bunnies exceed the current bottom-20% narrative-bunny zone; this is an explicitly visible layout proposal, not an unnoticed compliance pass. Silent decorations elsewhere keep their separate restrictions.
- The tiny fountain is substantially reduced after the first attempt; exact top-85%/12% bounds and ground occlusion remain subject to final measurement/acceptance.
- Sniglet is live text in the PDF, at least 18 pt on child-facing pages. Native balloons use curved paths and live lettering.
- Most new illustration masters are 1484 × 1060: useful review resolution, approximately 212 ppi at 7 × 5 inches, not a claimed 300 ppi print master.

## Hidden character

The sample uses the existing project Lamb-a identity in `assets/sprites/stuffie_studio/lamma.png`. It contains no child-facing arrow, label, prompt, count or search instruction. This set shows **one** proposed location. The final book would contain only two or three; other appearances and natural child discovery remain to be tested.

## Open recommendations

The full review still governs the remaining queue: opening dirty-castle source check, an accurate waterfall-clearing action, rescue-room continuity, other finale ceilings, cover/ending balance and a whole-book language/read-aloud pass. No source gap or master-audit finding is closed by these previews. Page-turn diagrams do not establish printer imposition.

## Evidence and rebuild

- [Generation jobs](generation_jobs.json): prompts, reference paths/hashes, native output hashes and candidate disposition, including rejected iterations.
- [Layout evidence](layout_evidence.json): source layers, bounded patches, native sizes and caption boxes.
- [Verification](verification.json): unchanged-book hashes, generated-file checks and visual-review qualifications.
- [Audit impact](../../../../design/audit_impacts/picture-book-before-after-20260930.json): applicable rules and exact changed-file coverage.
- [Comprehensive review](../../reviews/2026-09-30/REVIEW.md): original recommendations and full-book evidence.

Run `python -B books/chapter_one/previews/2026-09-30/build_previews.py` from the book worktree. Before screenshots are preserved inputs; the script rebuilds the comparison PDF, page screenshots and gallery. Their content is a review proposal, never an automatic update to `landscape/book.json`.

Repository destination: `Ebonyks/mermaid-roshan-reef`, branch `codex/mermaid-roshan-picture-book`, this versioned directory. Anonymous exact-revision retrieval is checked after publication. No runtime integration or release is part of this task.
