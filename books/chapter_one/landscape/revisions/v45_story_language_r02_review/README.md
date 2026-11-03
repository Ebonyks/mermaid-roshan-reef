# Mermaid Roshan and the Dust Bunnies: V45 r02 strict review

Status: SUPPORTING_CURRENT. **23of25 captions implemented; stories11and15 held with exact V44 words.** Page21 bubbles read “Sorry!” and “We’ll be gentle!”. No art changes or generation.

[Read](complete/READ_BOOK.html) · [Reading PDF](complete/Mermaid_Roshan_Book_V45.pdf) · [Email PDF](complete/Mermaid_Roshan_Book_V45_Email.pdf) · [Held-page shortening request](HELD_PAGES.md) · [Verification](complete/verification.json) · [Independent critique](peer_review/README.md).

The new arc moves from feeling overwhelmed to one small job, helping friends, asking for help, shared cleanup and belonging. Only exact supplied words are used on implemented pages; deliberate line breaks may differ. No words were cut and no body or bubble type was reduced (20pt/18pt logical, twice that in the review PDF). Page17 fits in its existing narrow column after wrapping, so no needless widening was applied.

Existing V44 image streams, alpha and nontext vectors remain. Text-only PDF replacement avoids picture recompression. All34 caption-free renders and all pixels outside old/new caption areas match V44;11unchanged entries (covers,7unchanged stories and2held stories) retain exact page content/render. Both PDFs are byte-identical reading/email copies,24,783,122bytes each; this is not a new lossless full-book print master. Earlier versions and source originals remain intact.

## Requested page report

| Story | Result | Caption controls (logical points) |
| --- | --- | --- |
| 4 | Done | Box unchanged |
| 5 | Done | Box unchanged |
| 6 | Done | Box unchanged |
| 7 | Done | y:60→84 |
| 8 | Done | Box unchanged |
| 9 | Done | align:center→left; width:440→180; x:32→46; manual line wrap |
| 10 | Done | y:58→84 |
| 11 | Held; exact V44 | Box unchanged |
| 14 | Done | line_baselines:[84, 58, 32]→None; width:338→410 |
| 15 | Held; exact V44 | Box unchanged |
| 16 | Done | line_baselines:[110, 84, 58]→None |
| 17 | Done | Box unchanged |
| 18 | Done | leading:None→22; y:88→98; manual line wrap |
| 19 | Done | Box unchanged |
| 21 | Done | Box unchanged; bubbles updated; authorized single-top-caption fallback |
| 22 | Done | Box unchanged; manual line wrap |
| 23 | Done | Box unchanged; manual line wrap |
| 24 | Done | Box unchanged |
| 25 | Done | Box unchanged |
| 26 | Done | leading:None→20 |
| 27 | Done | Box unchanged |
| 29 | Done | Box unchanged |
| 30 | Done | y:84→110 |
| 31 | Done | Box unchanged |
| 32 | Done | leading:None→20; width:424→456; x:40→24; manual line wrap |

## Caption and reading evidence

Exact V37/V42 composed-art method, actual caption-free delivery, same fill/median/worst-decile thresholds and stroke excluded: **V44 77PASS/7OUTLINE_REQUIRED/0FAIL; V45 99PASS/9OUTLINE_REQUIRED/0FAIL.** All9 outline-required lines have the existing1pt-or-heavier/halo treatment. The baseline is V44 itself; do not reuse V42's old86-line count or invent a V44 run from it. [Full line evidence](composed_caption_contrast.json).

Five focused final inspections and the independent review cover wording, geometry, artwork preservation, contrast and story flow. Native PDF halo text uses stroke/fill draw passes, which can repeat strings in plain extraction; verification accounts for those exact paint operations and separately checks one visible caption against the manuscript.

[Read-through evidence](read_aloud_review.json): an offline synthetic voiced rehearsal plus editorial cadence review, not a human listening session or qualified speech-language review. Preserve pauses at “Click!”, the promise, the apology and “Everyone needs help sometimes”. No reviewer rewording is authorized. Actual spoken read-aloud with Roshan remains open.

## Preserved scope and delivery

Input order550a0b86216dee020d5070428ab4ddcfe0da4dc1 and its48committed file hashes were verified before work. V44 art/source baseline49a199846c61a39a3735e162214706b3687f12d3;327source/font files sealed unchanged. [Scope](revision_scope.json), [controls](BOOK_CURRENT.json), [source seals](source_seals.json), [page status](page_status.json), [task impact](../../../../../design/audit_impacts/picture-book-v45-story-language-20261101.json). Rebuild uses the listed V44 PDF/font/renderer plus V45 controls and helper. Strict historical source checking requires a full Git clone with both pinned commits; the narrow publication packet is not the whole historical art archive.

Destination: Ebonyks/mermaid-roshan-reef, codex/mermaid-roshan-picture-book, this versioned folder; anonymous HTTPS verifies every manifest member at the immutable payload revision. Receipt and publication-impact metadata are excluded from their own manifest to avoid circular hashes. No game/dev/master/release change.

Rollback: restore BOOK_BASELINE.json to ../../book.json and use V44's sealed PDFs. The owner still reviews the new story facts (Puff's size/sneeze dust/apology, cleaning sparkles and Rumi's return-help offer). V44 geography/fountain findings, illustration acceptance, V41 printPart2, arrival imposition/gutter, physical proof, actual child read-aloud and qualifiedSLP remain open. The grown-up question card remains on its separate branch; [delivered quote-anchor map](question_card_anchor_map.json) records current versus requested text without changing that branch.

## Parallel V45 package preserved

A separate V45 draft was published during this task at01004e37ff00e51cb9048906fa64d019923541c3 (payload1cecfdb872b619f12da97e027ce5d8dca0cc3b45). Its entire version folder is preserved unchanged. It includes a declared page11 wording adaptation not yet owner-accepted. This r02 follows the supplied exact-word/hold rule and also holds15 for a confirmed tail overlap. Current pointers select this strict review; the earlier draft remains available for comparison and rollback. PDFs/proofs built before relocation retain exact bytes; only paths/control revision labels and documentation change. No artwork or words were regenerated for this reconciliation.
