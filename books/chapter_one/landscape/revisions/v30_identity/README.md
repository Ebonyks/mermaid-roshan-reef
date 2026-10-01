# V30 - comprehensive book polish

Status: `HISTORICAL_EVIDENCE`; published V30 baseline, superseded for current review by [V31](../v31_story_clarity/README.md). Original proof/generation/audit files remain unchanged.34 pages including covers;32 story pages;7 × 5 in landscape; Sniglet. Baseline `82a6dc1dba381c0b3ef507a8397512fa09ef624e`.

[Before/after of all34 pages](AUDIT_REVIEW.html) · [Reader](complete/READ_BOOK.html) · [Full PDF](complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Current page plan](../../PAGE_PLAN.md) · [Language review packet](SLP_REVIEW_PACKET.html) · [Print spread dummy](PRINT_DUMMY.html)

Six additional built-in candidates address recorded gaps: five selected derivatives and one rejected study. Across V29–V30, the polish has56 native candidates and29 selected derivatives. The [full prompt/reference/native-hash evidence](generation_evidence.json) records actual delivery layers and masks. Source originals are unchanged. The first trapped-face study is rejected; the stronger focused crop supplies only its declared facial polygon. V29’s rejected ceiling/scale/floor studies remain excluded and the accepted ceiling continues unchanged.

Independent final [character](character_final.json), [style](style_final.json) and [language](language_final.json) audits bind to the current proof. [Combined audit](visual_review.json):34/34 page minima meet internal4.9; overall minimum4.9, mean4.900. These are subjective editorial judgments, not master-audit or SLP acceptance. Resolved findings and actual score changes are documented.

Bubble quality is audited at native size and in final PDF renders. [Verification](complete/verification.json) checks all34 page pixels, manuscript, embedded font, source preservation and trim; [encoding evidence](complete/lossless_pdf_encoding.json) proves unchanged decoded image data. Native images are generally~212ppi at this trim, not300ppi.

Owner art/wording, Roshan's read-aloud/comprehension, physical print dummy and professional SLP review remain outstanding. The SLP packet applies developmental guidance without claiming sign-off.

## Build and delivery

From repository root, use the bundled Python runtime with Pillow, ReportLab, pypdf and pypdfium2:

```text
python -B books/chapter_one/landscape/render_book.py --output books/chapter_one/landscape/revisions/v30_identity/complete
python -B books/chapter_one/landscape/revisions/v30_identity/optimize_pdf_lossless.py books/chapter_one/landscape/revisions/v30_identity/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf
python -B books/chapter_one/landscape/revisions/v30_identity/verify_revision.py
python -B books/chapter_one/landscape/audit_book.py --proof books/chapter_one/landscape/revisions/v30_identity/complete --baseline books/chapter_one/landscape/revisions/v29_polish/complete
```

Rebuilding changes proof metadata/hash and requires final audit reconciliation. V30 adds six calls to V29’s50:56 polish candidates total;29 selected derivatives total. Optional native-copy scripts are staging helpers; the committed native PNGs are the durable project assets.

Established repository: `Ebonyks/mermaid-roshan-reef`; branch: `codex/mermaid-roshan-picture-book`; recipient access: anonymous HTTPS. [Manifest](manifest.json) lists exact source/build/review files and hashes. After push, `verify_remote.py <exact-commit> --receipt <output-path>` anonymously verifies the remote manifest and every required file. Remote byte verification proves delivery only. No dev/master integration or release is commissioned.
