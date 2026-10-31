from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[3]
src=Path(__file__).resolve().parent
read=lambda name:json.loads((src/name).read_text())
before=read('review_current_05/capture.json');after=read('review_current_06/capture.json')
select=lambda d:[{'id':x['id'],'phase_progress':x['phase_progress'],'widget_fill':x['widget_fill']} for x in d['captures'] if 'frost-complete' in x['id']]
old,new=select(before),select(after)
assert len(old)==len(new)==2
assert all(5.999<x['phase_progress']<6 for x in old)
assert all(x['phase_progress']==6 for x in new)
receipt={'status':'CURRENT_GUI_ENDPOINT_PASS','before':old,'after':new,
    'trigger':'Raw Canvas touch transforms place the final source-aligned point at0.999999934; the existing surface stops input at>=0.999, so exact world>=1.0 could leave5.999999605/6 forever.',
    'repair':'Only Chef authored-trace world completion now uses the same existing surface>=0.999 terminal-prefix convention. Goals/counts and wrong/passive/partial rules unchanged; sibling career thresholds unchanged.',
    'negative_evidence':'Current06 asserts that quarter, half and three-quarter earned trace prefixes do not complete; it requires the actual finished picture and exact6.0goal after the full raw GUI stroke at both widths.',
    'source_before':read('capture_current_05_receipt.json')['source_sha256'],
    'source_after':read('capture_current_06_receipt.json')['source_sha256'],
    'current_frame_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (src/'review_current_06').glob('*frost-complete*.png')},
    'limits':'Configured desktop Mobile fixture; exact physical-device/child/owner acceptance remains open.'}
(src/'endpoint_rounding_repair.json').write_text(json.dumps(receipt,indent=2)+'\n')
p=root/'design/audit_impacts/job-art-chef-20261019.json';d=json.loads(p.read_text())
note=' Actual GUI review reproduced a Chef-only frosting completion boundary: Canvas transforms return5.999999605/6 and the surface already stops its terminal prefix at>=0.999. Align the Chef world completion boundary to that existing convention, preserving exact goals and passive/wrong/partial rules; sibling thresholds unchanged. Before/after source-bound GUI receipts require the completed cake and exact6.0goal, with partial-prefix negatives. Full01was stopped before this source fix and is not a pass; full02required.'
if '5.999999605/6' not in d['scope']:d['scope']+=note
p.write_text(json.dumps(d,indent=2)+'\n')
p=root/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';text=p.read_text('utf-8')
if 'Chef endpoint boundary follow-up' not in text:
    text+='\nChef endpoint boundary follow-up2026-10-19: actual raw GUI review exposed a full source-aligned stroke at5.999999605/6. The scoped world check now honors the existing Chef surface terminal-prefix convention(>=0.999), with exact goals, sibling thresholds and passive/wrong/partial rules intact. Two-aspect before/after receipts require the finished cake and exact6.0goal; full01was explicitly interrupted before source repair, and full02must verify the frozen result.\n'
p.write_text(text,encoding='utf-8')
print('Recorded real GUI boundary defect and source-bound exact6.0repair; no broad gameplay/acceptance claim')
