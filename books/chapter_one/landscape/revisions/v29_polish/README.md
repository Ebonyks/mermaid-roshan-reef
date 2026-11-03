# V29 - comprehensive book polish

Status: `SUPPORTING_CURRENT`; complete iterated review proof.34 pages including covers;32 story pages;7 × 5 in landscape; Sniglet. Baseline `5da33b22c9b95358d98defe8e340a901d5470991`.

[Before/after of all34 pages](AUDIT_REVIEW.html) · [Reader](complete/READ_BOOK.html) · [Full PDF](complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf) · [Current page plan](../../PAGE_PLAN.md) · [Language review packet](SLP_REVIEW_PACKET.html)

50 built-in image-generation candidates were made for recorded gaps;24 selected derivatives and26 rejected studies are preserved. The [full prompt/reference/native-hash evidence](generation_evidence.json) records actual delivery layers and masks. Source originals are unchanged. Rejected ceiling/scale/floor studies are excluded; the approved coherent ceiling is reused.

Independent final [character](character_final.json), [style](style_final.json) and [language](language_final.json) audits bind to the current proof. [Combined audit](visual_review.json):29/34 page minima meet internal4.9; overall minimum4.8, mean4.885. These are subjective editorial judgments, not master-audit or SLP acceptance. Sub-target details are retained openly.

Bubble quality is audited at native size and in final PDF renders. [Verification](complete/verification.json) checks all34 page pixels, manuscript, embedded font, source preservation and trim; [encoding evidence](complete/lossless_pdf_encoding.json) proves unchanged decoded image data. Native images are generally~212ppi at this trim, not300ppi.

Owner art/wording, Roshan's read-aloud/comprehension, physical print dummy and professional SLP review remain outstanding. The SLP packet applies developmental guidance without claiming sign-off.

## Build and delivery

From repository root, use the bundled Python runtime with Pillow, ReportLab, pypdf and pypdfium2:

```text
python -B books/chapter_one/landscape/render_book.py --output books/chapter_one/landscape/revisions/v29_polish/complete
python -B books/chapter_one/landscape/revisions/v29_polish/optimize_pdf_lossless.py books/chapter_one/landscape/revisions/v29_polish/complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf
python -B books/chapter_one/landscape/revisions/v29_polish/verify_revision.py
python -B books/chapter_one/landscape/audit_book.py --proof books/chapter_one/landscape/revisions/v29_polish/complete --baseline books/chapter_one/landscape/revisions/v28_kindness/complete
```

Rebuilding changes proof metadata/hash and requires final audit reconciliation. Optional native-copy scripts are staging helpers; the committed native PNGs are the durable project assets.

Established repository: `Ebonyks/mermaid-roshan-reef`; branch: `codex/mermaid-roshan-picture-book`; recipient access: anonymous HTTPS. [Manifest](manifest.json) lists exact source/build/review files and hashes. After push, `verify_remote.py <exact-commit> --receipt <output-path>` anonymously verifies the remote manifest and every required file. Remote byte verification proves delivery only. No dev/master integration or release is commissioned.
