from pathlib import Path
import datetime, hashlib, html, json, shutil
from PIL import Image

B = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
C = B / 'assets_src/imagegen/candy_wrap_scene_context_v1_20261003'
A = C / 'attempt02'
Q4 = B / 'assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a4'
Q5 = Q4.with_name('comparison_a5')
assert not A.exists() and not Q5.exists()
A.mkdir()
for name in ('inputs', 'prompts', 'workflows', 'review_tools', 'checks'):
    (Q5 / name).mkdir(parents=True, exist_ok=True)

read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')

src = Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-d272eb29-5146-44ea-899c-0bc06e621053.png')
shutil.copyfile(src, A / 'native.png')
assert sha(src) == sha(A / 'native.png')
plan = read(C / 'PLAN_A2.json')
with Image.open(src) as im:
    dims, mode = list(im.size), im.mode
assert dims == [1672, 941] and mode == 'RGB'
write(A / 'SOURCE.json', dict(attempt=2, method='builtin_imagegen_targeted_foreground_removal_complete_scene', original_path=str(src), native_path=(A/'native.png').relative_to(B).as_posix(), sha256=sha(src), dimensions=dims, mode=mode, prompt=plan['prompt'], prompt_sha256=plan['prompt_sha256'], references=[dict(path=plan['source_path'], sha256=plan['source_sha256'])], native_preserved=True, runtime_ready=False, runtime_bound=False, owner_acceptance=None, qualification='Complete generated scene source preserved unchanged. A starting-source opinion does not accept motion, game fit, a new background or a cinematic frame.'))
opinions = [
    ('Character/costume and painted identity', 4.5, 'Established teal shell cap, coral bows, brown/rainbow hair, face, waistcoat and rounded painted contours remain recognizable in the complete room.'),
    ('Exactly two connected owned mittens', 4.5, 'Both coral quilted mittens connect to Roshan through visible bent sleeves. No outside arm or bare human fingers appears in this starting still.'),
    ('Partial-fold grasp and attached gold sheet', 4.5, 'The screen-left mitten grips the raised gold flap while the screen-right mitten braces it beside the supported red oval. The visible red crescent makes the unfinished state readable; continuous bending and closure remain unproved.'),
    ('Same supported foreground task', 4.5, 'One working red sweet, one attached gold sheet and the broad lavender worktop form a clear contact group; no replacement sweet has been added to the foreground.'),
    ('Attention to the task', 4.5, 'The inclined head and open eyes attend to the work area. A continuous attention performance remains unproved.'),
    ('Foreground clutter and target singularity', 4.6, 'The unwanted jars, sweet bowls and utensil pot are gone. The painted lavender surface continues across both sides without competing foreground tasks.'),
    ('Room/table context and material', 4.4, 'Established factory architecture and machinery provide painted scene context, but their dense highlights and small decorations remain a background hierarchy priority. This is not a passing review of the original runtime backdrop.'),
    ('Whole contextual starting source', 4.5, 'Provisional starting-still floor: two owned hands, readable partial grasp, one working sweet and clean foreground. Admitted only to a separate local motion-reference experiment. The complete wrapping task and runtime fit are not accepted.')
]
write(A/'DIRECT_REVIEW.json', dict(status='SOURCE_STARTING_STILL_4_5_PROVISIONAL_LOCAL_STUDY_ONLY', reviewed_utc=now(), direct_complete_native_review=True, native_sha256=sha(src), whole_source_score=4.5, opinions=[dict(item=i, score=s, evaluation=e, priority=s<=4.5) for i,s,e in opinions], qualification='Complete native directly inspected. Eight individual source opinions, background priority retained. No runtime, action, cinematic, device/child/owner acceptance.', runtime_bound=False, owner_acceptance=None))
write(C/'COMPLETE_SOURCE_REVIEW.json', dict(status='TWO_NATIVE_SOURCES_DIRECTLY_REVIEWED', reviewed_utc=now(), attempts=2, individual_opinions=16, selected_starting_source=(A/'native.png').relative_to(B).as_posix(), selected_source_sha256=sha(src), starting_source_score=4.5, prior_rejected_source_score=4.2, motion_score=None, current_production_wrap_score=2.8, runtime_bound=False, owner_acceptance=None, qualification='A1 failure preserved; A2 is a provisional partial-fold starting still. A5 motion uses changed framing, subject scale, geometry and background, so this observational comparison is not isolated-variable causal evidence.'))

old = read(Q4/'MANIFEST.json')
job_id='CANDY-FOLD-A5'
inp=Q5/'inputs'/f'{job_id}.png'
with Image.open(A/'native.png') as im:
    resized=im.resize((896,504), Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(896,512),'black')
    canvas.paste(resized,(0,4))
    canvas.save(inp)
write(Q5/'INPUT_NORMALIZATION.json', dict(method='whole_complete_canvas_uniform_contain_with_integer_rounding', source_path=(A/'native.png').relative_to(B).as_posix(), source_sha256=sha(src), source_dimensions=dims, input_path='inputs/'+job_id+'.png', input_sha256=sha(inp), input_dimensions=[896,512], mode='RGB', contained_dimensions=[896,504], offset=[0,4], padding='black 4 pixels top and bottom', no_crop=True, no_subject_isolation_or_repair=True, native_preserved=True, qualification='Technical whole-canvas conditioning for local motion reference only; no delivery-frame claim or replacement runtime artwork.'))
prompt_src=Q4/old['prompt_path']
prompt=Q5/'prompts'/f'{job_id}.txt'
shutil.copyfile(prompt_src,prompt)
assert sha(prompt)==old['prompt_sha256']
for binding in old['renderer']['bindings']:
    p=Q4/binding['packet_path']; t=Q5/binding['packet_path']
    t.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(p,t)
    assert sha(t)==binding['sha256']
write(Q5/'PLAN.json', dict(status='FRESH_CONTEXT_COMPARISON_PREPARED_INPUT_REVIEW_PENDING', planned_utc=now(), baseline='2b109a233c14050567aaa84dc975119b2e18a77e', current_production_wrap_score=2.8, prior_local_motion_scores={'A1':2.4,'A2':1.8,'A3':1.5,'A4':0.8}, source_score=4.5, source_status='partial_fold_still_only', purpose='Test whether a complete painted room context permits Roshan-owned hand contact, after outside human-arm failures on the neutral field.', comparison_limit='Background, framing, subject scale and source geometry change together. Prompt bytes, seed, renderer settings and seven developed workflow bindings remain identical to A4. No causal isolation or predicted passing result.', admission='One developed guarded quiet-idle FIFO job, local reference only. No installs, cancellation, workflow/model changes, runtime or cinematic integration.', source_review=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix()))
m=dict(schema='reef.local-candy-motion-study.v1', id='candy-context-fold-a5-20261003', created_utc=now(), baseline='2b109a233c14050567aaa84dc975119b2e18a77e', acceptance='LOCAL_MOTION_REFERENCE_ONLY', owner_approval=None, runtime_integration=False, authorization=old['authorization'], intention='Roshan herself carries the already-gripped golden paper across the remaining red crescent and slightly releases it. Only a far-fold component is attempted; complete wrap requirements remain unchanged.', profile=old['profile'], register=old['register'], source_path=(A/'native.png').relative_to(B).as_posix(), source_sha256=sha(src), source_dimensions=dims, source_status='STATIC_SOURCE_DRAFT_4.5_OWNER_UNASSIGNED', source_review=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix(), input_path='inputs/'+job_id+'.png', input_sha256=sha(inp), input_transform='Whole1672x941 complete scene contained896x504 on896x512 RGB, black4px top/bottom, no crop or subject repair.', prompt_path='prompts/'+job_id+'.txt', prompt_sha256=sha(prompt), queue_name='candy_context_fold_a5_20261003', seed=2026100301, renderer=old['renderer'], clip_contract=dict(entry='A2 complete painted scene: exactly two owned coral mittens connected to sleeves, screen-left mitten already gripping raised gold flap, screen-right bracing the same supported red sweet. This is an unbound starting scene; ordinary game entry unproved.', exit='Existing gold flap covers the remaining red crescent and the grasp slightly loosens; both hands remain connected. Neck pinches, opposing twists and full two-ended wrapper release are still required for the original complete wrap and are not attempted by this component.', duration_seconds=41/24, timeline=prompt.read_text(encoding='utf-8'), anchors=dict(unit='1672x941 complete source normalized coordinates', sweet_center_approx=[0.502,0.821], sweet_size_approx=[0.115,0.065], qualification='Direct visual targets only, not measured motion tolerance evidence.'), direction='Forward table work view in complete established painted Candy room context.', events='Reference only; gameplay owners and result callbacks unchanged.', interruptions='No runtime playback; one guarded local renderer job, no duplicate/cancel/restart.', required_review='Every41 full native canvases, exactly two continuously attached owned arms/mittens, same supported sweet, continuous attached gold-paper bend/cover/release, identity/style/attention. Component floor cannot accept full wrapping or current game.'), status='PREPARED_INPUT_VISUAL_REVIEW_AND_CHECK_PENDING', visual_review=None, complete_action_score=None, jobs=[dict(id=job_id,name='Contextual far long-edge fold component',source_path=(A/'native.png').relative_to(B).as_posix(),source_sha256=sha(src),input_path='inputs/'+job_id+'.png',input_sha256=sha(inp),prompt_path='prompts/'+job_id+'.txt',prompt_sha256=sha(prompt),queue_name='candy_context_fold_a5_20261003',seed=2026100301,owner_approval=None)], comparison='Observed scene-context comparison only. Same actual A4 prompt bytes/seed/settings/workflows, different complete source/framing/scale/geometry. Fresh actual entry and timeline; old A4 inherited entry/timeline errors are preserved and disclosed in PRIOR_CLIP_ENTRY_LABEL_LIMITATION.json.', source_region=[0,0,1672,941], input_visual_review=None, intended_component_only=True)
write(Q5/'MANIFEST.json',m)
worker=(Q4/'review_tools/queue_candy_far_fold_a4_v562.py').read_text(encoding='utf-8')
worker=worker.replace('comparison_a4','comparison_a5').replace('CANDY-FOLD-A4','CANDY-FOLD-A5').replace('candy_local_fold_a4_active_20261003','candy_local_fold_a5_active_20261003')
(Q5/'review_tools/queue_candy_context_fold_a5_v576.py').write_text(worker,encoding='utf-8',newline='\n')
archive=(Q4/'review_tools/archive_candy_far_fold_a4_v562.py').read_text(encoding='utf-8')
archive=archive.replace('comparison_a4','comparison_a5').replace('CANDY-FOLD-A4','CANDY-FOLD-A5').replace('candy_local_fold_a4_active_20261003','candy_local_fold_a5_active_20261003').replace('CANDY FAR LONG-EDGE FOLD A4','CANDY CONTEXT FAR-FOLD A5').replace('CANDY_A4_NATIVE_ARCHIVED','CANDY_A5_NATIVE_ARCHIVED').replace('job-candy-local-far-fold-a4-20261003.json','job-candy-painted-context-source-20261003.json').replace('Candy partial far-fold A4','Candy contextual partial far-fold A5')
(Q5/'review_tools/archive_candy_context_fold_a5_v576.py').write_text(archive,encoding='utf-8',newline='\n')

esc=lambda x:html.escape(str(x))
parts=[]
for attempt in (1,2):
    ad=C/f'attempt{attempt:02d}'; review=read(ad/'DIRECT_REVIEW.json'); source=read(ad/'SOURCE.json')
    ops=''.join('<tr><td>'+esc(o['item'])+'</td><td>'+esc(o['score'])+'/5</td><td>'+esc(o['evaluation'])+'</td></tr>' for o in review['opinions'])
    parts.append(f'<article><h2>Attempt {attempt} · {review["whole_source_score"]}/5 source</h2><p>{esc(review["status"])}</p><img src="attempt{attempt:02d}/native.png" alt="Complete painted Candy partial-fold starting scene attempt {attempt}"><table><thead><tr><th>Individual item</th><th>Score</th><th>Written evaluation</th></tr></thead><tbody>{ops}</tbody></table><details><summary>Exact generation prompt and source provenance</summary><pre>{esc(source["prompt"])}</pre><p>{esc(source["sha256"])}</p><a href="attempt{attempt:02d}/SOURCE.json">Source record</a> · <a href="attempt{attempt:02d}/DIRECT_REVIEW.json">Direct review</a></details></article>')
(C/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Candy wrapper · complete painted scene source review</title><style>body{margin:auto;max-width:1120px;padding:24px;background:#eef5fb;color:#24324a;font:17px/1.55 system-ui;box-sizing:border-box}h1,h2{line-height:1.2}article{background:white;border-radius:18px;padding:20px;margin:24px 0}img{display:block;width:100%;height:auto}table{width:100%;border-collapse:collapse}td,th{text-align:left;vertical-align:top;padding:10px;border-bottom:1px solid #dbe2ec}pre{white-space:pre-wrap;overflow-wrap:anywhere}p,td{overflow-wrap:anywhere}a{color:#184b85}</style><h1>Candy wrapper · complete painted starting scenes</h1><p>Two complete native sources · 16 individual written opinions · current in-game WRAP <strong>2.8/5</strong>. Attempt 1 is rejected at 4.2. Attempt 2 is a provisional <strong>4.5/5 partial-fold starting still</strong>; its busy background remains a priority. No motion score transfers from a still.</p><p><a href="../../../local_motion/candy_wrap_continuity_v1_20261003/index.html">Existing four failed local motion studies</a> · <a href="COMPLETE_SOURCE_REVIEW.json">Review summary</a> · <a href="PRIOR_CLIP_ENTRY_LABEL_LIMITATION.json">Prior inherited clip-label limitation</a></p><p>A5 compares this complete scene with the prior neutral-field study using the same actual motion prompt, seed and settings. Scene context, framing, subject scale and geometry change together; this is observational, not an isolated-variable causal experiment. All artwork is reversible and unbound. Full wrap, ordinary gameplay, device, child and owner acceptance remain open.</p>'+''.join(parts)+'</html>',encoding='utf-8',newline='\n')

licenses=B/'ASSET_LICENSES.md';raw=licenses.read_bytes();path=(A/'native.png').relative_to(B).as_posix();assert ('| `'+path+'` |').encode() not in raw
raw+=('\n| `'+path+'` | Builtin ImageGen targeted cleanup of complete contextual Candy starting scene | Original generated project artwork with OpenAI; existing character/wrapper/backdrop source attribution retained | SOURCE.json records exact prompt/reference/native hashes | Complete native preserved; only added foreground jars/bowls/tools removed. Starting still4.5 provisional, background4.4; no production/cinematic/motion/owner acceptance. |\n').encode()
n=licenses.with_name(licenses.name+'.v576_next');n.write_bytes(raw);n.replace(licenses)
shutil.copyfile(__file__,C/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';d=read(ip)
d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for base in (C,Q5) for p in base.rglob('*') if p.is_file()}|{'ASSET_LICENSES.md'})
d['validation'][-1].update(result='PASS',evidence=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix()+'; whole source4.5 provisional, background4.4 retained, both native sources and16 opinions illustrated.')
d['validation'].append(dict(command='Fresh complete-context A5 input review, exact developed queue admission and every native action frame review',result='PENDING',evidence=Q5.relative_to(B).as_posix()+'/MANIFEST.json; unqueued, no predicted motion acceptance.'))
write(ip,d)
print(json.dumps(dict(status='CONTEXT_A2_SOURCE_PRESERVED_AND_A5_PREPARED',dimensions=dims,source_sha256=sha(src),input_sha256=sha(inp),same_actual_A4_prompt=True,individual_source_opinions=16,queued=False)))
