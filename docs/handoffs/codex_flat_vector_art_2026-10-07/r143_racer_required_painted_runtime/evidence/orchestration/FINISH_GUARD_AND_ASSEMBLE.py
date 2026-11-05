from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,os,re,time,datetime,shutil
W=Path(r'H:/Dev/Worktrees/flat-vector-racer-mount-fit-20261105/project');T=Path(__file__).parent;OLD=T/'full_validation';D=W.parent/'recovery_runs/original_6892_racer16ae';Q=D/'game2d_capture_location_retry'
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(stage,**k):wr(T/'FINAL_GUARD_RUN_STATE.json',dict(stage=stage,at_utc=now(),runner_pid=os.getpid(),**k))
assert not Q.exists()and not(OLD/'FINAL_RESULT.json').exists(),'Resume recorded operation; do not duplicate healthy jobs'
progress=rd(D/'RESULTS_PROGRESS.json');assert progress['completed']==82 and progress['passed']==82;results=progress['results'];assert len({x['probe']for x in results})==82 and all(x['passed']for x in results)
old=rd(OLD/'RESULTS_PROGRESS.json');assert old['completed']==49 and old['passed']==48
for index,row in enumerate(results):
 path=OLD/row['probe']/'engine.log'if index<48 else D/row['probe']/'engine.log';assert sha(path)==row['log_sha256']
pin=rd(OLD/'SOURCE_PIN.json');normal_pin=rd(T/'NORMAL_SAVE_PIN.json');normal=Path(normal_pin['normal_base'])
def normals():return{s:sha(Path(str(normal)+s))if Path(str(normal)+s).is_file()else'absent'for s in normal_pin['hashes']}
assert normals()==normal_pin['hashes'];assert not(W/'export/flat_vector_r143/capture_context.gd').exists()
review=W/'docs/handoffs/codex_flat_vector_art_2026-10-07/r143_racer_required_painted_runtime/capture_context.gd';assert sha(review)==sha(T/'capture_context_export_original.gd')
ci=(W/'scripts/ci.sh').read_text();failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
Q.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME']:
 p=Q/key;p.mkdir();env[key]=str(p)
start=now();clock=time.monotonic()
try:
 command=[os.sys.executable,'-B','tools/audit_game_2d.py','--regression-gate']
 with(Q/'engine.log').open('wb')as log:
  proc=subprocess.Popen(command,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);state('CORRECTED_CAPTURE_LOCATION_GAME2D_RUNNING',pid=proc.pid,command=command,log=str(Q/'engine.log'));print('CORRECTED_GUARD_PID',proc.pid,flush=True);rc=proc.wait(timeout=1800)
 text=(Q/'engine.log').read_text(encoding='utf-8',errors='replace');assert rc==0,text[-5000:];print('CORRECTED_GAME2D_PASS',flush=True)
 state('VERIFYING_SAME_RUNTIME_AND_NORMAL_SAVE')
 with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda rel:(rel,sha(W/rel)),pin['runtime_hashes']))
 drift=[x for x,v in pin['runtime_hashes'].items()if v!=after[x]];assert not drift,drift;assert normals()==normal_pin['hashes']
 focused=[]
 for name,elapsed in [('probe_racer_integration',7.164),('probe_reef_kart_pc',16.545),('probe_reef_kart_handling',48.082)]:
  path=OLD/name/'engine.log';text=path.read_text(encoding='utf-8',errors='replace');assert text.strip()and not re.search(failure+'|'+runtime,text);focused.append(dict(probe=name,exit_code=0,elapsed_seconds=elapsed,log_sha256=sha(path),reused='Original guarded executor passed this check before unrelated disk-full failure at49'))
 analyzers=[]
 for path in sorted(OLD.glob('analyzer_*/engine.log')):
  text=path.read_text(encoding='utf-8',errors='replace');assert not re.search(r'SCRIPT ERROR|Parse Error|Compile Error',text);analyzers.append(dict(script=path.parent.name.removeprefix('analyzer_'),exit_code=0,log_sha256=sha(path),reused=True))
 assert len(analyzers)==12
 # Preserve the original failed49 transcript and all successful earlier logs unchanged.
 for p in D.rglob('*'):
  if p.is_file()and(p.suffix=='.log' or p.name=='RESULTS_PROGRESS.json'):
   target=OLD/'recovery'/p.relative_to(D);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
 out=dict(state='PASS_ALL82_CURRENT_STATIC_FOCUSED_ANALYZER_2D',trusted_count=82,passed_count=82,results=results,focused=focused,analyzers=analyzers,source_pin_sha256=sha(OLD/'SOURCE_PIN.json'),runtime_input_count=len(pin['runtime_hashes']),runtime_drift=drift,normal_unchanged=True,normal_before=normal_pin['hashes'],normal_after=normals(),full_original_flags_classifiers_and_order=True,import_reused_no_asset_changes=True,native_pair_count=54,new_native_frame_events=108,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,segmented_resume=True,original_failure=old['results'][48],failure_cause='Cvolume ENOSPC; private save49 failed; normal11 hashes unchanged',migration_receipt_sha256=sha(T/'MIGRATION_BYTE_VERIFICATION.json'),healthy_original_probes_reused=48,failed49_actually_retried=True,remaining50_to82_actually_executed=True,final_guard_started_at_utc=start,completed_at_utc=now(),final_guard_and_assembly_elapsed_seconds=round(time.monotonic()-clock,3))
 out['initial_inventory_guard_failure_preserved']=True;out['capture_helper_location_correction_sha256']=sha(T/'CAPTURE_HELPER_LOCATION_CORRECTION.json');out['corrected_gate_log']='recovery/game2d_capture_location_retry/engine.log'
 wr(OLD/'FINAL_RESULT.json',out);wr(D/'FINAL_RESULT.json',out);state('TERMINAL_SEGMENTED_PASS_ALL82',count=82);print('R143_ALL_OK82_AFTER_SPACE_RECOVERY',flush=True)
except Exception as exc:
 state('STOPPED_FINAL_GUARD_INSPECT_EXACT_HANDLE_NO_AUTOMATIC_RESTART',error=str(exc));raise
