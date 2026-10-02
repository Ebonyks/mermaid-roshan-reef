from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_river_join_study_v1_20261001';width=int(sys.argv[1]);assert width in [1280,1600]
out=f/'attempt_03';out.mkdir(exist_ok=True);gate=f/'runtime_gate';gate.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
target=f/Path(__file__).name
if not target.exists():shutil.copyfile(__file__,target)
receipt=gate/('capture%dv3.receipt.json'%width);assert not receipt.exists()
names=[gate/('capture%dv3.%s.log'%(width,x)) for x in ['stdout','stderr']]
home=b/'tmp'/('river_join_%d_v199'%width);home.mkdir(exist_ok=False)
env=os.environ.copy();env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8'
for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
 p=home/n;p.mkdir();env[k]=str(p)
cmd=['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe','--path',str(b),'-s','audit/job_river_join_study_v1_20261001/capture_join_study_v3.gd','--','--width='+str(width),'--touch','--classic-touch-test']
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
timed_out=False
with names[0].open('wb') as stdout,names[1].open('wb') as stderr:
 try:q=subprocess.run(cmd,cwd=b,env=env,stdout=stdout,stderr=stderr,timeout=100,creationflags=subprocess.CREATE_NO_WINDOW);code=q.returncode
 except subprocess.TimeoutExpired:code=-1;timed_out=True
logs=names[0].read_text(encoding='utf-8',errors='replace')+names[1].read_text(encoding='utf-8',errors='replace')
passed=code==0 and 'RIVER_JOIN_CAPTURE|PASS' in logs and not any(x in logs for x in ['SCRIPT ERROR','Parse Error','Assertion failed'])
write(receipt,{'status':'PASS_INHERITED_INPUT_CAPTURE_VISUAL_PENDING' if passed else 'FAIL_PRESERVED','command':cmd,'process_exit':code,'timed_out':timed_out,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'stdout_sha256':hashlib.sha256(names[0].read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256(names[1].read_bytes()).hexdigest(),'qualification':'Exact officialGodot4.7.2 Mobile desktop isolated non-runtime inherited input/flow study. No mounted production/network/complete-action/owner pass.'})
print(json.dumps(read(receipt)),flush=True);print(logs[-1600:],flush=True)
# Avoid shared-impact read/write races; parent updates coverage after both independent captures.
raise SystemExit(0 if passed else 1)
