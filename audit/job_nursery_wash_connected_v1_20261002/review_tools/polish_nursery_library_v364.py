from pathlib import Path
import datetime, hashlib, json, re, shutil

R = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F = R / 'audit/job_nursery_wash_connected_v1_20261002'
S = R / 'assets_src/imagegen/nursery_wash_connected_v1_20261002'
L = R / 'audit/job_artwork_refinement_live'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
def write(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

# Source and test inputs are frozen while the canonical suite runs.
boundary = read(F / 'SOURCE_CURRENT_MACHINE_V3.json')
assert all(sha(R/x['path']) == x['sha256'] for x in boundary['source_files'])
index = read(F / 'current_visual_v3/INDEX.json')
review = read(F / 'DIRECT_REVIEW_CURRENT_V3.json')
registry = read(L / 'ALL_ITEMS.json')
details = [x for x in index['native_details'] if x['case'] == 'actual_bubble_bath_1280']
assert len(details) == 6
for q in registry['items']:
    if q.get('capture_family') != 'nursery_wash_v3':
        continue
    ident = q['id']
    state = ident.removeprefix('NUR-WASH-STATE-').lower().replace('-', '_') if ident.startswith('NUR-WASH-STATE-') else ('clean' if ident.endswith(('CONSEQUENCE','TRANSITION')) else 'rub_palm')
    detail = next(x for x in details if x['state'] == state)
    assert sha(R/detail['path']) == detail['sha256']
    # The visible mounted-use card must show the actual screenshot, not a source still.
    q['preview_path'] = q['image_path'] = detail['path']
    q['preview_sha256'] = detail['sha256']
    q['image_scope'] = 'Unchanged full native actual Bubble Bath capture. The recorded region identifies the related runtime artwork; this screenshot is not cropped.'
    q['latest_refinement']['note'] = q['latest_refinement']['note'].replace('action3.9', 'action 3.9')
for q in registry['items']:
    if q['id'].startswith('NUR-WASH-SRC-'):
        q['latest_refinement']['note'] = q['latest_refinement']['note'].replace('action3.9', 'action 3.9')
        q['image_scope'] = q['image_scope'].replace('whole-canvas1024', 'whole-canvas 1024')
registry['display_revision'] = 'V34.1: mounted-use previews and score-lane labels corrected; individual opinions unchanged.'
write(L / 'ALL_ITEMS.json', registry)

p = L / 'all_items.html'
s = p.read_text(encoding='utf-8')
needle = 'function render()'
assert needle in s
s = s.replace(needle, "const displayScore=q=>q.capture_family==='nursery_wash_v3'?q.current_mounted_score:q.current_source_score;const scoreLabel=q=>q.capture_family==='nursery_wash_v3'?(q.id.includes('USE-ACTION')||q.id.includes('USE-ATTENTION')||q.id.includes('USE-TRANSITION')?'Current complete action / continuity':'Current mounted artwork'):'Current source/cell artwork';\n"+needle, 1)
old = "Current source/cell artwork: ${q.current_source_score===null?'review required':esc(q.current_source_score)+'/5'}"
assert old in s
s = s.replace(old, "${esc(scoreLabel(q))}: ${displayScore(q)==null?'review required':esc(displayScore(q))+'/5'}")
old = '(a.current_source_score??99)-(b.current_source_score??99)'
assert old in s
s = s.replace(old, '(displayScore(a)??99)-(displayScore(b)??99)')
s = s.replace("lane==='unreviewed'&&q.current_source_score===null", "lane==='unreviewed'&&q.kind==='source'&&q.current_source_score===null")
s = s.replace('All eight preserved WASH cases now have direct frame review; current washing rerender and repair remain open.', 'The dated eight-case wash review is preserved. Current Nursery review covers every captured frame; Doctor washing and the remaining Nursery action and room repairs remain open.')
p.write_text(s, encoding='utf-8', newline='\n')

replacements = {
 'All1631': 'All 1631', 'all1631': 'all 1631', 'on36': 'on 36', 'and36': 'and 36', 'plus36': 'plus 36',
 'at1280': 'at 1280', 'states4.5': 'states 4.5', 'stills4.5': 'stills 4.5', 'static4.5': 'static 4.5',
 'action3.9': 'action 3.9', 'wash3.9': 'wash 3.9', 'attention3.8': 'attention 3.8', 'room2.9': 'room 2.9',
 'clasp4.4': 'clasp 4.4', 'library1756': 'library 1756', 'adds14': 'adds 14', 'and13': 'and 13',
 'union1756': 'union 1756', 'plus10': 'plus 10', 'opinions;690': 'opinions; 690', 'priorities,385': 'priorities, 385',
 'RGBA1254': 'RGBA 1254', 'whole-canvas1024': 'whole-canvas 1024', 'washv3': 'wash v3',
 'covers1631': 'covers 1631', 'records1631': 'records 1631', 'provisional4.5': 'provisional 4.5',
}
def polish(text):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text
for p in [F/'index.html', S/'index.html']:
    p.write_text(polish(p.read_text(encoding='utf-8')), encoding='utf-8', newline='\n')
for path, marker in [('audit/MASTER_AUDIT_2026-08-09.md', 'Connected Nursery washing continuation'), ('design/05_DOC_LEDGER.md', None), ('audit/job_review_v2_20261001/index.html', None)]:
    p = R/path
    lines = p.read_text(encoding='utf-8').splitlines()
    lines = [polish(x) if (marker and marker in x) or (not marker and ('nursery_wash_connected_v1_20261002' in x or 'V34' in x or 'current-nursery' in x)) else x for x in lines]
    p.write_text('\n'.join(lines)+'\n', encoding='utf-8', newline='\n')
p = R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
imp = read(p)
scope = imp['scope']
phrase = ' Extend the refreshable known-item register'
parts = scope.split(phrase)
if len(parts) == 3 and parts[1] == parts[2]:
    scope = parts[0]+phrase+parts[1]
imp['scope'] = polish(scope)
imp['validation'].append({'command': 'V34.1 mounted-preview and current-score display correction', 'result': 'PENDING_BROWSER_QA', 'evidence': 'Every Nursery mounted-use preview is a byte-verified unchanged actual Bubble Bath capture. Opinions and frozen production source are unchanged.'})
target = F/'review_tools'/Path(__file__).name
assert not target.exists()
shutil.copyfile(Path(__file__), target)
imp['files'] = sorted(set(imp['files']) | {target.relative_to(R).as_posix()})
write(p, imp)
allow = R/'tmp/v2_preview_allowed.json'
write(allow, sorted(set(read(allow)) | set(imp['files']) | {x['path'] for x in index['native_details']}))
print('V34.1 corrected: 13 native mounted previews, source/mounted/action labels, lowest visible score sorting. Scores unchanged; all '+str(len(boundary['source_files']))+' frozen source hashes still match.')
