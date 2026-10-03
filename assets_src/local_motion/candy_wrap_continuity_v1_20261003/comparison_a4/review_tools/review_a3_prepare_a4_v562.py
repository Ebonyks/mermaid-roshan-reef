from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'; Q=P/'comparison_a3'; N=P/'comparison_a4'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
    tmp=p.with_name(p.name+'.v562_next');tmp.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');tmp.replace(p)
idx=read(Q/'attempt01/INDEX.json'); assert len(idx['frames'])==41 and len(idx['boards'])==7
assert all(sha(B/x['path'])==x['sha256'] for x in idx['frames']+idx['boards'])
frames=[]
for x in idx['frames']:
    i=x['index']
    if i==0:score,obs=4.5,'Intact initial partial-fold grip; two connected mittens and the same red crescent remain visible.'
    elif i<=10:score,obs=4.2,'Roshan retains the initial grip and exposed red crescent; minute face/paper contour changes do not perform a fold.'
    elif i<=13:score,obs=2.5,'An oversized third coral mitten intrudes from the lower/right border while both original mittens stay at the same grip.'
    elif i<=21:score,obs=1.8,'A large unrelated coral mitten and teal sleeve occupy the right foreground; Roshan does not fold or release the paper.'
    else:score,obs=1.2,'Two oversized unrelated foreground mittens surround and increasingly obscure the table; Roshan still holds the original partly open wrapper.'
    frames.append(dict(x,visual_frame_score=score,evaluation=f"Frame {i} at {x['timestamp_seconds']:.3f}s: {obs} Individual native-canvas opinion only; no useful-action/runtime acceptance.",direct_native_board_review=True,full_native_detail_review=i in [0,13,40],runtime_bound=False,owner_acceptance=None))
components=[
('Character identity and stable complete silhouette',3.8,'Roshan remains recognizable, but face/body contours drift and foreground duplication dominates the ending.'),
('Exactly two connected mittens owned by Roshan',1.0,'A third oversized mitten enters at frame11; a fourth arrives later. Their sleeves connect to off-screen bodies, not Roshan.'),
('Initial lower-free-edge grasp',4.2,'The starting partial-fold grasp is readable, though its exact over/under contact is small at this input scale.'),
('Existing mitten carries the attached flap',1.5,'Both authored mittens stay at the initial contact. The paper does not cross the remaining red crescent.'),
('Same sweet supported on the same table',4.3,'The central sweet and gold sheet remain supported, but unsupported foreground arms obscure their evidence.'),
('Gold paper occludes the remaining sweet surface',1.5,'The red crescent remains exposed throughout all41 canvases; no completed fold occurs.'),
('Release leaves the useful fold intact',1.5,'Roshan never opens the original grip or leaves a closed fold. Extra arms are not a release.'),
('Attention remains on useful task change',3.9,'Early gaze points toward the task, but later duplicated anatomy and body drift distract from any useful contact.'),
('Golden paper and painted quilted material continuity',4.2,'Central gold and quilted material largely survive. Extra foreground mittens have a different oversized, muddier finish.'),
('Whole far-fold closure/release component',1.5,'Rejected: no closure or release, plus catastrophic extra-hand ownership. It cannot contribute accepted pixels or motion to the actual wrapper.')]
review=dict(status='ALL41_NATIVE_FRAMES_REVIEWED_EXTRA_HANDS_COMPONENT_REJECTED',reviewed_utc=now(),prompt_id=idx['prompt_id'],native_frame_count=41,boards_reviewed=[x['path'] for x in idx['boards']],full_native_details=[0,13,40],individual_frames=frames,component_opinions=[dict(item=x,score=s,evaluation=e,priority=s<=4.5) for x,s,e in components],whole_component_score=1.5,qualification='All41 native896x512 canvases directly inspected on7 non-resampled boards plus three individual original-size details. A3 is reference-only and rejected. Source4.5 never transfers to action. Current in-game WRAP2.8 and the original full folding/neck/twist/release workflow remain open.',runtime_bound=False,owner_acceptance=None)
write(Q/'attempt01/DIRECT_REVIEW.json',review)
write(Q/'REVIEW_STATUS.json',dict(status=review['status'],whole_component_score=1.5,runtime_integration=False,owner_approval=None))
ip=B/'design/audit_impacts/job-candy-local-far-fold-a3-20261003.json';d=read(ip)
d['validation']=[x for x in d['validation'] if x['command'] not in ['Developed local90-second-quiet FIFO and exact installed bytes/benchmark admission','Directly inspect every41 native frame and each whole contact/fold/payoff']]
d['validation'] += [dict(command='Direct review every41 original-size native canvas and ten individual components',result='FAIL',evidence='comparison_a3/attempt01/DIRECT_REVIEW.json: whole1.5; added foreground hands from frame11, no closure/release. All original failed output retained.')]
d['acceptance_gaps']='A3 rejected1.5. Original full wrapping and current in-game WRAP2.8 remain open; no runtime/owner/device/child/all-job acceptance or finding closure.'
write(ip,d)
assert not N.exists();N.mkdir();(N/'review_tools').mkdir();(N/'inputs').mkdir();(N/'prompts').mkdir();(N/'workflows').mkdir()
prompt='''Roshan herself folds the golden paper over the red sweet on her table. Her existing right arm, at the left side of the image, bends downward and carries the paper across the remaining red crescent until it is covered. Her other existing mitten braces the sweet. Then she slightly loosens that grasp, leaving the gold folded. Only the girl's two existing arms perform this small useful action, both wrists continuously attached to her sleeves. Keep her size, table and camera fixed. No other person, foreground arm, extra hand, new sweet or new paper.
Sound: silence.
'''
(N/'prompts/CANDY-FOLD-A4.txt').write_text(prompt,encoding='utf-8',newline='\n')
m=read(Q/'MANIFEST.json');m.update(id='candy-far-fold-a4-20261003',created_utc=now(),intention='Prompt-only attempt to make Roshan herself perform the existing attached far-flap fold and small release, eliminating added foreground hands.',input_path='inputs/CANDY-FOLD-A4.png',prompt_path='prompts/CANDY-FOLD-A4.txt',prompt_sha256=sha(N/'prompts/CANDY-FOLD-A4.txt'),queue_name='candy_far_fold_a4_20261003',comparison='Only the positive action prompt changes from rejected A3. Exact source/input, seed, settings, installed workflow/model and intended far-fold closure/release component are identical. Original full wrapping success criteria stay unchanged.')
shutil.copyfile(Q/'inputs/CANDY-FOLD-A3.png',N/m['input_path']);assert sha(N/m['input_path'])==m['input_sha256']
for binding in m['renderer']['bindings']:
    shutil.copyfile(Q/binding['packet_path'],N/binding['packet_path']);assert sha(N/binding['packet_path'])==binding['sha256']
j=m['jobs'][0];j.update(id='CANDY-FOLD-A4',input_path=m['input_path'],prompt_path=m['prompt_path'],prompt_sha256=m['prompt_sha256'],queue_name=m['queue_name']);write(N/'MANIFEST.json',m)
plan=read(Q/'PLAN.json');plan.update(planned_utc=now(),intention=m['intention'],reuse_inventory='Exact A13 source and directly inspected whole-canvas normalized A3 input reused byte-for-byte; no new source generation or normalization. A3 rejected1.5 extra-hand ownership/no closure. No failed output pixels enter A4.',comparison=m['comparison']);write(N/'PLAN.json',plan)
write(N/'INPUT_REUSE_RECEIPT.json',dict(status='EXACT_BYTE_REUSE_DIRECTLY_INSPECTED_A3_INPUT',source_path=m['source_path'],source_sha256=m['source_sha256'],input_sha256=m['input_sha256'],previous_input=(Q/'inputs/CANDY-FOLD-A3.png').relative_to(B).as_posix(),normalization_evidence=(Q/'NORMALIZATION_RECEIPT.json').relative_to(B).as_posix(),direct_review_evidence=(Q/'INPUT_DIRECT_REVIEW.json').relative_to(B).as_posix(),qualification='Same complete input already directly reviewed at original size this turn; no crop, matte change or subject manipulation. Source-only4.5 is not a motion pass.'))
for filename in ['queue_candy_far_fold_a3_v560.py','archive_candy_far_fold_a3_v560.py']:
    text=(Q/'review_tools'/filename).read_text(encoding='utf-8').replace('comparison_a3','comparison_a4').replace('CANDY-FOLD-A3','CANDY-FOLD-A4').replace('candy_local_fold_a3_active_20261003','candy_local_fold_a4_active_20261003').replace('CANDY FAR LONG-EDGE FOLD A3','CANDY FAR LONG-EDGE FOLD A4').replace('CANDY_A3_NATIVE_ARCHIVED','CANDY_A4_NATIVE_ARCHIVED').replace('job-candy-local-far-fold-a3-20261003.json','job-candy-local-far-fold-a4-20261003.json').replace('Candy partial far-fold A3','Candy partial far-fold A4')
    (N/'review_tools'/filename.replace('a3_v560','a4_v562')).write_text(text,encoding='utf-8',newline='\n')
write(N/'REVIEW_STATUS.json',dict(status='EXACT_INPUT_REUSE_PROMPT_COMPARISON_READY',runtime_integration=False,owner_approval=None))
shutil.copyfile(__file__,N/'review_tools'/Path(__file__).name)
ni=B/'design/audit_impacts/job-candy-local-far-fold-a4-20261003.json'
write(ni,dict(id=ni.stem,scope=m['intention']+' Reference-only, no runtime or cinematic delivery; original whole wrapping and all-job objective unchanged.',baseline=m['baseline'],rules=d['rules'],findings=['MA-VIS-006','MA-PLAY-004'],files=sorted(x.relative_to(B).as_posix() for x in N.rglob('*') if x.is_file()),validation=[dict(command='Exact admitted input/source/workflow reuse',result='PASS',evidence='INPUT_REUSE_RECEIPT.json; source/input/model/workflow bytes identical, prompt-only.'),dict(command='Developed dispatcher admission and one nonduplicated quiet-idle render',result='PENDING',evidence='MANIFEST.json; source identity/motion remain separately auditable.'),dict(command='Inspect every41 native frame and exact two-hand ownership/fold/release',result='PENDING',evidence='No predicted action/visual/owner pass.')],acceptance_gaps='A4 unrendered. Current WRAP2.8, original full fold/neck grip/opposing twist/release, actual game/ordinary inputs/interruption/device/child/owner/all-job acceptance remain open.'))
print('A3 rejected1.5; A4 declared as exact-input/source/settings/seed prompt-only comparison.')
