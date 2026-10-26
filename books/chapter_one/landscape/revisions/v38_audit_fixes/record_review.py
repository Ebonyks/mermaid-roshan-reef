"""Record the final five scoped passes and current V38 review navigation."""
from pathlib import Path
import json,hashlib
V=Path(__file__).resolve().parent;L=V.parents[1];R=L.parents[2];C=V/'complete'
def read(p):return json.loads(p.read_text('utf8'))
def write(p,s):p.write_text(s,encoding='utf8',newline='\n')
def save(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
focus=[
('Named page controls and manuscript',['complete/page_00.png','complete/page_05.png','complete/page_09.png','complete/page_16.png','complete/page_18.png','complete/page_22.png','complete/page_33.png'],'A1/A3 three deliberate lines, identical words. A2 unified navy; A4 aligned subtitle. One foreground plug, pail in bank. Rear additions subordinate. No scene/pose replacement.'),
('Character identity, acting and context',['complete/contact_1.jpg','complete/contact_2.jpg','complete/contact_3.jpg','complete/contact_4.jpg','complete/contact_5.jpg','generation_evidence.json'],'Existing eyes/hair/tiara/ear/limbs and action contact stay V37. Tiny Lamma matches plush pale face/lashes/cheeks; sightings 10/rear. Both undersized bath trials rejected; original brush/chain acting retained.'),
('Alpha, joins and contact',['details/door_dust.png','details/pail_join.png','details/lamma.png','details/cobweb.png','details/carpet.png'],'No visible rectangle, cutout halo, floating pail, chain remnant or clipped dust identified. Original shells/tufts remain. Four new carpet drifts on bare red. Door wisps have no curls, face or Puff reveal.'),
('Typography, contrast and small details',['details/caption_splash_clearance.png','complete/page_00.png','complete/page_05.png','complete/page_16.png','complete/page_18.png','complete/page_22.png','composed_caption_contrast.json'],'Subtitle clears characters by over10pt. Actual page 16 glyph+stroke clears focal box by 2.12 pt; no splash/fin coverage. Four door wisps remain a quiet clue at reduced size. 79 PASS/7 OUTLINE_REQUIRED/0 FAIL, all supports present.'),
('Whole-book sequence, reveals and email',['complete/contact_1.jpg','complete/contact_2.jpg','complete/contact_3.jpg','complete/contact_4.jpg','complete/contact_5.jpg','details/email_export_review.png','complete/print_pagination.json','complete/email_verification.json'],'32 interiors+cover pair, story1right and13→14/23→24/27→28reveals. Sink/bath poses distinct. Rear promises beginning. Page25cloth/sofa, Whoosh14/15 and captions3/23 stay. No new email artifact identified; native/vector/alpha evidence passes.')
]
save(V/'visual_audits.json',dict(reviewer='One Codex AI reviewer; five focused passes, not independent human reviewers',date='2026-10-25',pdf_sha256=sha(C/'Mermaid_Roshan_LANDSCAPE_ROUGH.pdf'),email_sha256=sha(C/'Mermaid_Roshan_Book_V38_Email.pdf'),passes=[dict(pass_id=i+1,focus=f,inspected=p,observations=o,result='PASS_WITH_DECLARED_A9_HOLD',remaining_in_scope_defects=[],held=['A9 native resolution; exact V37 retained']) for i,(f,p,o) in enumerate(focus)],acceptance='No remaining identified defect in implemented A1-A8/A10. A9 held. Owner/child/SLP/trim/physical print remain open. Prior20run V37 review is historical, not counted as new V38 runs.'))
write(V/'README.md',"""# V38 — accepted V37 audit fixes

Status: `SUPPORTING_CURRENT`; review candidate. **A1–A8 and A10 implemented; A9 held after two native-resolution trials.** Five focused AI visual passes found no remaining identified defect in the implemented scope. Owner, child, SLP, trim and physical-print acceptance remain separate.

[Read](complete/READ_BOOK.html) · [Email PDF, 24.32 MB](complete/Mermaid_Roshan_Book_V38_Email.pdf) · [Before/after](REVISION_REVIEW.html) · [A1–A10 report](BUILD_REPORT.md) · [Five passes](visual_audits.json) · [Machine evidence](complete/verification.json) · [Manifest](manifest.json) · [Remote receipt](remote_verification.json).

The [accepted work order](../../../handoffs/2026-10-25_v38_audit_fixes/README.md) governs V38. V37 at `eb405fe45edbcc37b59bebebba475de445cffb58` remains untouched. Seven proofs change: front,5,9,16,18,22,rear. All other 27 proofs are byte-identical. All 307 unique V37 source/font files are sealed against that exact Git tree; its 331 source-key records are preserved.

Manual line breaks, unified navy caption, two-line subtitle, a shell pail replacing the bank plug, hidden Lamma, corner cobweb, four extra carpet drifts and four faint threshold wisps are implemented through bounded controls/masks. Original scenes and character actions stay intact.

A9 did not meet the brief: both generated outputs are 1330 px tall with small ponytail/brush contour drift. Neither is substituted. The approved 1332 px V37 bath stays exact. No padded/upscaled file is described as native detail. Final trim remains open; no print edition starts.

Caption gate: V37 **79 PASS / 6 OUTLINE_REQUIRED / 0 FAIL** of85 lines; V38 **79 / 7 / 0** of86. Every required support is present. The caption-free final composition includes local repairs and excludes stroke from contrast. Actual glyph+stroke focal geometry refines the font-wide unused accent height on16:2.12logical points clear of the unchanged focal box.

The 125,862,672-byte lossless master is preserved in [three exact binary parts](complete/master_parts/parts.json). Run `python reassemble_master.py` to reconstruct SHA-256 `d8125dde586bcfb2fd775cd6c034f4b27a73428b760663d30d9d684eae64c037`. The separate 24,324,210-byte email PDF preserves native dimensions, vector text/clips and 83 byte-exact alpha placements; minimum 40.230 dB/page.

Rebuild with `prepare_revision.py`, `../../render_book.py --book BOOK_CURRENT.json --output complete`, existing `../v34_editorial_polish/optimize_pdf_lossless.py`, then `reassemble_master.py --pack`, `email_export.py`, `build_review.py` and `verify_revision.py`. Use project Python with PDF dependencies. Root `../../audit_book.py` routes to V38 with V37 baseline. A changed PDF requires fresh visual review; rebuilds preserve native art.

Revert by restoring `BOOK_BASELINE.json` to `../../book.json` and using V37's sealed renderer/exports at its baseline commit. Do not edit the V37 folder. No game/runtime/dev/master/release/print-edition changes. [Impact](../../../../../design/audit_impacts/picture-book-v38-audit-fixes-20261025.json). Publication proves bytes, not creative acceptance.
""")
write(V/'BUILD_REPORT.md',"""# V38 A1–A10 build report

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
""")
write(R/'books/chapter_one/README.md',"""# Mermaid Roshan and the Hidden Rainbow

Status: `SUPPORTING_CURRENT`; [V38 audit fixes](landscape/revisions/v38_audit_fixes/README.md), exact owner manuscript,34 pages/32 interiors,14 × 10 inch review.

[Read](landscape/revisions/v38_audit_fixes/complete/READ_BOOK.html) · [Review PDF](landscape/revisions/v38_audit_fixes/complete/Mermaid_Roshan_Book_V38_Email.pdf) · [A1–A10](landscape/revisions/v38_audit_fixes/BUILD_REPORT.md) · [Before/after V37](landscape/revisions/v38_audit_fixes/REVISION_REVIEW.html) · [Design language](DESIGN_LANGUAGE.md).

A1–A8/A10 implemented; five focused AI passes identify no remaining defect in that scope. A9 held after two undersized trials; approved V37 bath stays exact. Caption contrast79 PASS/7 OUTLINE_REQUIRED/0 FAIL. All 27unnamed proofs and307 unique V37 source/font files preserved. Owner/child/SLP/resolution/trim/physical-print acceptance remain open. V36/V37 and original evidence stay published. No game changes.
""")
write(L/'REVIEW.md',"""# V38 review

Status: `SUPPORTING_CURRENT`. [A1–A10](revisions/v38_audit_fixes/BUILD_REPORT.md), [before/after](revisions/v38_audit_fixes/REVISION_REVIEW.html), [five passes](revisions/v38_audit_fixes/visual_audits.json), [machine evidence](revisions/v38_audit_fixes/complete/verification.json).

Seven named proofs change through captions and bounded additions. All 27unnamed proofs,307 unique source/font files and331 V37 source-key records stay exact. The old 20-run/seven-cycle V37 report is historical, not a new V38 claim.

Five focused AI passes identify no remaining implemented A1–A8/A10 defect. Seven native calls retain rejected spiral dust, unused broad dust changes and two undersized bath trials. The bath remains 1332 native pixels; A9 held, no print-resolution pass claimed.

Composed contrast79 PASS/7 OUTLINE_REQUIRED/0 FAIL of86 lines, all supports present. Actual page 16 glyph/stroke clears the unchanged focal region by 2.12 pt; unused font ascent is not ink. The 24.32 MB email preserves native sizes, vector/clips and83 exact alpha placements; minimum 40.230 dB/page.

Owner/child/SLP/final trim/PPI/A9 resolution/physical print remain open. No game/runtime/dev/master/release work.
""")
write(L/'STORY_COMPREHENSION_AUDIT.md',"""# V38 story-comprehension review

Status: `SUPPORTING_CURRENT`; editorial only, no child or clinical SLP acceptance.

Exact owner words and page order stay V37. Four faint threshold wisps support the sniffle without revealing Puff. Page9's clean-water pail answers draining and hints at10, leaving one story plug. Two silent Lamma sightings remain on 10 and the rear. Rear dust/web promise a cleaning beginning without revealing transformation.

Playroom/art-room line breaks keep phrases together; the Rumi caption is one evenly spaced navy block. Subtitle clears the cast. These are editorial judgments, not measured learning outcomes.

Eagle stays trapped under two bunnies; Roshan brushes each away before apology. Cooperative washing precedes Puff's rainbow reveal. Turns13→14,23→24,27→28, page25sofa/cloth and Whoosh14/15stay.

[Comparisons](revisions/v38_audit_fixes/REVISION_REVIEW.html), [binding order](revisions/v38_audit_fixes/complete/print_pagination.json), [five passes](revisions/v38_audit_fixes/visual_audits.json). Approved bath pose remains exact; native resolution held after two trials. Child read-aloud and professional speech-language review remain open.
""")
p=L/'PAGE_PLAN.md';s=p.read_text('utf8').replace('# V37 page plan','# V38 page plan').replace('(revisions/v36_next_draft/print_pagination.json)','(revisions/v38_audit_fixes/complete/print_pagination.json)').replace('Chirp, chirp! / “Someone in the playroom needs help!” said Roshan.','Chirp, chirp! / “Someone in the playroom / needs help!” said Roshan.').replace('In the art room, Roshan put the paints in their places. / Then she scrubbed the table. Scrub, scrub!','In the art room, Roshan put / the paints in their places. / Then she scrubbed the table. Scrub, scrub!');write(p,s)
p=R/'books/chapter_one/DESIGN_LANGUAGE.md';s=p.read_text('utf8');heading='## V38 owner decision (2026-10-25)'
if heading not in s:s+='''\n\n## V38 owner decision (2026-10-25)\n\nThe owner wrote: “Write the V38 Codex handoff for the V37 audit fixes, using your suggested defaults for Q1-Q6; leave Q7 (final trim) open.” The [accepted packet](handoffs/2026-10-25_v38_audit_fixes/README.md) governs A1–A10; the 2026-10-19 manuscript and character standards stay in force. This permits bounded rear Lamma/web/dust and door-dust additions and the higher-resolution W3b trial, without a new scene, pose, wording, game or release change.\n\n[V38](landscape/revisions/v38_audit_fixes/README.md) implements A1–A8/A10 with exact V37 originals and unnamed pages preserved. A9 held after two undersized trials with slight contour drift; approved bath stays exact. Five focused AI passes,307source/font seals and composed contrast are scoped evidence. V37's sealed folder is historical. Owner/child/SLP/final trim/PPI/physical-print gates stay open; no print edition starts.\n'''
write(p,s)
if not (V/'remote_verification.json').exists():save(V/'remote_verification.json',dict(status='PENDING_PUBLICATION',note='Replaced after exact-commit anonymous manifest/all-file verification; excluded from manifest to avoid circular hashes.'))
print('V38 visual review and current book docs recorded')
