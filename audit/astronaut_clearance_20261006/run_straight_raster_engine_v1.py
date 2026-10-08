from pathlib import Path
import subprocess,time,json,hashlib,ctypes,shutil,sys,datetime
r=Path(__file__).resolve().parents[2];a=Path(__file__).resolve().parent
engine=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
log=a/'PIPE_STRAIGHT_RASTER_ENGINE_V1_LOG.txt';receipt=a/'PIPE_STRAIGHT_RASTER_ENGINE_V1_RECEIPT.json';preflight=a/'PIPE_STRAIGHT_RASTER_ENGINE_V1_PREFLIGHT.json'
assert not any(p.exists() for p in [log,receipt,preflight]);start=time.monotonic();cap=110;limit=64*1024**2;floor=3*1024**3
jobs=[r/'tmp/astronaut_birthday_straight_raster_v1_20261007',r/'tmp/astronaut_pipe_straight_raster_negative_v1_20261007'];assert all(not p.exists() for p in jobs)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def occupancy():
 q=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^godot.*\\.exe$' -and $_.Name -notmatch '^godot-ai\\.exe$' } | Select-Object ProcessId,CreationDate,ExecutablePath) | ConvertTo-Json -Compress"],capture_output=True,text=True,timeout=10,check=True)
 v=json.loads(q.stdout) if q.stdout.strip() else [];return v if isinstance(v,list) else [v]
class Memory(ctypes.Structure):_fields_=[('length',ctypes.c_uint32),('load',ctypes.c_uint32)]+[(n,ctypes.c_uint64) for n in ['total','avail','page_total','page_avail','virt_total','virt_avail','extended']]
def resources():
 m=Memory();m.length=ctypes.sizeof(m);assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m));return {'physical_available_bytes':m.avail,'C_free_bytes':shutil.disk_usage('C:/').free}
def files(tree):
 values={}
 if tree.exists():
  for p in tree.rglob('*'):
   try:
    if p.is_file():values[str(p)]=p.stat().st_size
   except FileNotFoundError:pass
 return values
before=files(r/'.godot');cache_peaks={};output_peaks={};samples=[];steps=[];abort=None
bindings=[r/'project.godot',r/'scripts/opera_astronaut_surface.gd',r/'scripts/opera_gesture_surface.gd',r/'scripts/opera_career_world_2d.gd',r/'scripts/opera_astronaut_pipe_work.gd',r/'scripts/opera_astronaut_patch_work.gd',r/'scripts/opera_astronaut_valve_work.gd',r/'scripts/save_state.gd',r/'assets/opera/worlds/widgets/astronaut_pipe_straight_candidate_v1.png',a/'verify_birthday_straight_raster_v1.gd',a/'verify_straight_raster_negative_v1.gd']
frozen=[{'path':p.relative_to(r).as_posix(),'sha256':sha(p)} for p in bindings]
commands=[('import',[str(engine),'--headless','--path',str(r),'--import']),('surface analyzer',[str(engine),'--headless','--path',str(r),'--script','res://scripts/opera_astronaut_surface.gd','--check-only']),('birthday144',[str(engine),'--headless','--path',str(r),'--script','res://audit/astronaut_clearance_20261006/verify_birthday_straight_raster_v1.gd']),('negative17',[str(engine),'--headless','--path',str(r),'--script','res://audit/astronaut_clearance_20261006/verify_straight_raster_negative_v1.gd'])]
queue=Path('C:/Users/Peter/.codex/worktrees/job-art-runtime-sync-20261004/mermaid-roshan-reef/audit/job_game_clearance_coordination_v1_20261006/RESOURCE_QUEUE_V15.json');q=json.loads(queue.read_text(encoding='utf-8'));occupied=occupancy();initial=resources()
assert q.get('current_heavy_lease') is None and q.get('short_cpu_lease') is None and not occupied,'Actual/shared engine occupancy prevents launch'
assert min(initial.values())>=floor
assert sha(engine)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
version=subprocess.check_output([str(engine),'--version'],text=True).strip();assert version=='4.7.2.stable.official.ed1daf0bf'
for p in jobs:p.mkdir(parents=True)
preflight.write_text(json.dumps({'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'engine':str(engine),'engine_version':version,'source_bindings':frozen,'cap_seconds':cap,'output_cap_bytes':limit,'cache_growth_cap_bytes':limit,'resources_before':initial,'queue_snapshot_utc':q.get('utc'),'occupied':occupied,'commands':commands,'scope':'Owned one-engine focused import/analyzer/headless diagnostics; no exclusivegrant or strictQA11/fulltrusted/native acceptance claimed.'},indent=2)+'\n',encoding='utf-8')
with log.open('xb') as out:
 for label,command in commands:
  if occupancy():abort='Another real Godot process appeared before launch';break
  if time.monotonic()-start>=cap:abort='110scombined cap before next command';break
  begin=time.monotonic();offset=out.tell();out.write((label+'\n').encode());out.flush();process=subprocess.Popen(command,cwd=r,stdout=out,stderr=subprocess.STDOUT);print(json.dumps({'started':label,'owned_pid':process.pid}),flush=True);last_size=0
  while process.poll() is None:
   state=resources();cache=files(r/'.godot');output={}
   for job in jobs:output.update(files(job))
   if log.exists():output[str(log)]=log.stat().st_size
   for path,size in cache.items():cache_peaks[path]=max(cache_peaks.get(path,0),max(0,size-before.get(path,0)))
   for path,size in output.items():output_peaks[path]=max(output_peaks.get(path,0),size)
   samples.append({'seconds':round(time.monotonic()-start,3),'physical_available_bytes':state['physical_available_bytes'],'C_free_bytes':state['C_free_bytes'],'cache_observed_growth':sum(cache_peaks.values()),'output_observed_positive_bytes':sum(output_peaks.values())})
   if time.monotonic()-start>=cap:abort='110scombined cap'
   elif min(state.values())<floor:abort='actualmemory/diskfloor'
   elif sum(cache_peaks.values())>limit or sum(output_peaks.values())>limit:abort='sampledoutput/cachecap'
   with log.open('rb') as stream:stream.seek(offset);current=stream.read()
   if any(marker in current for marker in [b'SCRIPT ERROR',b'Parse Error',b'Compile Error',b'ERROR:']):abort='engineerror;stopownedhandle'
   if abort:
    process.terminate()
    try:process.wait(timeout=3)
    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=3)
    break
   time.sleep(0.25)
  steps.append({'label':label,'owned_pid':process.pid,'exit_code':process.returncode,'elapsed_seconds':round(time.monotonic()-begin,3),'abort':abort});print(json.dumps(steps[-1]),flush=True)
  if abort or process.returncode:break
text=log.read_text(encoding='utf-8',errors='replace');results=[json.loads(line.split('|',1)[1]) for line in text.splitlines() if line.startswith(('ASTRO_BIRTHDAY_RESULT|','ASTRO_PIPE_RESULT|'))]
source_ok=all(sha(r/x['path'])==x['sha256'] for x in frozen);ok=not abort and len(steps)==4 and all(x['exit_code']==0 for x in steps) and [x['checks'] for x in results]==[144,17] and all(x['failures']==0 for x in results) and source_ok
record={'result':'PASS' if ok else 'FAIL','closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'combined_seconds':round(time.monotonic()-start,3),'cap_seconds':cap,'steps':steps,'abort':abort,'evidence':results,'source_bindings':frozen,'source_bindings_match':source_ok,'resource_samples':samples,'cache_observed_growth_bytes':sum(cache_peaks.values()),'output_observed_positive_bytes':sum(output_peaks.values()),'sampling_limit':'Discrete rotating-file snapshots, not continuousmemory/output proof. Only direct standaloneprocess ownership is claimed.','log_sha256':sha(log),'native_runs':0,'scope':'CurrentH/Vcandidate focused143oldbirthdayassertions+1textureidentity and17negatives. Priorstoryfixture; no naturalfullroute/fulltrusted/nativeart/device/child/owner acceptance.'}
receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'result':record['result'],'seconds':record['combined_seconds'],'counts':[x['checks'] for x in results],'failures':[x['failures'] for x in results],'abort':abort,'source_match':source_ok,'receipt_sha256':sha(receipt)}),flush=True);sys.exit(0 if ok else 1)
