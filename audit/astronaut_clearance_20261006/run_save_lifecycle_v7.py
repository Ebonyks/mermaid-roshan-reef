from pathlib import Path
from datetime import datetime, timezone
import ctypes, hashlib, json, shutil, subprocess, sys, time
setup_start=time.monotonic()
root=Path(__file__).resolve().parents[2]
packet=Path(__file__).resolve().parent
engine=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def directory_bytes(path):
 return sum(q.stat().st_size for q in path.rglob('*') if q.is_file()) if path.exists() else 0
class MemoryStatus(ctypes.Structure):
 _fields_=[('length',ctypes.c_uint32),('load',ctypes.c_uint32),('total_phys',ctypes.c_uint64),('avail_phys',ctypes.c_uint64),('total_page',ctypes.c_uint64),('avail_page',ctypes.c_uint64),('total_virtual',ctypes.c_uint64),('avail_virtual',ctypes.c_uint64),('avail_extended',ctypes.c_uint64)]
memory=MemoryStatus();memory.length=ctypes.sizeof(memory)
assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
resource_before={'C_free_bytes':shutil.disk_usage('C:/').free,'physical_available_bytes':memory.avail_phys,'cache_bytes':directory_bytes(root/'.godot'),'artifact_cap_bytes':32*1024**2,'cache_growth_cap_bytes':16*1024**2}
assert resource_before['C_free_bytes']>=3*1024**3 and resource_before['physical_available_bytes']>=3*1024**3,'Small-check admission floor not met.'
version=subprocess.check_output([str(engine),'--version'],text=True).strip()
assert version=='4.7.2.stable.official.ed1daf0bf'
job=root/'tmp/astronaut_save_lifecycle_v7_20261007'
job.mkdir(parents=True,exist_ok=True)
assert not any(job.iterdir()), 'Prior artifacts must be preserved; no automatic retry.'
script='audit/astronaut_clearance_20261006/verify_save_lifecycle_v7.gd'
names=[script,'scripts/opera_astronaut_pipe_work.gd','scripts/opera_roshan_actor.gd','assets/opera/worlds/actors/animation/roshan_astronaut_sheet_a.png','audit/astronaut_clearance_20261006/PIPE_CONTACT_IMPLEMENTATION_PLAN.json','audit/astronaut_clearance_20261006/PIPE_CONTACT_REVIEW.json','audit/astronaut_clearance_20261006/CURRENT_ROUTE_CONTACT_RECHECK_PLAN.json','audit/astronaut_clearance_20261006/run_save_lifecycle_v7.py','scripts/main.gd','scripts/save_state.gd','scripts/opera_house.gd','scripts/opera_act.gd','scripts/opera_career_world_2d.gd','scripts/opera_astronaut_surface.gd','scripts/opera_gesture_surface.gd','scripts/castle_career_routes.gd','scripts/opera_world_hotspot_2d.gd','scripts/day_one_director.gd','scripts/chapter_two_director.gd','scripts/chapter_two_career_scene_adapter.gd','scripts/chapter_two_party_plan.gd','project.godot','design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md','tmp/astronaut_partial_save_repair_20261006/reef_save.json']
sources=[{'path':n,'sha256':sha(root/n)} for n in names]
log=packet/'SAVE_LIFECYCLE_V7_LOG.txt'; receipt=packet/'SAVE_LIFECYCLE_V7_RECEIPT.json'; preflight=packet/'SAVE_LIFECYCLE_V7_PREFLIGHT.json'
assert not log.exists() and not receipt.exists() and not preflight.exists()
base=[str(engine),'--headless','--path',str(root),'--script','res://'+script]
started=utc(); start=time.monotonic(); steps=[]
preflight.write_text(json.dumps({'started_utc':started,'engine_version':version,'engine_sha256':sha(engine),'sources':sources,'commands':[base+['--check-only'],base],'time_cap_seconds':150,'fixture':'Isolated ordinary test save; prior route prerequisites explicit in fixture. No original user save or phase/progress injection.','allocation':'Distinct ordinary/birthday current-source regression scope,150s per variant; not a retry or renewal of the terminal141.03s pipe diagnostic. Small headless only; no import/capture/fullCI.','resource_before':resource_before,'setup_seconds':round(start-setup_start,3),'no_automatic_retry':True},indent=2)+'\n',encoding='utf-8')
with log.open('xb') as output:
 for label,command in [('Godot analyzer',base+['--check-only']),('Ordinary route touch/save test',base)]:
  output.write(('\nSTEP '+label+'\n').encode()); output.flush()
  process=subprocess.Popen(command,cwd=root,stdout=output,stderr=subprocess.STDOUT)
  print(json.dumps({'step':label,'owned_pid':process.pid,'time_cap_seconds':150,'scope':'Small headless source/save diagnostic; no capture or import'}),flush=True)
  timed_out=False
  try: process.wait(timeout=max(1,150-(time.monotonic()-start)))
  except subprocess.TimeoutExpired:
   timed_out=True; process.terminate(); process.wait(timeout=15)
  steps.append({'label':label,'command':command,'owned_pid':process.pid,'exit_code':process.returncode,'timed_out':timed_out})
  if process.returncode!=0 or timed_out: break
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
errors=[line for line in lines if any(s in line for s in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])]
records=[json.loads(line.split('|',1)[1]) for line in lines if line.startswith('ASTRO_SAVE_RESULT|')]
resource_after={'C_free_bytes':shutil.disk_usage('C:/').free,'cache_bytes':directory_bytes(root/'.godot'),'artifact_bytes':directory_bytes(job)+log.stat().st_size+preflight.stat().st_size}
resource_after['cache_growth_bytes']=max(0,resource_after['cache_bytes']-resource_before['cache_bytes'])
resource_ok=resource_after['C_free_bytes']>=3*1024**3 and resource_after['artifact_bytes']<=resource_before['artifact_cap_bytes'] and resource_after['cache_growth_bytes']<=resource_before['cache_growth_cap_bytes']
matched=all(sha(root/s['path'])==s['sha256'] for s in sources)
passed=len(steps)==2 and all(s['exit_code']==0 and not s['timed_out'] for s in steps) and not errors and len(records)==1 and records[0]['failures']==0 and records[0]['checks']==91 and len(records[0].get('contact_requests',[]))==10 and matched and resource_ok
result={'started_utc':started,'finished_utc':utc(),'engine_version':version,'engine_sha256':sha(engine),'steps':steps,'elapsed_seconds':round(time.monotonic()-start,2),'time_cap_seconds':150,'setup_seconds':round(start-setup_start,3),'total_observed_seconds':round(time.monotonic()-setup_start,3),'resource_before':resource_before,'resource_after':resource_after,'resource_limits_pass':resource_ok,'errors':errors,'result':'PASS' if passed else 'FAIL','evidence':records,'sources':sources,'source_bindings_still_match':matched,'preflight_path':preflight.relative_to(root).as_posix(),'preflight_sha256':sha(preflight),'log_path':log.relative_to(root).as_posix(),'log_sha256':sha(log),'isolated_save_files':[{'path':q.relative_to(root).as_posix(),'size_bytes':q.stat().st_size,'sha256':sha(q)} for q in sorted(job.iterdir()) if q.is_file()],'meaning':'Genuine ordinary picture/object/input route from explicit route fixture; save/load, cancellation, natural finish/return/replay only. Current native visual/device/child/owner and full suite pending.'}
receipt.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'result':result['result'],'steps':steps,'checks':records[0]['checks'] if records else 0,'failed_checks':[x for x in records[0]['rows'] if not x['pass']] if records else [],'errors':errors[:8],'elapsed_seconds':result['elapsed_seconds'],'receipt_sha256':sha(receipt),'source_bindings_still_match':matched}),flush=True)
sys.exit(0 if passed else 1)
