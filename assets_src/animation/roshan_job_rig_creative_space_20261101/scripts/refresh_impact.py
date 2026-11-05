from pathlib import Path
import json
P=Path(__file__).resolve().parents[1];R=P.parents[2]
f=R/'design/audit_impacts/roshan-job-rig-creative-space-20261101.json'
d=json.loads(f.read_text(encoding='utf-8'))
d['files']=[a.relative_to(R).as_posix() for a in P.rglob('*') if a.is_file() and not any(x in a.relative_to(P).parts for x in ['.godot','__pycache__','raw']) and not a.name.endswith(('.uid','.import','.ffconcat'))]
d['files']+=['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md']
d['verification_base']='93166ab1828ab9857227d038f8833b92dfb2f9f1; initial source baseline preserved; see evidence/regression/base_reconciliation.json'
d['validation']=[
 dict(command='Godot 4.7.2-stable Mobile res://capture_all.gd',result='PASS',evidence='evidence/native_audit.json: 1757 frames; 873 exact seed RGBA cases; 125 mixtures/375 fresh-instance cases; 27144 live swaps; source poison/underlay controls.'),
 dict(command='Godot 4.7.2-stable Mobile res://contact_audit.gd',result='PASS',evidence='evidence/contact_audit.json: 152 active-contact frames; declared 3px bound; contact alpha; native grip/fixture/view and three original-clothing reinsertion controls.'),
 dict(command='python -B <packet>/scripts/source_gates.py; Aseprite master reopen/export comparison',result='PASS',evidence='evidence/source_gates.json: 84 checks; evidence/master_roundtrip.json: nine exact RGBA master round trips. Seed bones/rest/common weights/triangles and original curves preserved; no production/protected/save change.'),
 dict(command='Unchanged seed geometry/motion audits and same-floor job measurements; independent mixed-slot outlines',result='FAIL',evidence='evidence/numeric/summary.json: original/ballet/magician pass. Both new skins and both jobs fail seams; astronaut tail stretch .788 < .80 and valve speed/acceleration 142.22/856.73 exceed 140/650. evidence/mixed/audit.json: 45/375 inherited mixed-slot failures. REVIEW_CANDIDATE_NUMERICALLY_REJECTED; no floors changed.'),
 dict(command='Unchanged scripts/ci.sh static checks and trusted probe roster',result='PENDING',evidence='evidence/regression/; first import crash retained, fresh import passed; local scan-orchestrator timeout retained; initial timing-sensitive Slide audio failure retained; full result and fresh replay required.'),
 dict(command='Agent static native-frame inspection',result='FAIL',evidence='evidence/agent_visual_review.json: exact six named boards/frames; painter hard neckline/shoulder boundary rejected; astronaut lower-hood/neck and fin/costume joins need repair/review. Small boards do not accept native contours.'),
 dict(command='Normal-speed and complete frame-step human/owner/device/child review',result='PENDING',evidence='Review films/boards retained. Desktop player launch approval timed out; no normal-speed review claimed. Exact formal human/device/child/owner acceptance remains separately blocking.'),
 dict(command='Complete animation derivation provenance',result='PENDING',evidence='All four native revised-prompt events, native outputs, source inventory, hashes and edits retained. Per-IMAGE fitting call order was not separately transcribed; revisedPrompt events are not submitted-input records. Cleanup minutes/builtin billing were not separately exposed. No provenance-completeness claim.'),
 dict(command='Corrected seed anonymous remote verification',result='PASS',evidence='evidence/upstream_seed_remote_verification.json: b700b846d1d2f4b1843279f268e2bb12e4b1f4ec; exact frozen manifest and every payload file fetched anonymously and SHA-256 verified. Rejected 26bd6d1f excluded.'),
 dict(command='Shared-contract owner publication',result='PENDING',evidence='Shared contract remains owner-local freeze b2a5dfe9, not owner-published; this exact archival copy does not confer owner publication or acceptance.'),
 dict(command='Own downstream GitHub payload verification',result='PENDING',evidence='Transport receipt pending at source snapshot; later audit/receipts record binds exact payload commit, hashes, anonymous access and check time. Archive transport never accepts this rejected candidate.')]
final=P/'evidence/final_gates.json'
if final.exists():
    measured=json.loads(final.read_text(encoding='utf8'))
    if measured.get('passed'):
        item=next(x for x in d['validation'] if x['command'].startswith('Unchanged scripts/ci.sh'))
        item.update(result='PASS',evidence='evidence/final_gates.json: all 58 unchanged static checks (governance replay after path creation), approved 4.7.2 import, 2D NO_REGRESSION and all 82 trusted probes on current 93166ab base. Separate isolated prefix/tail scheduling; original failures retained. No test assertions or floors changed.')
receipt=R/'audit/receipts/roshan-job-rig-creative-space-20261101-remote.json'
if receipt.exists():
    d['files'].append(receipt.relative_to(R).as_posix())
    transport=json.loads(receipt.read_text(encoding='utf8'))
    if transport.get('passed'):
        item=next(x for x in d['validation'] if x['command']=='Own downstream GitHub payload verification')
        item.update(result='PASS',evidence='audit/receipts/roshan-job-rig-creative-space-20261101-remote.json: anonymous exact remote manifest/payload/source-reference fetches and SHA-256 checks at '+transport['payload_revision']+'. ARCHIVE_COMPLETE only; GENERATION_READY=false and DELIVERY_ACCEPTED=false.')
d['acceptance_gaps']='Numerically rejected source-only review candidate. Failed tail/job seams, astronaut tail stretch and valve timing, 45 inherited mixed-slot outlines, unpublished owner shared contract, unsupported authored views and pickup/release transitions, normal-speed human review (desktop launch approval timed out), device, child and owner acceptance remain blocking. Original source/curves/common rests/weights and contact/state passes do not establish natural motion or close findings. Full project gates and own anonymous publication receipts are reported separately.'
f.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print('IMPACT COVERAGE',len(d['files']),'files')
