from pathlib import Path
import hashlib, html, json, shutil

root=Path(__file__).resolve().parents[1]
family=root/'audit/day_one_pool_live_refinement_v2_20261001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tools=family/'review_tools'
tools.mkdir(exist_ok=True)
for name in ['run_pool_live_refinement_checks.py','run_pool_live_refinement_checks_retry_v2.py',
             'run_pool_live_refinement_checks_retry_v3.py','run_pool_live_refinement_checks_retry_v4.py',
             'run_pool_live_refinement_capture.py','run_pool_live_refinement_capture_v2.py',
             'run_pool_live_refinement_capture_v3.py','build_pool_live_action_boards.py',
             'build_pool_live_action_boards_v3.py','encode_pool_live_actions_v1.py','encode_pool_live_actions_v3.py']:
    target=tools/name
    if not target.exists():shutil.copyfile(root/'tmp'/name,target)
items=['Star wrapper','Metal can','Blue cap','Original leaf','Purple ribbon','Yellow sponge']
review={'schema':'reef.live-pool-refinement-review.v1','status':'IN_PROGRESS',
        'baseline':'5b8bfb989ca8012924115d45901252808edb9b62',
        'items':[{'slot':i,'name':name,'source_score':4.6,'initial_mount_score':None,
                  'contact_carry_drop_score':None,'stored_score':None,'whole_played_action_score':None,
                  'opinion':'Exact source opinions retained from published generation/reuse reviews. Current complete action inspection remains unfinished.'} for i,name in enumerate(items)],
        'iterations':[{'path':'native_actions_1280_v1','frames':431,'checks':23,'failed_checks':0,
                       'visual_status':'REJECTED_STORED_READABILITY','visual_review':'native_actions_1280_v1/VISUAL_REJECTION.json'},
                      {'path':'native_actions_1280_v2','frames':427,'checks':23,'failed_checks':0,
                       'visual_status':'REJECTED_DUPLICATE_BASKET','visual_review':'native_actions_1280_v2/VISUAL_REJECTION.json'},
                      {'path':'native_actions_1280_v3','frames':426,'checks':24,'failed_checks':0,
                       'visual_status':'FULL_SEQUENCE_REVIEW_PENDING','note':'Direct initial, first stored wrapper and final basket views show one clear basket and all six stored shapes. Complete action review remains pending; later per-item generic voice-session wiring is not captured here.'}],
        'implementation':'Two new reversible runtime1024POT images bind five selected complete-source props and fresh skimmer; original atlas/tool/leaf preserved. Roshan now carries the actual caught item at the net, drops it into a visible stored pose, and keeps basket contents through later phases. Shared basket removes duplicate rescue basket only in composed pool. Main retains monotonic catch progress. Existing accurate recordings are selected per item; no voice file or save key changes.',
        'machine':'Initial trusted cue-wiring failure preserved. Retry passes unchanged pool probe, parser/inference/exact4.7.2 analyzer/import and38 independent assertions including contact, stable carry, continuous landing, interrupt/restore, pixel packing and standalone/shared basket ownership. Full current CI and current voice-session/sibling/aspect/wardrobe verification remain required.',
        'outstanding':'Complete individually attributed current sequence inspection, continuous playback/ordinary HUD routes, target-device/child/owner acceptance, remaining pool work, all other job items and final comprehensive owner-approved report. No global4.5 pass/finding closure/integration/release.'}
p=family/'REVIEW.json'
if not p.exists():p.write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
style='body{background:#eef5fa;color:#26334e;font:17px/1.55 system-ui;margin:0}main{max-width:1200px;margin:auto;padding:24px}section,article{background:white;border-radius:18px;padding:20px;margin:18px 0}img,video{display:block;max-width:100%;height:auto}a{color:#5142a2}select,input,button{font:inherit;padding:8px}table{border-collapse:collapse;width:100%}td,th{padding:9px;text-align:left;border-bottom:1px solid #dde2ee}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:15px}.grid article{margin:0}small{display:block;color:#4c5771}code{overflow-wrap:anywhere}details{margin:14px 0}'
body=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pool live artwork refinement — preserved iterations</title>',f'<style>{style}</style><main><h1>Pool live artwork refinement</h1><p>Draft in progress. Each object, its mounting and its action are reviewed separately. Failed evidence remains visible; scripted checks never assign a visual pass.</p>',
      '<nav><a href="../job_artwork_refinement_live/index.html">All-jobs library</a> · <a href="../../assets_src/imagegen/day1_pool_trash_v2_20261001/index.html">Originals and six generated prop attempts</a> · <a href="../../assets_src/imagegen/day1_pool_skimmer_v2_20261001/index.html">Fresh skimmer source</a></nav>',
      '<section><h2>Individual evaluations</h2><div id="evaluation"></div></section>',
      '<section><h2>Reversible runtime artwork</h2><p>New paths preserve the earlier runtime atlas/tool and complete generated source masters. Original leaf pixels are unchanged. This is technical whole-canvas packing and padding; no appearance repair.</p><div class="grid"><article><h3>Complete source cards</h3><img src="../../assets/castle/day_one_pool/activities/refinement_v2/floating_trash_atlas.png" alt="Five new source cards and preserved leaf in reversible atlas"><a href="PACKING_PROVENANCE.json">Exact source and output hashes</a></article><article><h3>Fresh skimmer</h3><img src="../../assets/castle/day_one_pool/activities/refinement_v2/pool_skimmer.png" alt="Matte storybook skimmer with transparent mesh"><small>Complete1024×683 source padded to1024POT; no subject pixels changed.</small></article></div></section>',
      '<section><h2>Latest native capture: one shared basket</h2><p>426 lossless1280×720 frames, six actual local touch requests,24 scripted checks. No fixture texture, depth, position or motion override. Isolated save, clips marked seen. Later per-item voice-session wiring is a separate change.</p><img src="native_actions_1280_v3/frame_0000.webp" alt="Initial unobstructed production pool"><img src="native_actions_1280_v3/frame_0425.webp" alt="All six preserved collected items in one shared basket"><div class="grid">']
for i,name in enumerate(items):
    body.append(f'<article><h3>{html.escape(name)}</h3><video controls preload="none" src="native_actions_1280_v3/item_{i:02d}_native_timestamps.mp4"></video><small>One encoded frame per lossless native frame, measured timestamps. Compression is review-only; no interpolation or repeated frames.</small></article>')
body+=['</div><p><a href="native_actions_1280_v3/ACTION_RECEIPT.json">Native states and frame hashes</a> · <a href="native_actions_1280_v3/ENCODING_RECEIPT.json">One-to-one encoding verification</a></p><label>Inspect every native frame <input id="frame" type="range" min="0" max="425" value="0"></label><small id="frameLabel">Frame0</small><img id="nativeFrame" src="native_actions_1280_v3/frame_0000.webp" alt="Selected full native frame"><details><summary>All ordered inspection boards</summary><div id="boards"></div></details></section>',
      '<section><h2>Preserved failed attempts</h2><article><h3>First live layout: stored objects unreadable4.2</h3><img src="native_actions_1280_v1/frame_0430.webp" alt="Preserved first attempt with tiny obscured contents"><p>23/23 scripted checks passed. The stored cards reduced to small overlapping slivers. This failed visual review remains preserved.</p><a href="native_actions_1280_v1/VISUAL_REJECTION.json">Written first failure</a></article><article><h3>Enlarged layout: duplicate basket4.1</h3><img src="native_actions_1280_v2/frame_0000.webp" alt="Two overlapping baskets exposed by enlargement"><p>The seahorse activity drew another basket above the skimmer contents. Enlarging the reused source exposed the ownership defect. Its local basket is now hidden only when the composed pool binds the shared basket.</p><a href="native_actions_1280_v2/VISUAL_REJECTION.json">Written duplicate/occlusion failure</a></article></section>',
      '<section><h2>Verification and remaining work</h2><p id="machine"></p><p id="outstanding"></p><a href="focused_initial/RECEIPT.json">Original focused failure</a> · <a href="focused_retry_v4/RECEIPT.json">Focused retry</a> · <a href="focused_retry_v4/INDEPENDENT_TRANSFER_CHECKS.json">38 independent assertions</a> · <a href="../../design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json">Rules, scope and evidence</a></section>',
      '''<script>fetch('REVIEW.json').then(r=>r.json()).then(d=>{document.querySelector('#machine').textContent=d.machine;document.querySelector('#outstanding').textContent=d.outstanding;const table=document.createElement('table');const head=table.insertRow();for(const t of ['Item','Source','Initial mount','Contact/carry/drop','Stored','Written evaluation']){const c=document.createElement('th');c.textContent=t;head.append(c)}for(const i of d.items){const row=table.insertRow();for(const t of [i.name,i.source_score,i.initial_mount_score??'Pending',i.contact_carry_drop_score??'Pending',i.stored_score??'Pending',i.opinion])row.insertCell().textContent=t}document.querySelector('#evaluation').append(table)});document.querySelector('#frame').addEventListener('input',e=>{const n=Number(e.target.value);document.querySelector('#frameLabel').textContent='Native frame '+n;document.querySelector('#nativeFrame').src='native_actions_1280_v3/frame_'+String(n).padStart(4,'0')+'.webp'});fetch('native_actions_1280_v3/inspection_boards/MANIFEST.json').then(r=>r.json()).then(d=>{for(const b of d.boards){const figure=document.createElement('figure');const caption=document.createElement('figcaption');caption.textContent='Item '+b.item+' · native frames '+b.frame_indices[0]+'–'+b.frame_indices.at(-1);const img=document.createElement('img');img.loading='lazy';img.alt=caption.textContent;img.src='native_actions_1280_v3/'+b.path;figure.append(caption,img);document.querySelector('#boards').append(figure)}})</script></main></html>''']
(family/'index.html').write_text('\n'.join(body)+'\n',encoding='utf-8')
license_path=root/'ASSET_LICENSES.md'
text=license_path.read_text(encoding='utf-8')
paths=list(family.rglob('*.webp'))+list(family.rglob('*.png'))+list(family.rglob('*.mp4'))+list((root/'assets/castle/day_one_pool/activities/refinement_v2').glob('*.png'))
rows=[]
for asset in sorted(paths):
    relative=asset.relative_to(root).as_posix()
    if f'`{relative}`' in text:continue
    if '/refinement_v2/' in relative and not relative.startswith('audit/'):
        source='Owned complete Codex imagegen sources; original owned leaf reused'
        modification='Whole-canvas normalization/packing or transparent POT padding only; originals and native-source hashes preserved.'
    else:
        source='Official Godot4.7.2 Mobile diagnostic; underlying source rights retained'
        modification='Native lossless frame unchanged; boards only uniformly reduce complete frames and add exterior labels. Video uses exact measured timestamps, one frame per source. Review only.'
    rows.append(f'| `{relative}` | {source} | audit/day_one_pool_live_refinement_v2_20261001/PACKING_PROVENANCE.json and native receipts | {modification} |')
if rows:license_path.write_text(text.rstrip()+'\n'+'\n'.join(rows)+'\n',encoding='utf-8')
attr=root/'.gitattributes';text=attr.read_text(encoding='utf-8')
for line in ['audit/day_one_pool_live_refinement_v2_20261001/** -text whitespace=cr-at-eol','tools/pack_day_one_pool_refinement_atlas.gd -text whitespace=cr-at-eol','tools/capture_day_one_pool_live_refinement_actions.gd -text whitespace=cr-at-eol','tools/probe_day_one_pool_refinement.gd -text whitespace=cr-at-eol']:
    if line not in text:text=text.rstrip()+'\n'+line+'\n'
attr.write_text(text,encoding='utf-8')
master=root/'audit/MASTER_AUDIT_2026-08-09.md';text=master.read_text(encoding='utf-8')
marker='Pool live artwork refinement (2026-10-01):'
if marker not in text:
    paragraph=marker+' [Preserved native iterations and current library](day_one_pool_live_refinement_v2_20261001/index.html) bind five complete-source replacements and fresh skimmer at new1024POT paths, retain originals, and add visible carry/drop/persisted contents. Initial431-frame/23-check attempt fails stored readability4.2; enlarged427-frame/23-check attempt exposes duplicate basket4.1. Third426-frame/24-check capture shows one shared basket; complete individual sequence review remains pending, and later per-item voice-session wiring is not captured there. Unchanged focused pool, exact4.7.2 parser/import/analyzer and38 independent assertions pass at their recorded source; current wholeCI/wardrobe/aspect/device/child/owner and all-job acceptance remain separate. [Impact](../design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json). No finding closure or comprehensive approval.\n\n'
    text=text.replace('## 0. Planning entry\n\n','## 0. Planning entry\n\n'+paragraph,1)
    master.write_text(text,encoding='utf-8')
ledger=root/'design/05_DOC_LEDGER.md';text=ledger.read_text(encoding='utf-8')
if '`audit/day_one_pool_live_refinement_v2_20261001/index.html`' not in text:
    text=text.rstrip()+'\n\n| `audit/day_one_pool_live_refinement_v2_20261001/index.html` | 🟣 | `CANDIDATE`; reversible new pool runtime bindings and native iterations, exact-source failed431/427-frame attempts retained, shared-basket426-frame candidate and pending individual action review. Scoped focused machine evidence does not establish current wholeCI, full action, device/child/owner/global acceptance. |\n'
    ledger.write_text(text,encoding='utf-8')
live=root/'audit/job_artwork_refinement_live/index.html';text=live.read_text(encoding='utf-8')
link='<a href="../day_one_pool_live_refinement_v2_20261001/index.html">Live pool carry/drop and preserved failures</a>'
if link not in text:text=text.replace('<nav>','<nav>'+link,1);live.write_text(text,encoding='utf-8')
findings=root/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=findings.read_text(encoding='utf-8')
note=' 2026-10-01: reversible pool graphics/carry refinement and source-bound failed stored-layout/duplicate-basket attempts are retained in [bounded evidence](../../design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json). Shared basket/current sequence and all-job/external acceptance remain open; no lifecycle closure.'
for finding in ['MA-VIS-006','MA-PLAY-004']:
    start=text.index('## '+finding+'\n');end=text.find('\n## ',start+1)
    if end<0:end=len(text)
    segment=text[start:end]
    if note not in segment:
        line=next(line for line in segment.splitlines() if line.startswith('| history |'))
        replacement=line[:-2]+note+' |'
        text=text[:start]+segment.replace(line,replacement,1)+text[end:]
findings.write_text(text,encoding='utf-8')
impact_path=root/'design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json'
impact=json.loads(impact_path.read_text(encoding='utf-8'))
coverage={str(p.relative_to(root)).replace('\\','/') for p in family.rglob('*') if p.is_file()}
coverage.update(str(p.relative_to(root)).replace('\\','/') for p in (root/'assets/castle/day_one_pool/activities/refinement_v2').glob('*') if p.is_file())
coverage.update(['audit/job_artwork_refinement_live/index.html','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','.gitattributes'])
impact['files']=sorted(set(impact['files'])|coverage)
impact_path.write_text(json.dumps(impact,indent=2)+'\n',encoding='utf-8')
print('Updated candidate library; added',len(rows),'asset-license rows; impact paths',len(impact['files']))
