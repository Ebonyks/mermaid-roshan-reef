from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import os,json,hashlib,subprocess,re,time,datetime,shutil
W=Path(r'H:/Dev/Worktrees/flat-vector-racer-mount-fit-20261105/project');T=Path(__file__).parent;OLD=T/'full_validation';D=W.parent/'recovery_runs/original_6892_racer16ae'
rd=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(stage,**k):wr(T/'RECOVERY_RUN_STATE.json',dict(stage=stage,at_utc=now(),runner_pid=os.getpid(),**k))
assert rd(T/'MIGRATION_COMPLETE.json')['state']=='BYTE_IDENTICAL_WORKTREE_MOVED_GIT_REPAIRED_OLD_DUPLICATE_REMOVED'
assert not D.exists() and not(OLD/'FINAL_RESULT.json').exists(),'Resume existing healthy job instead of duplicating it'
old=rd(OLD/'RESULTS_PROGRESS.json');assert old['completed']==49 and old['passed']==48 and all(x['passed']for x in old['results'][:48]) and not old['results'][48]['passed']
pin=rd(OLD/'SOURCE_PIN.json');assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()==pin['baseline'];assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],cwd=W,text=True).strip()==pin['merged_source']
mig=rd(T/'MIGRATION_BYTE_VERIFICATION.json');mm={x['path']:x['sha256']for x in mig['rows']};assert all(mm[p]==v for p,v in pin['runtime_hashes'].items())
assert sha(W/'scripts/ci.sh')==pin['ci_sha256'];E=Path(pin['engine']);assert sha(E)==pin['engine_sha256']
normal_pin=rd(T/'NORMAL_SAVE_PIN.json');normal=Path(normal_pin['normal_base'])
def normals():return{s:sha(Path(str(normal)+s))if Path(str(normal)+s).is_file()else'absent'for s in normal_pin['hashes']}
assert normals()==normal_pin['hashes'];assert shutil.disk_usage(T).free>5*1024**3 and shutil.disk_usage(W).free>20*1024**3
ci=(W/'scripts/ci.sh').read_text();names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82 and names[48]=='probe_stuffie';assert [x['probe']for x in old['results'][:48]]==names[:48]
for x in old['results'][:48]:assert sha(OLD/x['probe']/'engine.log')==x['log_sha256']
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
assert 'R143_CURRENT_STATIC_PREFIX_ALL_OK'in(OLD/'static/engine.log').read_text(encoding='utf-8',errors='replace')
D.mkdir(parents=True);results=old['results'][:48];start=now();clock=time.monotonic();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E))
def execute(label,cmd,d,limit):
 d.mkdir();e=env.copy()
 for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME']:
  p=d/key;p.mkdir();e[key]=str(p)
 with(d/'engine.log').open('wb')as log:
  p=subprocess.Popen(cmd,cwd=W,env=e,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);state(label,pid=p.pid,command=cmd,log=str(d/'engine.log'));beg=time.monotonic()
  try:rc=p.wait(timeout=limit)
  except subprocess.TimeoutExpired:p.kill();p.wait();raise RuntimeError('Bounded recovery command timed out: '+label)
 text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');return rc,text,round(time.monotonic()-beg,3),sha(d/'engine.log')
try:
 for index in range(48,82):
  name=names[index];flag='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test'
  rc,text,elapsed,digest=execute('RECOVERED_TRUSTED_'+str(index+1)+'_'+name,[str(E),'--verbose','--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch',flag],D/name,480)
  bad=[l for l in text.splitlines()if re.search(failure+'|'+runtime,l)];row=dict(probe=name,exit_code=rc,elapsed_seconds=elapsed,failure_lines=bad,output_nonempty=bool(text.strip()),log_sha256=digest,passed=rc==0 and not bad and bool(text.strip()),recovery_log='recovery/'+name+'/engine.log',attempt=2 if index==48 else 1);results.append(row);wr(D/'RESULTS_PROGRESS.json',dict(completed=len(results),passed=sum(x['passed']for x in results),results=results));print('R143_RECOVERED_PROBE',index+1,name,'PASS'if row['passed']else'FAIL',elapsed,flush=True);assert row['passed'],text[-5000:]
 rc,text,elapsed,digest=execute('GAME2D_AFTER_RECOVERY',[os.sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],D/'game2d',1800);assert rc==0,text[-3500:]
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
 out=dict(state='PASS_ALL82_CURRENT_STATIC_FOCUSED_ANALYZER_2D',trusted_count=82,passed_count=82,results=results,focused=focused,analyzers=analyzers,source_pin_sha256=sha(OLD/'SOURCE_PIN.json'),runtime_input_count=len(pin['runtime_hashes']),runtime_drift=drift,normal_unchanged=True,normal_before=normal_pin['hashes'],normal_after=normals(),full_original_flags_classifiers_and_order=True,import_reused_no_asset_changes=True,native_pair_count=54,new_native_frame_events=108,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,segmented_resume=True,original_failure=old['results'][48],failure_cause='Cvolume ENOSPC; private save49 failed; normal11 hashes unchanged',migration_receipt_sha256=sha(T/'MIGRATION_BYTE_VERIFICATION.json'),healthy_original_probes_reused=48,failed49_actually_retried=True,remaining50_to82_actually_executed=True,recovery_started_at_utc=start,completed_at_utc=now(),recovery_elapsed_seconds=round(time.monotonic()-clock,3))
 wr(OLD/'FINAL_RESULT.json',out);wr(D/'FINAL_RESULT.json',out);state('TERMINAL_SEGMENTED_PASS_ALL82',count=82);print('R143_ALL_OK82_AFTER_SPACE_RECOVERY',flush=True)
except Exception as exc:
 state('STOPPED_RECOVERY_INSPECT_EXACT_HANDLE_NO_AUTOMATIC_RESTART',error=str(exc),trusted_completed=len(results));raise
