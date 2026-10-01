from pathlib import Path
import datetime, hashlib, html, json, shutil

root = Path(__file__).resolve().parents[1]
family = root / 'audit/day_one_pool_live_refinement_v2_20261001'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, d): p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
classic = 'native_actions_1280_return_v6'
fairy = 'native_actions_1600_fairy_return_v2'
huluu = 'native_actions_1600_huluu_return_v2'
names = ['Star wrapper','Metal can','Blue cap','Original leaf','Purple ribbon','Yellow sponge']
comments = [
 'The navy-edged star and broad violet folds stay distinct against the teal water. The actual wrapper enters the net at local contact, remains intact through travel, and lands as the same recognizable star card in the basket. It no longer shrinks backward away from the child before disappearing.',
 'The rounded rim, open mouth and broad green value bands make the metal can readable. Its initial placement clears the waterfall; feedback follows actual contact. Carry keeps the complete can on the net and the final basket pose retains the rim silhouette.',
 'The blue circular rim and broad toothed edge stay recognizable during approach, net contact and carry. The basket preserves a round blue cap rather than a small sliver. The corrected idle fingertip points below this live target rather than above the inactive seahorse.',
 'The original warm brown leaf and stem provide a clear contrast with water and the violet ribbon. The preserved source pixels remain unchanged. Contact precedes collection, the whole leaf travels on the net, and the stored lower-row card preserves the stem and leaf body.',
 'The two broad violet lobes and navy contour read as a ribbon on the quiet water, through local contact and on the net. The revised mounted arrangement separates it from the earlier cluttered join. The lower-row basket silhouette retains the loop and free ends.',
 'The selected ochre rounded sponge has broad porous marks and a toy-like contour; the rejected first cheese-like sponge is preserved in the source review. The complete sponge remains on the net until its short visible drop. Its final yellow block is identifiable beside the lower-row leaf and ribbon.'
]
receipt = json.loads((family/classic/'ACTION_RECEIPT.json').read_text())
boards = json.loads((family/classic/'inspection_boards/MANIFEST.json').read_text())['boards']
assert len(boards)==47
indices = [n for b in boards for n in b['frame_indices']]
assert indices == list(range(1,434))
review = json.loads((family/'REVIEW.json').read_text())
review.update(status='BOUNDED_PROP_REVIEW_COMPLETE_ACTOR_REFINEMENT_OPEN', updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 score_policy='Individual visual drafting opinions, not calibrated measurements or owner acceptance. User requested >=4.5; original <=4.5 priorities remain queued, so this draft uses4.6 for a cleared source/prop lane. Unreviewed lanes stay null.',
 latest_capture=classic,
 direct_review={'method':'Direct visual inspection of all47 ordered complete-frame boards, covering433 action frames, plus native initial0/final434. These are diagnostic full-canvas views, not ordinary HUD traversal or continuous video playback.',
   'capture':classic,'frame_count':435,'action_frame_count':433,'board_count':47,'ordered_frame_indices':indices,
   'boards':[{'path':classic+'/'+b['path'],'sha256':sha(family/classic/b['path']),'frame_indices':b['frame_indices']} for b in boards]},
 machine='Latest focused_return_v7 passes unchanged trusted pool and contextual-voice probes, parser/inference/import, six exact Godot4.7.2 analyzers and41 independent transfer/cue/return checks. The classic435-frame and two wide432-frame native captures each pass26 scripted checks and preserve matching before/after source hashes. Six classic review videos have exactly one encoded frame per retained native frame and measured timestamps. Contextual-voice stderr retains the engine playback-outside-tree diagnostic. Current unmodified whole CI remains required; earlier82-probe pass belongs to the previous source snapshot.',
 outstanding='Whole actor performance and hand/tool grips remain weak: static body translation/lean, no authored gaze/reach/tail propulsion, initial lower-body dust-bunny overlap and costume-specific contact gaps. Wide Fairy/Huluu review is limited to initial, first wrapper catch and final return, not all432 frames. Continuous playback/listening, ordinary HUD routes and remaining pool tasks, current full CI, device/child/owner acceptance and all other job objects remain open. No global4.5 pass, finding closure, dev integration, release or comprehensive report approval.')
review['items'] = []
for i,name in enumerate(names):
 action=receipt['actions'][i]
 review['items'].append({'slot':i,'name':name,'source_score':4.6,'initial_mount_score':4.6,
   'contact_carry_drop_score':4.6,'stored_score':4.6,'whole_played_action_score':4.2,
   'priority':True,'priority_reason':'The prop lane clears the drafting threshold; the shared character acting/grip lane does not.',
   'frames':{'first':action['start_frame'],'last':action['end_frame_exclusive']-1},
   'opinion':comments[i]+' Prop handling is a4.6 opinion in the complete classic sequence. Whole played action stays4.2 because the unchanged actor is translated and leaned without purposeful body acting. No costume, device or owner pass is inherited.'})
review['shared_items']=[
 {'id':'pool-skimmer-source','name':'Fresh matte skimmer source','score':4.6,'priority':False,'opinion':'Broad aqua shaft, pink grip and pale mesh retain storybook contours and a readable net opening. Source opinion does not certify every painted hand socket.'},
 {'id':'pool-persistent-basket','name':'One persistent basket and six stored objects','score':4.6,'priority':False,'opinion':'The single reused basket is large enough to show the six complete40px cards in a three-by-two arrangement. Contents remain visible into the next phase; the duplicate basket and earlier tiny-card failures are preserved.'},
 {'id':'pool-idle-cue','name':'Corrected live-object fingertip cue','score':4.6,'priority':False,'opinion':'Direct blue-cap view places the upward fingertip just below the live blue cap. Independent passive checks cover all six intended tips with no progress awards. Timed cue behavior in other routes remains open.'},
 {'id':'pool-final-return','name':'Final visible return and caption clearance','score':4.6,'priority':False,'opinion':'Classic final and both inspected wide costume finals show the complete cutout above the next bottom caption after the visible last landing and bounded return. Full region bounds end around570–572px while the caption starts around594px. This is local framing, not accepted body motion.'},
 {'id':'pool-actor-start-occlusion','name':'Initial actor and dust-bunny overlap','score':4.3,'priority':True,'opinion':'All three inspected initial views place a foreground dust bunny over Roshan’s lower body. The static-source hierarchy remains a specific mounting priority.'},
 {'id':'pool-classic-grip','name':'Classic painted hand and skimmer grip','score':4.2,'priority':True,'opinion':'The skimmer is positioned at the right wrist, but the relaxed straight arm does not visibly close around or reach toward the handle. The socket-distance assertion measures declared geometry only.'},
 {'id':'pool-fairy-grip','name':'Fairy painted hand and skimmer grip','score':4.1,'priority':True,'opinion':'The first caught-wrapper view puts the handle near the Fairy wrist, but the unchanged hand/arm pose does not convincingly grasp or scoop. Only initial0/catch22/final431 are directly reviewed in this wide attempt.'},
 {'id':'pool-huluu-grip','name':'Huluu painted hand and skimmer grip','score':3.5,'priority':True,'opinion':'The first caught-wrapper view shows crossed/folded arms while the net handle projects right from the lap/wrist region. This does not read as holding or controlling a skimmer. Only initial0/catch21/final431 are directly reviewed in this wide attempt; protected original portrait is unchanged.'},
 {'id':'pool-body-acting','name':'Attention, reach, swim and settle performance','score':3.8,'priority':True,'opinion':'The ordered classic frames show a complete static card moving with small whole-card lean. Face, arm, gaze and tail stay fixed while travel reverses. The final handoff switches to the room pose. The versioned action contract records this unaccepted performance gap.'}
]
old_paths={i['path'] for i in review['iterations']}
for path in ['native_actions_1280_v4','native_actions_1600_fairy_v1','native_actions_1600_huluu_v1','native_actions_1280_pointer_v5',classic,fairy,huluu]:
 r=json.loads((family/path/'ACTION_RECEIPT.json').read_text())
 if path not in old_paths:
  review['iterations'].append({'path':path,'frames':len(r['frames']),'checks':len(r['checks']),
    'failed_checks':sum(not c['pass'] for c in r['checks']),
    'visual_status':('PROP_SEQUENCE_REVIEWED_ACTOR_WEAK' if path==classic else 'LIMITED_WARDROBE_VIEWS_ACTOR_WEAK' if path in [fairy,huluu] else 'PRESERVED_SUPERSEDED_ATTEMPT'),
    'direct_visual_coverage':('all433 action frames on47 boards plus initial/final' if path==classic else 'initial, first wrapper catch, final only' if path in [fairy,huluu] else 'See preserved attempt-specific reviews; no complete pass claimed')})
write(family/'REVIEW.json',review)
write(family/'WARDROBE_GRIP_REVIEW_RETURN_V2.json',{
 'status':'WEAK_ACTOR_CONTACT_PRESERVED','updated_utc':review['updated_utc'],
 'views':[{'capture':p,'direct_frames':ns,'hashes':[{'path':f'{p}/frame_{n:04d}.webp','sha256':sha(family/p/f'frame_{n:04d}.webp')} for n in ns]} for p,ns in [(fairy,[0,22,431]),(huluu,[0,21,431])]],
 'reviews':[i for i in review['shared_items'] if i['id'] in ['pool-actor-start-occlusion','pool-fairy-grip','pool-huluu-grip','pool-final-return']],
 'qualification':'Candidate machine geometry and final caption clearance pass; painted grasp and acting remain priorities. No protected original edit, full wide-frame or continuous-playback approval.'})
helpers=family/'review_tools';helpers.mkdir(exist_ok=True)
for p in sorted((root/'tmp').glob('*pool_live*')):
 if p.suffix=='.py' and p.name!='update_pool_review_return_v6.py':
  dst=helpers/p.name
  if not dst.exists():shutil.copyfile(p,dst)
  elif sha(dst)!=sha(p):raise AssertionError('Preserve existing helper '+str(dst))
shutil.copyfile(Path(__file__),helpers/'update_pool_review_return_v6.py')
style='body{background:#eef5fa;color:#26334e;font:17px/1.55 system-ui;margin:0}main{max-width:1200px;margin:auto;padding:24px}section,article{background:white;border-radius:18px;padding:20px;margin:18px 0}img,video{display:block;max-width:100%;height:auto}a{color:#5142a2}select,input,button{font:inherit;padding:8px}table{border-collapse:collapse;width:100%}td,th{padding:9px;text-align:left;border-bottom:1px solid #dde2ee}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:15px}.grid article{margin:0}small{display:block;color:#4c5771}code{overflow-wrap:anywhere}details{margin:14px 0}.scroll{overflow-x:auto}.weak{border-left:5px solid #b6585f}'
body=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pool artwork — current individual review and preserved iterations</title>',f'<style>{style}</style><main><h1>Pool artwork: props improved, actor work open</h1><p>The six prop transfers have a4.6 drafting opinion in this captured classic sequence. The whole played actions remain4.2 because grip and character acting are weak. The audit stays open across all job days and Opera training.</p>',
 '<nav><a href="../job_artwork_refinement_live/index.html">All-jobs library</a> · <a href="../../assets_src/imagegen/day1_pool_trash_v2_20261001/index.html">Originals and generated prop attempts</a> · <a href="../../assets_src/imagegen/day1_pool_skimmer_v2_20261001/index.html">Fresh skimmer source</a> · <a href="REVIEW.json">Individual review data</a></nav>',
 '<section><h2>Six individually reviewed props</h2><p>435 retained classic frames: initial0, all433 action frames inspected in47 ordered boards, and final434. Scores describe these exact views. A source or prop-handling score never grants a whole-action, costume or owner pass.</p><div id="evaluation" class="scroll"></div></section>',
 '<section><h2>Reversible new runtime files</h2><p>Original atlas, leaf and skimmer remain preserved. Complete generated cards use whole-canvas normalization/packing; the skimmer uses transparent square padding. No painted subject repair or protected-original change.</p><div class="grid"><article><h3>Complete prop cards</h3><img src="../../assets/castle/day_one_pool/activities/refinement_v2/floating_trash_atlas.png" alt="Five new whole prop cards and original leaf"><a href="PACKING_PROVENANCE.json">Packing sources and hashes</a></article><article><h3>Fresh skimmer</h3><img src="../../assets/castle/day_one_pool/activities/refinement_v2/pool_skimmer.png" alt="Fresh matte aqua and pink toy skimmer"></article></div></section>',
 f'<section><h2>Current six complete prop sequences</h2><img src="{classic}/frame_0000.webp" alt="Current initial pool: six separate targets and initial actor overlap"><img src="{classic}/frame_0434.webp" alt="Current final view: six stored objects, visible actor clear of next caption"><div class="grid">']
for i,name in enumerate(names):
 body.append(f'<article><h3>{html.escape(name)}</h3><p>{html.escape(comments[i])}</p><video controls preload="none" src="{classic}/item_{i:02d}_native_timestamps.mp4"></video><small>Silent diagnostic video: one encoded frame per retained native frame at measured readback timestamps. Whole-canvas encoding only; no interpolation, invented frames or motion repair. Continuous playback is not yet visually accepted.</small></article>')
body += [f'</div><a href="{classic}/ACTION_RECEIPT.json">Native states and frame hashes</a> · <a href="{classic}/ENCODING_RECEIPT.json">One-to-one timestamp verification</a> · <a href="ACTION_CONTRACT_RETURN_V6.json">Current action contract and acting gaps</a><details><summary>All47 ordered boards: every classic action frame</summary><div id="boards"></div></details></section>',
 '<section><h2>Inspect the exact native frames</h2><p>The two wide432-frame attempts each pass26 machine checks. Their direct visual review covers initial, first wrapper catch and final return only. Remaining wide frames are supplied for inspection.</p><label>Capture <select id="capture"><option value="native_actions_1280_return_v6">Classic1280×720 ·435 frames</option><option value="native_actions_1600_fairy_return_v2">Fairy1600×720 ·432 frames</option><option value="native_actions_1600_huluu_return_v2">Huluu1600×720 ·432 frames</option></select></label><label>Frame <input id="frame" type="range" min="0" max="434" value="0"></label><small id="frameLabel">Frame0</small><img id="nativeFrame" src="native_actions_1280_return_v6/frame_0000.webp" alt="Selected complete native frame"></section>',
 '<section><h2>Shared artwork and remaining weak items</h2><div id="shared" class="grid"></div><div class="grid">']
for p,n,label in [(huluu,21,'Huluu3.5: folded arms do not control the handle'),(fairy,22,'Fairy4.1: handle near wrist, grasp not convincing')]:
 body.append(f'<article class="weak"><h3>{label}</h3><img src="{p}/frame_{n:04d}.webp" alt="{label}"><a href="{p}/frame_0431.webp">Final return: complete cutout clear of caption</a></article>')
body += ['</div><a href="WARDROBE_GRIP_REVIEW_RETURN_V2.json">Exact limited wardrobe review</a></section>',
 '<section><h2>Preserved failures and earlier versions</h2><p>Successful machine checks in these attempts did not certify visual quality. Each failed image/sequence remains at its original path.</p><div class="grid">']
for p,n,title,report in [('native_actions_1280_v1',430,'Stored readability4.2: tiny overlapping slivers','VISUAL_REJECTION.json'),('native_actions_1280_v2',0,'Duplicate basket4.1: contents concealed','VISUAL_REJECTION.json'),('native_actions_1280_v4',81,'Idle cue4.2: points above inactive seahorse','IDLE_CUE_REJECTION.json'),('native_actions_1280_pointer_v5',425,'Phase return4.2: next caption covers lower body','HANDOFF_REJECTION.json')]:
 body.append(f'<article class="weak"><h3>{title}</h3><img loading="lazy" src="{p}/frame_{n:04d}.webp" alt="Preserved failed view"><a href="{p}/{report}">Written failure</a></article>')
body+=['</div><details><summary>All retained native attempts and their limits</summary><div id="iterations"></div></details></section>',
 '<section><h2>Machine evidence and acceptance still required</h2><p id="machine"></p><p id="outstanding"></p><a href="focused_return_v7/RECEIPT.json">Latest focused process results</a> · <a href="focused_return_v7/INDEPENDENT_TRANSFER_CHECKS.json">41 independent assertions</a> · <a href="focused_initial/RECEIPT.json">Original focused failure</a> · <a href="../../design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json">Rules and changed-file coverage</a></section>',
 '''<script>fetch('REVIEW.json').then(r=>r.json()).then(d=>{for(const k of ['machine','outstanding'])document.getElementById(k).textContent=d[k];const t=document.createElement('table');const h=t.insertRow();for(const v of ['Item','Source','Mount','Prop transfer','Stored','Whole action','Evaluation']){const c=document.createElement('th');c.textContent=v;h.append(c)}for(const i of d.items){const r=t.insertRow();for(const v of [i.name,i.source_score,i.initial_mount_score,i.contact_carry_drop_score,i.stored_score,i.whole_played_action_score,i.opinion])r.insertCell().textContent=v}document.getElementById('evaluation').append(t);for(const i of d.shared_items){const a=document.createElement('article');if(i.priority)a.className='weak';const h=document.createElement('h3');h.textContent=i.name+' · '+i.score+'/5';const p=document.createElement('p');p.textContent=i.opinion;a.append(h,p);document.getElementById('shared').append(a)}for(const i of d.iterations){const p=document.createElement('p');const a=document.createElement('a');a.href=i.path+'/ACTION_RECEIPT.json';a.textContent=i.path+' · '+i.frames+' frames, '+i.checks+' checks';p.append(a,document.createTextNode(' · '+i.visual_status+' · '+(i.direct_visual_coverage??i.note??'See preserved review')));document.getElementById('iterations').append(p)}});function show(){const c=document.getElementById('capture').value,n=Number(document.getElementById('frame').value);document.getElementById('frameLabel').textContent=c+' · native frame '+n;document.getElementById('nativeFrame').src=c+'/frame_'+String(n).padStart(4,'0')+'.webp'}document.getElementById('frame').addEventListener('input',show);document.getElementById('capture').addEventListener('change',()=>{const s=document.getElementById('frame');s.max=document.getElementById('capture').value==='native_actions_1280_return_v6'?434:431;s.value=0;show()});fetch('native_actions_1280_return_v6/inspection_boards/MANIFEST.json').then(r=>r.json()).then(d=>{for(const b of d.boards){const f=document.createElement('figure'),c=document.createElement('figcaption'),i=document.createElement('img');c.textContent='Item '+b.item+' · native frames '+b.frame_indices[0]+'–'+b.frame_indices.at(-1);i.loading='lazy';i.alt=c.textContent;i.src='native_actions_1280_return_v6/'+b.path;f.append(c,i);document.getElementById('boards').append(f)}})</script></main></html>''']
(family/'index.html').write_text('\n'.join(body)+'\n',encoding='utf-8')
licenses=root/'ASSET_LICENSES.md';text=licenses.read_text(encoding='utf-8');rows=[]
for p in sorted(family.rglob('*')):
 if p.suffix.lower() not in ['.png','.webp','.mp4']:continue
 rel=p.relative_to(root).as_posix()
 if f'`{rel}`' not in text:
  rows.append(f'| `{rel}` | Official Godot4.7.2 Mobile diagnostic; underlying owned source rights retained | audit/day_one_pool_live_refinement_v2_20261001/PACKING_PROVENANCE.json and exact native receipts | Complete native lossless frame; boards uniformly reduce whole frames with exterior labels; review video preserves measured timestamps and one source frame per encoded frame. No appearance repair. Review only. |')
if rows:licenses.write_text(text.rstrip()+'\n'+'\n'.join(rows)+'\n',encoding='utf-8')
master=root/'audit/MASTER_AUDIT_2026-08-09.md';text=master.read_text(encoding='utf-8')
start=text.index('Pool live artwork refinement (2026-10-01):');end=text.index('\n\n',start)
text=text[:start]+'Pool live artwork refinement (2026-10-01): [Individual current prop/actor review and preserved failures](day_one_pool_live_refinement_v2_20261001/index.html) binds five new complete-source props and fresh skimmer at reversible1024POT paths, retaining originals. The current classic435-frame attempt passes26 scripted checks; all433 action frames directly reviewed on47 ordered boards give each prop mount/contact/carry/drop/stored lane4.6, while every whole played action remains4.2. Shared body acting3.8, classic grip4.2, initial dust-bunny overlap4.3 and limited wide Fairy grip4.1/Huluu grip3.5 remain named priorities. Two wide432-frame/26-check attempts are inspected only at initial, first wrapper catch and final. Current final return clears the next caption in all three inspected finals. Earlier tiny contents4.2, duplicate basket4.1, idle cue4.2 and caption-covered return4.2 are preserved failures. Latest focused unchanged pool/contextual-voice/parser/import/analyzer and41 independent assertions pass; raw diagnostics remain. Current wholeCI, continuous playback/ordinary routes, remaining pool/all-job objects and device/child/owner approval remain open. [Impact](../design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json). No finding closure, global pass or comprehensive approval.'+text[end:]
master.write_text(text,encoding='utf-8')
ledger=root/'design/05_DOC_LEDGER.md';text=ledger.read_text(encoding='utf-8');lines=text.splitlines()
for i,line in enumerate(lines):
 if line.startswith('| `audit/day_one_pool_live_refinement_v2_20261001/index.html`'):
  lines[i]='| `audit/day_one_pool_live_refinement_v2_20261001/index.html` | 🟣 | `CANDIDATE`; current classic435-frame/26-check capture with all433 action frames directly reviewed on47 boards. Six prop lanes4.6; whole actions4.2 and individually named acting/grip/initial-overlap priorities remain. Two wide432-frame attempts have limited initial/catch/final visual review. Four earlier visual failures retained.41 focused independent assertions; current fullCI, ordinary-route/device/child/owner/global acceptance remain separate. |'
ledger.write_text('\n'.join(lines)+'\n',encoding='utf-8')
findings=root/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=findings.read_text(encoding='utf-8')
note=' 2026-10-01 current pool continuation: all433 classic action frames reviewed; six prop lanes4.6 but whole actions4.2. Body acting3.8, classic/Fairy/Huluu grips4.2/4.1/3.5 and initial actor overlap4.3 remain explicit priorities. Corrected cue/final caption clearance are bounded candidate evidence; fullCI, ordinary routes and creative acceptance remain open. [Current review](../day_one_pool_live_refinement_v2_20261001/REVIEW.json).'
for finding in ['MA-VIS-006','MA-PLAY-004']:
 start=text.index('## '+finding+'\n');end=text.find('\n## ',start+1);end=len(text) if end<0 else end
 segment=text[start:end];line=next(l for l in segment.splitlines() if l.startswith('| history |'))
 if note not in segment:text=text[:start]+segment.replace(line,line[:-2]+note+' |',1)+text[end:]
findings.write_text(text,encoding='utf-8')
impact_path=root/'design/audit_impacts/day-one-pool-live-refinement-v2-20261001.json';impact=json.loads(impact_path.read_text())
impact['files']=sorted(set(impact['files'])|{p.relative_to(root).as_posix() for p in family.rglob('*') if p.is_file()})
write(impact_path,impact)
print('Current review updated:',len(rows),'new license rows;',len(impact['files']),'covered paths. Six prop lanes4.6, whole actions4.2; actor priorities remain.')
