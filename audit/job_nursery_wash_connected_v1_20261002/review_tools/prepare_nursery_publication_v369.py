from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,html
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
imp=read(ip)
state=read(R/'build/nursery_local_scrub_active_20261002/STATE.json')
assert state['jobs'][0]['native_prompt_id']
write(P/'DISPATCH_SNAPSHOT_V1.json',state)
native=Path(state['jobs'][0]['receipt_path'])
shutil.copyfile(native,P/'RENDER_RUNNING_SNAPSHOT_V1.json')
shutil.copyfile(native.with_name('workflow.api.json'),P/'workflow_submitted_a1.api.json')
write(P/'DISPATCH_RECEIPT.json',{'status':'SUBMITTED_NATIVE_REFERENCE_STUDY','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prompt_id':state['jobs'][0]['native_prompt_id'],'queue_name':state['jobs'][0]['name'],'manifest_sha256':sha(P/'MANIFEST.json'),'native_receipt':str(native),'submitted_graph_sha256':sha(P/'workflow_submitted_a1.api.json'),'qualification':'Exact single local native submission after successful same-profile benchmark and90-second quiet queue admission. Running is not successful render, visual review, runtime integration or owner acceptance. Live worker remains under ignored build; dated snapshots are preserved.'})
body='''<!doctype html><meta charset="utf-8"><title>Nursery connected scrub — local motion study</title><style>body{font:18px/1.55 system-ui;background:#edf5fa;color:#263552;max-width:1000px;margin:30px auto;padding:24px}img,video{max-width:100%}article{background:white;border-radius:20px;padding:24px}code{overflow-wrap:anywhere}a{color:#4b467d}</style><article><a href="../../../audit/job_nursery_wash_connected_v1_20261002/index.html">Current Nursery game review</a><h1>Connected palm scrubbing and attention</h1><p>One bounded local ComfyUI study has been submitted through the developed workflow. It tests two gentle rubbing strokes with joined wrists, true opposite-palm contact and attention to the hands. The preserved palm02 source meets the provisional static 4.5 floor; current complete gameplay washing remains 3.9 and attention 3.8.</p><p><strong>Motion reference only.</strong> This study has no runtime, cinematic delivery or owner acceptance. Review every generated frame before using it as movement direction; a render receipt alone grants no visual score.</p><img src="inputs/NUR-SCRUB-A1.png" alt="Whole source on a neutral study input mat"><p><a href="MANIFEST.json">Bound source, prompt, workflow and clip contract</a> · <a href="prompts/NUR-SCRUB-A1.txt">Exact timeline prompt</a> · <a href="DISPATCH_RECEIPT.json">Native dispatch evidence</a> · <a href="workflow_submitted_a1.api.json">Actual submitted graph</a></p><p>Current render and frame review pending. All failed attempts will remain available.</p></article>'''
(P/'index.html').write_text(body,encoding='utf-8',newline='\n')
p=F/'index.html';s=p.read_text(encoding='utf-8');link='<section id="motion-study"><h2>Next movement study</h2><p>A bounded <a href="../../assets_src/local_motion/nursery_connected_scrub_v1_20261002/index.html">connected-palm scrubbing and attention study</a> is submitted through the developed local ComfyUI workflow. Motion reference only; every native frame still needs review. Current gameplay action 3.9 and attention 3.8 are unchanged.</p></section>'
assert 'id="motion-study"' not in s
s=s.replace('</body>',link+'</body>') if '</body>' in s else s+link
p.write_text(s,encoding='utf-8',newline='\n')
p=R/'design/05_DOC_LEDGER.md'
with p.open('a',encoding='utf-8',newline='\n') as h:h.write('| `assets_src/local_motion/nursery_connected_scrub_v1_20261002/index.html` | 🟣 | `CANDIDATE_REFERENCE_STUDY`; one exact native ComfyUI submission through the unchanged developed GGUF workflow, current installation/input/prompt hashes and quiet admission bound. Tests connected palm strokes and attentive gaze; native output/frame review pending. Static floor does not transfer to motion or current gameplay. No runtime/cinematic/device/child/owner acceptance. |\n')
p=R/'.gitattributes'
with p.open('a',encoding='utf-8',newline='\n') as h:
    h.write('audit/job_nursery_wash_connected_v1_20261002/** -text\nassets_src/imagegen/nursery_wash_connected_v1_20261002/** -text\nassets_src/local_motion/nursery_connected_scrub_v1_20261002/** -text\n')
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,P] for p in base.rglob('*') if p.is_file()})
write(ip,imp)
write(R/'tmp/v2_preview_allowed.json',sorted(set(read(R/'tmp/v2_preview_allowed.json'))|set(imp['files'])))
prior=read(R/'audit/job_review_v2_20261001/GEOLOGY_SUPPORTED_GEODE_SUPPLEMENT_FILES_V11.json')
print(json.dumps({'impact_files':len(imp['files']),'bytes':sum((R/p).stat().st_size for p in imp['files'] if (R/p).is_file()),'prior_map_files':len(prior['files']),'prior_map_unchanged':len(prior.get('unchanged_required_files',{})),'submission':state['jobs'][0]['native_prompt_id']}))
