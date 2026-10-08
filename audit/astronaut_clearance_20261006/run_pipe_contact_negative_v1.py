from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, time
root=Path(__file__).resolve().parents[2]
packet=Path(__file__).resolve().parent
engine=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
version=subprocess.check_output([str(engine),'--version'],text=True).strip()
assert version=='4.7.2.stable.official.ed1daf0bf'
job=root/'tmp/astronaut_pipe_contact_negative_v1_20261007'
job.mkdir(parents=True,exist_ok=True)
assert not any(job.iterdir()), 'Prior artifacts must be preserved; no automatic retry.'
script='audit/astronaut_clearance_20261006/verify_pipe_contact_negative_v1.gd'
names=[script,'audit/astronaut_clearance_20261006/run_pipe_contact_negative_v1.py','scripts/main.gd','scripts/save_state.gd','scripts/opera_house.gd','scripts/opera_act.gd','scripts/opera_career_world_2d.gd','scripts/opera_astronaut_surface.gd','scripts/opera_astronaut_pipe_work.gd','scripts/opera_gesture_surface.gd','scripts/castle_career_routes.gd','scripts/opera_world_hotspot_2d.gd','scripts/day_one_director.gd','scripts/chapter_two_director.gd','scripts/chapter_two_career_scene_adapter.gd','scripts/chapter_two_party_plan.gd','scripts/opera_roshan_actor.gd','assets/opera/worlds/actors/animation/roshan_astronaut_sheet_a.png','audit/astronaut_clearance_20261006/PIPE_CONTACT_IMPLEMENTATION_PLAN.json','assets/opera/worlds/props/goal_astronaut.png','project.godot','design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md','scripts/opera_roshan_actor.gd']
sources=[{'path':n,'sha256':sha(root/n)} for n in names]
log=packet/'PIPE_CONTACT_NEGATIVE_V1_LOG.txt'; receipt=packet/'PIPE_CONTACT_NEGATIVE_V1_RECEIPT.json'; preflight=packet/'PIPE_CONTACT_NEGATIVE_V1_PREFLIGHT.json'
assert not log.exists() and not receipt.exists() and not preflight.exists()
base=[str(engine),'--headless','--path',str(root),'--script','res://'+script]
started=utc(); start=time.monotonic(); steps=[]
preflight.write_text(json.dumps({'started_utc':started,'engine_version':version,'engine_sha256':sha(engine),'sources':sources,'commands':[base+['--check-only'],base],'time_cap_seconds':28,'fixture':'Isolated test save, prior Day One boss defeated and first six party jobs completed; No original user save or earned pipe progress injection. No original user save or phase/progress injection.','allocation':'Small headless check only; no import or capture.'},indent=2)+'\n',encoding='utf-8')
with log.open('xb') as output:
 for label,command in [('Godot analyzer',base+['--check-only']),('Birthday pipe-contact touch test',base)]:
  output.write(('\nSTEP '+label+'\n').encode()); output.flush()
  process=subprocess.Popen(command,cwd=root,stdout=output,stderr=subprocess.STDOUT)
  print(json.dumps({'step':label,'owned_pid':process.pid,'time_cap_seconds':28,'scope':'Small headless source/save diagnostic; no capture or import'}),flush=True)
  timed_out=False
  try: process.wait(timeout=max(1,28-(time.monotonic()-start)))
  except subprocess.TimeoutExpired:
   timed_out=True; process.terminate(); process.wait(timeout=15)
  steps.append({'label':label,'command':command,'owned_pid':process.pid,'exit_code':process.returncode,'timed_out':timed_out})
  if process.returncode!=0 or timed_out: break
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
errors=[line for line in lines if any(s in line for s in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])]
records=[json.loads(line.split('|',1)[1]) for line in lines if line.startswith('ASTRO_PIPE_RESULT|')]
contacts=records[0].get('contacts',[]) if records else []
matched=all(sha(root/s['path'])==s['sha256'] for s in sources)
passed=len(steps)==2 and all(s['exit_code']==0 and not s['timed_out'] for s in steps) and not errors and len(records)==1 and records[0]['failures']==0 and matched
result={'started_utc':started,'finished_utc':utc(),'engine_version':version,'engine_sha256':sha(engine),'steps':steps,'prior_attempt_seconds':121.32,'cumulative_native_seconds':round(time.monotonic()-start+121.32,2),'elapsed_seconds':round(time.monotonic()-start,2),'time_cap_seconds':28,'errors':errors,'result':'PASS' if passed else 'FAIL','evidence':records,'sources':sources,'source_bindings_still_match':matched,'preflight_path':preflight.relative_to(root).as_posix(),'preflight_sha256':sha(preflight),'log_path':log.relative_to(root).as_posix(),'log_sha256':sha(log),'isolated_save_files':[{'path':q.relative_to(root).as_posix(),'size_bytes':q.stat().st_size,'sha256':sha(q)} for q in sorted(job.iterdir()) if q.is_file()],'contacts':contacts,'meaning':'Negative-only real-input driver reaches actual contact interval and deliberately perturbs actor position or sampled pose; live owner eligibility must reject both and conserve unearned tile. Other current-source positive/save lifecycle proof is separately sealed in V5. Manual source-jaw geometry is candidate only; native motion, remaining phases, save/reload/full route, fullCI and independent/device/child/owner review pending.'}
receipt.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'result':result['result'],'steps':steps,'checks':records[0]['checks'] if records else 0,'failed_checks':[x for x in records[0]['rows'] if not x['pass']] if records else [],'contacts':contacts,'errors':errors[:8],'elapsed_seconds':result['elapsed_seconds'],'receipt_sha256':sha(receipt),'source_bindings_still_match':matched}),flush=True)
sys.exit(0 if passed else 1)
