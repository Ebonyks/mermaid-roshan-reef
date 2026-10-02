from pathlib import Path
import datetime, hashlib, json, shutil, difflib

R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
old=R/'assets_src/local_motion/day2_batch1_20260930'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
imp=read(ip)
imp['scope']+=' Prepare and run one bounded connected-palm scrubbing/attention reference study using the already-developed local ComfyUI GGUF wrapper and exact current installed workflow bytes. Whole-canvas neutral input only; no runtime/cinematic integration or score transfer. Review every generated frame before choosing a further attempt; retain failures and dispatch evidence.'
imp['validation'].append({'command':'Connected Nursery ComfyUI scrubbing reference study v1','result':'PENDING','evidence':'assets_src/local_motion/nursery_connected_scrub_v1_20261002/MANIFEST.json; existing local workflow, identity/contact/attention and full-frame review remain required.'})
write(ip,imp)  # Scope before dependent work.
assert not P.exists()
for sub in ['inputs','prompts','workflows']:(P/sub).mkdir(parents=True,exist_ok=True)
(P/'.gdignore').write_text('',encoding='utf-8')
source='assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_palm_attempt02/native.png'
bindings=[]
for x in read(old/'MANIFEST.json')['renderer']['bindings']:
    if x.get('check_installed_bytes',True):
        installed=Path(x['installed_path'])
    else:
        installed=old/x['packet_path']
    assert installed.is_file()
    destination=P/x['packet_path'];destination.parent.mkdir(exist_ok=True,parents=True)
    shutil.copyfile(installed,destination)
    bindings.append({'installed_path':str(installed),'packet_path':x['packet_path'],'sha256':sha(destination),'check_installed_bytes':True,'historical_binding_sha256':x['sha256']})
current=Path('H:/MermaidReefTools/LocalVideo/render_local.py').read_text(encoding='utf-8')
prior=(old/'workflows/render_local_current.py').read_text(encoding='utf-8')
diff=''.join(difflib.unified_diff(prior.splitlines(True),current.splitlines(True),fromfile='historical_developed_render_local',tofile='current_installed_render_local'))
(P/'workflows/CURRENT_INSTALLED_CHANGE.diff').write_text(diff,encoding='utf-8',newline='\n')
prompt='''Roshan quietly washes the far cupped palm with her near hand, keeping both wrists joined to her body and both hands touching above the basin.
0.00-0.25s: remain in the exact source contact pose; her eyes gently notice her hands.
0.25-1.20s: the near palm makes two short gentle back-and-forth rubbing strokes across the far cupped palm; a small contained patch of lather stays between the contacting palms.
1.20-1.70s: the hands settle back into the original connected contact pose; eyes stay attentive to the hands.
Keep the fixed camera, body, rainbow tail, apron, gingham sleeves, hair, basin, faucet, pedestal and neutral background unchanged. Faucet stays off. Preserve the rounded painted 2D storybook outlines, broad pastel value bands and simplified childlike anatomy. No realistic skin, clap, prayer pose, detached hand, extra limb, new object, foam explosion, camera movement, text or reward effect.
Sound: silence.
'''
(P/'prompts/NUR-SCRUB-A1.txt').write_text(prompt,encoding='utf-8',newline='\n')
gd='''extends SceneTree

func _initialize() -> void:
\tvar source: Image = Image.load_from_file("res://'''+source+'''")
\tif source == null or source.get_size() != Vector2i(1254, 1254):
\t\tquit(2)
\t\treturn
\tsource.convert(Image.FORMAT_RGBA8)
\tsource.resize(448, 448, Image.INTERPOLATE_LANCZOS)
\tvar mat: Image = Image.create(896, 512, false, Image.FORMAT_RGBA8)
\tmat.fill(Color("dfedf1"))
\tmat.blend_rect(source, Rect2i(0, 0, 448, 448), Vector2i(224, 32))
\tmat.convert(Image.FORMAT_RGB8)
\tvar error: Error = mat.save_png("res://assets_src/local_motion/nursery_connected_scrub_v1_20261002/inputs/NUR-SCRUB-A1.png")
\tprint("NUR_INPUT_NORMALIZATION|", error, "|whole-canvas uniform448, centered896x512 RGB mat")
\tquit(error)
'''
(P/'normalize_input.gd').write_text(gd,encoding='utf-8',newline='\n')
manifest={'schema':'reef.local-nursery-motion-study.v1','id':'nursery-connected-scrub-v1-20261002','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':imp['baseline'],'acceptance':'LOCAL_MOTION_REFERENCE_ONLY','owner_approval':None,'runtime_integration':False,'authorization':'Owner directed local animations through the developed ComfyUI workflow, with continuing iterative graphics and true-action review. This bounded study addresses current washing action 3.9 and attention 3.8; no new service/model/install or cinematic/game delivery method.',
'intention':'Roshan notices her hands, gently rubs the far cupped palm with the near palm, then settles while maintaining contact.',
'profile':'design/animation/ROSHAN_MOVEMENT_LANGUAGE.md','register':'Everyday attentive helping; quiet body/tail and purposeful hand effort.',
'source_path':source,'source_sha256':sha(R/source),'source_dimensions':[1254,1254],'source_status':'STATIC_SOURCE_DRAFT_4.5_OWNER_UNASSIGNED','source_review':'assets_src/imagegen/nursery_wash_connected_v1_20261002/rub_palm_attempt02/SOURCE_REVIEW.json',
'input_path':'inputs/NUR-SCRUB-A1.png','input_sha256':None,'input_transform':'Uniform entire1254-square RGBA canvas resized448 square, alpha over a flat neutral mat centered at(224,32) on896x512 RGB. No isolated art/object transform or semantic repair. Native preserved; study input is not runtime pixels.',
'prompt_path':'prompts/NUR-SCRUB-A1.txt','prompt_sha256':sha(P/'prompts/NUR-SCRUB-A1.txt'),'queue_name':'nursery_scrub_a1_20261002','seed':2026100201,
'renderer':{'server':'http://127.0.0.1:8190','root':'H:/MermaidReefTools/LocalVideo','python':read(old/'MANIFEST.json')['renderer']['python'],'entrypoint':'workflows/render_gguf.py','preset':'quick','settings':read(old/'MANIFEST.json')['renderer']['settings'],'fps':24,'bindings':bindings,'admission':'One FIFO study; native queue plus90-second quiet idle, duplicate submission protection and same-settings successful graph benchmark required. Existing developed CLI unmodified. No cancellation/restart/download/install.'},
'clip_contract':{'entry':'Near palm contacts far cupped palm; body, prop and tail fixed. Faucet off.','exit':'Same contact pose, gaze to hands; no claimed seamless loop.','duration_seconds':41/24,'timeline':prompt,'anchors':'Source-normalized spout(0.76,0.48), palm contact(0.67,0.47), basin lip(0.74,0.57), base(0.74,0.94). Measurement/control targets, not acceptance.','direction':'Existing three-quarter work view only.','events':'No gameplay/input/save/reward/effect/sound owner changes; reference-only.','interruptions':'No runtime playback. Local renderer failure stops this attempt; existing jobs never cancelled.','required_review':'All41 unchanged native frames: joined wrists, opposite-palm contact, short reciprocal strokes, down gaze, stable body/tail/material/fixtures and entry/exit. Preserve failure; no automatic score/pass from successful render.'},
'status':'INPUT_NORMALIZATION_PENDING','visual_review':None,'complete_action_score':None}
write(P/'MANIFEST.json',manifest)
for name in ['BROWSER_LIBRARY_V365.png','BROWSER_SOURCE_V365.png','BROWSER_REVIEW_V365.png','BROWSER_GEODE_WITHHELD_V365.png']:
    shutil.copyfile(Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')/name,F/name)
write(F/'BROWSER_QA_V365.json',{'status':'PASS_VISIBLE_CURRENT_REVIEW_DISPLAY','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':['Seven original source images load at1254 square; lazy final wet card loaded after focus.','27 new Nursery items found; seven use opinions sort by current mounted/action score with actual full native captures.','Room2.9, attention3.8, action3.9 remain visible priorities.','Five prior Geode use entries explicitly withhold mounted/action after shared source change.','Actual Bubble Bath1600 native viewer reaches final frame257; phase1 nextcatch and zero career stars match partial-route scope.'],'screenshots':[{'path':(F/n).relative_to(R).as_posix(),'sha256':sha(F/n)} for n in ['BROWSER_LIBRARY_V365.png','BROWSER_SOURCE_V365.png','BROWSER_REVIEW_V365.png','BROWSER_GEODE_WITHHELD_V365.png']],'note':'Browser write to the external worktree was denied; identical proof bytes staged under authorized root/tmp then copied through approved worktree file operation. No screenshot editing. This checks the review UI, not device/owner acceptance.'})
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
imp=read(ip)
for x in imp['validation']:
    if x['command']=='V34.1 mounted-preview and current-score display correction':x.update(result='PASS',evidence='audit/job_nursery_wash_connected_v1_20261002/BROWSER_QA_V365.json; exact native captures and score labels directly checked in the browser.')
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,P] for p in base.rglob('*') if p.is_file()})
write(ip,imp)
p=R/'ASSET_LICENSES.md'
with p.open('a',encoding='utf-8',newline='\n') as h:h.write('| `assets_src/local_motion/nursery_connected_scrub_v1_20261002/**` | Local ComfyUI motion reference study from exact preserved Nursery palm02 generation | Original project draft reference; inherited exact source provenance | Bound MANIFEST source/input/prompt/workflow hashes and receipts | Whole-canvas neutral study input, unchanged developed local workflow. No runtime or cinematic delivery pixels; every native generated frame requires visual review. Owner/device/child acceptance unassigned. |\n')
print('Prepared one connected Nursery scrub reference-only study, current installed binding diff and four unchanged browser proofs.')
print('Installed renderer difference:\n'+diff)
