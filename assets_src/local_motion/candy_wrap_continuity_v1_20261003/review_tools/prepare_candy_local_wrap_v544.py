from pathlib import Path
import copy, datetime, hashlib, json, shutil, subprocess

B = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
OLD = B / 'assets_src/local_motion/nursery_connected_scrub_v4_20261002'
P = B / 'assets_src/local_motion/candy_wrap_continuity_v1_20261003'
V = '79f20126e01454132fe245fb3b8a03e700b9ca31'
PY = 'C:/Users/Peter/AppData/Local/Python/bin/python.exe'
GODOT = 'C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
SOURCE = 'assets_src/imagegen/candy_wrap_contact_v1_20261003/attempt07/native.png'
SOURCE_SHA = '7207d74c283e6c45c61e0d453ab5c476027611065f84ce75750407875816f467'
IP = B / 'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
def update(p, raw):
    task_next = p.with_name(p.name + '.candy_v544_next')
    task_next.write_bytes(raw)
    task_next.replace(p)

assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=B).decode().strip()==V
assert subprocess.check_output(['git','branch','--show-current'],cwd=B).decode().strip()=='codex/job-art-review-v2-20261001'
assert subprocess.check_output(['git','rev-parse','origin/codex/job-art-review-v2-20261001'],cwd=B).decode().strip()==V
assert not P.exists() and not IP.exists()
assert sha(B/SOURCE)==SOURCE_SHA
ci=read(B/'audit/job_candy_workflow_current_v1_20261003/full_ci_v1/RECEIPT.json')
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and len(ci['source_checks'])==783
rows=[{'path':x['path'],'sha256':x['before_sha256']} for x in ci['source_checks']]
assert all(sha(B/x['path'])==x['sha256'] for x in rows)
old=read(OLD/'MANIFEST.json')
rules=read(OLD/'PLAN.json')['rules']+['DL-MOT-02','DL-MOT-07','DL-VIS-01','DL-VIS-02','DL-VIS-03','DL-VIS-04','DL-VIS-05','DL-VIS-06','DL-VIS-07','DL-READ-01','DL-READ-02','DL-READ-03']
rules=list(dict.fromkeys(rules))
scope='Developed local ComfyUI reference study of the actual Candy Maker golden-paper fold, sliding neck grip, counter-twist and release. Reuse the complete existing A7 opening atlas cell with exact Godot region extraction and whole-cell technical model normalization. Preserve all native originals and rejected bridges; no production binding or cinematic delivery. Review every resulting native frame and register written continuity/contact/material opinions.'
P.mkdir();(P/'review_tools').mkdir();(P/'inputs').mkdir();(P/'prompts').mkdir();(P/'source_frames').mkdir();(P/'workflows').mkdir()
(P/'.gdignore').write_text('',encoding='utf-8')
plan={'status':'PLANNED_BEFORE_DERIVATION_OR_RENDER','created_utc':now(),'baseline':V,'scope':scope,'rules':rules,'findings':['MA-VIS-006','MA-PLAY-004'],'prior_turn_classification':'PROGRESS: immutable V published; all23323 anonymous remote bytes matched; complete original journal preserved in12 lossless bounded shards.','inventory':[{'path':SOURCE,'sha256':SOURCE_SHA,'region':[0,0,627,627],'role':'Complete existing authored opening cell; static contact4.5, material4.5; not continuous motion acceptance.'},{'path':'audit/job_candy_wrap_contact_runtime_v1_20261003/DIRECT_REVIEW_A5.json','role':'All412 native canvases inspected; whole4.1 rejected for pose/support snaps and entry/exit defects.'},{'path':'assets_src/imagegen/candy_wrap_contact_v1_20261003/attempt10/DIRECT_REVIEW.json','role':'All4 bridge states inspected; whole4.2 rejected, outer-fan grip and oversized belly remain.'},{'path':OLD.relative_to(B).as_posix()+'/MANIFEST.json','role':'Existing installed local model/workflow/settings/quiet-idle admission, reused byte-exact.'}],'reuse_decision':'Existing painted opening cell meets this source purpose. Exact authored-cell extraction is technical reuse; no new ImageGen redraw is needed merely to prepare the local workflow. New local frames address the confirmed missing temporal action.','gap':'Pose endpoints do not show the long-edge fold, inward mitten slide, opposing wrist rotation or honest release. Source sweet size/table anchors must not change to conceal this gap.','lane':'LOCAL_MOTION_REFERENCE_ONLY; interactive gameplay work study, not cinematic review or runtime delivery','predeclared_review':{'frames':41,'native_canvas':[896,512],'duration_seconds':41/24,'action_order':['look at sweet and fold continuous long edges','slide mittens to attached narrow untwisted necks','opposing wrist roll tightens pleats','release both necks leaving same wrapped oval supported'],'inspection_anchors':{'unit':'627x627 original authored cell coordinates, before technical whole-cell transform','original_sweet_center':[309,523],'original_sweet_size_approx':[114,49],'neck_centers_approx':[[247,523],[371,523]],'table_front_y_approx':617,'qualification':'Predeclared visual inspection targets only, not measured motion evidence or tolerance-based acceptance.'},'hard_failures':['Sweet size or table position changes','Hands grip outer fans during twist','Paper or sweet disappears/replaces instantly','Detached mittens/extra anatomy or identity drift','Premature tied rings before wrist rotation','Incomplete fold/twist/release or invented background motion']},'required_evidence':['Exact source/region/pixel equivalence, inspected technical input','Pinned installed workflow/model bytes, same-settings successful benchmark,90second quiet-idle FIFO, OS duplicate guard','One native prompt id and receipt, all41 independently decoded full canvases and per-frame written opinions','All783 current literal production members unchanged; parser/inference/import of extraction helper','Authority/coverage/2D no-regression and published-review evidence separately','No source endpoint, machine or reference score transferred to current game, device, child or owner acceptance']}
write(P/'PLAN.json',plan)
impact={'id':'job-candy-local-wrap-continuity-20261003','scope':scope,'baseline':V,'rules':rules,'findings':plan['findings'],'files':[(P/'PLAN.json').relative_to(B).as_posix()], 'validation':[{'command':'Developed local workflow and full native wrapping review','result':'PENDING','evidence':(P/'PLAN.json').relative_to(B).as_posix()}], 'acceptance_gaps':'Current in-game wrapping2.8 and prior unbound actual action4.1 remain belowfloor. This new reference is unreviewed and unbound. Exact runtime, entry/exit, interruption, two supported aspects, phone, child, owner, all-job, integration and release remain open; no cinematic delivery or blocked Nursery reference-upload/browser-status retry.'}
write(IP,impact)
write(P/'PRODUCTION_BOUNDARY.json',{'status':'ALL783_CURRENT_LITERAL_MEMBERS_MATCH_BEFORE_STUDY','checked_utc':now(),'baseline':V,'members':rows,'prior_full_ci':'audit/job_candy_workflow_current_v1_20261003/full_ci_v1/RECEIPT.json','qualification':'Exact unchanged production boundary only. Local reference work cannot inherit a visual/runtime pass.'})
helper=P/'review_tools/extract_complete_open_cell.gd'
helper.write_text('''extends SceneTree

func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	assert(args.size() == 3)
	var source: Image = Image.load_from_file(args[0])
	assert(source != null and source.get_size() == Vector2i(1254, 1254))
	var cell: Image = source.get_region(Rect2i(0, 0, 627, 627))
	assert(cell.get_size() == Vector2i(627, 627))
	assert(cell.save_png(args[1]) == OK)
	var normalized: Image = cell.duplicate()
	normalized.resize(448, 448, Image.INTERPOLATE_LANCZOS)
	var mat: Image = Image.create(896, 512, false, Image.FORMAT_RGBA8)
	mat.fill(Color("dfedf1"))
	mat.blend_rect(normalized, Rect2i(0, 0, 448, 448), Vector2i(224, 32))
	mat.convert(Image.FORMAT_RGB8)
	assert(mat.save_png(args[2]) == OK)
	print("CANDY_SOURCE_CELL|PASS|complete authored627x627 region, uniform448x448 model mat896x512")
	quit(0)
''',encoding='utf-8',newline='\n')
source_frame=P/'source_frames/CANDY-WRAP-OPEN-A7.png'
model_input=P/'inputs/CANDY-WRAP-A1.png'
proc=subprocess.run([GODOT,'--headless','--path',str(B),'--script',str(helper),'--',str(B/SOURCE),str(source_frame),str(model_input)],cwd=B,capture_output=True,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW)
(P/'EXTRACTION.stdout.log').write_bytes(proc.stdout);(P/'EXTRACTION.stderr.log').write_bytes(proc.stderr)
assert proc.returncode==0 and b'CANDY_SOURCE_CELL|PASS|' in proc.stdout
from PIL import Image
with Image.open(B/SOURCE) as original, Image.open(source_frame) as derived, Image.open(model_input) as input_image:
    assert original.mode==derived.mode=='RGBA'
    assert original.crop((0,0,627,627)).tobytes()==derived.tobytes()
    assert input_image.mode=='RGB' and input_image.size==(896,512)
write(P/'SOURCE_CELL_EQUIVALENCE.json',{'status':'PASS_LITERAL_COMPLETE_AUTHORED_CELL_PIXELS','source_path':SOURCE,'source_sha256':SOURCE_SHA,'region':[0,0,627,627],'derived_path':source_frame.relative_to(B).as_posix(),'derived_sha256':sha(source_frame),'method':'OfficialGodot4.7.2 Image.get_region exact complete authored atlas cell; independent readonly RGBA pixel equality','model_input_path':model_input.relative_to(B).as_posix(),'model_input_sha256':sha(model_input),'transform':'Whole627x627 cell uniformly normalized448x448 then placed at224,32 on896x512 dfedf1 neutral RGB mat; technical model input only. No appearance repair or isolated-subject edit.','native_preserved':True,'runtime_binding':False})
for binding in old['renderer']['bindings']:
    assert sha(OLD/binding['packet_path'])==binding['sha256']
    if binding.get('check_installed_bytes',True): assert sha(Path(binding['installed_path']))==binding['sha256']
    shutil.copyfile(OLD/binding['packet_path'], P/binding['packet_path'])
prompt='''Roshan wraps the one red oval sweet in the existing golden paper on her lavender table. Her two coral quilted oven mittens do the work continuously, with both forearms connected. She looks down at the sweet. The sweet stays on the table at the same position and retains exactly its original width and height under the wrapper.
0.0-0.55s: both mittens fold the two long golden paper edges over the red sweet, enclosing it in that same sheet. 0.55-0.90s: the mittens visibly slide inwards along the attached paper to pinch the two narrow necks immediately beside the oval; loose flared ends remain outside the grips, untwisted. 0.90-1.35s: the wrists roll in opposite directions once, tightening the paper pleats at those two necks. 1.35-1.70s: both mittens release outwards and rest beside the finished golden sweet, still supported at its original place. Do the sequence once; no loop or reversal.
Keep the painted face, hair, rainbow ribbon, teal hat/waistcoat, white sleeves and lavender table stable. Locked camera and plain pale mat. Preserve the navy/plum contours and soft painted storybook material. No extra hands, fingers, limbs, tails, new objects, ties, text, effects or background scene. Do not make the oval bigger, grip the outer fans, pre-twist the necks, dissolve the sweet, teleport the paper or wobble the table.
Sound: silence.
'''
(P/'prompts/CANDY-WRAP-A1.txt').write_text(prompt,encoding='utf-8',newline='\n')
m=copy.deepcopy(old)
job={'id':'CANDY-WRAP-A1','name':'Golden paper actual fold-slide-twist-release continuity study','source_path':SOURCE,'source_sha256':SOURCE_SHA,'input_path':'inputs/CANDY-WRAP-A1.png','input_sha256':sha(model_input),'prompt_path':'prompts/CANDY-WRAP-A1.txt','prompt_sha256':sha(P/'prompts/CANDY-WRAP-A1.txt'),'queue_name':'candy_wrap_a1_20261003','seed':2026100301,'owner_approval':None}
m.update(schema='reef.local-candy-motion-study.v1',id='candy-wrap-continuity-v1-20261003',created_utc=now(),baseline=V,authorization='Owner directed developed local ComfyUI animations and iterative job/action artwork review; one bounded local study, no external upload/new model/install/runtime or cinematic delivery.',intention=plan['predeclared_review']['action_order'],profile='design/animation/ROSHAN_MOVEMENT_LANGUAGE.md',register='Ribbon Glide quiet concentrating hand work; still support, one useful action and settle.',source_path=SOURCE,source_sha256=SOURCE_SHA,source_dimensions=[1254,1254],source_status='STATIC_SOURCE_DRAFT_4.5_OWNER_UNASSIGNED',source_review='assets_src/imagegen/candy_wrap_contact_v1_20261003/attempt07/DIRECT_REVIEW.json',source_region=[0,0,627,627],input_path=job['input_path'],input_sha256=job['input_sha256'],input_transform='Exact complete627x627 opening atlas cell, Godot whole-cell448x448 normalization on neutral896x512 RGB mat; originalRGBA cell pixels independently equal. Technical model input only.',prompt_path=job['prompt_path'],prompt_sha256=job['prompt_sha256'],queue_name=job['queue_name'],seed=job['seed'],status='BOUND_INPUT_READY_FOR_DIRECT_INPUT_REVIEW_AND_QUIET_IDLE_DISPATCH',visual_review=None,complete_action_score=None,comparison={'prior_actual_action':'audit/job_candy_wrap_contact_runtime_v1_20261003/DIRECT_REVIEW_A5.json','prior_score':4.1,'current_in_game_score':2.8,'changed':'Continuous local workflow instead of four discrete pose keys; existing painted opening reused. All rejected images and exact current sources preserved.'},jobs=[job],input_visual_review={'status':'PENDING_DIRECT_NATIVE_INPUT_INSPECTION','source_score_transfer':False})
m['clip_contract']={'entry':'Existing A7 opening cell, one red sweet on one gold sheet, supported lavender table. No current-game entry claim.','exit':'Same supported oval enclosed in golden paper; both narrow necks visibly twisted before release. No loop/seam claim.','duration_seconds':41/24,'timeline':prompt,'anchors':plan['predeclared_review']['inspection_anchors'],'direction':'Existing forward table working view only.','events':'Reference only; gameplay/input/reward/save/completion sources unchanged.','interruptions':'No runtime playback; renderer failures preserve the one attempt without cancellation/restart of existing jobs.','required_review':'Every41 full native canvases, fold continuity, neck contact through opposing wrist twist, conserved sweet/table/identity, honest release. Native still or machine pass is never full-action acceptance.'}
m.pop('input_visual_review',None)
m['input_visual_review']={'status':'PENDING_DIRECT_NATIVE_INPUT_INSPECTION','source_score_transfer':False}
write(P/'MANIFEST.json',m)
worker=OLD/'review_tools/queue_nursery_motion_a4_v422.py'
code=worker.read_text(encoding='utf-8')
changes={'nursery_connected_scrub_v4_20261002':'candy_wrap_continuity_v1_20261003','NUR-SCRUB-A4':'CANDY-WRAP-A1','build/nursery_local_scrub_a4_active_20261002':'build/candy_local_wrap_a1_active_20261003','NURSERY_LOCAL_MOTION':'CANDY_LOCAL_MOTION'}
for a,z in changes.items():
    assert a in code
    code=code.replace(a,z)
code=code.replace('Dispatch one connected Nursery scrub study','Dispatch one connected Candy wrapping study')
target=P/'review_tools/queue_candy_wrap_a1_v544.py';compile(code,str(target),'exec');target.write_text(code,encoding='utf-8',newline='\n')
write(P/'DISPATCHER_DERIVATION.json',{'source_path':worker.relative_to(B).as_posix(),'source_sha256':sha(worker),'changes':changes,'qualification':'Packet/job/check-label/isolated-state identifiers and descriptive docstring only. Benchmark,90second idle, validation, OS-held lock, prior prompt recovery and installed CLI/models remain unchanged.'})
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
attribute=b'\n# Native review-only Candy local motion packet\nassets_src/local_motion/candy_wrap_continuity_v1_20261003/** -text\n'
assert b'assets_src/local_motion/candy_wrap_continuity_v1_20261003/**' not in (B/'.gitattributes').read_bytes()
update(B/'.gitattributes',(B/'.gitattributes').read_bytes()+attribute)
license_rows='\n| `'+source_frame.relative_to(B).as_posix()+'` | Exact A7 builtin ImageGen original complete authored atlas cell | Project generated source; original/source license row preserved | `'+SOURCE+'`, SHA-256 `'+SOURCE_SHA+'` | Godot complete627x627 cell extraction only; readonly RGBA equality proven; reference-only. |\n| `'+model_input.relative_to(B).as_posix()+'` | Same complete A7 opening cell | Same source/provenance, preserved original | `'+SOURCE+'` | Whole-cell448x448 technical model normalization on896x512 neutral mat; no creative repair or runtime binding. |\n'
update(B/'ASSET_LICENSES.md',(B/'ASSET_LICENSES.md').read_bytes()+license_rows.encode('utf-8'))
files={x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()}
files.update(['.gitattributes','ASSET_LICENSES.md'])
impact['files']=sorted(files)
impact['validation'].append({'command':'OfficialGodot4.7.2 exact authored-cell extraction; readonly independent pixel equality; all783 literal current source hashes','result':'PASS','evidence':(P/'SOURCE_CELL_EQUIVALENCE.json').relative_to(B).as_posix()+'; '+(P/'PRODUCTION_BOUNDARY.json').relative_to(B).as_posix()})
write(IP,impact)
print(json.dumps({'status':'CANDY_LOCAL_STUDY_PREPARED_NOT_SUBMITTED','packet':str(P),'input':str(model_input),'source_sha256':SOURCE_SHA,'input_sha256':sha(model_input),'current_members_unchanged':783,'scoped_files':len(files)}))
