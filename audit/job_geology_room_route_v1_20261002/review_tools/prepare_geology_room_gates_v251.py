from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geology_room_route_v1_20261002';prefix=f.relative_to(b).as_posix()
p=b/'design/audit_impacts/job-geology-room-route-review-20261002.json'
d=json.loads(p.read_text());d['rules']=sorted(set(d['rules'])|{'DL-INT-12','DL-QA-01','DL-QA-02'})
s=(b/'audit/job_geode_coherent_runtime_v1_20261002/review_tools/run_coherent_runtime_gates_v247.py').read_text()
s=s.replace('audit/job_geode_coherent_runtime_v1_20261002',prefix).replace('job-geode-coherent-runtime-20261002','job-geology-room-route-review-20261002').replace('capture_v2.gd','capture.gd').replace('run_coherent_runtime_gates_v247.py','run_geology_room_gates_v251.py').replace('geode_coherent_runtime_','geology_room_route_').replace('_v247','_v251').replace("'ALL4_INTENTIONAL_PHASES' in logs","'ALL4_EARNED_LIBRARY_RETURN_AND_DEV_BACK' in logs").replace("'GEODE_GATE|'","'GEOLOGY_ROOM_GATE|'")
(f/'review_tools/run_geology_room_gates_v251.py').write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()})
p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared route-review wrappers; no frozen source edits.')
