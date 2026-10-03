from pathlib import Path
import copy,datetime,hashlib,json,os,shutil,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
OLD=R/'assets_src/local_motion/nursery_connected_scrub_v2_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v3_20261002'
S=R/'assets_src/imagegen/nursery_scrub_attention_fresh_v1_20261002/attempt02'
ip=R/'design/audit_impacts/job-nursery-scrub-fresh-a3-20261002.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
pub=read(R/'tmp/scannable_job_review_r_publish_v415/RECEIPT.json')
BASE=pub['revision'];assert pub['status']=='TOPIC_CANDIDATE_PUBLISHED_REMOTE_VERIFICATION_PENDING'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],cwd=R).decode().strip()=='codex/job-art-review-v2-20261001'
subprocess.run(['git','fetch','origin','codex/job-art-review-v2-20261001'],cwd=R,check=True,capture_output=True)
assert subprocess.check_output(['git','rev-parse','origin/codex/job-art-review-v2-20261001'],cwd=R).decode().strip()==BASE
assert read(OLD/'REVIEW_STATUS.json')['status']=='MACHINE_RENDER_COMPLETE_VISUAL_REJECTED'
assert sha(S/'native.png')=='19782bdf6092388bd23cd29306559d6afbbf5986e449369057b72279e31187a2'
assert read(S/'SOURCE_REVIEW.json')['whole_source_score']==4.5
assert not P.exists() and not ip.exists()
P.mkdir();(P/'review_tools').mkdir();(P/'.gdignore').write_text('',encoding='utf-8')
rules=read(OLD/'PLAN.json')['rules']
plan=dict(status='PLANNED_BEFORE_NORMALIZATION_OR_RENDER',baseline=BASE,created_utc=now(),scope='One bounded local source-only A3 Nursery reciprocal scrub comparison. Reuse freshly generated unbound down-gaze A2 still, preserve exact A2 rub prompt/seed/settings/developed workflow. Whole-canvas technical input normalization only, no isolated art repair. Existing old-source upload remains blocked; nothing leaves this computer. Preserve all failed takes, native frames and receipts; no production/runtime/cinematic binding.',rules=rules,findings=['MA-VIS-006','MA-PLAY-004'],gap='Old-source A2 holds its palms instead of two reciprocal strokes (2.8/action3.0) and gaze remains away (3.1). Fresh source down-gaze4.6 and clearer low palms4.5 provide a named source change; source success does not prove motion.',inventory=[dict(path=OLD.relative_to(R).as_posix()+'/attempt01/DIRECT_REVIEW.json',role='All41 failed A2 reference frames; preserved, excluded as accepted motion'),dict(path=S.relative_to(R).as_posix()+'/native.png',sha256=sha(S/'native.png'),role='New text-only source provisionally4.5/down-gaze4.6, unbound, reused without external upload'),dict(path='audit/job_nursery_wash_connected_v1_20261002/DIRECT_REVIEW_CURRENT_V3.json',role='Current game wash3.9/attention3.8 remains separate')],required_evidence=['Fresh native unchanged/source-only prompt/settings/seed/workflow comparison','Whole-canvas RGB mat transform and native source hashes','Existing benchmark and90second quiet-idle single FIFO admission; no duplicate/restart/cancel/install','Native receipt and every41 direct decoded original frame review, motion/contact/material/gaze/entry-exit separately','All783 current production boundary literal unchanged','Mandatory authority/coverage/2D gates and exact durable anonymous publication; no owner/device/child/all-job claim'])
write(P/'PLAN.json',plan)
write(ip,dict(id='job-nursery-scrub-fresh-a3-20261002',scope=plan['scope'],baseline=BASE,rules=rules,findings=plan['findings'],files=[(P/'PLAN.json').relative_to(R).as_posix()],validation=[dict(command='Local fresh-source Nursery reciprocal scrub A3 and all41 native-frame review',result='PENDING',evidence=P.relative_to(R).as_posix()+'/PLAN.json')],acceptance_gaps='Fresh source still4.5/gaze4.6 is unbound; A1/A2 action failures retained. Existing game wash3.9/attention3.8 and all production bytes unchanged. Local video is motion reference, never runtime/cinematic pixels. All41 native visual review, actual complete action/ordinary routes, device/child/owner/comprehensive/integration/release acceptance and both pending explicit approvals remain separate.'))
for sub in ('inputs','prompts','workflows'):(P/sub).mkdir()
m=copy.deepcopy(read(OLD/'MANIFEST.json'))
for x in m['renderer']['bindings']:
 assert sha(OLD/x['packet_path'])==x['sha256']==sha(Path(x['installed_path']))
 target=P/x['packet_path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(OLD/x['packet_path'],target)
source=(S/'native.png').relative_to(R).as_posix()
gd='''extends SceneTree

func _initialize() -> void:
\tvar source: Image = Image.load_from_file("res://SOURCE")
\tif source == null or source.get_size() != Vector2i(1230, 1278):
\t\tquit(2)
\t\treturn
\tsource.convert(Image.FORMAT_RGBA8)
\tsource.resize(431, 448, Image.INTERPOLATE_LANCZOS)
\tvar mat: Image = Image.create(896, 512, false, Image.FORMAT_RGBA8)
\tmat.fill(Color("dfedf1"))
\tmat.blend_rect(source, Rect2i(0, 0, 431, 448), Vector2i(232, 32))
\tmat.convert(Image.FORMAT_RGB8)
\tvar error: Error = mat.save_png("res://OUTPUT")
\tprint("NUR_A3_INPUT|", error, "|whole-canvas431x448 centered896x512 RGB mat")
\tquit(error)
'''.replace('SOURCE',source).replace('OUTPUT',(P/'inputs/NUR-SCRUB-A3.png').relative_to(R).as_posix())
(P/'NORMALIZE_INPUT.gd.source.txt').write_text(gd,encoding='utf-8',newline='\n')
build=R/'build/nur_a3_normalize_v416';assert not build.exists();build.mkdir()
script=build/'normalize.gd';script.write_text(gd,encoding='utf-8',newline='\n')
env=os.environ.copy();env['APPDATA']=str(build/'Roaming');env['LOCALAPPDATA']=str(build/'Local')
engine='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
cmd=[engine,'--headless','--path',str(R),'-s',str(script)]
out=subprocess.run(cmd,cwd=R,env=env,capture_output=True,timeout=120,creationflags=subprocess.CREATE_NO_WINDOW)
(P/'NORMALIZE_INPUT.stdout.log').write_bytes(out.stdout);(P/'NORMALIZE_INPUT.stderr.log').write_bytes(out.stderr)
write(P/'NORMALIZE_INPUT.receipt.json',dict(status='PASS' if out.returncode==0 else 'FAIL_PRESERVED',command=cmd,process_exit=out.returncode,source_path=source,source_sha256=sha(S/'native.png'),script_sha256=sha(script),stdout_sha256=sha(P/'NORMALIZE_INPUT.stdout.log'),stderr_sha256=sha(P/'NORMALIZE_INPUT.stderr.log'),transform='Entire1230x1278 RGBA canvas normalized431x448 preserving ratio to nearest pixel, over the same flat dfedf1 mat centered232,32 on896x512 RGB. No source pixel edit/crop/isolated-subject transform. Native preserved. Technical model input only, not runtime/delivery art.',checked_utc=now()))
assert out.returncode==0,out.stderr.decode(errors='replace')[-1000:]
shutil.copyfile(OLD/m['prompt_path'],P/'prompts/NUR-SCRUB-A3.txt')
m.update(id='nursery-connected-scrub-v3-20261002',baseline=BASE,created_utc=now(),source_path=source,source_sha256=sha(S/'native.png'),source_dimensions=[1230,1278],source_review=(S/'SOURCE_REVIEW.json').relative_to(R).as_posix(),source_status='STATIC_SOURCE_DRAFT_4.5_OWNER_UNASSIGNED',input_path='inputs/NUR-SCRUB-A3.png',input_sha256=sha(P/'inputs/NUR-SCRUB-A3.png'),input_transform=read(P/'NORMALIZE_INPUT.receipt.json')['transform'],prompt_path='prompts/NUR-SCRUB-A3.txt',prompt_sha256=sha(P/'prompts/NUR-SCRUB-A3.txt'),queue_name='nursery_scrub_a3_20261002',status='BOUND_INPUT_READY_FOR_QUIET_IDLE_DISPATCH',visual_review=None,complete_action_score=None,intention='Use the fresh naturally attentive source for the same two short reciprocal low palm-rubbing strokes and return. Source change only; down gaze is already present.',comparison=dict(prior_manifest=OLD.relative_to(R).as_posix()+'/MANIFEST.json',prior_review=OLD.relative_to(R).as_posix()+'/attempt01/DIRECT_REVIEW.json',changed='Fresh text-only A2 source and necessary same-family whole-canvas technical input. No crop or subject pixel repair.',preserved='Exact rub prompt bytes, seed2026100201, settings896x512/41frames/24steps, developed installed workflow/model bytes. All previous originals, native outputs, scores and failures unchanged.'))
assert m['prompt_sha256']==read(OLD/'MANIFEST.json')['prompt_sha256']
m['clip_contract'].update(entry='Fresh low joined palms and down gaze; faucet off, no claimed current-game entry.',exit='Same down gaze/low contact, no seamless-loop claim.',anchors='Fresh source normalized approximate control targets: palm contact(0.67,0.53), spout(0.80,0.49), basin lip(0.76,0.56), support base(0.76,0.95). Source-only inspection targets, not measured socket/motion acceptance.',required_review='Every41 native whole canvas: two reciprocal sliding strokes across opposite cupped palm, continuously joined arms, down gaze, off tap, contained lather, stable hair/costume/rainbow tail/fixture/support and entry-exit. No progress award or accepted runtime/cinematic motion from rendering success.')
m['jobs'][0].update(id='NUR-SCRUB-A3',name='Fresh attentive source reciprocal scrub comparison',source_path=m['source_path'],source_sha256=m['source_sha256'],source_dimensions=m['source_dimensions'],input_path=m['input_path'],input_sha256=m['input_sha256'],prompt_path=m['prompt_path'],prompt_sha256=m['prompt_sha256'],queue_name=m['queue_name'])
write(P/'MANIFEST.json',m)
worker=OLD/'review_tools/queue_nursery_motion_a2_v401.py';text=worker.read_text(encoding='utf-8')
changes={'nursery_connected_scrub_v2_20261002':'nursery_connected_scrub_v3_20261002','NUR-SCRUB-A2':'NUR-SCRUB-A3','build/nursery_local_scrub_a2_active_20261002':'build/nursery_local_scrub_a3_active_20261002'}
for a,b in changes.items():assert a in text;text=text.replace(a,b)
target=P/'review_tools/queue_nursery_motion_a3_v416.py';compile(text,str(target),'exec');target.write_text(text,encoding='utf-8',newline='\n')
write(P/'DISPATCHER_DERIVATION.json',dict(source_path=worker.relative_to(R).as_posix(),source_sha256=sha(worker),changes=changes,qualification='Only packet path/job identity/isolated state directory changed. Benchmark, quiet-idle, duplicate prevention and installed CLI/workflows unchanged.'))
write(P/'SOURCE_COMPARISON.json',dict(status='PASS_SOURCE_ONLY_COMPARISON_READY',prior_source_sha256=read(OLD/'MANIFEST.json')['source_sha256'],new_source_sha256=m['source_sha256'],prompt_identical=True,prompt_sha256=m['prompt_sha256'],seed=m['seed'],settings=m['renderer']['settings'],installed_workflow_unchanged=True,native_source_unchanged=True,reference_uploaded=False,runtime_integration=False,source_static_floor=4.5,current_game_action_score=3.9,qualification='No motion score assigned before review. Whole-canvas normalization is technical input only.'))
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
attrs=R/'.gitattributes';attrs.write_bytes(attrs.read_bytes()+b'\nassets_src/local_motion/nursery_connected_scrub_v3_20261002/** -text\n')
licenses=R/'ASSET_LICENSES.md';licenses.write_bytes(licenses.read_bytes()+b'\n| `assets_src/local_motion/nursery_connected_scrub_v3_20261002/**` | Existing developed local ComfyUI source-only A3 reference using new text-only attentive Nursery native | Original project source; exact provenance inherited from fresh source manifest | Exact native source/input/prompt/workflow/receipt hashes | Whole-canvas technical RGB input only; prompt/seed/settings/workflow unchanged from rejected A2. All41 frames require individual review. Non-runtime motion reference; no external upload or cinematic delivery. |\n')
note='Fresh-source Nursery A3 continuation (2026-10-02): [one bounded local source-only motion comparison](../assets_src/local_motion/nursery_connected_scrub_v3_20261002/index.html) reuses the new text-only attentive A2 native (unbound still4.5/gaze4.6) with identical rub prompt, seed, admitted settings and developed workflow. All41 native frames pending independent review; old A1/A2 failures and current game wash3.9/attention3.8 remain. Whole-canvas technical input only, no blocked old-reference upload, runtime/cinematic/device/child/owner/all-job acceptance. [Impact](../design/audit_impacts/job-nursery-scrub-fresh-a3-20261002.json).'
master=R/'audit/MASTER_AUDIT_2026-08-09.md';raw=master.read_text(encoding='utf-8');raw=raw.replace('## 0. Planning entry\n','## 0. Planning entry\n\n'+note+'\n',1).replace('### Development task index\n','### Development task index\n\n'+note+'\n',1);master.write_text(raw,encoding='utf-8',newline='\n')
ledger=R/'design/05_DOC_LEDGER.md';ledger.write_bytes(ledger.read_bytes()+b'\n| `assets_src/local_motion/nursery_connected_scrub_v3_20261002/index.html` | '+ '🟣'.encode()+b' | `CANDIDATE_REFERENCE_ONLY`; fresh attentive text-only A2 source reused locally; same rub prompt/seed/admitted settings/developed workflow as rejected old-source A2. Whole-canvas technical input only. All41 native frames pending direct review; current production/action3.9/attention3.8 unchanged. No external reference upload/runtime/cinematic/device/child/owner/all-job acceptance. |\n')
(P/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Fresh-source Nursery scrub A3</title><style>body{font:18px system-ui;max-width:1100px;margin:36px auto;padding:0 20px;background:#f1f5fa;color:#253449}img{width:100%;height:auto}</style><h1>Fresh-source Nursery scrub A3</h1><p>One bounded local source-only motion comparison. The fresh downward-looking painting is provisionally4.5 as a still, gaze4.6. Rub prompt, seed, admitted settings and developed local workflow remain identical to rejected A2.</p><img src="inputs/NUR-SCRUB-A3.png" width="896" height="512" alt="Whole-canvas technical model input; fresh attentive Nursery source on neutral mat"><p>Rendering/all41 individual native-frame motion reviews are pending. Current game wash3.9/attention3.8 unchanged. No runtime, cinematic, device, child, owner or all-job acceptance; no existing reference leaves the computer.</p><p><a href="MANIFEST.json">Exact bound manifest</a> · <a href="SOURCE_COMPARISON.json">Source-only comparison</a> · <a href="../nursery_connected_scrub_v2_20261002/index.html">Preserved rejected A2/all41 frames</a></p></html>',encoding='utf-8',newline='\n')
d=read(ip);d['files']=sorted({x.relative_to(R).as_posix() for x in P.rglob('*') if x.is_file()}|{'.gitattributes','ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','design/05_DOC_LEDGER.md'});d['validation'].append(dict(command='Whole-canvas Godot4.7.2 technical source-only input and exact prompt/settings/workflow comparison',result='PASS',evidence=(P/'NORMALIZE_INPUT.receipt.json').relative_to(R).as_posix()+'; '+(P/'SOURCE_COMPARISON.json').relative_to(R).as_posix()));write(ip,d)
print('NURSERY_A3_SOURCE_ONLY_READY|new attentive native reused locally|same prompt/seed/settings/workflow|external uploads false|render/visual pending')
