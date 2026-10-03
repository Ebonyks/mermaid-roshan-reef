from pathlib import Path
import datetime, hashlib, json, shutil

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'
Q5=P/'comparison_a5'; A=Q5/'attempt01';Q6=P/'comparison_a6'
C=B/'assets_src/imagegen/candy_wrap_scene_context_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
    n=p.with_name(p.name+'.v580_next');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n');n.replace(p)

idx=read(A/'INDEX.json');assert len(idx['frames'])==41 and len(idx['boards'])==7
observations=[
 (4.5,'The decoded opening preserves the complete painted partial-fold source: two attached mittens, one red sweet and one supported gold sheet; no motion consequence yet.'),
 (4.4,'Both owned wrists remain attached; a small initial grip change leaves the same red crescent exposed.'),
 (4.4,'The mitten grip begins narrowing the raised gold edge; the sweet remains supported and partially exposed.'),
 (4.3,'Both mittens start drawing the flap back toward Roshan instead of bringing it down across the sweet.'),
 (4.2,'The gripped gold edge narrows to a strip; uncovered red area persists and the opposite hand also pulls rather than braces.'),
 (4.1,'The strip is lifted between both owned hands; this motion has not reduced visible red candy.'),
 (4.0,'The screen-left wrist rises and the long edge moves away from the viewer, exposing more red surface.'),
 (4.0,'Two connected hands continue holding the lifted strip; no covering edge crosses the remaining crescent.'),
 (3.9,'The paper reads as an elevated stretched band while the red sweet sits exposed beneath it.'),
 (3.9,'Both mittens pull the same band upward; the requested stable supporting hand is absent.'),
 (3.8,'The gold flap moves farther back and its crinkle pattern simplifies; the sweet stays uncovered.'),
 (3.8,'An unsupported-looking strip arches above the candy; the original near sheet still rests on the tabletop.'),
 (3.8,'The left end rises while the central strip sags; this explains a lift rather than the requested covering fold.'),
 (3.7,'The raised flap rounds into a smooth gold roll; the same red sweet remains exposed in front of it.'),
 (3.7,'A pale crease appears inside the screen-left grip and mitten quilt detail changes; both wrists are still owned, but paper coverage fails.'),
 (3.7,'The paper band stays raised and rounded; there is no completed long-edge fold over the candy.'),
 (3.7,'The screen-left mitten tugs one corner higher while the opposite mitten holds the band above the sweet.'),
 (3.7,'The curled flap stretches sideways between the hands; red visibility remains unchanged from the recent exposed state.'),
 (3.7,'The left grip lifts the gold corner again; both sleeves remain attached, but the long edge stays behind the sweet.'),
 (3.7,'The left mitten becomes rounder while holding the elevated corner; neither hand presses paper onto the red oval.'),
 (3.7,'The lifted corner twists locally while the central band sags above the uncovered sweet.'),
 (3.7,'A local corner turn continues with both hands still grasping; it is not closure, a neck pinch or release.'),
 (3.6,'The left mitten turns downward around the corner while the band remains behind the exposed sweet.'),
 (3.6,'The left grip points down but the gold edge is still raised; no covering front moves over the candy.'),
 (3.6,'The mittens converge slightly around the raised band; the visible red oval remains unobscured.'),
 (3.6,'Both hands hold above the tabletop with a localized gold curl; the other hand still does not brace the sweet.'),
 (3.6,'The raised edge is gathered toward the right mitten; the sweet keeps the same exposed position.'),
 (3.6,'The right-side band thickens and its crinkles change; no continuous covering bend can be followed across the red surface.'),
 (3.6,'The left corner is drawn toward the body; the supported sweet remains uncovered below the gold band.'),
 (3.6,'Both connected mitten hands remain in the same raised work group; the desired closure endpoint is still missing.'),
 (3.6,'The raised flap becomes a broad gold wedge near the right grip; the red candy remains in front of it.'),
 (3.6,'The hands maintain their grip on the wedge; no loose released hand or stable finished fold is visible.'),
 (3.6,'The gold edge is raised diagonally across the torso-side of the sweet; the front red face remains exposed.'),
 (3.6,'The same elevated wedge shifts slightly under the mittens; complete covering still does not occur.'),
 (3.6,'The left glove turns near the raised corner; the sweet is still uncovered and the paper does not settle over it.'),
 (3.6,'The near sheet remains flat while the far band stays raised; there is no single readable finished fold.'),
 (3.5,'The band rises higher and broadens between both hands; this increases separation from the sweet.'),
 (3.5,'Both wrists remain connected, but the gold edge lifts toward the body rather than down across the candy.'),
 (3.5,'The broad lifted band continues to obscure the lower vest instead of the red sweet.'),
 (3.5,'The almost-final pose still grips the raised gold band; the requested small release is absent.'),
 (3.5,'The final canvas has two owned hands, one exposed red sweet and a lifted gold band. Neither coverage nor release reaches the declared exit.')
]
assert len(observations)==41
frames=[]
for row,(score,evaluation) in zip(idx['frames'],observations):
    assert sha(B/row['path'])==row['sha256']
    frames.append(dict(**row,visual_frame_score=score,evaluation=evaluation,direct_native_review=True,priority=score<=4.5))
components=[
 ('Exactly two owned arms and hand attachment',4.5,'Across all41 complete canvases, the same two coral mittens remain attached through Roshan’s sleeves. No outside human hand appears. This source/framing outcome does not prove that context alone caused the improvement.'),
 ('Mitten identity and quilt/crease continuity',4.2,'The coral mitten family remains readable, but the left thumb/inner pale crease and quilt detail soften or reshape during the grip changes, especially frame14.'),
 ('Same sweet, support and target continuity',4.2,'One red sweet stays on the same gold sheet/table; its outline and red material become lumpier as the flap pulls away. No substituted sweet appears.'),
 ('Attached golden-paper material and bend',3.7,'The raised flap simplifies into a smooth rolled band, then a wider wedge. Its relationship to the sheet below is ambiguous and the crinkle pattern changes; a covering bend is absent.'),
 ('Far long-edge direction and complete coverage',1.5,'The edge lifts back toward Roshan and progressively exposes the sweet. No frame covers the remaining red crescent, including the final endpoint.'),
 ('Steady brace and useful hand roles',3.1,'Both hands manipulate the elevated band. The opposite mitten does not visibly steady the sweet while one hand performs the covering fold.'),
 ('Release and settled completed fold',2.0,'Both mittens still hold the raised band in the final frame. There is no slightly released grip leaving a completed fold in place.'),
 ('Painted character/room style and scene stability',4.4,'The established complete painted family remains recognizable and avoids the prior outside-human intrusion. Small generative contour/material changes and the dense room remain refinements; no runtime fit is established.'),
 ('Attention, timing and one useful consequence',3.7,'Roshan attends to the work group with a contained gesture, but the principal motion reverses the intended operation. Quiet acting cannot pass an absent wrapping consequence.'),
 ('Whole contextual far-fold component',3.1,'Rejected: substantially better hand ownership, but the paper lifts away and the sweet remains uncovered. Original full-wrap neck pinch/opposing twists/release and current in-game WRAP2.8 remain open.')
]
write(A/'DIRECT_REVIEW.json',dict(status='REJECTED_LIFTS_FLAP_AWAY_NO_COVER_OR_RELEASE',reviewed_utc=now(),whole_component_score=3.1,complete_wrapping_score=None,current_production_wrap_score=2.8,direct_every_native_frame_review=True,frame_count=41,board_count=7,native_details_reviewed=[0,14,22,40],individual_frames=frames,component_opinions=[dict(item=i,score=s,evaluation=e,priority=s<=4.5) for i,s,e in components],qualification='Every41 complete native decoded canvases inspected on seven non-resampled original-size boards, plus four exact native details. Reference-only, unbound. All41 individual canvas opinions and10 components written. Hand ownership improvement is observational; source/framing/scale/geometry changed together. No continuous far-fold coverage or release, no complete wrapping/current-game/cinematic/device/child/owner acceptance.'))
write(Q5/'REVIEW_STATUS.json',dict(status='LOCAL_REFERENCE_REJECTED_A5_3_1',whole_component_score=3.1,native_frames_reviewed=41,component_opinions=10,source_still_score=4.5,runtime_integration=False,owner_acceptance=None,manifest_preserved_sha256=sha(Q5/'MANIFEST.json')))
idx['status']='ALL41_NATIVE_FRAMES_DIRECTLY_REVIEWED_REFERENCE_REJECTED_3_1';idx['direct_review']='DIRECT_REVIEW.json';write(A/'INDEX.json',idx)

assert not Q6.exists()
for name in ('inputs','prompts','workflows','review_tools','checks'):(Q6/name).mkdir(parents=True,exist_ok=True)
old=read(Q5/'MANIFEST.json');m=json.loads(json.dumps(old));job_id='CANDY-FOLD-A6'
prompt='''0–1.3s: Roshan lowers the golden-paper flap toward the viewer and lays it FLAT over the red sweet. The long edge already held by her two coral mittens moves steadily toward the BOTTOM of the picture, crossing the red surface until all red is hidden under the same gold paper. Her wrists stay joined to her own sleeves. The sweet stays on the lavender table; the sheet under it stays in place. 1.3–1.7s: she presses the completed fold once, loosens both grips and rests her mittens beside the covered sweet.
Keep exactly this girl, her two mitten hands, one sweet and one sheet. Keep the painted character, room, table and camera stable. Show one downward covering fold with a quiet finish. No lifting the flap back toward her body, rolled strip, extra hands, changed sweet, new paper, tied necks, twists or glow.
Sound: silence.
'''
inp=Q6/'inputs'/f'{job_id}.png';shutil.copyfile(Q5/old['input_path'],inp)
pp=Q6/'prompts'/f'{job_id}.txt';pp.write_text(prompt,encoding='utf-8',newline='\n')
for binding in old['renderer']['bindings']:
    t=Q6/binding['packet_path'];t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Q5/binding['packet_path'],t)
    assert sha(t)==binding['sha256']
m.update(id='candy-context-fold-a6-20261003',created_utc=now(),intention='Prompt-only direction repair after A5 wrongly lifts the flap back: existing long edge moves toward bottom of image, covers red, presses once and slightly releases.',input_path='inputs/'+job_id+'.png',input_sha256=sha(inp),prompt_path='prompts/'+job_id+'.txt',prompt_sha256=sha(pp),queue_name='candy_context_fold_a6_20261003',status='BOUND_UNCHANGED_CONTEXT_INPUT_REVIEWED_CHECK_PENDING',comparison='Only the action prompt changes from A5. Exact complete-scene source, normalized input, seed2026100301, admitted settings and seven installed workflow bindings are unchanged. All prior failures and original complete-wrap criteria remain unchanged.')
m['clip_contract'].update(exit='Same gold flap laid flat toward viewer over all visible red, pressed once, hands slightly released beside the covered sweet. The original whole wrapper still requires neck pinches/opposing twists and complete two-ended release.',timeline=prompt)
m['input_visual_review']=dict(status='EXACT_UNCHANGED_A5_INPUT_BYTES_DIRECTLY_REVIEWED',evidence=(Q5/'INPUT_DIRECT_REVIEW.json').relative_to(B).as_posix(),input_sha256=sha(inp),source_score_transfer=False)
m['jobs']=[dict(id=job_id,name='Prompt-only downward covering far-fold component',source_path=m['source_path'],source_sha256=m['source_sha256'],input_path=m['input_path'],input_sha256=m['input_sha256'],prompt_path=m['prompt_path'],prompt_sha256=m['prompt_sha256'],queue_name=m['queue_name'],seed=m['seed'],owner_approval=None)]
assert sha(inp)==old['input_sha256']
write(Q6/'MANIFEST.json',m)
write(Q6/'PLAN.json',dict(status='ONE_PROMPT_ONLY_DIRECTION_COMPARISON_PREPARED',planned_utc=now(),baseline=m['baseline'],source_and_input_unchanged=True,seed_and_settings_unchanged=True,prior_failure=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix(),prior_component_score=3.1,current_production_wrap_score=2.8,acceptance='LOCAL_MOTION_REFERENCE_ONLY',no_predicted_acceptance=True,qualification='Far-fold component only; no neck/twist/full-wrapper requirement has been removed.'))
worker=(Q5/'review_tools/queue_candy_context_fold_a5_v576.py').read_text(encoding='utf-8').replace('comparison_a5','comparison_a6').replace('CANDY-FOLD-A5','CANDY-FOLD-A6').replace('candy_local_fold_a5_active_20261003','candy_local_fold_a6_active_20261003')
(Q6/'review_tools/queue_candy_context_fold_a6_v580.py').write_text(worker,encoding='utf-8',newline='\n')
archive=(Q5/'review_tools/archive_candy_context_fold_a5_v576.py').read_text(encoding='utf-8').replace('comparison_a5','comparison_a6').replace('CANDY-FOLD-A5','CANDY-FOLD-A6').replace('candy_local_fold_a5_active_20261003','candy_local_fold_a6_active_20261003').replace('CANDY CONTEXT FAR-FOLD A5','CANDY CONTEXT DOWNWARD FOLD A6').replace('CANDY_A5_NATIVE_ARCHIVED','CANDY_A6_NATIVE_ARCHIVED').replace('Candy contextual partial far-fold A5','Candy prompt-only downward far-fold A6')
(Q6/'review_tools/archive_candy_context_fold_a6_v580.py').write_text(archive,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,Q5/'review_tools'/Path(__file__).name)
shutil.copyfile('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/CANDY_CONTEXT_BROWSER_V578.jpg',C/'BROWSER_SOURCE_REPORT_V578.jpg')
write(C/'BROWSER_VERIFY_V578.json',dict(status='ACTUAL_DESKTOP_REPORT_SOURCE_LOADING_AND_16_OPINIONS_VERIFIED',checked_utc=now(),url='http://127.0.0.1:8880/assets_src/imagegen/candy_wrap_scene_context_v1_20261003/index.html?revision=context-a2#attempt-2',source_images=[dict(path='attempt01/native.png',loaded_dimensions=[1672,941]),dict(path='attempt02/native.png',loaded_dimensions=[1672,941])],individual_opinions=16,viewport_width=1280,document_scroll_width=1265,horizontal_overflow=False,screenshot_sha256=sha(C/'BROWSER_SOURCE_REPORT_V578.jpg'),qualification='Browser report proof only. Not ordinary gameplay, motion acceptance, device/child/owner review.'))
lim=read(C/'PRIOR_CLIP_ENTRY_LABEL_LIMITATION.json');lim['additional_inherited_label_limitations']=dict(prior_manifest='assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a4/MANIFEST.json',timeline='Inherited old far-fold/pale-mat prose differs from the actual separately hash-bound A4 prompt file.',input_visual_review='Inherited pointer names comparison_a2 despite the exact actual A13 source/input bindings. Native frame reviews inspected the actual source/input and output.',new_contract='A5/A6 fresh complete-scene entry, source and actual timeline/input review; prior published A4 bytes preserved.')
write(C/'PRIOR_CLIP_ENTRY_LABEL_LIMITATION.json',lim)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';d=read(ip)
d['scope']+=' A5 all41 native frames/10 components rejected3.1 for reverse lifting direction. One A6 prompt-only direction comparison with the same exact complete source/input/seed/settings/workflow is prepared.'
d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for base in(C,Q5,Q6) for p in base.rglob('*') if p.is_file()})
d['validation'].append(dict(command='Every41 A5 native canvases and10 separate component opinions',result='FAIL',evidence=(A/'DIRECT_REVIEW.json').relative_to(B).as_posix()+'; hand ownership4.5, far fold1.5/whole3.1 rejected. Original declared coverage/release criteria unchanged.'))
d['validation'].append(dict(command='A6 prompt-only downward fold local comparison',result='PENDING',evidence=(Q6/'MANIFEST.json').relative_to(B).as_posix()+'; no predicted score, exact same source/input/seed/settings/workflow.'))
write(ip,d)
print(json.dumps(dict(status='A5_3_1_FAILURE_REVIEWED_A6_DIRECTION_PROMPT_PREPARED',native_frames=41,components=10,new_prompt_sha256=sha(pp),same_input_sha256=sha(inp),queued=False)))
