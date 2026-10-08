from pathlib import Path
from datetime import datetime,timezone
import ctypes,hashlib,json,os,shutil,subprocess,sys,time
root=Path(__file__).resolve().parents[2];packet=Path(__file__).resolve().parent
engine=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
log=packet/'RELEASE_OWNERSHIP_REGRESSION_V1_LOG.txt';receipt=packet/'RELEASE_OWNERSHIP_REGRESSION_V1_RECEIPT.json';preflight=packet/'RELEASE_OWNERSHIP_REGRESSION_V1_PREFLIGHT.json'
CAP=360;FLOOR=3*1024**3;OUTPUT_CAP=64*1024**2;CACHE_CAP=64*1024**2
configs=[('Pipe contact73','verify_pipe_contact_v6.gd','astronaut_pipe_contact_v6_20261007',73,'ASTRO_PIPE_RESULT|',None),('Contact negatives17','verify_pipe_contact_negative_v2.gd','astronaut_pipe_contact_negative_v2_20261007',17,'ASTRO_PIPE_RESULT|',None),('Correction1280','verify_pipe_correction_aspect_v2.gd','astronaut_pipe_correction_aspects_v2_20261007',57,'ASTRO_PIPE_RESULT|',1280),('Correction1600','verify_pipe_correction_aspect_v2.gd','astronaut_pipe_correction_aspects_v2_20261007',57,'ASTRO_PIPE_RESULT|',1600),('Ordinary allmechanics91','verify_save_lifecycle_v8.gd','astronaut_save_lifecycle_v8_20261007',91,'ASTRO_SAVE_RESULT|',None)]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def utc():return datetime.now(timezone.utc).isoformat()
def size(path):return sum(q.stat().st_size for q in path.rglob('*') if q.is_file()) if path.exists() else 0
class MemoryStatus(ctypes.Structure):
 _fields_=[('length',ctypes.c_uint32),('load',ctypes.c_uint32),('total_phys',ctypes.c_uint64),('avail_phys',ctypes.c_uint64),('total_page',ctypes.c_uint64),('avail_page',ctypes.c_uint64),('total_virtual',ctypes.c_uint64),('avail_virtual',ctypes.c_uint64),('avail_extended',ctypes.c_uint64)]
def resources():
 m=MemoryStatus();m.length=ctypes.sizeof(m);assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m));return {'C_free_bytes':shutil.disk_usage('C:/').free,'physical_available_bytes':m.avail_phys,'cache_bytes':size(root/'.godot')}
def occupancy():
 command="@(Get-CimInstance Win32_Process -Filter \"Name='Godot_v4.7.2-stable_win64.exe'\" | Select-Object ProcessId) | ConvertTo-Json -Compress"
 q=subprocess.run(['powershell','-NoProfile','-Command',command],capture_output=True,text=True,timeout=15);assert q.returncode==0
 return json.loads(q.stdout) if q.stdout.strip() else []
assert not any(q.exists() for q in [log,receipt,preflight]);assert not occupancy(),'One owned engine process at a time'
for folder in set(c[2] for c in configs):
 job=root/'tmp'/folder;assert not job.exists() or not any(job.iterdir()),'Preserve prior artifacts';job.mkdir(parents=True,exist_ok=True)
for _,fixture,folder,*_ in configs:assert 'res://tmp/'+folder in (packet/fixture).read_text(),'Fixture/output target mismatch'
version=subprocess.check_output([str(engine),'--version'],text=True).strip();assert version=='4.7.2.stable.official.ed1daf0bf';engine_sha=sha(engine);assert engine_sha=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
before=resources();assert min(before['C_free_bytes'],before['physical_available_bytes'])>=FLOOR
names=sorted(set(['audit/astronaut_clearance_20261006/'+c[1] for c in configs]+['audit/astronaut_clearance_20261006/run_release_ownership_regressions_v1.py','audit/astronaut_clearance_20261006/PIPE_RELEASE_OWNERSHIP_PLAN.json','scripts/main.gd','scripts/save_state.gd','scripts/opera_astronaut_surface.gd','scripts/opera_astronaut_pipe_work.gd','scripts/opera_roshan_actor.gd','scripts/opera_career_world_2d.gd','scripts/opera_gesture_surface.gd','scripts/opera_house.gd','scripts/opera_act.gd','scripts/castle_career_routes.gd','scripts/opera_world_hotspot_2d.gd','scripts/day_one_director.gd','scripts/chapter_two_director.gd','scripts/chapter_two_career_scene_adapter.gd','scripts/chapter_two_party_plan.gd','assets/opera/worlds/actors/animation/roshan_astronaut_sheet_a.png','assets/opera/worlds/props/goal_astronaut.png','project.godot','design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md','tmp/astronaut_partial_save_repair_20261006/reef_save.json']))
sources=[{'path':n,'sha256':sha(root/n)} for n in names]
steps=[];evidence=[];errors=[];started=utc();begin=time.monotonic()
preflight.write_text(json.dumps({'started_utc':started,'engine_version':version,'engine_sha256':engine_sha,'sources':sources,'resource_before':before,'combined_cap_seconds':CAP,'output_cap_bytes':OUTPUT_CAP,'cache_growth_cap_bytes':CACHE_CAP,'configs':configs,'no_automatic_retry':True,'scope':'Current-source regression refresh after native-confirmed owned release repair; actual touch/save/negative/correction behavior unchanged. One sequential engine, isolated outputs; no import/art/capture/fullCI. Prior measured costs preserved in repair plan.'},indent=2)+'\n')
with log.open('xb') as output:
 for fixture in dict.fromkeys(c[1] for c in configs):
  command=[str(engine),'--headless','--path',str(root),'--script','res://audit/astronaut_clearance_20261006/'+fixture,'--check-only']
  output.write(('\nANALYZER '+fixture+'\n').encode());output.flush();q=subprocess.run(command,cwd=root,stdout=output,stderr=subprocess.STDOUT,timeout=max(1,CAP-(time.monotonic()-begin)));steps.append({'label':'Analyzer '+fixture,'command':command,'exit_code':q.returncode})
  if q.returncode:break
 if all(x['exit_code']==0 for x in steps):
  for label,fixture,folder,count,marker,width in configs:
   command=[str(engine),'--headless','--path',str(root),'--script','res://audit/astronaut_clearance_20261006/'+fixture];env=os.environ.copy()
   if width:env['ASTRO_PIPE_WIDTH']=str(width)
   output.write(('\nRUN '+label+'\n').encode());output.flush();offset=log.stat().st_size
   process=subprocess.Popen(command,cwd=root,stdout=output,stderr=subprocess.STDOUT,env=env);print(json.dumps({'step':label,'owned_pid':process.pid,'combined_cap_seconds':CAP}),flush=True)
   timed_out=False
   try:process.wait(timeout=max(1,CAP-(time.monotonic()-begin)))
   except subprocess.TimeoutExpired:
    timed_out=True;process.terminate();process.wait(timeout=10)
   output.flush();lines=log.read_bytes()[offset:].decode('utf-8',errors='replace').splitlines()
   found=[json.loads(x.split('|',1)[1]) for x in lines if x.startswith(marker)];errs=[x for x in lines if any(t in x for t in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])];errors.extend(errs)
   check_ok=len(found)==1 and found[0]['checks']==count and found[0]['failures']==0 and (not width or found[0].get('width')==width)
   steps.append({'label':label,'command':command,'owned_pid':process.pid,'exit_code':process.returncode,'timed_out':timed_out,'checks_expected':count,'behavior_pass':check_ok})
   if found:evidence.append({'label':label,'fixture':fixture,**found[0]})
   print(json.dumps({'step':label,'exit_code':process.returncode,'checks':found[0]['checks'] if found else 0,'failures':found[0]['failures'] if found else None,'behavior_pass':check_ok,'errors':errs[:4]}),flush=True)
   if process.returncode or timed_out or not check_ok or errs:break
lines=log.read_text(encoding='utf-8',errors='replace').splitlines();errors=list(dict.fromkeys(errors+[x for x in lines if any(t in x for t in ['ERROR:','SCRIPT ERROR','Parse Error','Compile Error'])]))
after=resources();after['artifact_bytes']=sum(size(root/'tmp'/folder) for folder in set(c[2] for c in configs))+log.stat().st_size+preflight.stat().st_size;after['cache_growth_bytes']=max(0,after['cache_bytes']-before['cache_bytes']);resource_ok=after['C_free_bytes']>=FLOOR and after['artifact_bytes']<=OUTPUT_CAP and after['cache_growth_bytes']<=CACHE_CAP
matched=all(sha(root/b['path'])==b['sha256'] for b in sources);passed=len(steps)==9 and len(evidence)==5 and not errors and all(x['exit_code']==0 and x.get('behavior_pass',True) for x in steps) and matched and resource_ok
result={'started_utc':started,'finished_utc':utc(),'result':'PASS' if passed else 'FAIL','engine_version':version,'engine_sha256':engine_sha,'steps':steps,'evidence':evidence,'total_checks':sum(x['checks'] for x in evidence),'elapsed_seconds':round(time.monotonic()-begin,3),'time_cap_seconds':CAP,'resource_before':before,'resource_after':after,'resource_limits_pass':resource_ok,'sources':sources,'source_bindings_still_match':matched,'errors':errors,'log_path':log.relative_to(root).as_posix(),'log_sha256':sha(log),'preflight_sha256':sha(preflight),'meaning':'Refreshed original73pipe/17negative/57+57twoaspect correction/91ordinary allmechanics/save assertions on owned currentsource after release guard. Actual behavior, not visual/4.6/fulltrusted/independent/device/child/owner or integration acceptance.'};receipt.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':result['result'],'checks':result['total_checks'],'elapsed_seconds':result['elapsed_seconds'],'source_match':matched,'resource_pass':resource_ok,'errors':errors[:8],'receipt_sha256':sha(receipt)}),flush=True);sys.exit(0 if passed else 1)
