from pathlib import Path
import datetime,hashlib,json,shutil
from PIL import Image
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=read(P/'MANIFEST.json')
input=P/d['input_path']
with Image.open(input) as im: assert im.mode=='RGB' and im.size==(896,512)
d['input_sha256']=sha(input)
d['status']='BOUND_INPUT_READY_FOR_QUIET_IDLE_DISPATCH'
d['input_visual_review']={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'Root direct native visual inspection','result':'Complete native source identity retained by technical normalization: full head/hair, both joined wrists/palms, rainbow tail, basin/faucet/pedestal visible; neutral mat does not repair the artwork.','source_score_transfer':False}
job={k:d[k] for k in ['source_path','source_sha256','input_path','input_sha256','prompt_path','prompt_sha256','queue_name','seed','owner_approval']}
job.update(id='NUR-SCRUB-A1',name='Connected palm scrubbing and attention',source_style_status=d['source_status'])
d['jobs']=[job]
write(P/'MANIFEST.json',d)
worker=(R/'tools/queue_day2_local_motion.py').read_text(encoding='utf-8')
worker=worker.replace('ROOT = Path(__file__).resolve().parents[1]','ROOT = next(p for p in Path(__file__).resolve().parents if (p / "project.godot").is_file())')
worker=worker.replace('PACKET = ROOT / "assets_src/local_motion/day2_batch1_20260930"','PACKET = ROOT / "assets_src/local_motion/nursery_connected_scrub_v1_20261002"')
worker=worker.replace('== 5','== 1',1)
line='\tassert next(j for j in data["jobs"] if j["id"] == "D2A-0446")["source_style_status"] == "OWNER_REJECTED_TOO_LIFELIKE"\n'
assert line in worker
worker=worker.replace(line,'\tassert data["jobs"][0]["id"] == "NUR-SCRUB-A1" and data["source_status"] == "STATIC_SOURCE_DRAFT_4.5_OWNER_UNASSIGNED"\n')
worker=worker.replace('ROOT / "build/day2_local_motion_active_20260930"','ROOT / "build/nursery_local_scrub_active_20261002"')
worker=worker.replace('DAY2_LOCAL_MOTION|PASS|5 exact source/input/prompt bindings; pinned installed workflow; nursery style rejection; local reference lane','NURSERY_LOCAL_MOTION|PASS|1 exact source/input/prompt binding; pinned current installed workflow; candidate static floor4.5; reference-only')
worker=worker.replace('Dispatch the Day Two study FIFO through the existing local video CLI.','Dispatch one connected Nursery scrub study through the existing local video CLI. Derived from the existing Day Two FIFO worker; exact one-job schema and repository root/defaults are the only dispatcher changes.')
dest=F/'review_tools/queue_nursery_motion_v367.py'
assert not dest.exists()
dest.write_text(worker,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
p=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(p)
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,P] for p in base.rglob('*') if p.is_file()})
write(p,imp)
print('One-job FIFO bound. It reuses quiet admission/duplicate protection and the unchanged developed CLI; it never grades or integrates output.')
