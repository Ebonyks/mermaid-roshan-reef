from pathlib import Path
import datetime, hashlib, json, os, re, shutil, subprocess, sys, time
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_geology_river_runtime_v1_20261002'
impact=r/'design/audit_impacts/job-geology-river-painted-runtime-20261002.json'
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
gate=out/'runtime_gate';gate.mkdir(exist_ok=True)
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
arg=sys.argv[1]
action=re.sub(r'v\d+$','',arg)
commands={
 'parser':[py,'-X','utf8','-B','-m','gdtoolkit.parser','scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_hotspot_catalog.gd','scripts/opera_world_hotspot_2d.gd','audit/job_geology_river_runtime_v1_20261002/capture_geology_river_runtime.gd'],
 'inference':[py,'-X','utf8','-B','tools/lint_inference.py','scripts/opera_geology_surface.gd','scripts/opera_career_world_2d.gd','scripts/opera_hotspot_catalog.gd','scripts/opera_world_hotspot_2d.gd','audit/job_geology_river_runtime_v1_20261002/capture_geology_river_runtime.gd'],
 'import':[godot,'--headless','--path',str(r),'--import'],
 'analyzer':[godot,'--headless','--path',str(r),'--check-only','--script','audit/job_geology_river_runtime_v1_20261002/capture_geology_river_runtime.gd'],
 'authority':[py,'-X','utf8','-B','tools/audit_document_authority.py'],
 'development':[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'],
 '2d':[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'],
 'capture1280':[godot,'--path',str(r),'-s','audit/job_geology_river_runtime_v1_20261002/capture_geology_river_runtime.gd','--','--width=1280','--touch','--classic-touch-test'],
 'capture1600':[godot,'--path',str(r),'-s','audit/job_geology_river_runtime_v1_20261002/capture_geology_river_runtime.gd','--','--width=1600','--touch','--classic-touch-test'],
}
assert action in commands
d=json.loads(impact.read_text())
names=[gate/(arg+'.'+suffix) for suffix in ['stdout.log','stderr.log','receipt.json']]
tool=r/'audit/job_geology_river_runtime_v1_20261002/review_tools/run_geology_river_gates_v216.py'
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in names}|{tool.relative_to(r).as_posix()})
write(impact,d)
if not tool.exists():shutil.copyfile(Path(__file__),tool)
assert not names[2].exists(),'Preserve every completed gate attempt; use new attempt name.'
env=os.environ.copy();env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8'
if arg.startswith('capture'):
 home=r/'tmp'/('geology_river_'+arg+'_v216');home.mkdir(exist_ok=False)
 for k,name in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
  p=home/name;p.mkdir();env[k]=str(p)
now=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with names[0].open('wb') as stdout,names[1].open('wb') as stderr:
 result=subprocess.run(commands[action],cwd=r,env=env,stdout=stdout,stderr=stderr,timeout=360 if arg.startswith('capture') else 240,creationflags=subprocess.CREATE_NO_WINDOW)
logs=names[0].read_text(encoding='utf-8',errors='replace')+names[1].read_text(encoding='utf-8',errors='replace')
errors=[line for line in logs.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|Assertion failed|Failed loading resource|Missing painted geology source',line)]
passed=result.returncode==0 and not errors
if arg.startswith('capture'):passed=passed and 'ALL4_INTENTIONAL_PHASES' in logs
receipt={'status':'PASS' if passed else 'FAIL_PRESERVED','command':commands[action],'process_exit':result.returncode,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-now,'blocking_diagnostics':errors,'stdout_sha256':sha(names[0]),'stderr_sha256':sha(names[1]),'qualification':'Scoped machine evidence; no visual, physical device, child, owner or full-suite acceptance.'}
write(names[2],receipt)
d=json.loads(impact.read_text());d['validation'].append({'command':' '.join(commands[action]),'result':'PASS' if passed else 'FAIL','evidence':names[2].relative_to(r).as_posix()})
if arg.startswith('capture') or action == 'import':
 d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for folder in [out,r/'assets/opera/worlds/geology/painted_river_v1_20261002'] for p in folder.rglob('*') if p.is_file()})
write(impact,d)
print('GEODE_GATE|'+arg+'|'+receipt['status']+'|'+str(round(receipt['elapsed_seconds'],1))+'s')
if not passed:print('\n'.join(errors[-8:]));print(logs[-2000:])
sys.exit(0 if passed else 1)
