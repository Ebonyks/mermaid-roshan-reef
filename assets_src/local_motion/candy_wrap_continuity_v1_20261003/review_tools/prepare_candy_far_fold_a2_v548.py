from pathlib import Path
import copy, datetime, hashlib, json, shutil, subprocess
from PIL import Image

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'
Q=P/'comparison_a2'
M=B/'assets_src/imagegen/candy_wrap_contact_v1_20261003'
N=M/'attempt11'
IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
ORIGINAL=Path('C:/Users/Peter/.codex/generated_images/01a0f309-110a-7602-af22-f30d657bd017/exec-9a15e06a-04e8-46d8-838f-b2d2e693acb4.png')
GODOT='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
    task_next=p.with_name(p.name+'.v548_next')
    task_next.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    task_next.replace(p)
def update(p,raw):
    task_next=p.with_name(p.name+'.v548_next');task_next.write_bytes(raw);task_next.replace(p)
assert not N.exists() and not Q.exists()
assert read(P/'REVIEW_STATUS.json')['whole_reference_action_score']==2.4
plan=read(M/'PLAN_A11.json');assert plan['status']=='PLANNED_BEFORE_BUILTIN_IMAGEGEN'
N.mkdir();Q.mkdir();(Q/'review_tools').mkdir();(Q/'workflows').mkdir();(Q/'inputs').mkdir();(Q/'prompts').mkdir()
shutil.copyfile(ORIGINAL,N/'native.png');assert sha(ORIGINAL)==sha(N/'native.png')
with Image.open(N/'native.png') as im:
    assert im.mode=='RGBA' and im.size==(1254,1254)
    dimensions=list(im.size);alpha=list(im.getchannel('A').getextrema())
source={'attempt':11,'method':'builtin_imagegen_precise_object_edit','native_path':(N/'native.png').relative_to(B).as_posix(),'source_original':str(ORIGINAL),'sha256':sha(N/'native.png'),'dimensions':dimensions,'mode':'RGBA','alpha_extrema':alpha,'reference_path':plan['reuse_inventory'][0]['path'],'reference_sha256':plan['reuse_inventory'][0]['sha256'],'prompt_sha256':plan['prompt_sha256'],'prompt':plan['prompt'],'regions':[[0,0,1254,1254]],'grid':[1,1],'native_preserved':True,'runtime_ready':False,'runtime_bound':False,'owner_acceptance':None,'qualification':'One complete pose, not four quarters. Native1254-square source is outside runtime. It supplies a far-edge fold grip rather than the requested near-edge grip; alternate use is independently reviewed, no unseen motion pass.'}
write(N/'SOURCE.json',source)
review={'status':'ALTERNATE_FAR_EDGE_FOLD_SOURCE_DRAFT_4_5_NEAR_EDGE_ROLE_REJECTED','reviewed_utc':now(),'direct_native_review':True,'native_sha256':source['sha256'],'whole_source_score':4.5,'requested_near_edge_role_score':4.0,'production_binding':False,'owner_acceptance':None,'opinions':[{'item':'Connected mitten support','score':4.5,'evaluation':'Two quilted mittens remain attached to white-sleeved forearms. Screen-right mitten braces the same red sweet and paper; screen-left lifts one edge without detached hands.'},{'item':'Far long-edge folding grip','score':4.5,'evaluation':'Raised flap originates on the far long edge beside the left half of the sweet. This can prepare a far-edge fold, provided the actual transition carries that edge over the sweet.'},{'item':'Requested near long-edge grip','score':4.0,'evaluation':'Generator did not place the screen-left grip on the near edge closest to the viewer. The original requested near-edge role is not accepted. Do not relabel it as that pose.'},{'item':'Golden paper and sweet material','score':4.5,'evaluation':'The same red oval, gold creases, plum contours and lavender table remain readable. Source proportions are visually close; no measured cross-source anchor tolerance pass is claimed.'},{'item':'Identity and work attention','score':4.5,'evaluation':'Hat, brown hair/rainbow ribbon, face, waistcoat/gold buttons and sleeves remain recognizable. Eye direction is lower toward the work; static concentration only.'},{'item':'Alternate far-fold source','score':4.5,'evaluation':'Useful provisional source for the same physical wrapping workflow using the far long edge first. It is not the originally requested near-edge pose, a temporal bridge, a full wrap or in-game approval.'}],'qualification':'Original near-edge request remains failed4.0. Far-edge-first folding achieves the same wrapping purpose without a new design or invented mechanic; reuse this existing returned art for a separately declared far-fold component test. Source4.5 remains an inclusive priority and grants no action/runtime/owner pass.'}
write(N/'DIRECT_REVIEW.json',review)
(N/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Candy source A11 — far-edge fold grip</title><style>body{font:18px/1.5 system-ui;max-width:900px;margin:32px auto;padding:0 20px;background:#edf5fa;color:#25344b}img{max-width:100%;height:auto;background:#e3edf3}</style><h1>A11: far-edge folding grip</h1><p>Single preserved builtin ImageGen native. Alternate far-edge fold source4.5/5 provisional; requested near-edge grip4.0/5 rejected. No actual action or runtime/owner acceptance.</p><img src="native.png" width="1254" height="1254" alt="Connected screen-left mitten lifts the far paper edge while the other mitten braces the same sweet"><p>The actual edge differs from the requested near edge. Far-edge-first folding can perform the same wrapping workflow; the separate component test must show that specific edge enclosing the sweet.</p><p><a href="DIRECT_REVIEW.json">Every source opinion</a> · <a href="SOURCE.json">Exact prompt/reference/native provenance</a> · <a href="../../../local_motion/candy_wrap_continuity_v1_20261003/index.html">Complete local reference review</a></p></html>',encoding='utf-8',newline='\n')
old=read(P/'MANIFEST.json')
scope='One local far-long-edge folding component test using the exact returned A11 source. Original near-edge source request remains rejected; alternate far-edge grip4.5 is a provisional source-only role. Simplify the failed four-action take to one visible fold for readable motion, preserving complete wrap/neck/twist/release requirements as still open. No production binding, saved/input/reward change or cinematic delivery.'
write(Q/'PLAN.json',{'status':'PLANNED_BEFORE_MODEL_INPUT_OR_DISPATCH','created_utc':now(),'baseline':old['baseline'],'scope':scope,'findings':['MA-VIS-006','MA-PLAY-004'],'rules':read(P/'PLAN.json')['rules'],'inventory':[{'path':source['native_path'],'sha256':source['sha256'],'role':'Existing returned A11 alternate far-edge folding grip, source-only4.5; near-role4.0 rejected.'},{'path':(P/'attempt01/DIRECT_REVIEW.json').relative_to(B).as_posix(),'role':'All41 A1 frames whole2.4 rejected; corners lift but red sweet never enclosed.'}],'gap':'A1 preserves open corner grips instead of folding. Test only actual far-long-edge closure over the same supported sweet, with right mitten bracing it. This substep does not redefine success for the complete wrapping action.','predeclared_review':{'milestone':'Far long edge visibly travels over the red oval; the opposite mitten maintains support; no instant replacement or paper/sweet growth.','identity':'Head/torso/hat/face/hair/costume/table steady, two connected mittens, no new anatomy.','continuity':'Inspect all41 native frames and actual edge path, not only the ending.','whole_wrap':'Neck slide, counter-roll, honest release and current-game fitting remain separately required.'}})
helper=Q/'review_tools/normalize_complete_fold_source.gd'
helper.write_text('''extends SceneTree

func _initialize() -> void:
	var args: PackedStringArray = OS.get_cmdline_user_args()
	assert(args.size() == 2)
	var source: Image = Image.load_from_file(args[0])
	assert(source != null and source.get_size() == Vector2i(1254, 1254))
	var normalized: Image = source.duplicate()
	normalized.resize(448, 448, Image.INTERPOLATE_LANCZOS)
	var mat: Image = Image.create(896, 512, false, Image.FORMAT_RGBA8)
	mat.fill(Color("dfedf1"))
	mat.blend_rect(normalized, Rect2i(0, 0, 448, 448), Vector2i(224, 32))
	mat.convert(Image.FORMAT_RGB8)
	assert(mat.save_png(args[1]) == OK)
	print("CANDY_FOLD_INPUT|PASS|whole1254x1254 source uniformly448x448 on896x512 model mat")
	quit(0)
''',encoding='utf-8',newline='\n')
model_input=Q/'inputs/CANDY-FOLD-A2.png'
proc=subprocess.run([GODOT,'--headless','--path',str(B),'--script',str(helper),'--',str(N/'native.png'),str(model_input)],cwd=B,capture_output=True,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW)
(Q/'NORMALIZATION.stdout.log').write_bytes(proc.stdout);(Q/'NORMALIZATION.stderr.log').write_bytes(proc.stderr)
assert proc.returncode==0 and b'CANDY_FOLD_INPUT|PASS|' in proc.stdout
prompt='''Roshan folds the FAR long golden-paper edge over the same red oval sweet. Her screen-left coral oven mitten already grips that raised edge between her body and the sweet: it brings the edge forwards and down, across the sweet. Her screen-right mitten stays beside the sweet to brace it on the lavender table. Show the paper bend continuously around the oval; by the end the red sweet is covered by that gold flap. The near paper edge still rests on the table. One deliberate fold only.
Keep the sweet exactly the same size and place. Keep two quilted mittens connected to her arms, and keep the painted face, hat, hair/rainbow ribbon, sleeves, waistcoat and table stable. Eyes attend to the contact. Locked camera and pale mat. No corner flapping, tied necks, twists, release, growth, disappearance, new fingers/objects, glow, text or background.
Sound: silence.
'''
(Q/'prompts/CANDY-FOLD-A2.txt').write_text(prompt,encoding='utf-8',newline='\n')
for binding in old['renderer']['bindings']:
    assert sha(P/binding['packet_path'])==binding['sha256']
    if binding.get('check_installed_bytes',True):assert sha(Path(binding['installed_path']))==binding['sha256']
    shutil.copyfile(P/binding['packet_path'],Q/binding['packet_path'])
job={'id':'CANDY-FOLD-A2','name':'Far long-edge fold component','source_path':source['native_path'],'source_sha256':source['sha256'],'input_path':'inputs/CANDY-FOLD-A2.png','input_sha256':sha(model_input),'prompt_path':'prompts/CANDY-FOLD-A2.txt','prompt_sha256':sha(Q/'prompts/CANDY-FOLD-A2.txt'),'queue_name':'candy_far_fold_a2_20261003','seed':old['seed'],'owner_approval':None}
m=copy.deepcopy(old);m.update(id='candy-far-fold-a2-20261003',created_utc=now(),source_path=job['source_path'],source_sha256=job['source_sha256'],source_dimensions=dimensions,source_review=(N/'DIRECT_REVIEW.json').relative_to(B).as_posix(),source_region=[0,0,1254,1254],input_path=job['input_path'],input_sha256=job['input_sha256'],input_transform='Whole new1254x1254 source uniformly448x448 on same896x512 neutral RGB mat. No crop/subject repair. Preserved original native.',prompt_path=job['prompt_path'],prompt_sha256=job['prompt_sha256'],queue_name=job['queue_name'],intention='Far long edge closes over the same supported red oval; one component of complete wrapping.',comparison={'prior_take':(P/'attempt01/DIRECT_REVIEW.json').relative_to(B).as_posix(),'changed':'Source grip plus action prompt: exact A11 alternate far-edge pose and one fold instead of four-action corner-held take. Not a prompt-only comparison.','preserved':'Seed2026100301,896x512/41frames/24steps GGUF model/workflow/benchmark/90second quiet-idle/duplicate guard; all783 current source bytes.','whole_wrap_acceptance':False},jobs=[job],status='BOUND_FAR_FOLD_INPUT_PENDING_DIRECT_REVIEW',visual_review=None,complete_action_score=None,input_visual_review={'status':'PENDING_DIRECT_NATIVE_INPUT_INSPECTION','source_score_transfer':False})
m['clip_contract']={'entry':'A11 alternate far-edge grip with screen-right mitten bracing the same sweet; no actual game entry proof.','exit':'Far flap closes continuously over original red oval; near edge still rests. Neck/twist/release are not attempted and remain required for full wrap.','duration_seconds':41/24,'timeline':prompt,'anchors':{'unit':'1254x1254 complete source normalized coordinates','sweet_center_approx':[0.503,0.821],'sweet_size_approx':[0.185,0.09],'qualification':'Visual inspection targets only; no measured motion tolerance pass.'},'direction':'Forward table work view.','events':'Reference-only; inherited gameplay owners unchanged.','interruptions':'No runtime playback; one guarded local renderer job, no duplicate/cancel/restart.','required_review':'All41 full native canvases, far-edge origin/continuous bend/cover, steady sweet and support, connected mittens/style/identity. Component score cannot pass full wrapping/current game.'}
write(Q/'MANIFEST.json',m)
worker=P/'review_tools/queue_candy_wrap_a1_v544.py';code=worker.read_text(encoding='utf-8')
changes={'PACKET = ROOT / "assets_src/local_motion/candy_wrap_continuity_v1_20261003"':'PACKET = ROOT / "assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a2"','CANDY-WRAP-A1':'CANDY-FOLD-A2','build/candy_local_wrap_a1_active_20261003':'build/candy_local_fold_a2_active_20261003'}
for a,z in changes.items():assert a in code;code=code.replace(a,z)
target=Q/'review_tools/queue_candy_far_fold_a2_v548.py';compile(code,str(target),'exec');target.write_text(code,encoding='utf-8',newline='\n')
write(Q/'DISPATCHER_DERIVATION.json',{'source_path':worker.relative_to(B).as_posix(),'source_sha256':sha(worker),'changes':changes,'qualification':'Identifiers/packet/state only; admission and installed CLI unchanged.'})
archive=P/'review_tools/archive_candy_wrap_a1_v546.py';code=archive.read_text(encoding='utf-8')
changes={'P=R/\'assets_src/local_motion/candy_wrap_continuity_v1_20261003\'':'P=R/\'assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a2\'','candy_local_wrap_a1_active_20261003':'candy_local_fold_a2_active_20261003','CANDY-WRAP-A1':'CANDY-FOLD-A2','CANDY FOLD-SLIDE-TWIST-RELEASE A1':'CANDY FAR LONG-EDGE FOLD A2','CANDY_A1_NATIVE_ARCHIVED':'CANDY_A2_NATIVE_ARCHIVED'}
for a,z in changes.items():assert a in code;code=code.replace(a,z)
target=Q/'review_tools/archive_candy_far_fold_a2_v548.py';compile(code,str(target),'exec');target.write_text(code,encoding='utf-8',newline='\n')
write(Q/'ARCHIVER_DERIVATION.json',{'source_path':archive.relative_to(B).as_posix(),'source_sha256':sha(archive),'changes':changes,'qualification':'Only packet/job/state/board labels; same path containment, exact output hash, direct decoding and guarded helper self-copy.'})
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
license_rows='\n| `'+source['native_path']+'` | Builtin ImageGen precise contact edit of exact A7 opening cell | OpenAI generated project artwork; original source/provenance preserved | Prompt/reference/native hashes in attempt11/SOURCE.json | New single complete pose. Requested near-edge role4.0 rejected; alternate far-fold still4.5 provisional, unbound. |\n| `'+model_input.relative_to(B).as_posix()+'` | Same preserved complete A11 native | Same project source/provenance | attempt11/SOURCE.json | Uniform whole-canvas technical448x448 normalization on896x512 neutral mat; reference-only. |\n'
update(B/'ASSET_LICENSES.md',(B/'ASSET_LICENSES.md').read_bytes()+license_rows.encode('utf-8'))
d=read(IP);d['scope']+=' Preserve the returned A11 near-role failure4.0 and provisional alternate far-fold source4.5. Test far-edge closure as a substep with changed source/prompt and unchanged seed/settings, keeping full wrapping requirements open.'
d['files']=sorted(set(d['files'])|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()}|{x.relative_to(B).as_posix() for x in N.rglob('*') if x.is_file()})
d['validation'].append({'command':'Direct complete builtin ImageGen A11 native review and exact native preservation','result':'PASS','evidence':(N/'DIRECT_REVIEW.json').relative_to(B).as_posix()+' alternate far-fold source4.5; requested near role4.0 rejected, no motion acceptance.'})
d['validation'].append({'command':'Far-long-edge actual component reference motion','result':'PENDING','evidence':(Q/'PLAN.json').relative_to(B).as_posix()})
write(IP,d)
print(json.dumps({'native':source['native_path'],'sha256':source['sha256'],'size':dimensions,'alternate_source_score':4.5,'near_request_score':4.0,'model_input':str(model_input),'status':'A2_PREPARED_NOT_DISPATCHED','covered_files':len(d['files'])}))
