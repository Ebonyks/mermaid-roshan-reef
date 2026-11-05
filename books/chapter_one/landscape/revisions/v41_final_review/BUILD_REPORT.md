# V41 Part1 build report

Status: SUPPORTING_CURRENT; implementation and machine/visual acceptance are separate.

| Item | Result | Evidence |
| --- | --- | --- |
| Arrival repair | Done for review: complete original geography; no otter; four-tower castle; grounded plane | [Recipe](world_composition_provenance.json), [comparison](REVISION_REVIEW.html) |
| B1 dust | Done for review:0.291667in and2.25994:1 with exact audit method | [Measurements](dust_visibility.json), [actual page](complete/page_05.png) |
| B2 bath | Done: A9 closed as not needed at selected11in; no third take or enlargement | [Scope](revision_scope.json), [proof](complete/page_09.png) |
| P1 geometry | Held for owner illustration acceptance | [Work order](../../../handoffs/2026-10-26_v41_print_edition/README.md#p1-page-geometry) |
| P2 page extension | Held for owner illustration acceptance | Same work order; no print page extensions |
| P3 one enlargement | Held for owner illustration acceptance | No print enlargement; factor/PPI not applicable |
| P4 typography | Held for owner illustration acceptance | Existing review Sniglet controls exact |
| P5 arrival at print size | Held for owner illustration acceptance | Native sources preserved, review only |
| P6 bath print | Held for owner illustration acceptance | Current bath exact; no upscale |
| P7 print checks | Held for owner illustration acceptance | No print300ppi/bleed/safe-zone claim |
| P8 print files | Held for owner illustration acceptance | Only14×10in review master/reading PDF |

All70 handoff manifest inputs were independently verified against their pinned commits; [receipt](input_manifest_verification.json). Native source/font seal count322. All34 proof PNGs match actual lossless master renders;32 unnamed proofs and caption-free content are exact versus baseline. All346 previous source records, exact32-page words, manual breaks, caption controls, covers, pagination and reveal turns remain. [Verification](complete/verification.json) and [scope](revision_scope.json).

Caption contrast uses the same86-line composed-art sampling with contour excluded:79PASS,7OUTLINE_REQUIRED with actual support,0FAIL; V39 was79/7/0. No score is inferred. [Contrast](composed_caption_contrast.json).

Lossless master155,933,363bytes, SHA2562841e53057aa7b46add33ffab929535005f8a3e1a969563564c9f4580f6b5423; three exact binary parts. PNG-predictor encoding preserves decoded pixels. A bounded96MiB decoder allowance handles this trusted local6Kpage's80.9MB decodedRGB; historical helper/source unchanged. Email24,934,773bytes, SHA2567bc45c490eb590b89d0a51c3a18526d26bb3755689cf872b91ea64e095301259; minimum40.041704dB/page. Email keeps native image sizes, vector text/clips and lossless alpha; actual per-page40dB gate and25MB cap recorded in complete/email_verification.json. Initial85andarrival35 quality trials exceeded25MB despite fidelity passing, so the6Karrival JPEG quality was reduced only subject to that same page-fidelity gate; master unchanged.

Three actual built-in image-edit calls, all prompts/references/native attempts preserved. First arrival raw join rejected. Current output restores native central landmarks with only declared sky/foreground boundary repair; local source composition is not a full-scene redraw. The initial plane-on-grass pilot was corrected60nativepixels upward; original pilot critique is retained. [Generation](generation_evidence.json), [peer rounds](peer_review/README.md), [five passes](visual_audits.json).

Authority/development and52unit tests are executed and stdout retained in validation_results.json. Static-book scope makes Godot/runtime/device/game probes not applicable. Old V40's mechanical success did not establish contextual acceptance; its arrival is OWNER_REJECTED and historical. No finding closure or game-wide audit claim.

Required stop: owner illustration acceptance before Part2. Physical print, child and qualifiedSLP remain open. No printPPI/enlargement factors can be reported yet. No invented sources or print acceptance substitute for those gaps. Exact-revision anonymous publication receipt follows in remote_verification.json; manifest/receipt and final publication-only critique are excluded from circular payload hashing.
