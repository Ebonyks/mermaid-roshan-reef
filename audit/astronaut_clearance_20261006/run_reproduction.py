from pathlib import Path
from datetime import datetime,timezone
import subprocess,sys,json,hashlib,time,re,os
ROOT=Path(__file__).resolve().parents[2];B=Path(__file__).resolve().parent
ENGINE='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
kind=sys.argv[1]
if kind in ['import_direct','repair_complete','pipe_routes']:ENGINE=ENGINE.replace('_console.exe','.exe')
if kind in ['import','import_isolated','import_recovery','import_direct']:
 command=[ENGINE,'--headless','--path',str(ROOT),'--import','--verbose'];timeout=720;name={'import':'IMPORT','import_isolated':'IMPORT_ISOLATED','import_recovery':'IMPORT_RECOVERY','import_direct':'IMPORT_DIRECT'}[kind]
elif kind=='pipe_routes':
 command=[ENGINE,'--headless','--path',str(ROOT),'--script',str(B/'verify_pipe.gd')];timeout=120;name='PIPE_ROUTES'
elif kind=='baseline':
 command=[ENGINE,'--headless','--path',str(ROOT),'--script',str(B/'reproduce_focus.gd')];timeout=120;name='BASELINE_FOCUS'
elif kind in ['repair','repair_complete']:
 command=[ENGINE,'--headless','--path',str(ROOT),'--script',str(B/'verify_input.gd')];timeout=120;name='REPAIR_INPUT' if kind=='repair' else 'REPAIR_INPUT_COMPLETE'
else:raise ValueError(kind)
version=subprocess.check_output([ENGINE,'--version'],text=True).strip()
assert version=='4.7.2.stable.official.ed1daf0bf',version
started=datetime.now(timezone.utc);log=B/(name+'_LOG.txt')
env=os.environ.copy()
if kind in ['import_isolated','import_recovery','import_direct']:
 for key in ['APPDATA','LOCALAPPDATA']:
  d=ROOT/'tmp'/'astronaut_engine_20261006'/key
  d.mkdir(parents=True,exist_ok=True);env[key]=str(d)
 command.extend(['--debug-server','tcp://127.0.0.1:6207','--lsp-port','6208','--dap-port','6209'])
 if kind=='import_recovery':command.append('--recovery-mode')
with log.open('xb') as f:
 p=subprocess.Popen(command,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
 last=0;t0=time.monotonic();timed_out=False
 while p.poll() is None:
  elapsed=time.monotonic()-t0
  if elapsed>timeout:
   p.terminate();p.wait(timeout=15);timed_out=True;break
  if elapsed-last>=30:
   last=elapsed;print(json.dumps({'job':kind,'live_pid':p.pid,'elapsed_seconds':round(elapsed,1),'log_bytes':log.stat().st_size}),flush=True)
  time.sleep(1)
text=log.read_text(encoding='utf-8',errors='replace')
errors=[l for l in text.splitlines() if any(w in l for w in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error','Error importing','Cannot load resource'])]
evidence=[]
for l in text.splitlines():
 if l.startswith(('ASTRO_FOCUS_EVIDENCE|','ASTRO_INPUT_RESULT|','ASTRO_PIPE_RESULT|')):evidence.append(json.loads(l.split('|',1)[1]))
r={'started_utc':started.isoformat(),'finished_utc':datetime.now(timezone.utc).isoformat(),'command':command,'engine_version':version,'engine_sha256':sha(ENGINE),'exit_code':p.returncode,'timed_out':timed_out,'result':'PASS' if p.returncode==0 and not errors else 'FAIL','errors':errors,'log_path':log.relative_to(ROOT).as_posix(),'log_sha256':sha(log),'evidence':evidence,'sources':[{'path':n,'sha256':sha(ROOT/n)} for n in ['scripts/opera_gesture_surface.gd','scripts/opera_career_world_2d.gd','audit/astronaut_clearance_20261006/reproduce_focus.gd','scripts/opera_astronaut_surface.gd','scripts/probe_opera_gesture_quality.gd','audit/astronaut_clearance_20261006/verify_input.gd','audit/astronaut_clearance_20261006/verify_pipe.gd','audit/astronaut_clearance_20261006/run_reproduction.py']],'meaning':'Retained exact-engine result. Import failure is not an input reproduction. No visual/device/child/owner acceptance.'}
with (B/(name+'_RECEIPT.json')).open('x',encoding='utf-8',newline='\n') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(r,ensure_ascii=False),flush=True)
sys.exit(0 if kind=='baseline' and evidence and evidence[0]['failures']==1 and evidence[0]['rows'][0]['pass'] and not evidence[0]['rows'][1]['pass'] else (p.returncode or bool(errors)))
