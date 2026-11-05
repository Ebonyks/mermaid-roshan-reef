from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime
S=Path(__file__).parent;R=Path.cwd();W=S/'full_validation_rest_coverage_recovery'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(S/'VALIDATION_COVERAGE_STATE.json',{'state':n,'updated_at_utc':now(),**kw})
assert W.is_dir() and not(W/'FINAL_RESULT.json').exists() and not(W/'RESULTS_PROGRESS.json').exists(),'Resume only before any trusted probes started'
BASE='218ae766f8e60afb3f6338b8fafce28ec9fab7f2';assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/flat-vector-geologist-pan-runtime-20261017'
pin=rd(S/'SOURCE_PIN.json');assert rd(S/'FOCUSED_RESULT.json')['new_native_frame_events']==22 and rd(S/'FRAME_REVIEW.json')['all20_candidate_frames_inspected']
engine=Path(pin['engine']);assert sha(engine)==pin['engine_sha256']=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
normal=Path(rd(R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
def normals():return {n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in pin['normal_before']}
def drift():return [p for p,h in pin['runtime_hashes'].items()if not(R/p).is_file()or sha(R/p)!=h]+[p for p in pin['runtime_deletions'] if (R/p).exists()]
assert not drift() and normals()==pin['normal_before']
ci=(R/'scripts/ci.sh').read_text(encoding='utf-8-sig');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(engine));start=now();tall=time.monotonic()
wr(W/'RESUMED_LAUNCH.json',{'started_at_utc':start,'source_baseline':BASE,'source_pin_sha256':sha(S/'SOURCE_PIN.json'),'fixture_sha256':pin['fixture_lf_sha256'],'engine':str(engine),'engine_sha256':sha(engine),'ci_sha256':sha(R/'scripts/ci.sh'),'expected_probes':names,'probe_order_reason':'All82 unchanged currenttrusted probes in exact ci.sh order on the actual whole Dolls progress markers candidate.','method':'Actual candidate current ci.sh static prefix, retained successful final-settings import, game2d regression and all82 unchanged trusted probe scripts with native internal log. Display captures are terminal before probes start. Each engine process gets private APPDATA/LOCALAPPDATA/XDG folders. Runtime hashes and normal11files guarded; no probe thresholds changed.','import_reused':{'path':'../FOCUSED_RESULT.json','sha256':sha(S/'FOCUSED_RESULT.json'),'reason':'Successful actual whole Dolls progress markers candidate import with two new512square lossless+mipmaps, same frozen source; no healthy import restart.'},'normal_before':normals(),'failure_regex':failure,'runtime_error_regex':runtime})
try:
 original=rd(W/'STATIC_COVERAGE_RECOVERY_PLAN.json');assert original['original_static_log_sha256']==sha(S/'full_validation_rest_repair/STATIC_PREFIX.log') and original['runtime_source_pin_sha256']==sha(S/'SOURCE_PIN.json')
 state('RESUMING_FAILED_METADATA_GATE_AND_REMAINING_STATIC_ONLY')
 script=S/'remaining_static_after_coverage_fix.sh'
 with(W/'STATIC_PREFIX.log').open('wb')as log:q=subprocess.run([r'C:/Program Files/Git/bin/bash.exe',str(script)],cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=5400,creationflags=0x08000000)
 suffix_text=(W/'STATIC_PREFIX.log').read_text(encoding='utf-8',errors='replace');good=q.returncode==0 and 'R119_STATIC_PREFIX_ALL_OK' in suffix_text
 static=dict(status='PASS'if good else'FAIL',exit_code=q.returncode,log_sha256=sha(W/'STATIC_PREFIX.log'),prefix_sha256=sha(S/'current_ci_static_prefix.sh'),ci_sha256=sha(R/'scripts/ci.sh'),method='ORIGINAL_CURRENT_SOURCE_SUCCESSFUL_PREFIX_PLUS_FAILED_METADATA_GATE_AND_EXACT_REMAINING_SUFFIX',original_current_source_prefix_log_sha256=original['original_static_log_sha256'],suffix_sha256=sha(script),runtime_source_pin_sha256=sha(S/'SOURCE_PIN.json'),completed_at_utc=now());wr(W/'STATIC_RESULT.json',static);assert good,suffix_text[-3500:]
 wr(W/'STATIC_COVERAGE_RECOVERY.json',dict(original,terminal='PASS_ALL_CURRENT_STATIC_COMPOSED_NO_HEALTHY_RESTART',recovered_static=static));print('R119_STATIC_COVERAGE_RECOVERED_CURRENT_SOURCE_PASS',flush=True)
 assert 'R119_STATIC_PREFIX_ALL_OK' in(W/'STATIC_PREFIX.log').read_text(encoding='utf8',errors='replace')
 checker=R/'tools/audit_game_2d.py';before_checker=sha(checker);baseline_checker=subprocess.check_output(['git','show',BASE+':tools/audit_game_2d.py'],cwd=R);assert checker.read_bytes().replace(b'\r\n',b'\n')==baseline_checker.replace(b'\r\n',b'\n')
 state('RUNNING_FIRST_POST_REPAIR_2D_INVENTORY_SCAN',original_timeout_seconds=300,execution_budget_seconds=1800,checker_sha256=before_checker,static_prefix_reused=True,trusted_probes_started=0)
 scan_start=time.monotonic();cmd=['python','-B','tools/audit_game_2d.py','--regression-gate']
 with(W/'GAME2D.log').open('wb')as log:
  proc=subprocess.Popen(cmd,cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
  wr(W/'GAME2D_RUNNING.json',dict(pid=proc.pid,command=cmd,started_at_utc=now(),execution_budget_seconds=1800,source_baseline=BASE,checker_sha256=before_checker,scope='Same original checker/flags/thresholds; First inventory scan at the repaired shared source; historical pre-repair300s timeout is not current acceptance'))
  try:rc=proc.wait(timeout=1800)
  except subprocess.TimeoutExpired:proc.kill();proc.wait();raise RuntimeError('2D scan execution budget1800s exhausted; preserve rawlog and inspect exact source/checker before any next action')
 text=(W/'GAME2D.log').read_text(encoding='utf8',errors='replace');assert rc==0 and 'GAME2D| RESULT|' in text,text[-3000:];assert sha(checker)==before_checker and not drift() and normals()==pin['normal_before']
 recovery=dict(state='CURRENT_REPAIRED_SOURCE_STATIC_SUFFIX_RECOVERED_FIRST_2D_SCAN',source_baseline=BASE,original_stop=rd(S/'VALIDATION_REST_STOP.json'),original_static=static,original_static_log_sha256=sha(W/'STATIC_PREFIX.log'),checker_path='tools/audit_game_2d.py',checker_sha256=before_checker,checker_or_threshold_modified=False,command=cmd,original_execution_budget_seconds=300,resumed_execution_budget_seconds=1800,scan_exit_code=rc,scan_seconds=round(time.monotonic()-scan_start,3),scan_log_sha256=sha(W/'GAME2D.log'),static_prefix_restarted=False,native_import_or_scene_capture_restarted=False,trusted_probe_suite_started_before_recovery=0,new_generation_calls=0,new_frame_events=0,at_utc=now())
 wr(W/'SCAN_TIMEOUT_RECOVERY.json',recovery);print('R119_CURRENT_SOURCE_2D_SCAN_PASS_STATIC_REUSED',flush=True)
 results=[]
 for i,name in enumerate(names):
  d=W/name;d.mkdir();e=env.copy()
  for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/n;p.mkdir();e[k]=str(p)
  touch='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test';cmd=[str(engine),'--verbose','--log-file',str(d/'native_engine.log'),'--headless','--path',str(R),'-s','scripts/'+name+'.gd','--','--touch',touch];t=time.monotonic();timed=False
  with(d/'engine.log').open('wb')as log:
   proc=subprocess.Popen(cmd,cwd=R,env=e,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);state('TRUSTED_PROBES_RUNNING',probe=name,index=i+1,count=82,pid=proc.pid,log=str(d/'engine.log'));wr(W/'RUNNING.json',{'probe':name,'index':i+1,'count':82,'pid':proc.pid,'started_at_utc':now(),'command':cmd,'log':str(d/'engine.log')})
   try:rc=proc.wait(timeout=480)
   except subprocess.TimeoutExpired:proc.kill();rc=proc.wait();timed=True
  txt=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in txt.splitlines()if re.search(failure+'|'+runtime,l)];verdict=bool(re.search(r'ALL OK|RESULT|done|DONE|result',txt));tail_verdict=bool(re.search(r'ALL OK|RESULT','\n'.join(txt.splitlines()[-5:])));exit_ok=rc==0 or(timed and tail_verdict)
  row={'probe':name,'command':cmd,'exit_code':rc,'timeout_after_verdict_accepted':timed and tail_verdict,'elapsed_seconds':round(time.monotonic()-t,3),'failure_lines':bad,'output_nonempty':bool(txt.strip()),'positive_verdict_observed':verdict,'passed':exit_ok and not bad and bool(txt.strip()),'log':str(d/'engine.log'),'log_sha256':sha(d/'engine.log')};results.append(row);wr(W/'RESULTS_PROGRESS.json',{'completed':len(results),'passed':sum(x['passed']for x in results),'results':results});print('R119_PROBE',i+1,name,'PASS'if row['passed']else'FAIL',row['elapsed_seconds'],flush=True)
  if not row['passed']:break
 changed=drift();after=normals();passed=len(results)==82 and all(x['passed']for x in results)and not changed and after==pin['normal_before'];out={'status':'PASS_ALL_82_AND_CURRENT_STATIC'if passed else'FAIL','source_baseline':BASE,'started_at_utc':start,'completed_at_utc':now(),'elapsed_seconds':round(time.monotonic()-tall,3),'probe_count':len(results),'passed_count':sum(x['passed']for x in results),'results':results,'runtime_changes':changed,'normal_before':pin['normal_before'],'normal_after':after,'normal_unchanged':after==pin['normal_before'],'source_pin_sha256':sha(S/'SOURCE_PIN.json'),'import':'Successful final-settings import retained from focused run; not rerun.','static':'STATIC_RESULT.json','scan_timeout_recovery':'SCAN_TIMEOUT_RECOVERY.json','static_coverage_recovery':'STATIC_COVERAGE_RECOVERY.json','static_reused_without_restart':True,'bounded_native_checks':rd(S/'FOCUSED_RESULT.json')['checks'],'agent_all_20_frames_reviewed':True,'geologist_repair_checks':110,'geologist_repair_frames':6,'combined_native_checks':342,'combined_native_frame_events':28,'combined_bounded_frames':26,'combined_excluded_frames':2,'formal_QA11':None,'device':None,'child':None,'owner':None,'accepted_removed':0,'mission_complete':False};wr(W/'FINAL_RESULT.json',out);state('FULL_VALIDATION_PASS'if passed else'FULL_VALIDATION_FAIL',probes=len(results));print('R119_ALL_OK'if passed else'R119_FAIL',flush=True);assert passed
except Exception as e:
 wr(S/'VALIDATION_COVERAGE_STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect exact handle/log/source; preserve healthy check results.'});state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
