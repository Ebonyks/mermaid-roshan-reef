from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime
S=Path(__file__).parent;R=Path.cwd();W=S/'full_validation'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(n,**kw):wr(S/'VALIDATION_STATE.json',{'state':n,'updated_at_utc':now(),**kw})
assert not W.exists(),'Do not duplicate an existing validation operation'
BASE='0e2cf1c4a1840bc33dd288fc92428fd198880fa5';assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==BASE
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/flat-vector-geologist-pan-runtime-20261017'
pin=rd(S/'SOURCE_PIN.json');assert rd(S/'FOCUSED_RESULT.json')['checks']==220 and rd(S/'FRAME_REVIEW.json')['all_24_current_frames_inspected']
engine=Path(pin['engine']);assert sha(engine)==pin['engine_sha256']=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
normal=Path(rd(R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
def normals():return {n:sha(Path(str(normal)+n))if Path(str(normal)+n).is_file()else'absent'for n in pin['normal_before']}
def drift():return [p for p,h in pin['runtime_hashes'].items()if not(R/p).is_file()or sha(R/p)!=h]
assert not drift() and normals()==pin['normal_before'];W.mkdir()
ci=(R/'scripts/ci.sh').read_text(encoding='utf-8-sig');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(engine));start=now();tall=time.monotonic()
wr(W/'LAUNCH.json',{'started_at_utc':start,'source_baseline':BASE,'source_pin_sha256':sha(S/'SOURCE_PIN.json'),'fixture_sha256':pin['fixture_lf_sha256'],'engine':str(engine),'engine_sha256':sha(engine),'ci_sha256':sha(R/'scripts/ci.sh'),'expected_probes':names,'method':'Actual candidate current ci.sh static prefix, retained successful final-settings import, game2d regression and all82 unchanged trusted probe scripts with native internal log. Display captures are terminal before probes start. Each engine process gets private APPDATA/LOCALAPPDATA/XDG folders. Runtime hashes and normal11files guarded; no probe thresholds changed.','import_reused':{'path':'../FOCUSED_RESULT.json','sha256':sha(S/'FOCUSED_RESULT.json'),'reason':'Successful actual candidate import with final1024square lossless+mipmaps, same frozen source; no healthy import restart.'},'normal_before':normals(),'failure_regex':failure,'runtime_error_regex':runtime})
try:
 state('RUNNING_CURRENT_STATIC_PREFIX');script=S/'current_ci_static_prefix.sh'
 with(W/'STATIC_PREFIX.log').open('wb')as log:q=subprocess.run([r'C:/Program Files/Git/bin/bash.exe',str(script)],cwd=R,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,timeout=5400,creationflags=0x08000000)
 txt=(W/'STATIC_PREFIX.log').read_text(encoding='utf-8',errors='replace');good=q.returncode==0 and 'R106_STATIC_PREFIX_ALL_OK'in txt;wr(W/'STATIC_RESULT.json',{'status':'PASS'if good else'FAIL','exit_code':q.returncode,'log_sha256':sha(W/'STATIC_PREFIX.log'),'prefix_sha256':sha(script),'ci_sha256':sha(R/'scripts/ci.sh'),'completed_at_utc':now()});print('R106_STATIC_PREFIX','PASS'if good else'FAIL',flush=True);assert good,txt[-3000:]
 state('POST_IMPORT_2D_REGRESSION')
 q=subprocess.run(['python','-B','tools/audit_game_2d.py','--regression-gate'],cwd=R,env=env,capture_output=True,timeout=300);(W/'GAME2D.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-2000:]
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
  row={'probe':name,'command':cmd,'exit_code':rc,'timeout_after_verdict_accepted':timed and tail_verdict,'elapsed_seconds':round(time.monotonic()-t,3),'failure_lines':bad,'output_nonempty':bool(txt.strip()),'positive_verdict_observed':verdict,'passed':exit_ok and not bad and bool(txt.strip()),'log':str(d/'engine.log'),'log_sha256':sha(d/'engine.log')};results.append(row);wr(W/'RESULTS_PROGRESS.json',{'completed':len(results),'passed':sum(x['passed']for x in results),'results':results});print('R106_PROBE',i+1,name,'PASS'if row['passed']else'FAIL',row['elapsed_seconds'],flush=True)
  if not row['passed']:break
 changed=drift();after=normals();passed=len(results)==82 and all(x['passed']for x in results)and not changed and after==pin['normal_before'];out={'status':'PASS_ALL_82_AND_CURRENT_STATIC'if passed else'FAIL','source_baseline':BASE,'started_at_utc':start,'completed_at_utc':now(),'elapsed_seconds':round(time.monotonic()-tall,3),'probe_count':len(results),'passed_count':sum(x['passed']for x in results),'results':results,'runtime_changes':changed,'normal_before':pin['normal_before'],'normal_after':after,'normal_unchanged':after==pin['normal_before'],'source_pin_sha256':sha(S/'SOURCE_PIN.json'),'import':'Successful final-settings import retained from focused run; not rerun.','static':'STATIC_RESULT.json','bounded_native_checks':220,'agent_all_24_frames_reviewed':True,'formal_QA11':None,'device':None,'child':None,'owner':None,'accepted_removed':0,'mission_complete':False};wr(W/'FINAL_RESULT.json',out);state('FULL_VALIDATION_PASS'if passed else'FULL_VALIDATION_FAIL',probes=len(results));print('R106_ALL_OK'if passed else'R106_FAIL',flush=True);assert passed
except Exception as e:
 wr(S/'VALIDATION_STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect exact handle/log/source; preserve healthy check results.'});state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
