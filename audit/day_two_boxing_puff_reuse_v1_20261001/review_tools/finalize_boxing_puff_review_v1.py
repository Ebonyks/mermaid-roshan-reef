from pathlib import Path
import datetime, hashlib, html, json, shutil

r = Path.cwd()
f = r / 'audit/day_two_boxing_puff_reuse_v1_20261001'
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8'))
def write(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

assert not (f / 'REVIEW.json').exists(), 'Preserve earlier reports'
v2 = read(f / 'native_timed_reuse_v2/CAPTURE_RECEIPT.json')
v3 = read(f / 'native_timed_reuse_v3/CAPTURE_RECEIPT.json')
boards = read(f / 'native_timed_reuse_v2/inspection_boards/MANIFEST.json')['boards']
assert len(v2['frames']) == 157 and len(boards) == 20
assert [n for b in boards for n in b['frame_indices']] == list(range(157))
checks = []
def check(name, condition, evidence):
    checks.append(dict(name=name, result='PASS' if condition else 'FAIL', evidence=evidence))
for run, data in [('native_timed_reuse_v2', v2), ('native_timed_reuse_v3', v3)]:
    proc = read(f/run/'PROCESS_RECEIPT.json')
    check(run+' exact unchanged source boundary', proc['status']=='PASS' and proc['source_unchanged'], 'PROCESS_RECEIPT.json')
    check(run+' all frame bytes/dimensions declared', all(sha(f/run/x['path'])==x['sha256'] for x in data['frames']), 'CAPTURE_RECEIPT.json')
    check(run+' isolated awarded stars unchanged', data['gameplay_progress_unchanged'], 'CAPTURE_RECEIPT.json; local phase_progress deliberately advances once')
    for n, a in enumerate(data['actions']):
        frames = [x for x in data['frames'] if a['first_frame']<=x['index']<=a['last_frame']]
        hits = [x['landed_punches'] for x in frames]
        progress = [x['phase_progress'] for x in frames]
        first_hit = next(x for x in frames if x['landed_punches']==1)
        check(f'{run} action{n} one intentional accepted punch', hits[0]==0 and hits[-1]==1 and set(hits)=={0,1} and hits==sorted(hits), 'No manually assigned hit count; actual local touch/drag/release production handler')
        check(f'{run} action{n} no passive phase award', all(x['phase_progress']==0 for x in frames if x['landed_punches']==0) and progress[-1]==1 and progress==sorted(progress), 'Explicit catalog-phase fixture; phase progress1 is not a star/save award')
        check(f'{run} action{n} hit refresh and subsequent settle', first_hit['impact_time']>0.45 and frames[-1]['impact_time']==0 and not frames[-1]['touch_owners'], 'Engine state around rendered frame; rendered clearing reviewed separately')
        check(f'{run} action{n} monotonic native timestamps', all(x['seconds']<y['seconds'] for x,y in zip(frames,frames[1:])), 'Capture fps cap is not a device performance measurement')
check('All v2 ordered boards carry original complete frame indices', all(sha(f/'native_timed_reuse_v2'/b['path'])==b['sha256'] for b in boards), 'Twenty directly reviewed full-canvas boards; thumbnails are display-only')
write(f/'CAUSAL_CHECKS.json', dict(status='PASS' if all(x['result']=='PASS' for x in checks) else 'FAIL', checks=checks, qualification='These are source/input/phase/effect invariants, not visual acceptance or ordinary route coverage.'))
assert all(x['result']=='PASS' for x in checks)

actions = []
for n,a in enumerate(v2['actions']):
    rows = [x for x in v2['frames'] if a['first_frame']<=x['index']<=a['last_frame']]
    hit = next(x for x in rows if x['landed_punches']==1)
    actions.append(dict(action=n, **a, contact_frame=hit['index'], individual_puff_style_score=4.6, individual_puff_contact_fit_score=4.6, puff_end_timing_score=4.2, complete_action_score=4.0,
        opinion='Clean rounded lavender/white puff remains legible over the glove and pad/imp torso without hiding the face or leaving the original vertical marks. Actual punch refreshes the effect once. Existing alpha falls only to approximately0.45 before the draw condition stops; this makes the end visibly abrupt. Flat procedural coral gloves have heavier simpler contours than the painted props, and imp reaction switches between complete cards without sufficient authored recovery acting. These shared weaknesses keep the complete action below target.',
        prior_contact_puff=('Expected friendly counter feedback is already active before the player punch; no phase award. Production receive_friendly_hit sets this cloud at center/bottom, then the accepted punch refreshes it at the target.' if a['mode']=='boxing_imp' else 'No puff before player contact in this jab capture.')))
direct_v2 = [8,39,47,78,87,117,125,156]
final_v3 = [a['last_frame'] for a in v3['actions']]
write(f/'native_timed_reuse_v2/VISUAL_REVIEW.json', dict(status='ALL_157_FRAMES_DIRECTLY_REVIEWED_IN_20_ORDERED_BOARDS', updated_utc=now, boards=boards, individually_viewed_full_native_frames=direct_v2, actions=actions,
    render_state_limit='Full native frame117 and156 still show residual cloud despite recorded impact_time0. State and rendered pixels can differ by one frame. These first zero-state snapshots are not proof of clear final pixels. Extra rendering is captured independently in v3.',
    gaps='Silent native frame review, not continuous playback, listening, root viewport input traversal, ordinary job progression, phone, child or owner approval.'))
write(f/'native_timed_reuse_v3/VISUAL_REVIEW.json', dict(status='FOUR_EXTRA_SETTLED_FINAL_VIEWS_DIRECTLY_REVIEWED', updated_utc=now,
    supplied_frame_count=len(v3['frames']), directly_viewed_frame_indices=final_v3, frames=[x for x in v3['frames'] if x['index'] in final_v3],
    settled_final_puff_absence_score=4.6, complete_action_score=None,
    opinion='All four complete native final views directly inspected. Three extra rendered frames after the first zero engine-state capture show the puff fully cleared at both1280 and1600 widths in jab and imp modes. The remaining164 supplied frames are not newly visually reviewed; no v2 whole-action score is inherited by this attempt.'))
profile = read(f/'PROFILE.json')
profile['updated_utc']=now
profile['status']='SOURCE_AND_STATIC_CONTACT_4_6_EFFECT_END_4_2_ORIGINAL_STILL_BOUND'
profile['reused_source']['role']='Existing exact clean lavender/white friendly puff. Source-purpose, all four static contact cases and all four v2 timed contact fits4.6; ending timing4.2 remains a separate priority.'
profile['acceptance']='Original2.5 remains live. Candidate is exact existing art at a non-runtime review path. Complete v2 actions4.0; effect end4.2. Four v3 settled finals4.6 establish only absence after extra render settling. No all-route, device/child/owner pass.'
write(f/'PROFILE.json', profile)
review = dict(id='D2A-0394', updated_utc=now, status=profile['status'], original=profile['original'], reused_source=profile['reused_source'],
    static_review='native_context_v1/VISUAL_REVIEW.json', timed_review='native_timed_reuse_v2/VISUAL_REVIEW.json', final_settling_review='native_timed_reuse_v3/VISUAL_REVIEW.json', causal_checks='CAUSAL_CHECKS.json', actions=actions,
    individual_scores=[dict(item='Original coral impact source',score=2.5,priority=True),dict(item='Exact reused lavender/white source',score=4.6,priority=False),dict(item='Clean puff contact fit in both modes and widths',score=4.6,priority=False),dict(item='Puff end timing',score=4.2,priority=True),dict(item='Shared procedural glove visual coherence',score=4.0,priority=True),dict(item='Imp reaction/recovery acting',score=3.8,priority=True),dict(item='Complete fixture action',score=4.0,priority=True)],
    retained_failure=dict(path='native_timed_reuse_v1/FAILURE_NOTE.json',description='Root viewport dispatch attempt failed its accepted-punch assertion and was stopped after verifying its exact capture process. Cause unresolved. Local handler tests do not clear this ordinary input-route gap.'),
    acceptance_gaps=profile['acceptance'])
write(f/'REVIEW.json', review)

def fig(src,caption):
    return '<figure><a href="'+html.escape(src)+'"><img loading="lazy" src="'+html.escape(src)+'" alt="'+html.escape(caption)+'"></a><figcaption>'+html.escape(caption)+'</figcaption></figure>'
page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Boxing puff — exact reuse and action audit</title><style>body{font:17px/1.55 system-ui;background:#eef4ff;color:#26304e;margin:0}main{max-width:1180px;margin:auto;padding:24px}section{background:white;padding:20px;border-radius:16px;margin:18px 0}h1,h2,h3{line-height:1.2}a{color:#514195}img{max-width:100%;display:block;height:auto}figure{margin:16px 0}figcaption{font-size:14px;color:#4c5368}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:9px;border-bottom:1px solid #d8dfec}input{width:100%}select{font:inherit;padding:8px}.source{background:repeating-conic-gradient(#dce5ed 0% 25%,#f8fbff 0% 50%) 50%/24px 24px}.source img{width:256px;margin:auto}code{overflow-wrap:anywhere}</style><main><h1>Boxing impact puff — reversible reuse review</h1><p><a href="../job_artwork_refinement_live/index.html">All-jobs library</a> · <a href="REVIEW.json">Individual scores and evidence</a> · <a href="CAUSAL_CHECKS.json">Causal machine checks</a></p><section><h2>Individual artwork passes; the ending still needs refinement</h2><p>D2A-0394’s live coral source remains2.5/5 because unrelated vertical marks survive on both sides. A clean lavender/white puff already exists in the approved source family. Its exact bytes, rounded contour and sparse broad highlights fit at4.6/5; this is a reuse replacement draft and requires no new image generation. The live binding is unchanged.</p><p>All eight static comparison views and all157 native frames from four local-handler actions were directly inspected. Twenty ordered boards preserve the full canvas. The puff’s contact appearance earns4.6, but its end timing stays4.2: the existing renderer removes the cloud when roughly45% opacity still remains. The complete action is4.0, with shared glove style and imp recovery acting also below target. Four extended final captures confirm complete clearing after three additional rendered frames; their entire actions are not newly visually accepted.</p></section><section><h2>Original and reusable source</h2><div class="grid"><div class="source">'''
page += fig('../../assets/opera/worlds/props/fx_bop_puff.png','Original source — 2.5/5; stray vertical remnants on each side')+'</div><div class="source">'+fig('clean_puff_exact_reuse.png','Exact existing source — 4.6/5; no repainted or regenerated pixels')+'</div></div></section><section><h2>Individual drafting scores</h2><table><tr><th>Item or interaction</th><th>Score /5</th><th>Review result</th></tr>'
for row in review['individual_scores']:
    page+='<tr><td>'+html.escape(row['item'])+'</td><td>'+str(row['score'])+'</td><td>'+('Refinement priority' if row['priority'] else 'Bounded draft meets target')+'</td></tr>'
page+='</table><p>Scores are judgments about these exact sources and captured uses. They do not transfer to other jobs, devices or unreviewed actions.</p></section><section><h2>Static original/candidate comparisons</h2><div class="grid">'
for view in read(f/'native_context_v1/VISUAL_REVIEW.json')['views']:
    page+=fig('native_context_v1/'+view['path'],str(view['viewport'][0])+' '+view['mode']+' — '+('clean reuse4.6' if 'clean_reuse' in view['path'] else 'original2.5')+'; explicit static impact fixture')
page+='</div></section><section><h2>Sequencing and cause</h2><p>The child’s local touch press, eight forward drag requests and release use the unchanged production handler. Each action produces exactly one accepted punch and one unit of local phase progress. Stored Opera stars do not change. Jab has no pre-contact puff. Imp already has friendly counter feedback before the player’s hit; receive_friendly_hit creates that lower cloud without damage or progress, and the later accepted punch refreshes the effect at the target. That expected event is not scored as a false award.</p><p>The lavender contact cloud leaves the pad or imp face readable. The procedural coral gloves have a much flatter treatment and heavier outline than the painted mitts, costume and room. The imp’s reaction changes between whole cards with an abrupt pose switch and insufficient authored recovery. These weaknesses keep the complete action below target.</p><p>The first zero-state wide captures still show the preceding rendered cloud. Engine state and pixels can differ by one frame here; extra final views below confirm clearing. Frame timestamps describe native capture cadence under a60fps cap, not phone performance.</p></section><section><h2>All157 original native action frames</h2><label>Action <select id="action"></select></label><label>Frame <input id="frame" type="range" min="0" max="39" value="0"></label><p id="state"></p><a id="full"><img id="native" alt="Complete native boxing action frame"></a><p><a href="native_timed_reuse_v2/CAPTURE_RECEIPT.json">Source, input, state, timing and file hashes</a>. Explicit phase fixture and actual local GUI-handler requests; ordinary HUD navigation and root viewport dispatch are not accepted by this evidence.</p></section><section><h2>Contact and final full-frame evidence</h2><div class="grid">'
for i in direct_v2:
    page+=fig('native_timed_reuse_v2/'+v2['frames'][i]['path'],f'v2 native frame{i} — directly inspected; the final wide zero-state views retain a one-frame cloud')
page+='</div><h3>Extended capture: four settled endings</h3><div class="grid">'
for i in final_v3:
    x=v3['frames'][i];page+=fig('native_timed_reuse_v3/'+x['path'],f'v3 native frame{i}, {x["width"]} {x["mode"]} — puff absent; final view4.6 only')
page+='</div></section><section><h2>Every ordered inspection board</h2><p>All20 boards below were directly viewed. Each thumbnail keeps its complete native canvas and frame index; display normalization and labels provide no runtime artwork or synthetic motion.</p>'
for b in boards:
    page+=fig('native_timed_reuse_v2/'+b['path'],f'Action{b["action"]}: frames{b["frame_indices"][0]}–{b["frame_indices"][-1]}')
page+='</section><section><h2>Preserved failures and remaining scope</h2><p><a href="native_timed_reuse_v1/FAILURE_NOTE.json">First root viewport dispatch assertion failure</a> remains recorded. The successful local-handler route is narrower and does not waive that gap. v2 retains the zero-state/render mismatch; v3 supplies168 frames, with only its four final views newly visually reviewed.</p><p>Original sources, game bindings, protected character/voice/book art and all gameplay code remain unchanged. Current actual job-day routes, Opera training traversal, other shared career-world draw contexts, device, child and owner acceptance remain open. Source4.6 does not close MA-VIS-006 or approve the report. Reversible binding and end-timing refinement are the next scoped work.</p></section></main><script>const DATA='+json.dumps(v2,ensure_ascii=False)+';const pick=document.getElementById("action"),slider=document.getElementById("frame"),im=document.getElementById("native"),state=document.getElementById("state"),full=document.getElementById("full");DATA.actions.forEach((a,i)=>{let o=document.createElement("option");o.value=i;o.textContent=a.width+" "+a.mode;pick.appendChild(o)});function show(){let a=DATA.actions[+pick.value];slider.min=a.first_frame;slider.max=a.last_frame;let n=+slider.value;if(n<a.first_frame||n>a.last_frame){n=a.first_frame;slider.value=n}let x=DATA.frames[n];im.src="native_timed_reuse_v2/"+x.path;full.href=im.src;state.textContent="Frame "+n+" · t="+x.seconds.toFixed(3)+"s · accepted punches="+x.landed_punches+" · impact state="+x.impact_time.toFixed(3)+" (one-frame render/state limit retained)"}pick.addEventListener("change",()=>{slider.value=DATA.actions[+pick.value].first_frame;show()});slider.addEventListener("input",show);show();</script></html>'
(f/'index.html').write_text(page,encoding='utf-8',newline='\n')

tools=f/'review_tools';tools.mkdir(exist_ok=True)
for name in ['run_boxing_puff_timed_reuse_v1.py','run_boxing_puff_timed_reuse_v2.py','run_boxing_puff_timed_reuse_v3.py','build_boxing_puff_timed_boards_v2.py','finalize_boxing_puff_review_v1.py']:
    p=r/'tmp'/name
    if p.exists():shutil.copyfile(p,tools/name)

licenses=r/'ASSET_LICENSES.md';text=licenses.read_text(encoding='utf-8')
for p in sorted(f.rglob('*')):
    if p.suffix.lower() not in ['.png','.webp','.mp4']:continue
    rel=p.relative_to(r).as_posix()
    if '`'+rel+'`' in text:continue
    text+='\n| `'+rel+'` | Mermaid Roshan approved source art / Godot native diagnostic capture | Existing project provenance; review-only derivative | Local project | '+('Exact existing clean-puff bytes; source/hash in PROFILE.json' if p.name=='clean_puff_exact_reuse.png' else 'Complete native rendered frame or uniformly scaled inspection board; no synthetic motion; capture/source hashes retained')+'; no runtime or owner approval |'
licenses.write_text(text+'\n',encoding='utf-8',newline='\n')
attrs=r/'.gitattributes';s=attrs.read_text(encoding='utf-8');line='audit/day_two_boxing_puff_reuse_v1_20261001/** -text'
if line not in s:attrs.write_text(s+'\n'+line+'\n',encoding='utf-8',newline='\n')

master=r/'audit/MASTER_AUDIT_2026-08-09.md';s=master.read_text(encoding='utf-8');heading=s.find('\n')
entry='\nBoxing puff exact-reuse review (2026-10-01): [illustrated source/action audit](day_two_boxing_puff_reuse_v1_20261001/index.html) preserves D2A-0394’s live2.5 source. Existing clean art reaches source/static/timed-contact4.6 at both widths, while end timing4.2 and complete action4.0 remain priorities. All157 v2 frames were directly inspected on20 ordered boards; four v3 extended final views confirm clearing after the retained state/render mismatch. First root-dispatch failure remains unresolved; local-handler tests do not establish ordinary routes. Runtime binding, protected originals and finding lifecycles unchanged. [Impact](../design/audit_impacts/day-two-boxing-puff-reuse-v1-20261001.json).\n'
assert 'Boxing puff exact-reuse review (2026-10-01)' not in s
master.write_text(s[:heading+1]+entry+s[heading+1:],encoding='utf-8',newline='\n')
ledger=r/'design/05_DOC_LEDGER.md';s=ledger.read_text(encoding='utf-8');marker='| `assets_src/imagegen/day1_playroom_sign_v2_20261001/index.html`'
pos=s.index(marker);end=s.index('\n',pos)+1
entry='| `audit/day_two_boxing_puff_reuse_v1_20261001/index.html` | 🟣 | `CANDIDATE`; D2A-0394 original2.5 remains bound. Exact clean source/static/timed-contact4.6; end timing4.2, whole action4.0 and shared glove/recovery acting remain priorities. All157 v2 frames directly reviewed in20 boards; four v3 final views prove only settled clearing. Root-dispatch failure preserved; local-handler input is narrower. No actual route/device/child/owner/global acceptance. |\n'
ledger.write_text(s[:end]+entry+s[end:],encoding='utf-8',newline='\n')
root=r/'audit/job_artwork_refinement_live/index.html';s=root.read_text(encoding='utf-8');marker='<h1>Mermaid Roshan jobs artwork — live review entry</h1>'
assert s.count(marker)==1
s=s.replace(marker,marker+'<p><a href="../day_two_boxing_puff_reuse_v1_20261001/index.html">Boxing puff: live source2.5, exact reuse/contact4.6, fade ending4.2 and complete action4.0</a>. Original binding unchanged; illustrated timed review includes preserved failures.</p>')
root.write_text(s,encoding='utf-8',newline='\n')
status=r/'audit/job_artwork_refinement_live/STATUS.json';a=read(status)
a['current_boxing_puff']=dict(status=profile['status'], source_score=4.6, static_and_timed_contact_score=4.6, end_timing_score=4.2, full_action_score=4.0, current_original_source_score=2.5, runtime_binding_changed=False, review='audit/day_two_boxing_puff_reuse_v1_20261001/REVIEW.json', ordinary_route_acceptance=False)
write(status,a)

impact_path=r/'design/audit_impacts/day-two-boxing-puff-reuse-v1-20261001.json';a=read(impact_path)
a['scope']=profile['scope']+' Eight original/candidate static contexts inspected. All157 v2 frames directly reviewed on20 full-canvas boards and eight full native contact/final frames. Reuse contact4.6; existing fade end4.2, glove coherence4.0, imp recovery3.8 and complete action4.0 stay priorities. Four extra-settled v3 endings4.6 do not establish full action. First root input fixture failure remains unresolved. No production files, bindings, protected art or finding lifecycles changed.'
a['files']=sorted(set([p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()]+['.gitattributes','ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md','audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/STATUS.json']))
a['validation'] += [dict(command='Native parser/inference/exact4.7.2 analyzer and source-bound static/local-handler timed requests',result='PASS',evidence='native_context_v1/PROCESS_RECEIPT.json; native_timed_reuse_v2/PROCESS_RECEIPT.json; native_timed_reuse_v3/PROCESS_RECEIPT.json; CAUSAL_CHECKS.json'),dict(command='Direct individual and ordered full-canvas source/action review',result='PARTIAL',evidence='REVIEW.json; static and timed contact4.6; end4.2 and whole4.0 remain priorities; v2 final render/state mismatch and failed v1 root request preserved')]
a['acceptance_gaps']=review['acceptance_gaps']+' Ordinary root/HUD routes and complete in-world job-day contexts remain open. No finding closure.'
write(impact_path,a)
print(json.dumps({'status':'REPORT_SAVED_ORIGINALS_UNCHANGED','checks':len(checks),'v2_reviewed_frames':157,'v3_final_views':final_v3,'family_files':len(a['files'])}))
