from pathlib import Path
import collections, datetime, hashlib, html, json, os, shutil, subprocess

B = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P = B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'
S = B/'audit/job_shared_background_review_v1_20261003'
L = B/'audit/job_artwork_refinement_live'
BASE = 'ae3880df4244139a4f681034b530a5ee2c68895d'
PY = 'C:/Users/Peter/AppData/Local/Python/bin/python.exe'
IP = B/'design/audit_impacts/job-candy-shared-library-continuation-20261003.json'
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
esc = lambda x: html.escape(str(x))

def put(p, raw):
    p.parent.mkdir(parents=True, exist_ok=True)
    nxt=p.with_name(p.name+'.v565_next'); nxt.write_bytes(raw); nxt.replace(p)

def write(p, d, compact=False):
    put(p,(json.dumps(d,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)+'\n').encode())

assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip()==BASE
assert not IP.exists()
write(IP,dict(id='job-candy-shared-library-continuation-20261003',scope='Preserve A3/A4 local motion failures with all native frame opinions; evaluate all65 omitted shared sources and six exact joined source contexts; update only known source opinions in the refreshable illustrated library, archive exact W anonymous remote verification and hosted status. No production/art mutation, source-to-action transfer or finding closure.',baseline=BASE,rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-ASSET-01','DL-ASSET-02','DL-ASSET-03','DL-ASSET-04','DL-ASSET-05','DL-ASSET-06','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-READ-01','DL-READ-02','DL-READ-03','DL-LAY-01','DL-LAY-03','DL-LAY-05','DL-LAY-06','DL-LAY-07','DL-LAY-08','DL-MOT-01','DL-MOT-03','DL-MOT-10','DL-MOT-11','DL-MOT-12','DL-MOT-13','DL-QA-03','DL-QA-07'],findings=['MA-VIS-006','MA-PLAY-004'],files=[],validation=[dict(command='Direct current source and native motion review, literal production recheck and fresh structural gates',result='PENDING',evidence='Declared scope before report/register changes; historical gates are not new revision evidence.')],acceptance_gaps='Current game WRAP2.8; original full fold/neck pinch/opposing twist/release, actual ordinary story/training use, remaining sources/cells/jobs, device, child, owner and comprehensive report approval remain open.'))

# The actual A4 native canvases were inspected, not estimated from a render exit.
Q=P/'comparison_a4'; idx=read(Q/'attempt01/INDEX.json')
assert len(idx['frames'])==41 and all(sha(B/x['path'])==x['sha256'] for x in idx['frames']+idx['boards'])
def frame_opinion(i):
    if i==0:return 4.5,'Intact starting partial-fold pose; this still is not useful motion.'
    if i<=2:return 2.0,'An unrelated black-sleeved human hand enters from the upper left. Roshan’s two mittens remain at their original paper contact.'
    if i<=9:return 1.5,'The external hand touches the hat or rainbow hair instead of moving Roshan’s mitten and attached gold flap across the sweet.'
    if i<=12:return 1.0,'The external hand draws a colorful strip across the chest; the sweet is not covered by the attached flap.'
    if i<=20:return 0.8,'Roshan’s rainbow/body deforms into an elongated wrapped shape; the table task and original mitten contact lose continuity.'
    if i<=24:return 0.8,'An additional partial hand/arm appears lower left while the external hand grips the hat; the wrong subject is being manipulated.'
    return 0.5,'Two unrelated black-sleeved hands grip the hat/body; Roshan and the gold sweet task remain distorted. No correct fold, owned contact or useful release.'
frames=[]
for x in idx['frames']:
    score,op=frame_opinion(x['index']); frames.append(dict(**x,visual_frame_score=score,evaluation=f"Frame {x['index']} at {x['timestamp_seconds']:.3f}s: {op} Complete native-canvas drafting opinion only; no runtime acceptance.",direct_native_board_review=True,full_native_detail_review=x['index'] in [1,13,40],runtime_bound=False,owner_acceptance=None))
opinions=[('Character identity and stable complete silhouette',1.0,'The face/hat remain briefly recognizable, then the body and rainbow stretch into a different object.'),('Exactly two connected mittens owned by Roshan',1.0,'A black-sleeved human hand enters at frame1; later two external hands manipulate Roshan. They do not belong to her authored arms.'),('Initial lower-free-edge grasp',4.2,'Frame0 preserves the partial-fold still. This isolated starting contact cannot pass the action.'),('Existing mitten carries the attached flap',1.0,'The authored mittens do not perform the requested fold; another person touches the character instead.'),('Same sweet supported on the same table',2.0,'The table task persists initially, but the relevant contact and object continuity are lost as the character deforms.'),('Gold paper occludes the remaining sweet surface',1.0,'There is no truthful attached-flap closure over the same sweet.'),('Release leaves the useful fold intact',1.0,'There is no completed useful fold or release by Roshan’s original hand.'),('Attention remains on useful task change',1.5,'External hands and identity drift dominate attention instead of a legible paper fold.'),('Golden paper and painted quilted material continuity',1.5,'The human black sleeves and distorted rainbow/body replace the intended painted paper-and-mitten workflow.'),('Whole far-fold closure/release component',0.8,'Rejected: unrelated human hands manipulate the character, which distorts; no useful wrapper fold or release occurs.')]
write(Q/'attempt01/DIRECT_REVIEW.json',dict(status='ALL41_NATIVE_FRAMES_REVIEWED_EXTERNAL_HANDS_AND_BODY_DISTORTION_REJECTED',reviewed_utc=now(),prompt_id=idx['prompt_id'],native_frame_count=41,boards_reviewed=[x['path'] for x in idx['boards']],full_native_details=[1,13,40],individual_frames=frames,component_opinions=[dict(item=i,score=s,evaluation=e,priority=True) for i,s,e in opinions],whole_component_score=0.8,qualification='All41 native896x512 canvases directly inspected on7 non-resampled boards plus original-size details1/13/40. Rejected reference-only A4; source4.5 never transfers to motion. Current in-game WRAP2.8 and original complete wrapper workflow remain open.',runtime_bound=False,owner_acceptance=None))
for name in ['comparison_a3','comparison_a4']:
    q=P/name; r=read(q/'attempt01/DIRECT_REVIEW.json'); status=read(q/'REVIEW_STATUS.json')
    status.update(status=r['status'],whole_component_score=r['whole_component_score'],direct_native_frames_reviewed=41,direct_review_path=(q/'attempt01/DIRECT_REVIEW.json').relative_to(B).as_posix(),updated_utc=now(),runtime_bound=False,owner_acceptance=None)
    write(q/'REVIEW_STATUS.json',status)
    ip=B/f'design/audit_impacts/job-candy-local-far-fold-{name[-2:]}-20261003.json';d=read(ip)
    for v in d['validation']:
        if 'Inspect every41' in v['command'] or 'hand' in v['command'].lower() and v['result']=='PENDING':v.update(result='FAIL',evidence=(q/'attempt01/DIRECT_REVIEW.json').relative_to(B).as_posix()+f'; all41 inspected, whole component {r["whole_component_score"]}/5 rejected.')
        elif v['result']=='PENDING' and ('dispatcher' in v['command'].lower() or 'render' in v['command'].lower()):v.update(result='PASS',evidence=(q/'attempt01/RENDER_RECEIPT.json').relative_to(B).as_posix()+'; completed exact native render and archive, separate from failed visual opinion.')
        elif v['result']=='PASS' and 'archival' in v['command']:v['evidence']=(q/'attempt01/RENDER_RECEIPT.json').relative_to(B).as_posix()+'; all41 native canvases archived; actual visual review failed separately.'
    d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in q.rglob('*') if p.is_file()})
    d['acceptance_gaps']=f'Native render/archive complete; actual reference component {r["whole_component_score"]}/5 rejected. Current production WRAP2.8, complete fold/neck/twist/release and ordinary runtime/device/child/owner/all-job acceptance remain open.';write(ip,d)
write(P/'INPUT_FRAMING_DIAGNOSIS.json',dict(status='OBSERVATIONS_RECORDED_CAUSAL_INFERENCE_UNPROVEN',recorded_utc=now(),observations=['A3 extra mitten arms enter while original mittens stay at their contact.','A4 human black-sleeved hands manipulate the hat/body and distort Roshan instead of folding paper.','A3/A4 share identical complete neutral-mat input/source/seed/model/workflow; only the prompt differs.'],inference='The neutral-field cutout may be interpreted as an illustration or object being handled by an outside person. This is a hypothesis, not a measured model diagnosis.',next_comparison='Inventory painted full scene/context input and retained original whole poses before another materially different source experiment. Do not repeatedly rerun the same input with synonymous prompts.',qualification='No replacement model, cropped subject, pixel repair, production binding or cinematic acceptance is authorized by this inference.'))

join_notes={
 'KITCHEN':(4.5,'The unchanged12 tiles form a continuous painted4096x2304 room without an obvious missing or broken tile join. Rounded aqua cabinetry and lavender masonry fit the world. The bright lamps and dense right-side counter/shelf cluster compete for attention. Baked oven/card ownership and actual figure layering require live room evidence.'),
 'OPERA':(4.1,'The complete8-tile painted3640x2048 stage joins coherently across columns, doorways and drapery. The balcony fascia on both outer sides contains conspicuous ragged pale cleanup patches. Whole source-context floor fails; live training/job staging and actor occlusion are separate.'),
 'PLAYROOM':(4.3,'The complete8-tile3640x2048 room has coherent doors and balcony geometry. Fine balusters/lights and dense repeating pink floor pavers occupy large areas, weakening broad painted bands and task hierarchy. No actor/contact or touch-context claim.'),
 'DINING':(2.5,'The joined2048x1152 artwork exposes the mismatch: uniform plum ceiling, flat cream columns and cyan arch sit against painted masonry, while a heavy navy perspective grid crosses a second differently aligned square-floor pattern. Preserve the established room staging in a targeted painted repair; do not invent a new scene.'),
 'MOVIE':(2.4,'The joined2048x1152 room repeats the flat ceiling/column construction and giant perspective grid. Saturated red floor and tiny repeated yellow polygons compete with the intended calm painted room and stronger reusable cloud seating/screen-frame props. Source-context priority; live screen/content ownership remains separate.'),
 'HALL_PARTIAL_C0_C1':(4.3,'Only two columns of the7280x2048 hall are shown. Cream/gold shell architecture is coherent; fine repeated wall/floor motifs and glossy reflections reduce broad-band calm. The four tile join appears continuous in this limited span. This is not a whole-hall or runtime review.')}
additional=read(S/'ADDITIONAL_QA_JOINS.json')
contexts=[]
kitchen=read(S/'KITCHEN_QA_JOIN.json')
contexts.append(dict(name='KITCHEN',path=(S/'KITCHEN_UNCHANGED_NATIVE_QA_JOIN.png').relative_to(B).as_posix(),sha256=sha(S/'KITCHEN_UNCHANGED_NATIVE_QA_JOIN.png'),dimensions=[4096,2304],source_count=12,scope='Complete12-tile source family',direct_join_context_review=True,source_context_score=4.5,evaluation=join_notes['KITCHEN'][1]))
for x in additional['joins']:
    score,note=join_notes[x['name']];assert sha(B/x['path'])==x['sha256'];x.update(direct_join_context_review=True,source_context_score=score,evaluation=note);contexts.append(x)
additional['qualification']='All five additional unchanged-pixel joins directly inspected at original size. Source composition only, not native-generation per-playable-screen coverage, mounted runtime, action or owner acceptance.';write(S/'ADDITIONAL_QA_JOINS.json',additional)
write(S/'DIRECT_JOIN_CONTEXT_REVIEW.json',dict(status='ALL6_NONRESAMPLED_SOURCE_CONTEXTS_DIRECTLY_REVIEWED',reviewed_utc=now(),contexts=contexts,qualification='Existing unmodified image tiles were joined at literal offsets solely for QA. No production/background repair pixels, native source coverage or mounted-game acceptance are created. Hall scope is partial only.'))
reviews=read(S/'DIRECT_SOURCE_REVIEW.json');assert len(reviews['sources'])==65
css='body{font:18px/1.5 system-ui;color:#26344c;background:#edf4fa;max-width:1220px;margin:30px auto;padding:0 20px}a{color:#504096}article,header,section{padding:22px;background:white;border-radius:16px;margin:22px 0}img{display:block;max-width:100%;height:auto;background:repeating-conic-gradient(#dae4ec 0% 25%,#f8fbff 0% 50%) 50%/24px 24px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}.grid article{margin:0;min-width:0}.priority{border:2px solid #e0a56c}button{font:inherit;padding:12px;border-radius:10px;border:1px solid #9dabbd;cursor:pointer}code{overflow-wrap:anywhere}small{display:block}pre{white-space:pre-wrap;overflow-wrap:anywhere}'
body='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Shared job artwork:65 omitted sources</title><style>'+css+'</style><header><h1>Shared job artwork:65 omitted sources</h1><p>All65 complete native originals and six unchanged-pixel context joins were directly inspected.53 inclusive priorities;37 below4.5. These are individual source opinions; actual gameplay sequencing, touch targets, live object ownership and child/device/owner acceptance remain open.</p><p><a href="../job_artwork_refinement_live/all_items.html">Refreshable individual library</a> · <a href="DIRECT_SOURCE_REVIEW.json">All source scores/hashes</a> · <a href="DIRECT_JOIN_CONTEXT_REVIEW.json">All joined-context opinions</a></p><button id="weak">Show priorities only</button> <button id="all">Show all65 sources</button><p id="count">65 sources shown</p></header><section><h2>Interactions across each room painting</h2>'
for x in contexts:
    path=os.path.relpath(B/x['path'],S).replace('\\','/');body+='<article><h3>'+esc(x['name'])+' · source context '+str(x['source_context_score'])+'/5</h3><a href="'+esc(path)+'"><img loading="lazy" src="'+esc(path)+'" alt="Exact unchanged source-tile join '+esc(x['name'])+'"></a><p>'+esc(x['evaluation'])+'</p><small>'+esc(x['scope'])+'</small></article>'
body+='</section><section><h2>Every individual source</h2><p>Each atlas is shown as its complete unchanged source. Separate per-cell written reviews for its eight authored states remain a further coverage task; the whole-sheet grade is not a pass for each state or for motion.</p><div class="grid">'
for x in reviews['sources']:
    assert sha(B/x['path'])==x['sha256'];path=os.path.relpath(B/x['path'],S).replace('\\','/');body+='<article class="item '+('priority' if x['priority'] else '')+'" data-priority="'+str(x['priority']).lower()+'" id="'+esc(x['id'])+'"><h3>'+esc(x['id'])+' · '+str(x['source_score'])+'/5</h3><a href="'+esc(path)+'"><img loading="lazy" src="'+esc(path)+'" width="'+str(x['dimensions'][0])+'" height="'+str(x['dimensions'][1])+'" alt="Complete unchanged original '+esc(x['id'])+'"></a><p>'+esc(x['evaluation'])+'</p><p><strong>Refinement:</strong> '+esc(x['refinement'])+'</p><small>'+esc(x['path'])+' · '+str(x['dimensions'][0])+'×'+str(x['dimensions'][1])+'</small><details><summary>Exact source hash and aliases</summary><code>'+x['sha256']+'</code><p>'+esc(', '.join(x['aliases']))+'</p></details></article>'
body+='</div></section><script>function filter(weak){let n=0;for(const e of document.querySelectorAll(".item")){e.hidden=weak&&e.dataset.priority!=="true";if(!e.hidden)n++;}document.getElementById("count").textContent=n+" sources shown";}document.getElementById("weak").onclick=()=>filter(true);document.getElementById("all").onclick=()=>filter(false);</script></html>';put(S/'index.html',body.encode())

# Save all23,578 actual remote checks, losslessly, below the existing scanner ceiling.
archive=P/'previous_w_remote_verified';assert not archive.exists();archive.mkdir()
src=B/'tmp/candy_local_remote_v558';result=read(src/'RESULT.json');assert result['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and result['revision']==BASE and result['files_including_manifest']==23578
shutil.copyfile(src/'RESULT.json',archive/'RESULT.json');shutil.copyfile(B/'tmp/candy_local_publish_v558/RECEIPT.json',archive/'PUBLICATION_RECEIPT.json')
raw=(src/'VERIFICATION_JOURNAL.jsonl').read_bytes();lines=raw.splitlines(keepends=True);assert len(lines)==23578 and all(readrow.get('matches') is True for readrow in map(json.loads,lines))
parts=[];chunk=b'';first=0
for line in lines:
    if chunk and len(chunk)+len(line)>900000:
        name=f'JOURNAL_PART_{len(parts)+1:03d}.jsonl';put(archive/name,chunk);parts.append(dict(path=name,bytes=len(chunk),sha256=sha(archive/name),first_line=first,line_count=chunk.count(b'\n')));first+=chunk.count(b'\n');chunk=b''
    chunk+=line
if chunk:
    name=f'JOURNAL_PART_{len(parts)+1:03d}.jsonl';put(archive/name,chunk);parts.append(dict(path=name,bytes=len(chunk),sha256=sha(archive/name),first_line=first,line_count=chunk.count(b'\n')))
assert b''.join((archive/x['path']).read_bytes() for x in parts)==raw
write(archive/'JOURNAL_SHARDS.json',dict(status='PASS_LOSSLESS_ALL23578_ANONYMOUS_BYTE_ROWS',revision=BASE,original_bytes=len(raw),original_sha256=hashlib.sha256(raw).hexdigest(),rows=23578,max_shard_bytes=900000,parts=parts,qualification='Concatenate listed shard bytes in listed order to reconstruct the complete original journal; no row omissions or summaries.'))
host=P/'previous_w_hosted_snapshot_v565';host.mkdir(exist_ok=False)
for endpoint,name in [('actions/runs/37108271815','RUN.json'),('actions/runs/37108271815/jobs?per_page=100','JOBS.json')]:
    r=subprocess.run(['C:/Program Files/GitHub CLI/gh.exe','api','repos/Ebonyks/mermaid-roshan-reef/'+endpoint],cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);put(host/name,r.stdout);put(host/(name+'.stderr.log'),r.stderr);assert r.returncode==0
run=read(host/'RUN.json');assert run['head_sha']==BASE
write(host/'OBSERVATION.json',dict(status='EXACT_W_HOSTED_COMPLETE_SUCCESS' if run['status']=='completed' and run['conclusion']=='success' else 'EXACT_W_HOSTED_STATUS_SNAPSHOT',checked_utc=now(),revision=BASE,run_id=run['id'],run_status=run['status'],conclusion=run['conclusion'],qualification='Actual API snapshot only; an in-progress/null result is not success. No new revision or visual/owner acceptance transfer.'))

# Update the65 existing primary entries without adding source/capture duplicates.
for name,target in [('ALL_ITEMS.json','ALL_ITEMS_V46.original.json'),('all_items.html','all_items_V46.original.html'),('CURRENT_BOUNDARY_REFRESH.json','BOUNDARY_V46.original.json')]:assert not (L/target).exists();shutil.copyfile(L/name,L/target)
reg=read(L/'ALL_ITEMS.json');assert reg['display_revision']=='V46' and len(reg['items'])==2044
byid={x['id']:x for x in reg['items']}
for x in reviews['sources']:
    r=byid[x['id']];assert r['kind']=='source' and r['current_source_score'] is None and r['current_checkout_sha256']==x['sha256']
    r.update(current_source_score=x['source_score'],evaluation=x['evaluation'],refinement=x['refinement'],priority=x['priority'],individual_review_utc=reviews['reviewed_utc'],image_path=x['path'],image_scope='Complete unchanged native source; direct original-size source review',source_qualification='Directly reviewed whole source only. Current room mounting, action, ordinary story/training, device, child and owner acceptance remain open.',latest_refinement=dict(report=S.relative_to(B).as_posix()+'/index.html#'+x['id'],note=x['evaluation']))
    r['original_reports']=list(dict.fromkeys(r['original_reports']+[S.relative_to(B).as_posix()+'/index.html']))
pri=[x for x in reg['items'] if x.get('current_source_score') is not None and x['current_source_score']<=4.5 and x.get('capture_family') not in ['geode_current_v1','nursery_wash_v3']]
unique={x['path'] for x in pri if x['kind'] in ['source','runtime source']}
pending=[x for x in reg['items'] if x['kind']=='source' and x.get('current_source_score') is None]
assert len(pri)==947 and len(unique)==658 and len(pending)==294
reg['counts'].update(inclusive_current_source_priorities=len(pri),unique_source_file_priorities=len(unique),unreviewed_current_source=len(pending),new_shared_background_source_opinions=65)
reg.update(display_revision='V47',updated_utc=now(),refresh_command='python -B audit/job_artwork_refinement_live/review_tools/refresh_current_job_review_v47.py',scope='V47:2044 known entries/1280 primary sources/328 pose cells/151 runtime-use-action entries/285 source object regions.947 inclusive source-cell-region priorities,658 unique source-file priorities,294 unreviewed primary sources.65 existing omitted shared source entries now individually reviewed:53 inclusive priorities/37 below4.5. All164 A1-A4 local reference canvases and40 component opinions reviewed; all four motion studies rejected. Production WRAP2.8 and783 literal source boundary unchanged. No source-to-action, current older capture, owner, integration or release acceptance.')
reg['review_resources'].append(dict(path=S.relative_to(B).as_posix()+'/index.html',scope='All65 existing native omitted shared sources and six unchanged-pixel context joins directly inspected;53 source priorities/37 below4.5. Atlas cell/action acceptance separate.'))
for x in reg['review_resources']:
    if x['path']==P.relative_to(B).as_posix()+'/index.html':x['scope']='All164 A1-A4 complete native reference canvases/28 original-size boards/12 details/40 component opinions. A1 whole2.4/A2 farfold1.8/A3 farfold1.5/A4 farfold0.8 rejected; no runtime transfer.'
write(L/'ALL_ITEMS.json',reg,True);assert (L/'ALL_ITEMS.json').stat().st_size<4194304
shutil.copyfile(L/'review_tools/refresh_current_job_review_v46.py',L/'review_tools/refresh_current_job_review_v47.py')
notice='<p><a href="../job_shared_background_review_v1_20261003/index.html">New:65 omitted shared originals individually reviewed</a> ·53 inclusive priorities/37 below4.5; six joined source contexts. <a href="../../assets_src/local_motion/candy_wrap_continuity_v1_20261003/index.html">All164 Candy local reference frames/40 component opinions</a>: A3 1.5/A4 0.8 rejected. V47 retains2044 entries;947 source-cell-region priorities/658 unique source priorities/294 primary sources still unreviewed. Current WRAP2.8 remains unchanged.</p>'
for name in ['index.html','all_items.html']:
    t=(L/name).read_text(encoding='utf-8').replace('refresh_current_job_review_v46.py','refresh_current_job_review_v47.py');t=t.replace('<h1>',notice+'<h1>',1);put(L/name,t.encode())
builder=(P/'review_tools/build_candy_local_review_v554.py').read_text()
old="[('a1','A1: complete wrapping reference',P),('a2','A2: far long-edge fold component',Q)]";assert old in builder
builder=builder.replace(old,"[('a1','A1: complete wrapping reference',P),('a2','A2: far long-edge fold component',Q),('a3','A3: partial far-fold reference',P/'comparison_a3'),('a4','A4: prompt-only partial far-fold reference',P/'comparison_a4')]")
builder=builder.replace("IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'","IP=B/'design/audit_impacts/job-candy-shared-library-continuation-20261003.json'")
builder=builder.replace('A12 grip4.3 is rejected; A13 partial fold4.5 is source-only. Complete neck grip, opposing twist, release and runtime acceptance remain open.','A12 grip4.3 is rejected; A13 partial fold4.5 is source-only. A3 far-fold1.5 and A4 far-fold0.8 fail with extra hands and body distortion. No completed closure or release. Complete neck grip, opposing twist, release and runtime acceptance remain open.')
builder=builder.replace('previous_v_remote_verified/RESULT.json','previous_w_remote_verified/RESULT.json').replace('Previous immutable V remote verification','Previous immutable W remote verification')
put(P/'review_tools/build_candy_local_review_v565.py',builder.encode());shutil.copyfile(P/'review_tools/build_candy_local_review_v565.py',B/'tmp/build_candy_local_review_v565.py')
res=subprocess.run([PY,'-X','utf8','-B',str(B/'tmp/build_candy_local_review_v565.py')],cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);print(res.stdout.decode().strip());assert res.returncode==0,res.stderr.decode()

# Authority facts are additions, leaving every dated record and finding lifecycle intact.
summary='Shared source and Candy motion continuation (2026-10-03): [all65 omitted native sources and six joined source contexts](SHARED) individually reviewed;53 inclusive priorities/37 below4.5. Dining source-context2.5/Movie2.4, Library isolation and flat stacking-toy3.0 are named priorities. [All164 native A1-A4 local reference canvases/28 boards/12 details/40 component opinions](MOTION) inspected; A3 1.5/A4 0.8 rejected for extra hands, failed fold and character distortion. V47 retains2044 entries/947 source-cell-region priorities/658 unique source priorities/294 unreviewed primary sources. Exact W all23578 anonymous remote bytes verified; current game WRAP2.8 and783 literal production members unchanged. Whole wrapper, remaining source/cell/use/action/ordinary-route/device/child/owner/comprehensive report acceptance remain open; finding lifecycle, integration and release unchanged.'
for path,sh,mo in [('audit/MASTER_AUDIT_2026-08-09.md','job_shared_background_review_v1_20261003/index.html','../assets_src/local_motion/candy_wrap_continuity_v1_20261003/index.html'),('audit/findings/ACTIVE_FINDINGS_2026-08-13.md','../job_shared_background_review_v1_20261003/index.html','../../assets_src/local_motion/candy_wrap_continuity_v1_20261003/index.html'),('audit/animation/README.md','../job_shared_background_review_v1_20261003/index.html','../../assets_src/local_motion/candy_wrap_continuity_v1_20261003/index.html')]:
    p=B/path;t=p.read_text(encoding='utf-8');note=summary.replace('SHARED',sh).replace('MOTION',mo)
    if path.endswith('MASTER_AUDIT_2026-08-09.md'):
        for marker in ['## 0. Planning entry','## Development task index']:
            assert marker in t;t=t.replace(marker,marker+'\n\n'+note,1)
    elif path.endswith('README.md'):
        marker='## Start an animation task here';assert marker in t;t=t.replace(marker,note+'\n\n'+marker,1)
    else:
        i=t.index('\n')+1;t=t[:i]+'\n'+note+'\n'+t[i:]
    put(p,t.encode())
ledger=B/'design/05_DOC_LEDGER.md';t=ledger.read_text(encoding='utf-8');old='all82 local reference native canvases/14 boards/six details/20 component opinions. A1 complete wrap2.4 and A2 far-fold1.8 rejected.13 contact originals/43 source states reviewed; source/action lanes separate, no runtime or owner acceptance.'
assert old in t;t=t.replace(old,'all164 local reference native canvases/28 boards/12 details/40 component opinions. A1 complete wrap2.4/A2 far-fold1.8/A3 far-fold1.5/A4 far-fold0.8 rejected.13 contact originals/43 source states reviewed; source/action lanes separate, no runtime or owner acceptance.')
t+='\n| `audit/job_shared_background_review_v1_20261003/index.html` | 🟢 | `SUPPORTING_CURRENT`; all65 previously omitted native shared sources/six literal joined contexts reviewed;53 inclusive source priorities/37 below4.5. Whole-atlas opinions do not accept every cell/action. No production or owner acceptance. |\n| `audit/job_shared_background_review_v1_20261003/DIRECT_SOURCE_REVIEW.json` | 🟢 | `SUPPORTING_CURRENT`; exact65 existing source IDs/hashes/individual scores and refinement guidance; current mounting/action/owner opinions unassigned. |\n| `audit/job_artwork_refinement_live/ALL_ITEMS_V46.original.json` | ⚪ | `HISTORICAL_SUPPORTING`; exact2044-entry register before65 existing shared source entries received direct individual opinions. |\n';put(ledger,t.encode())
licenses=(B/'ASSET_LICENSES.md').read_bytes()
for x in S.glob('*.png'):
    path=x.relative_to(B).as_posix()
    if ('| `'+path+'` |').encode() not in licenses:licenses+=('\n| `'+path+'` | Exact project source tile pixels; QA reconstruction | Inherited original artwork license/provenance; individual source paths/hashes retained in join manifests | Local original sources, not downloaded or generated replacement art | Non-resampled literal-offset QA join only; no production, source-resolution, runtime or owner acceptance. |\n').encode()
put(B/'ASSET_LICENSES.md',licenses)
res=subprocess.run([PY,'-X','utf8','-B',str(L/'review_tools/refresh_current_job_review_v47.py')],cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);assert res.returncode==0,res.stderr.decode();print(res.stdout.decode().strip())
boundary=read(P/'PRODUCTION_BOUNDARY.json');bad=[x for x in boundary['members'] if sha(B/x['path'])!=x['sha256']];assert len(boundary['members'])==783 and not bad
write(P/'PRODUCTION_BOUNDARY_END_V565.json',dict(status='PASS_ALL783_LITERAL_MEMBERS_UNCHANGED',checked_utc=now(),baseline=BASE,boundary_path=(P/'PRODUCTION_BOUNDARY.json').relative_to(B).as_posix(),boundary_sha256=sha(P/'PRODUCTION_BOUNDARY.json'),checked_members=783,changed_members=bad,qualification='No production change; prior exact production machine checks remain separate from this expanded review revision and failed motion opinions.'))
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
allow=B/'tmp/v2_preview_allowed.json';allowed=read(allow);assert isinstance(allowed,list)
write(allow,sorted(set(allowed)|{p.relative_to(B).as_posix() for folder in [P,S] for p in folder.rglob('*') if p.is_file()}|{x['path'] for x in reviews['sources']}))
affected=['ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/animation/README.md','design/05_DOC_LEDGER.md']
affected += [(L/x).relative_to(B).as_posix() for x in ['ALL_ITEMS.json','ALL_ITEMS_V46.original.json','all_items.html','all_items_V46.original.html','BOUNDARY_V46.original.json','CURRENT_BOUNDARY_REFRESH.json','index.html','review_tools/refresh_current_job_review_v47.py']]
d=read(IP);d['files']=sorted(set(d['files'])|set(affected)|{p.relative_to(B).as_posix() for folder in [P,S] for p in folder.rglob('*') if p.is_file()})
d['validation']=[dict(command='Every65 native shared primary source and six unchanged-pixel joins directly inspected',result='PASS',evidence='audit/job_shared_background_review_v1_20261003/DIRECT_SOURCE_REVIEW.json and DIRECT_JOIN_CONTEXT_REVIEW.json; coverage only,53 source priorities/37 below4.5 remain.'),dict(command='Every164 A1-A4 native local canvas and40 component opinions directly reviewed',result='FAIL',evidence='All four native DIRECT_REVIEW.json records; A3 1.5/A4 0.8 rejected. No source score or machine-render exit transfers.'),dict(command='V47 current known-item refresh and783 literal production members',result='PASS',evidence='CURRENT_BOUNDARY_REFRESH.json:2044 registered source matches; PRODUCTION_BOUNDARY_END_V565.json all783 unchanged. Older Geologist/Nursery mounted claims withheld.'),dict(command='Exact W23578 anonymous remote byte rows losslessly preserved',result='PASS',evidence='previous_w_remote_verified/RESULT.json and JOURNAL_SHARDS.json; every row matches, exact reconstructed journal hash.'),dict(command='Fresh authority/development/document tests/game2d regression gates',result='PENDING',evidence='Required on actual expanded review revision before commit/push. Strict zero-debt/visual/owner acceptance not implied.')];write(IP,d)
print(json.dumps(dict(status='EXPANDED_REVIEW_REPORTS_SAVED',sources=65,source_priorities=53,register_items=2044,register_priorities=947,unique_priority_sources=658,primary_unreviewed=294,registry_bytes=(L/'ALL_ITEMS.json').stat().st_size,native_motion_frames=164,native_component_opinions=40,remote_journal_rows=23578,journal_shards=len(parts),hosted_status=run['status'],hosted_conclusion=run['conclusion'])))
