from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,time,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
G=F/'runtime_gate'
G.mkdir(exist_ok=True)
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json'
imp=read(ip)
if Path(__file__).parent != F/'review_tools':shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
label=sys.argv[1]
action=label.split('_')[0]
gd=sorted(x for x in imp['files'] if x.endswith('.gd'))
commands={'parser':[py,'-X','utf8','-B','-m','gdtoolkit.parser',*gd], 'inference':[py,'-X','utf8','-B','tools/lint_inference.py',*gd], 'authority':[py,'-X','utf8','-B','tools/audit_document_authority.py'], 'development':[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'], 'analyzer':[godot,'--headless','--path',str(R),'--check-only','--script','scripts/opera_nursery_surface.gd']}
assert action in commands
paths=[G/(label+'.'+suffix) for suffix in ['stdout.log','stderr.log','receipt.json']]
assert not any(x.exists() for x in paths),'Preserve earlier gate attempts.'
imp['files']=sorted(set(imp['files'])|{x.relative_to(R).as_posix() for x in paths}|{(F/'review_tools'/Path(__file__).name).relative_to(R).as_posix()})
write(ip,imp)
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
with paths[0].open('wb') as out,paths[1].open('wb') as err:
    result=subprocess.run(commands[action],cwd=R,env=env,stdout=out,stderr=err,timeout=420,creationflags=subprocess.CREATE_NO_WINDOW)
logs='\n'.join(x.read_text(encoding='utf-8',errors='replace') for x in paths[:2])
errors=[x for x in logs.splitlines() if any(s in x for s in ['SCRIPT ERROR','Parse Error','Compile Error','Assertion failed'])]
passed=result.returncode==0 and not errors
receipt={'status':'PASS' if passed else 'FAIL_PRESERVED','command':commands[action],'process_exit':result.returncode,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'blocking_diagnostics':errors,'stdout_sha256':sha(paths[0]),'stderr_sha256':sha(paths[1]),'qualification':'Scoped machine verification. No creative/device/child/owner/global approval.'}
write(paths[2],receipt)
imp=read(ip);imp['validation'].append({'command':' '.join(commands[action]),'result':'PASS' if passed else 'FAIL','evidence':paths[2].relative_to(R).as_posix()});write(ip,imp)
print('NURSERY_GATE|'+label+'|'+receipt['status']+'|'+str(round(receipt['elapsed_seconds'],1))+'s',flush=True)
if not passed:print(logs[-4000:])
sys.exit(0 if passed else 1)
