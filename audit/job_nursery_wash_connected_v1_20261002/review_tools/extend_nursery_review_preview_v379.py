from pathlib import Path
import hashlib,json,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002';P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
allowed_path=R/'tmp/v2_preview_allowed.json';allowed=set(read(allowed_path))
added={p.relative_to(R).as_posix() for root in [F,P] for p in root.rglob('*') if p.is_file()}
added.update(r['path'] for r in read(F/'doctor_dated_full_review_v1/INDEX.json')['native_details'])
for path in added:
 assert (R/path).resolve().is_relative_to(R.resolve()) and (R/path).is_file()
 assert not path.startswith(('.git/','.codex/','.claude/','.secrets/','.github/','assets/book/','assets/audio/voices/','assets/characters/friends/'))
write(allowed_path,sorted(allowed|added))
target=F/'review_tools'/Path(__file__).name;shutil.copyfile(Path(__file__),target)
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip);imp['files']=sorted(set(imp['files'])|{target.relative_to(R).as_posix()});write(ip,imp)
print('LOCAL_PREVIEW|exact new review paths available|loopback-only server unchanged|'+str(len(added-allowed))+' added paths')
