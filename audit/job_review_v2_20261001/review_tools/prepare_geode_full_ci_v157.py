from pathlib import Path
import json, shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
impact=r/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
d=json.loads(impact.read_text(encoding='utf-8'))
folder=r/'audit/job_geode_runtime_v1_20261001/review_tools';folder.mkdir(exist_ok=False)
target=folder/'run_geode_full_ci_v1.py'
d['files']=sorted(set(d['files'])|{target.relative_to(r).as_posix(),'audit/job_review_v2_20261001/review_tools/prepare_geode_full_ci_v157.py'})
impact.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
s=(r/'audit/job_review_v2_20261001/review_tools/run_v2_full_ci_retry_v2.py').read_text(encoding='utf-8')
s=s.replace("family=root/'audit/job_review_v2_20261001'","family=root/'audit/job_geode_runtime_v1_20261001'")
s=s.replace("folder=family/'full_ci_candidate_retry_v2'","folder=family/'full_ci_v1'")
s=s.replace('job-review-separate-v2-20261001.json','job-geode-painted-runtime-20261001.json')
s=s.replace('audit/job_review_v2_20261001/full_ci_candidate_retry_v2','audit/job_geode_runtime_v1_20261001/full_ci_v1')
s=s.replace(" write(folder/'SOURCE_BEFORE.json'", " paths.update(['scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','tools/capture_geode_runtime_route.gd','tools/capture_geode_runtime_route.gd.uid'])\n paths.update('assets/opera/worlds/geology/painted_geode_v1_20261001/'+name+suffix for name in ['closed.png','early_crack.png','middle_open.png','open_embedded.png'] for suffix in ['', '.import'])\n write(folder/'SOURCE_BEFORE.json'",1)
s=s.replace('Prior full299-file production boundary plus current pool resources/tools and approved character source family; source hashes bind this local run, not a hosted commit or creative acceptance.','Fresh current local production boundary includes the actual painted geode and visible celebration-rest repair plus current pool/boxing/character family. All current literal bytes frozen; inheritedG suite does not establish this new result. No hosted/creative acceptance.')
s=s.replace('Official Godot4.7.2 unmodified distinctV2 full retry2 scripts/ci.sh','Official Godot4.7.2 unmodified painted-geode production full suite1 scripts/ci.sh')
target.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),r/'audit/job_review_v2_20261001/review_tools/prepare_geode_full_ci_v157.py')
print('Prepared source-bound fresh entire trusted suite runner; no previous baseline result reused.')
