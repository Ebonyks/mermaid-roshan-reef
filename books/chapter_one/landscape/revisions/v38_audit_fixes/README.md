# V38 — accepted V37 audit fixes

Status: `SUPPORTING_CURRENT`; review candidate. **A1–A8 and A10 implemented; A9 held after two native-resolution trials.** Five focused AI visual passes found no remaining identified defect in the implemented scope. Owner, child, SLP, trim and physical-print acceptance remain separate.

[Read](complete/READ_BOOK.html) · [Email PDF, 24.32 MB](complete/Mermaid_Roshan_Book_V38_Email.pdf) · [Before/after](REVISION_REVIEW.html) · [A1–A10 report](BUILD_REPORT.md) · [Five passes](visual_audits.json) · [Machine evidence](complete/verification.json) · [Manifest](manifest.json) · [Remote receipt](remote_verification.json).

The [accepted work order](../../../handoffs/2026-10-25_v38_audit_fixes/README.md) governs V38. V37 at `eb405fe45edbcc37b59bebebba475de445cffb58` remains untouched. Seven proofs change: front,5,9,16,18,22,rear. All other 27 proofs are byte-identical. All 307 unique V37 source/font files are sealed against that exact Git tree; its 331 source-key records are preserved.

Manual line breaks, unified navy caption, two-line subtitle, a shell pail replacing the bank plug, hidden Lamma, corner cobweb, four extra carpet drifts and four faint threshold wisps are implemented through bounded controls/masks. Original scenes and character actions stay intact.

A9 did not meet the brief: both generated outputs are 1330 px tall with small ponytail/brush contour drift. Neither is substituted. The approved 1332 px V37 bath stays exact. No padded/upscaled file is described as native detail. Final trim remains open; no print edition starts.

Caption gate: V37 **79 PASS / 6 OUTLINE_REQUIRED / 0 FAIL** of85 lines; V38 **79 / 7 / 0** of86. Every required support is present. The caption-free final composition includes local repairs and excludes stroke from contrast. Actual glyph+stroke focal geometry refines the font-wide unused accent height on16:2.12logical points clear of the unchanged focal box.

The 125,862,672-byte lossless master is preserved in [three exact binary parts](complete/master_parts/parts.json). Run `python reassemble_master.py` to reconstruct SHA-256 `d8125dde586bcfb2fd775cd6c034f4b27a73428b760663d30d9d684eae64c037`. The separate 24,324,210-byte email PDF preserves native dimensions, vector text/clips and 83 byte-exact alpha placements; minimum 40.230 dB/page.

Rebuild with `prepare_revision.py`, `../../render_book.py --book BOOK_CURRENT.json --output complete`, existing `../v34_editorial_polish/optimize_pdf_lossless.py`, then `reassemble_master.py --pack`, `email_export.py`, `build_review.py` and `verify_revision.py`. Use project Python with PDF dependencies. Root `../../audit_book.py` routes to V38 with V37 baseline. A changed PDF requires fresh visual review; rebuilds preserve native art.

Revert by restoring `BOOK_BASELINE.json` to `../../book.json` and using V37's sealed renderer/exports at its baseline commit. Do not edit the V37 folder. No game/runtime/dev/master/release/print-edition changes. [Impact](../../../../../design/audit_impacts/picture-book-v38-audit-fixes-20261025.json). Publication proves bytes, not creative acceptance.
