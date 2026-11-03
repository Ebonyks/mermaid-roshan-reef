# V40 — arrival in one connected place

Status: SUPPORTING_CURRENT; static-book review candidate. Owner PDF3 / story2 is a wider blended composition showing the playground and Pearl Castle together, without the otter. All other 33 proofs, exact manuscript, captions, page order and V39 corrections remain unchanged.

[Read](complete/READ_BOOK.html) · [Email PDF](complete/Mermaid_Roshan_Book_V40_Email.pdf) · [Before/after](REVISION_REVIEW.html) · [Build report](BUILD_REPORT.md) · [Layer recipe](composition_provenance.json) · [Five focused audits](visual_audits.json) · [Second AI](peer_review/README.md) · [Machine evidence](complete/verification.json) · [Manifest](manifest.json).

This is a condensed book layout from existing approved artwork, not an exact runtime camera or geographic scale map. The native panorama supplies the connected landscape/path; the actual castle retains Roshan's stained glass. Existing slide and current runtime swing layers form the playground. The exact demo frame396 supplies the plane and its landing wheels through an alpha-only irregular cutout. No otter pixels enter that isolation. No new scene generation, RGB retouch, relighting, warped panorama or new character art is used. Sources, crops, scales, shadow fitting and hashes are in the layer recipe. Source originals and V39 remain intact.

The first candidate's tires overlapped foreground leaves. Independent critique rejected that contact; the complete plane moved onto clear stone and separate existing oval shadows now meet the tires. The rejected snapshot and exact critique are retained under peer_review. Publication and AI review do not constitute owner acceptance.

Rebuild: run ../v39_owner_corrections/reassemble_master.py for the exact baseline PDF when needed; compose_arrival.py; ../../render_book.py --book BOOK_CURRENT.json --output complete; ../v34_editorial_polish/optimize_pdf_lossless.py complete/Mermaid_Roshan_LANDSCAPE_ROUGH.pdf; reassemble_master.py --pack; email_export.py; build_review.py. The current master is also reconstructible byte-for-byte from complete/master_parts/parts.json using reassemble_master.py. Fresh changed exports require actual new visual review, followed by verify_revision.py and local_validation.py --run-contract-gates. No generation is rerun.

Rollback: restore BOOK_BASELINE.json to ../../book.json and reopen V39 at f55c094cfde2c1722eb210c74f85b868a4158ce9. No V39 file is edited. Native source resolution, A9 bath-resolution hold, owner/child/qualified SLP, final trim/PPI and physical print remain open. No print edition, game/runtime/dev/master/release or game-wide master-audit satisfaction claim.

Publication receipt is recorded in remote_verification.json after the exact-revision anonymous check; it is separate publication metadata, excluded from the payload hash cycle.
