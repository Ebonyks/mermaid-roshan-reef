from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,subprocess,sys,time,re
root=Path(__file__).resolve().parents[2];packet=Path(__file__).resolve().parent
lane=sys.argv[1];assert lane in ['baseline','repair']
engine=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
version=subprocess.check_output([str(engine),'--version'],text=True).strip();assert version=='4.7.2.stable.official.ed1daf0bf'
prefix='PARK_PROP_'+lane.upper();log=packet/(prefix+'_LOG.txt');receipt=packet/(prefix+'_RECEIPT.json');preflight=packet/(prefix+'_PREFLIGHT.json')
assert not any(p.exists() for p in [log,receipt,preflight]),'Preserve previous run; no retry overwrite.'
names=['scripts/opera_astronaut_surface.gd','scripts/opera_gesture_surface.gd','scripts/probe_opera_gesture_quality.gd','scripts/opera_career_world_2d.gd','scripts/chapter_two_career_scene_adapter.gd','project.godot','assets/opera/worlds/props/goal_astronaut.png','audit/astronaut_clearance_20261006/run_park_prop.py']
sources=[{'path':n,'sha256':sha(root/n)} for n in names]
commands=[('Parser',[sys.executable,'-B','-m','gdtoolkit.parser','scripts/opera_astronaut_surface.gd','scripts/probe_opera_gesture_quality.gd']),('Inference',[sys.executable,'-B','tools/lint_inference.py','scripts/opera_astronaut_surface.gd','scripts/probe_opera_gesture_quality.gd']),('Astronaut analyzer',[str(engine),'--headless','--path',str(root),'--script','res://scripts/opera_astronaut_surface.gd','--check-only']),('Trusted gesture probe',[str(engine),'--headless','--path',str(root),'--script','res://scripts/probe_opera_gesture_quality.gd'])]
start=time.monotonic();started=utc();steps=[]
preflight.write_text(json.dumps({'started_utc':started,'engine_version':version,'engine_sha256':sha(engine),'sources':sources,'commands':commands,'time_cap_seconds':90,'allocation':'Small headless source/input checks only, no import/capture','lane':lane},indent=2)+'\n',encoding='utf-8')
with log.open('xb') as out:
 for label,cmd in commands:
  out.write(('\nSTEP '+label+'\n').encode());out.flush()
  process=subprocess.Popen(cmd,cwd=root,stdout=out,stderr=subprocess.STDOUT)
  print(json.dumps({'label':label,'owned_pid':process.pid}),flush=True)
  timeout=False
  try:process.wait(timeout=max(1,90-(time.monotonic()-start)))
  except subprocess.TimeoutExpired:timeout=True;process.terminate();process.wait(timeout=15)
  steps.append({'label':label,'command':cmd,'owned_pid':process.pid,'exit_code':process.returncode,'timed_out':timeout})
  if process.returncode!=0 or timeout:break
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
errors=[s for s in lines if any(x in s for x in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])]
failures=[s for s in lines if 'GESTURE_QUALITY|FAIL|' in s]
results=[s for s in lines if s.startswith('GESTURE_QUALITY|result:')]
match=all(sha(root/s['path'])==s['sha256'] for s in sources)
passed=len(steps)==len(commands) and all(s['exit_code']==0 and not s['timed_out'] for s in steps) and not errors and len(results)==1 and 'ALL OK' in results[0] and match
value={'lane':lane,'result':'PASS' if passed else 'FAIL','started_utc':started,'finished_utc':utc(),'engine_version':version,'engine_sha256':sha(engine),'sources':sources,'source_bindings_still_match':match,'steps':steps,'elapsed_seconds':round(time.monotonic()-start,2),'errors':errors,'failures':failures,'probe_result':results,'preflight_path':preflight.relative_to(root).as_posix(),'preflight_sha256':sha(preflight),'log_path':log.relative_to(root).as_posix(),'log_sha256':sha(log),'meaning':'Bound native asset/draw-route, genuine-input mechanical compatibility at2sizes only. No rendered-native visual, complete acting, device, child, owner or4.6acceptance.'}
receipt.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8');print(json.dumps({'result':value['result'],'failures':failures,'errors':errors[:5],'probe_result':results,'source_bindings_still_match':match,'receipt_sha256':sha(receipt)}),flush=True)
sys.exit(0 if passed else 1)
