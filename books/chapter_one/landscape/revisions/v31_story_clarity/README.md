# V31 - story clarity and belonging

Status: `HISTORICAL_EVIDENCE`; original published V31 review proof. Current edition: [V32](../v32_rainbow_story/README.md). Its water treatment and separate ending have been superseded; original artwork and audits remain evidence.34 pages including both covers;32 interiors;7 x5 inches landscape;Sniglet. Exact V30 baseline: `19ee6ce8ec4c20c05714f101d0d222a33477e400`.

[All-page before/after](AUDIT_REVIEW.html) · [Reader](complete/READ_BOOK.html) · [Full PDF](complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Bound spread dummy](PRINT_DUMMY.html) · [Language review packet](SLP_REVIEW_PACKET.html) · [Manifest](manifest.json)

Page12 now describes partial progress with clear aqua water, reserving the rainbow for13. Both captions avoid the unsupported stream count. Page23 retains the correct castle hall, completed doors, route lights and source stairs, but replaces the welcoming rainbow door with closed shadowed violet and a narrow mysterious glow. Roshan's cautious expression matches the rumble. Page31 gives Grand Puff thanks and an invitation to rest; it resolves the main encounter before32's inclusive nap instead of reopening the Eagle subplot. Tiny sleepy bunnies support that settling rhythm. A discreet canonical Lamma peek joins the rear cover, while the old31 cameo is removed; two sightings remain.

An additional early exploration page was analyzed but not selected: a simple insert/delete spoils both reveal turns, and compensating by merging bath actions would reduce their visual clarity. The existing castle-entry/dirty-hall setup remains. This is an editorial choice available for owner review, not a new scene invention.

Five built-in image-generation calls produce local candidate pixels only. Exact [prompts, references, native hashes and delivered masks](generation_evidence.json) are durable project assets. The initial composed mask errors were caught and revised: waterfall lane/reflection scope follows material boundaries, and the original stair artwork remains unchanged. Complete full-scene bases, V30 character repairs, strong21 and exact landing29 are retained.

[Independent audit](visual_review.json), [PDF/pixel/source verification](complete/verification.json) and [stress checks](complete/stress_results.json) separate observations from machine evidence.29 page PNGs remain byte-identical to V30. The lossless PDF uses embedded editable Sniglet; native artwork remains approximately212ppi at trim, not a certified300ppi press master. No professional SLP approval, child test, print approval or game-wide master-audit satisfaction is claimed.

## Rebuild and delivery

```text
python -B books/chapter_one/landscape/render_book.py --output books/chapter_one/landscape/revisions/v31_story_clarity/complete
python -B books/chapter_one/landscape/revisions/v31_story_clarity/optimize_pdf_lossless.py books/chapter_one/landscape/revisions/v31_story_clarity/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf
python -B books/chapter_one/landscape/revisions/v31_story_clarity/verify_revision.py
python -B books/chapter_one/landscape/audit_book.py --proof books/chapter_one/landscape/revisions/v31_story_clarity/complete --baseline books/chapter_one/landscape/revisions/v30_identity/complete
```

Rebuilds require reconciliation of actual proof/audit hashes. Established destination: `Ebonyks/mermaid-roshan-reef`, branch `codex/mermaid-roshan-picture-book`; anonymous HTTPS recipient access. After push, `verify_remote.py <exact-commit> --receipt <outside-repo-output>` fetches the exact remote manifest and every required file without credentials. Publication and byte identity do not grant creative acceptance. No dev/master integration or game release is commissioned.
