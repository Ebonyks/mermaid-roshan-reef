from pathlib import Path
import hashlib,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=r/'audit/job_geode_supported_celebration_v1_20261002'
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
p=f/'review_tools/run_supported_geode_gates_v322.py';s=p.read_text();assert "'geode_route_emblems_'+arg+'_v276'" in s;s=s.replace("'geode_route_emblems_'+arg+'_v276'","'geode_supported_'+arg+'_v322'");p.write_text(s,encoding='utf-8',newline='\n')
write(f/'CAPTURE_PREPARATION_FAILURE_V1.json',{'status':'PRE_ENGINE_SAVE_HOME_COLLISION_PRESERVED','action':'capture1280v1','failure':'Copied helper still named prior task isolated save directory; that directory already exists. Engine never launched, no capture or source changed.','repair':'Use unique geode_supported_<attempt>_v322 isolated save home. Preserve previous task home and evidence.'})
for oldname,newname in [('prepare_geode_route_boards_v306.py','prepare_supported_geode_boards_v323.py'),('prepare_geode_route_native_still_boards_v307.py','prepare_supported_geode_stills_v323.py')]:
 s=(r/'audit/job_geode_route_emblem_runtime_v1_20261002/review_tools'/oldname).read_text()
 s=s.replace('job_geode_route_emblem_runtime_v1_20261002','job_geode_supported_celebration_v1_20261002').replace('job-geode-route-emblem-runtime-20261002','job-geode-supported-celebration-20261002').replace('attempt_02','attempt_01').replace('==373','==375').replace('v2.receipt','v1.receipt').replace('_V2_','_V1_').replace('_V2.json','_V1.json')
 s=s.replace('previousK receipt applies only to its prior368 source boundary.','previousL receipt applies only to its prior373 source boundary.').replace('earlierK','earlierL')
 (f/'review_tools'/newname).write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
p=r/'design/audit_impacts/job-geode-supported-celebration-20261002.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()});write(p,d)
print('Unique capture save home corrected; failure preserved and fresh evidence tools prepared.')
