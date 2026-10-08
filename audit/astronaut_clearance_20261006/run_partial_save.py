from pathlib import Path
from datetime import datetime, timezone
import subprocess, json, hashlib, time, sys
root=Path(__file__).resolve().parents[2]
packet=Path(__file__).resolve().parent
engine=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
version=subprocess.check_output([str(engine),'--version'],text=True).strip()
assert version=='4.7.2.stable.official.ed1daf0bf'
job=root/'tmp/astronaut_partial_save_20261006'
job.mkdir(parents=True,exist_ok=True)
assert not any(job.iterdir()), 'Preserve prior save diagnostic artifacts; no automatic overwrite/retry.'
script='audit/astronaut_clearance_20261006/reproduce_partial_save.gd'
names=[script,'audit/astronaut_clearance_20261006/run_partial_save.py','scripts/main.gd','scripts/save_state.gd','scripts/opera_house.gd','scripts/opera_act.gd','scripts/opera_career_world_2d.gd','scripts/opera_astronaut_surface.gd','scripts/opera_gesture_surface.gd','scripts/castle_career_routes.gd','scripts/opera_world_hotspot_2d.gd','project.godot']
sources=[{'path':n,'sha256':sha(root/n)} for n in names]
log=packet/'PARTIAL_SAVE_BASELINE_LOG.txt'
receipt=packet/'PARTIAL_SAVE_BASELINE_RECEIPT.json'
assert not log.exists() and not receipt.exists()
command=[str(engine),'--headless','--path',str(root),'--script','res://'+script]
started=datetime.now(timezone.utc).isoformat()
start=time.monotonic();timed_out=False
with log.open('xb') as output:
 process=subprocess.Popen(command,cwd=root,stdout=output,stderr=subprocess.STDOUT)
 print(json.dumps({'owned_pid':process.pid,'time_cap_seconds':90,'scope':'Small headless save diagnostic; no capture or import'}),flush=True)
 try: process.wait(timeout=90)
 except subprocess.TimeoutExpired:
  timed_out=True;process.terminate();process.wait(timeout=15)
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
errors=[line for line in lines if any(s in line for s in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])]
records=[json.loads(line.split('|',1)[1]) for line in lines if line.startswith('ASTRO_SAVE_RESULT|')]
savefiles=[{'path':p.relative_to(root).as_posix(),'size_bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(job.iterdir()) if p.is_file()]
result={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'command':command,'engine_version':version,'engine_sha256':sha(engine),'owned_pid':process.pid,'exit_code':process.returncode,'elapsed_seconds':round(time.monotonic()-start,2),'timed_out':timed_out,'time_cap_seconds':90,'errors':errors,'execution_result':'PASS' if not errors and not timed_out and records else 'FAIL','save_acceptance_result':'PASS' if process.returncode==0 and not errors and records else 'FAIL','evidence':records,'sources':sources,'source_bindings_still_match':all(sha(root/s['path'])==s['sha256'] for s in sources),'log_path':log.relative_to(root).as_posix(),'log_sha256':sha(log),'isolated_save_files':savefiles,'meaning':'Falsifiable headless partial-save baseline; no visual/current-native/whole-action/device/child/owner acceptance; no original save read/write; fixture story prerequisites and production cancel callback explicitly scoped.'}
receipt.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'execution_result':result['execution_result'],'save_acceptance_result':result['save_acceptance_result'],'exit_code':process.returncode,'errors':errors[:8],'evidence':records,'receipt_sha256':sha(receipt),'source_bindings_still_match':result['source_bindings_still_match']}),flush=True)
sys.exit(0 if result['execution_result']=='PASS' else 1)
