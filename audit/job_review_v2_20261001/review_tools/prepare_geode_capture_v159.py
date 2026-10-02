from pathlib import Path
import json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_geode_runtime_v1_20261001';impact=r/'design/audit_impacts/job-geode-painted-runtime-20261001.json'
d=json.loads(impact.read_text(encoding='utf-8'))
for width in [1280,1600]:
 receipt=json.loads((out/'attempt_02'/('CAPTURE_'+str(width)+'.json')).read_text(encoding='utf-8'))
 d['files'].append((out/'attempt_03'/('CAPTURE_'+str(width)+'.json')).relative_to(r).as_posix())
 for x in receipt['views']:d['files'].append((out/'attempt_03'/x['path']).relative_to(r).as_posix())
d['files']=sorted(set(d['files'])|{'audit/job_review_v2_20261001/review_tools/prepare_geode_capture_v159.py','audit/job_review_v2_20261001/review_tools/run_geode_runtime_gates_v160.py'})
impact.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
s=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/run_geode_runtime_gates_v156.py').read_text(encoding='utf-8').replace("action=arg.removesuffix('v2')","action=re.sub(r'v\\d+$','',arg)").replace('run_geode_runtime_gates_v156.py','run_geode_runtime_gates_v160.py')
Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/run_geode_runtime_gates_v160.py').write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),r/'audit/job_review_v2_20261001/review_tools/prepare_geode_capture_v159.py')
print('Final36 native paths covered before capture; new runner preserves all prior attempts.')
