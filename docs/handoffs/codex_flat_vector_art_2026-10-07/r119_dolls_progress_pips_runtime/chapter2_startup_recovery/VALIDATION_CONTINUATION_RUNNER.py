from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime,shutil
S=Path(__file__).parent;U=Path.cwd();OLD=S/'full_validation_rest_coverage_recovery';W=S/'full_validation_chapter2_child_recovery';D=S/'chapter2_startup_recovery'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(S/'VALIDATION_CH2DIAG_STATE.json',dict(state=n,at_utc=now(),**kw))
assert not W.exists(),'Never duplicate a current recovery'
base=rd(OLD/'FINAL_RESULT.json');pin=rd(S/'SOURCE_PIN.json');plan=rd(D/'CURRENT_RETRY_PLAN.json');assert base['probe_count']==72 and base['passed_count']==71 and not base['runtime_changes'] and base['normal_unchanged'];assert base['source_pin_sha256']==sha(S/'SOURCE_PIN.json')==plan['source_pin_sha256'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='218ae766f8e60afb3f6338b8fafce28ec9fab7f2'
engine=Path(pin['engine']);assert sha(engine)==pin['engine_sha256'];ci=(U/'scripts/ci.sh').read_text(encoding='utf-8-sig');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82 and names[71]=='probe_chapter2';failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
normal=Path(rd(U/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
def normals():return {n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in pin['normal_before']}
def drift():return [p for p,h in pin['runtime_hashes'].items()if not(U/p).is_file()or sha(U/p)!=h]+[p for p in pin['runtime_deletions']if(U/p).exists()]
try:
 assert not drift() and normals()==pin['normal_before'];assert rd(OLD/'STATIC_RESULT.json')['status']=='PASS';assert rd(OLD/'SCAN_TIMEOUT_RECOVERY.json')['scan_exit_code']==0
 for row in base['results'][:71]:assert row['passed']and sha(Path(row['log']))==row['log_sha256']
 W.mkdir();start=time.monotonic();started=now();results=base['results'][:71];loads=[]
 for name in ['STATIC_RESULT.json','STATIC_PREFIX.log','STATIC_COVERAGE_RECOVERY.json','GAME2D.log','SCAN_TIMEOUT_RECOVERY.json','RESUMED_LAUNCH.json']:
  shutil.copy2(OLD/name,W/name)
 wr(W/'LAUNCH.json',dict(source_baseline=base['source_baseline'],source_pin_sha256=sha(S/'SOURCE_PIN.json'),engine=str(engine),engine_sha256=sha(engine),ci_sha256=sha(U/'scripts/ci.sh'),expected_probes=names,started_at_utc=started,method='Retain71exact-source successful probes and completed static/2D; one unchanged Chapter2retry after measured host capacity, then73..82once. Original30second child deadline,480second outer deadlines,classifiers,source and all trusted probe bytes unchanged. Preserve original failure; no performance or product acceptance from capacity sampling.',retry_plan_sha256=sha(D/'CURRENT_RETRY_PLAN.json'),normal_before=normals()))
 wr(W/'RESULTS_PROGRESS.json',dict(completed=71,passed=71,results=results,prior_failed_attempt=base['results'][-1]))
 env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(engine));ready=False
 diag=rd(S/'chapter2_standalone_child_diagnostic/RESULT.json');assert diag['exit_code']==0 and diag['child_result_observed']and diag['receipt_written']and diag['elapsed_seconds']<30 and not diag['original_trusted_gate_satisfied']
 assert not(D/'ORIGINAL_GATE_RETRY_DISPATCHED.json').exists(),'Originalgate retry cap already used'
 wr(D/'EXECUTION_BASIS.json',dict(state='EXACT_ORIGINAL_CHILD_DIAGNOSTIC_COMPLETED_INSIDE_UNCHANGED30S_BUDGET',diagnostic=diag,diagnostic_is_not_original_gate_acceptance=True,source_pin_sha256=sha(S/'SOURCE_PIN.json'),previous_capacity_wait_ended_without_probe_dispatch=True,original_child_deadline_ms=30000,original_failed_probe_retry_cap=1,at_utc=now()))
 print('R119_CHAPTER2_DIAGNOSTIC_BASIS_CONFIRMED_UNCHANGED_ORIGINAL_RETRY',flush=True)
 for i in range(71,82):
  name=names[i];d=W/name;d.mkdir();e=env.copy()
  for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/n;p.mkdir();e[k]=str(p)
  touch='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test';cmd=[str(engine),'--verbose','--log-file',str(d/'native_engine.log'),'--headless','--path',str(U),'-s','scripts/'+name+'.gd','--','--touch',touch];t=time.monotonic();timed=False
  if i==71:
   with(D/'ORIGINAL_GATE_RETRY_DISPATCHED.json').open('x',encoding='utf-8')as mark:json.dump(dict(original_gate_retry_number=1,command=cmd,source_pin_sha256=sha(S/'SOURCE_PIN.json'),original_child_deadline_ms=30000,at_utc=now()),mark,indent=2)
  with(d/'engine.log').open('wb')as f:
   proc=subprocess.Popen(cmd,cwd=U,env=e,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);state('ORIGINAL_TRUSTED_PROBES_RUNNING_WITH71_PRIOR_PASSES_RETAINED',probe=name,index=i+1,count=82,pid=proc.pid,log=str(d/'engine.log'));wr(W/'RUNNING.json',dict(probe=name,index=i+1,count=82,pid=proc.pid,command=cmd,started_at_utc=now()))
   try:rc=proc.wait(timeout=480)
   except subprocess.TimeoutExpired:proc.kill();rc=proc.wait();timed=True
  text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in text.splitlines()if re.search(failure+'|'+runtime,l)];tail=bool(re.search(r'ALL OK|RESULT','\n'.join(text.splitlines()[-5:])));row=dict(probe=name,command=cmd,exit_code=rc,timeout_after_verdict_accepted=timed and tail,elapsed_seconds=round(time.monotonic()-t,3),failure_lines=bad,output_nonempty=bool(text.strip()),positive_verdict_observed=bool(re.search(r'ALL OK|RESULT|done|DONE|result',text)),passed=(rc==0 or(timed and tail))and not bad and bool(text.strip()),log=str(d/'engine.log'),log_sha256=sha(d/'engine.log'));results.append(row);wr(W/'RESULTS_PROGRESS.json',dict(completed=len(results),passed=sum(x['passed']for x in results),results=results,prior_failed_attempt=base['results'][-1]));print('R119_PROBE',i+1,name,'PASS'if row['passed']else'FAIL',row['elapsed_seconds'],flush=True)
  if not row['passed']:break
 changed=drift();after=normals();passed=len(results)==82 and all(x['passed']for x in results)and not changed and after==pin['normal_before'];out=dict(base);out.update(status='PASS_ALL_82_AND_CURRENT_STATIC'if passed else'FAIL',completed_at_utc=now(),elapsed_seconds=round(base['elapsed_seconds']+time.monotonic()-start,3),probe_count=len(results),passed_count=sum(x['passed']for x in results),results=results,runtime_changes=changed,normal_after=after,normal_unchanged=after==pin['normal_before'],chapter2_startup_recovery='CHAPTER2_STARTUP_RECOVERY.json',prior_failed_attempts=[base['results'][-1]],healthy_static_or71probes_restarted=False)
 recovery=dict(plan,state='RECOVERED_ALL82_SAME_SOURCE'if passed else'RETRY_OR_REMAINING_PROBE_FAILED_STOP',execution_basis=rd(D/'EXECUTION_BASIS.json'),original_failed_attempt=base['results'][-1],replayed_chapter2=results[71],static_and71healthy_probes_restarted=False,remaining73through82_executed_once=passed,normal_unchanged=out['normal_unchanged'],runtime_changes=changed,at_utc=now());wr(W/'CHAPTER2_STARTUP_RECOVERY.json',recovery);wr(W/'FINAL_RESULT.json',out);state('ALL82_CURRENT_STATIC_PASS_RECOVERED_SINGLE_CHAPTER2_RETRY'if passed else'FAILED_NO_MORE_RETRIES',probes=len(results),passed=out['passed_count']);print('R119_ALL_OK'if passed else'R119_FAIL',flush=True);assert passed
except Exception as e:wr(S/'VALIDATION_CH2DIAG_STOP.json',dict(state='STOPPED_INSPECT_EXACT_CAPACITY_OR_ORIGINAL_GATE_FAILURE_NO_RETRY',error=str(e),at_utc=now()));state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
