# V37 — character and composition stress repair

Status: `SUPPORTING_CURRENT`; R7 review candidate. **20 initial run-throughs, seven revisions, five focused audits per revision. The final five found no remaining character/composition defect.** One AI reviewer; this is not independent human or publication acceptance.

[Read the book](complete/READ_BOOK.html) · [Review PDF, 24.17 MB](complete/Mermaid_Roshan_Book_V37_Email.pdf) · [Every run and comparison](STRESS_REPORT.md) · [Before/after](AUDIT_REVIEW.html) · [Final five audits](r07_audits.json) · [Machine verification](complete/verification.json) · [Manifest](manifest.json) · [Remote receipt](remote_verification.json).

34 pages, 32 interiors, 14 × 10 inch review. The owner manuscript, page turns, poses and source scenes remain intact. Bounded repairs unify hair/eyes/crown details, remove uncommissioned jewelry, restore bunny-ear continuity, ground the table sponge, soften rocky dust and clean repair joins. Captions 14 and 23 read as unified groups. The separately commissioned new rear scene is now in the book with spoiler-free copy.

The final gate seals 274 pre-existing source/font files against baseline `b5288f2ca2bab1e36d51fd9a00616de0dc30c2c0`, checks all 34 exact PDF proofs, the unchanged manuscript/order, geometry and pixels outside declared repairs. Caption contrast has 0 failures; six lines require and receive an outline. Email export preserves native image dimensions, vector text, clips and 75 alpha-mask placements; every page measures at least 40 dB against the lossless master.

The lossless master is 125.16 MB, exceeding GitHub's per-file limit. [Three exact binary parts](complete/master_parts/parts.json) preserve its original bytes. Download/clone the packet, then run `python reassemble_master.py` to reconstruct and verify the complete PDF. The smaller PDF above is a separate disclosed email derivative; the master and native artwork were not downsampled.

[Generation evidence](generation_evidence.json) records 33 calls, 32 selected native candidates and one rejected take, all exact input crops, prompts, native output hashes and exposed masks. Original files and V36 remain untouched. Failed revision proofs/controls and five-pass records are retained. Raw intermediate PDF builds are local staging; final master bytes and all required production sources are published.

Print remains open: the bath image is 1332 native pixels tall against the 1800 target, and final trim/PPI/physical print are unresolved. Owner illustration approval, child read-aloud and SLP review remain separate. No game changes or release acceptance.

Rebuild: use `BOOK_CURRENT.json` with `../../render_book.py --book <snapshot> --output <complete>`, run the unchanged `../v34_editorial_polish/optimize_pdf_lossless.py`, then `reassemble_master.py --pack`, `verify_revision.py` and `email_export.py`. Root `../../audit_book.py` routes V37 to the scoped strict gate with V36 as baseline. Generated natives are never edited by this rebuild.

To revert the review, restore the exact V36 `BOOK_BASELINE.json` to `../../book.json` and use the original V36 renderer/export at the baseline commit. The published V36 PDFs and all original sources remain available under `../v36_next_draft/`.
