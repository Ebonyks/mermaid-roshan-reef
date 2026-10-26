# V38 A1–A10 build report

Status: `SUPPORTING_CURRENT`; static-book evidence. [Accepted work order](../../../handoffs/2026-10-25_v38_audit_fixes/README.md) at `1106170e845522afb48aadd20198500abed8cd28`; exact V37 baseline `eb405fe45edbcc37b59bebebba475de445cffb58`.

| Item | Result | Evidence |
| --- | --- | --- |
| A1 | DONE —22: three manual lines, no orphan, exact words/20pt/box/navy. | [Proof22](complete/page_22.png), [controls](BOOK_CURRENT.json). |
| A2 | DONE —16: all navy, halo/1pt outline, baselines110/84/58, clear splash/fin. | [Proof16](complete/page_16.png), [detail](details/caption_splash_clearance.png), [glyph geometry](complete/verification.json). |
| A3 | DONE —18: “needs help” together; same words, white and outline. | [Proof18](complete/page_18.png). |
| A4 | DONE — two 13 pt navy subtitle lines, right edge428.2, baselines262/246; inset/character clearance. | [Front](complete/page_00.png), [text geometry](complete/page_provenance.json). |
| A5 | DONE — clean-water shell pail replaces all bank plug/chain; foreground plug stays. | [Proof9](complete/page_09.png), [join](details/pail_join.png), [bounds/mask](BOOK_CURRENT.json). |
| A6 | DONE — tiny white plush head around far left curtain; silent sightings 10/rear. | [Rear](complete/page_33.png), [Lamma](details/lamma.png), [references](generation_evidence.json). |
| A7 | DONE — one thin corner web, four extra grey dust drifts, original shells/tufts preserved. | [Web](details/cobweb.png), [carpet](details/carpet.png), [outside-mask checks](complete/verification.json). |
| A8 | DONE — four faint plain lavender-grey wisps at closed threshold; no curl/face/reveal. | [Door](complete/page_05.png), [detail](details/door_dust.png), [rejected and selected takes](generation_evidence.json). |
| A9 | HELD — both native groups below 1800 px, slight contour drift. Exact V37 cutout/placement retained; print-edition upscale deferred. | [Two trials](generation_evidence.json), [hold](revision_scope.json), [unchanged bath](complete/page_09.png). |
| A10 | DONE — composed caption-free PDF method including actual local repairs, stroke excluded. | [86 lines/counts](composed_caption_contrast.json), [TSV](composed_caption_contrast.tsv), [strict gate](complete/verification.json). |

| Gate | V37 | V38 |
| --- | ---: | ---: |
| PASS | 79 | 79 |
| OUTLINE_REQUIRED, supported | 6 | 7 |
| FAIL | 0 | 0 |
| Lines | 85 | 86 |

Seven ImageGen calls; all native bytes, prompts, references/hashes, crop windows, masks and rejections retained. A5 one viable take; A6/A7shared local-edit reference plus focused carpet correction; A8 spiral take rejected, plain take selected; A9 two undersized trials then stop. Provider revision, seed and monetary usage are not exposed. No animation claim.

The [input remote receipt](handoff_remote_verification.json) verifies all 67supplied files anonymously at declared commits, alongside the [Git-byte receipt](handoff_local_verification.json). [Before/after](REVISION_REVIEW.html), [five passes](visual_audits.json), [email gate](complete/email_verification.json), [pagination](complete/print_pagination.json), [render provenance](complete/page_provenance.json) and [payload receipt](remote_verification.json) separate implementation, evidence and publication.

Page 16 global ascent overlaps the old focal box by 1.12 pt due to unused accent height. Actual glyph+stroke ends at 125.88; unchanged focal region starts 128, leaving2.12logical points. Actual ink+stroke is checked against every focal region; conservative layout-box inset checks stay. No collision is ignored and no focal boundary moved.

Open: A9 resolution, owner illustration approval, child reading, professional speech-language review, final trim/PPI and physical print. Q7 stays open. No invented story moment, new scene or game change. The [manifest](manifest.json) and [remote receipt](remote_verification.json) identify exact published commit, hashes, anonymous access and check time; publication is not creative acceptance.
