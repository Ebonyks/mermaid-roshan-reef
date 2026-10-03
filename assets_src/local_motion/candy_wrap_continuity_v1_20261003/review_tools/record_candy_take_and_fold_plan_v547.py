from pathlib import Path
import datetime, hashlib, json, shutil

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'
A=P/'attempt01'
M=B/'assets_src/imagegen/candy_wrap_contact_v1_20261003'
IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
    task_next=p.with_name(p.name+'.v547_next')
    task_next.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    task_next.replace(p)
idx=read(A/'INDEX.json');assert len(idx['frames'])==41 and len(idx['boards'])==7
assert all(sha(B/x['path'])==x['sha256'] for x in idx['frames']+idx['boards'])
assert read(A/'RENDER_RECEIPT.json')['status']=='PASS'
archiver=P/'review_tools/archive_candy_wrap_a1_v546.py'
before=archiver.read_text(encoding='utf-8')
shutil.copyfile(archiver,P/'review_tools/archive_candy_wrap_a1_v546_before_self_copy_fix.py')
old="shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)"
assert old in before
new="if Path(__file__).resolve() != (P/'review_tools'/Path(__file__).name).resolve():shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)"
code=before.replace(old,new);compile(code,str(archiver),'exec')
task_next=archiver.with_name(archiver.name+'.v547_next');task_next.write_text(code,encoding='utf-8',newline='\n');task_next.replace(archiver)
write(P/'ARCHIVER_SELF_COPY_FAILURE_V547.json',{'status':'INITIAL_ARCHIVE_HELPER_FAILED_AFTER_COMPLETE_NATIVE_ARCHIVE','observed_process_exit':1,'error_type':'shutil.SameFileError','operation':'Unnecessary self-copy while directly launching the saved packet helper','native_render_status':'PASS','preserved_native_frames':41,'preserved_native_boards':7,'index_written_before_failure':True,'recovery':'Independently verify existing receipts,41 frame/7 board hashes and complete index. Do not rerun generator or decoder. Guard same resolved helper path and finish coverage here.','prior_helper':(P/'review_tools/archive_candy_wrap_a1_v546_before_self_copy_fix.py').relative_to(B).as_posix(),'fixed_helper':archiver.relative_to(B).as_posix(),'qualification':'Helper failure retained; this is not a failed model render or an artistic pass.'})
notes=[
'Intact opening: both mittens hold outer sheet corners and the red oval is exposed.',
'Opening contact remains; gold sheet and red oval retain the initial broad layout.',
'Head and mitten edges shift slightly; the paper remains flat under the exposed sweet.',
'Both corner grips persist with minor cloth/highlight change; no enclosing long-edge fold.',
'The supporting table remains legible while the mittens still grip the outer corners.',
'Paper center stays open; hand posture and painted highlights fluctuate without a fold.',
'Near-held corner contact continues; the original red oval remains wholly visible.',
'The sheet remains rectangular and open; no hand travels to an attached wrapper neck.',
'Torso and glove highlights shift subtly; both grips still own sheet corners.',
'Both mittens stay outside the sweet; neither long edge has closed over its belly.',
'The paper stays open despite the prescribed first fold interval nearing its end.',
'The red sweet is still exposed; no semantic fold payoff is visible.',
'Right forearm starts moving and the right corner lifts; the long sheet edges stay open.',
'Right mitten raises its outside corner and the puff sleeve changes shape; no enclosure.',
'Both elbows widen, lifting outer paper corners rather than folding long edges around the sweet.',
'Connected mittens spread outward; the open gold sheet remains under the red oval.',
'Raised corner grips widen further; no inward slide or narrow-neck formation occurs.',
'The right paper corner rises while the opposite grip stays at the outer sheet edge.',
'Both arms reach outward around an open sheet; the central sweet remains exposed.',
'Raised corners persist and the paper center remains flat; this does not pinch wrapper necks.',
'Both gloves continue holding distant corners; no contact migrates inward to the sweet.',
'Corner lifting settles slightly, but the sheet remains open and the red oval unchanged.',
'Right thumb/grip elongates along a raised corner; no enclosed belly or untwisted neck exists.',
'Hands move closer to the same outside corners; the intended counter-twist has no neck target.',
'The sheet lifts along its side corners, retaining an open rectangular center.',
'Both coral mittens still grip sheet corners; there is no opposing roll around narrow necks.',
'Lower sleeve and thumb shapes vary while the gold center remains open.',
'Same corner-held sheet persists; no attached fan/neck structure has formed.',
'Mittens draw slightly inward but remain on the outer paper; red sweet stays exposed.',
'The right outer corner flexes while the paper still lies open under the sweet.',
'Glove thumb outlines reshape; the sequence still lacks an enclosed gold oval.',
'Small inward hand motion does not create either narrow neck or a readable wrist counter-roll.',
'The paper center is still open; both hands remain outside the sweet near corners.',
'Hands begin settling at outer sheet edges, with no completed wrapper to release.',
'The right paper edge flexes; the original red oval is fully visible rather than enclosed.',
'Both glove grips remain on the sheet; no honest release of a finished sweet occurs.',
'The hands lower toward the outside corners; the sheet and exposed red oval remain.',
'End settling preserves an open sheet, not the directed wrapped-and-released result.',
'Glove/fold highlights fluctuate and faint mat artifacts persist; no wrapping payoff.',
'Both mittens still contact outer edges; no fan, neck or completed gold belly is present.',
'Final canvas ends with the original red sweet exposed on an open sheet, both gloves still holding it.'
]
assert len(notes)==41
frames=[]
for row,note in zip(idx['frames'],notes):
    i=row['index'];s=4.5 if i==0 else (4.3 if i<12 else (4.1 if i<22 else 3.9))
    frames.append(dict(**row,visual_frame_score=s,evaluation=f'Frame{i} at{row["timestamp_seconds"]:.3f}s: '+note+' Individual reference-canvas opinion only; no whole-action or current-game acceptance.',direct_native_board_review=True,full_native_detail_review=i in [13,24,40],runtime_bound=False,owner_acceptance=None))
opinions=[
('identity_style',4.4,'Painted face, hat, brown hair/rainbow ribbon and costume remain recognizable. Puff sleeves, mitten/quilt/vest highlights and a faint halo/mat artifact change during the take; no current-game style acceptance.'),
('attention',3.2,'Eyes remain broadly forward and mouth stays open; no clear sustained eyeline to the paper contact point is established.'),
('connected_mittens',4.1,'Two forearms remain connected and mittens hold paper. Late thumb/cloth shapes morph; contact stays at outer corners rather than useful long-edge/neck locations.'),
('supported_sweet',4.4,'The red oval remains supported near its starting place through the take. It stays exposed; preservation of a stationary sweet is not the wrapping action.'),
('table_and_material',4.2,'Lavender table and golden paper remain recognizable, with small edge/highlight changes and faint mat artifacts. No gross table jump like the earlier pose-key study.'),
('long_edge_fold',1.8,'No long-edge closure encloses the sweet. The local model lifts the two outer corners and leaves a rectangular gold sheet beneath a red oval through the final frame.'),
('slide_to_necks',1.8,'Mittens never travel to narrow attached wrapper necks because no enclosed belly or neck structure is formed.'),
('opposing_twist',1.5,'No opposing wrist roll tightens neck pleats. Small glove movements on a flat corner-held sheet cannot stand in for twisting.'),
('release_result',1.8,'Last frame retains both gloves on outer sheet edges and the exposed red sweet. No completed wrapper is released and inspected.'),
('whole_reference_action',2.4,'Complete41-frame take fails the required fold-slide-twist-release. Smooth corner lifting and source resemblance cannot average away the missing job verb. Rejected and unbound.')]
review={'status':'ALL41_NATIVE_FRAMES_REVIEWED_REFERENCE_ACTION_REJECTED','reviewed_utc':now(),'prompt_id':idx['prompt_id'],'native_frame_count':41,'boards_reviewed':[x['path'] for x in idx['boards']],'full_native_details':[13,24,40],'individual_frames':frames,'component_opinions':[{'item':k,'score':s,'evaluation':e,'runtime_bound':False,'owner_acceptance':None} for k,s,e in opinions],'whole_reference_action_score':2.4,'current_game_score':2.8,'prior_unbound_actual_action_score':4.1,'source_score_transfer':False,'geometry_measurements':None,'qualification':'Every41 complete native canvases directly inspected on7 non-resampled original-size boards and3 additional full-native details. Semantic action fails directly; no unmeasured geometric tolerance pass, runtime, cinematic, device, child or owner acceptance.','next_gap':'Opening mittens grip outer corners and model continues that action. Generate only the missing near-long-edge folding grip with opposite-hand support, then test an actual fold transition without pretending that a substep passes the complete wrap.'}
write(A/'DIRECT_REVIEW.json',review)
write(P/'REVIEW_STATUS.json',{'status':'MACHINE_RENDER_COMPLETE_VISUAL_REJECTED','whole_reference_action_score':2.4,'native_frames_reviewed':41,'review_path':(A/'DIRECT_REVIEW.json').relative_to(B).as_posix(),'manifest_sha256':sha(P/'MANIFEST.json'),'runtime_integration':False,'owner_approval':None})
write(P/'ARCHIVE_RECOVERY_V547.json',{'status':'PASS_ALL_EXISTING_NATIVE_ARTIFACTS_VERIFIED_NO_REGENERATION','checked_utc':now(),'prompt_id':idx['prompt_id'],'frames':41,'boards':7,'all_frame_board_hashes_match':True,'render_receipt_sha256':sha(A/'RENDER_RECEIPT.json'),'index_sha256':sha(A/'INDEX.json'),'source_original_unchanged':True,'helper_failure':'ARCHIVER_SELF_COPY_FAILURE_V547.json'})
assert not (M/'PLAN_A11.json').exists() and not (M/'attempt11').exists()
prompt='''Use case: precise-object-edit. Asset type: one transparent complete Candy Maker working pose for the existing polished painted2D game. Input image is the exact existing A7 opening cell, edit target and identity/style authority.
Change only the hand contact, necessary connected forearm bends and downward eyeline to prepare a truthful long-edge paper fold. Her left-on-screen coral quilted mitten grasps the middle-left portion of the NEAR long gold paper edge, the edge closest to the viewer, just left of the red sweet. Lift that near edge slightly toward the sweet. Her right-on-screen mitten gently braces the far-right side of the SAME sweet and paper against the SAME lavender tabletop. Two connected oven mittens, no bare fingers. Both mittens must contact the actual paper/sweet, not its two distant outer corners. The red oval remains clearly visible between the mittens and exactly the same size and location as the reference. This is the preparation for the first fold, not a finished wrapper.
Preserve this same single character, canvas proportions, forward camera, complete hair/rainbow ribbon and teal hat, face proportions, teal waistcoat/gold buttons, white puff sleeves, table outline/support and golden sheet material. Keep the original red oval center near normalized(.493,.834) and its width/height near(.182,.078); preserve tabletop and head anchors. Only the local mitten/contact/forearm/eyeline change is requested. Do not redraw the design, increase candy size, add tied necks or finished gold fans, add another pose, add extra anatomy/tail, crop anything, create a background, shadow halo, labels or grid. Genuine transparent background. Return ONE complete polished matte-to-satin storybook raster pose, not a pose sheet or vector diagram.
'''
plan={'status':'PLANNED_BEFORE_BUILTIN_IMAGEGEN','created_utc':now(),'attempt':11,'baseline':read(P/'PLAN.json')['baseline'],'gap':'All41 local A1 frames fail wrapping; existing corner grips guide lifting/flapping. No reviewed source provides a near-long-edge mitten grip with the opposite mitten bracing the same sweet for a visible folding transition.','reuse_inventory':[{'path':(P/'source_frames/CANDY-WRAP-OPEN-A7.png').relative_to(B).as_posix(),'sha256':sha(P/'source_frames/CANDY-WRAP-OPEN-A7.png'),'role':'Exact complete authored A7 opening cell, preserved edit target; no new scene.'},{'path':(A/'DIRECT_REVIEW.json').relative_to(B).as_posix(),'role':'All41 reference frames rejected2.4, complete wrap remains open.'},{'path':(M/'COMPLETE_SOURCE_REVIEW.json').relative_to(B).as_posix(),'role':'Ten prior sources and40 state opinions, including rejected A9/A10 bridge grips; originals preserved.'}],'prompt':prompt,'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'method':'builtin_imagegen_precise_object_edit','transparent_background':True,'runtime_binding':False,'native_preservation_required':True,'required_review':['Both mittens contact intended near edge and opposite sweet support','Original sweet size/position and table/head anchors conserved in normalized coordinates','Identity/style/anatomy/opacity preserved','Local fold test separate from full wrapping/runtime/owner acceptance'],'owner_acceptance':None}
write(M/'PLAN_A11.json',plan)
d=read(IP);d['scope']+=' After actual A1 rejection, regenerate one missing long-edge folding grip via builtin ImageGen; preserve exact edit target, prompt, native output and individual review before any later local fold test.'
d['files']=sorted(set(d['files'])|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()}|{(M/'PLAN_A11.json').relative_to(B).as_posix()})
d['validation'].append({'command':'All41 complete native reference frame and10 component opinions; preserved archive helper failure and independent recovery','result':'FAIL','evidence':(A/'DIRECT_REVIEW.json').relative_to(B).as_posix()+' whole2.4; '+(P/'ARCHIVER_SELF_COPY_FAILURE_V547.json').relative_to(B).as_posix()})
d['validation'].append({'command':'Verified native artifact recovery with no duplicate generation/decode','result':'PASS','evidence':(P/'ARCHIVE_RECOVERY_V547.json').relative_to(B).as_posix()})
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
d['files']=sorted(set(d['files'])|{(P/'review_tools'/Path(__file__).name).relative_to(B).as_posix()})
write(IP,d)
print(json.dumps({'native_take':'ALL41_REVIEWED_REFERENCE_REJECTED_2_4','helper_failure':'PRESERVED_RECOVERED_WITHOUT_REGENERATION','next':'A11_SPECIFIC_FOLD_GRIP_PLANNED','prompt_sha256':plan['prompt_sha256']}))
