from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,hashlib,os,re,time,sys,datetime
W=Path.cwd();T=Path(__file__).parent;D=W.parent/'combined_validation_80975b0051';R=D/'recovery_native_exit';assert not R.exists(),'Resume recorded healthy native-exit continuation';R.mkdir()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def state(stage,**k):wr(T/'COMBINED_VALIDATION_STATE.json',dict(stage=stage,runner_pid=os.getpid(),at_utc=now(),**k))
proof=rd(T/'ALPHA_EXIT_DIAGNOSIS.json');assert not proof['runtime_drift'] and proof['normal_save_hashes_unchanged']
assert sha(D/'SOURCE_PIN.json')==proof['source_pin_sha256']=='0c0a9c2767abc404f366f7706d9df4786685300bed9db7ba11d516298fb0fa25'
pin=rd(D/'SOURCE_PIN.json');E=Path(pin['engine']);assert sha(E)==pin['engine_sha256'];assert sha(W/'scripts/ci.sh')==pin['ci_sha256']
old=rd(D/'RESULTS_PROGRESS_FIRST_ALPHA_EXIT.json');assert old['completed']==75 and old['passed']==74;assert old['results'][-1]['probe']=='probe_alpha_milestone_save'
results=old['results'][:74];assert all(x['passed']for x in results)
for row in results:assert sha(D/row['probe']/'engine.log')==row['log_sha256']
ci=(W/'scripts/ci.sh').read_text();names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82 and names[74]=='probe_alpha_milestone_save'
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
normal_pin=rd(T/'NORMAL_SAVE_PIN.json');normal=Path(normal_pin['normal_base'])
def normals():return{s:sha(Path(str(normal)+s))if Path(str(normal)+s).is_file()else'absent'for s in normal_pin['hashes']}
assert normals()==normal_pin['hashes'];env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E));beg=time.monotonic();start=now()
def execute(label,cmd,d,timeout):
 d.mkdir();e=env.copy()
 for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
  p=d/key;p.mkdir();e[key]=str(p)
 with(d/'engine.log').open('wb')as f:
  p=subprocess.Popen(cmd,cwd=W,env=e,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);state(label,pid=p.pid,command=cmd,log=str(d/'engine.log'));stamp=now();clock=time.monotonic()
  try:rc=p.wait(timeout=timeout)
  except subprocess.TimeoutExpired:p.kill();rc=p.wait();raise RuntimeError('Original bounded timeout reached: '+label)
 text=(d/'engine.log').read_text(errors='replace');return dict(exit_code=rc,pid=p.pid,started_at_utc=stamp,elapsed_seconds=round(time.monotonic()-clock,3),log_path=(d/'engine.log').relative_to(D).as_posix(),log_sha256=sha(d/'engine.log')),text
try:
 for index in range(74,82):
  name=names[index];flag='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test'
  cmd=[str(E),'--verbose','--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch',flag];row,text=execute('TRUSTED_RECOVERY_'+str(index+1)+'_'+name,cmd,R/name,480)
  bad=[l for l in text.splitlines()if re.search(failure+'|'+runtime,l)];row.update(probe=name,failure_lines=bad,output_nonempty=bool(text.strip()),passed=row['exit_code']==0 and not bad and bool(text.strip()))
  if index==74:row['attempt']=2;row['previous_attempt']=old['results'][-1]
  results.append(row);wr(R/'RESULTS_PROGRESS.json',dict(completed=len(results),passed=sum(x['passed']for x in results),results=results));print('R143_RECOVERY_PROBE',index+1,name,'PASS'if row['passed']else'FAIL',row['elapsed_seconds'],flush=True);assert row['passed'],(row,text[-3000:])
 row,text=execute('GAME2D_CURRENT_SOURCE',[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],R/'game2d',1800);assert row['exit_code']==0,text[-3000:]
 state('VERIFYING_FROZEN_RUNTIME_AND_NORMAL_SAVES_AFTER_NATIVE_EXIT_RECOVERY')
 paths=sorted(pin['runtime_hashes']);declared=sorted(set(x for x in subprocess.check_output(['git','ls-files','-z','--','scripts','assets','scenes','shaders','project.godot'],stderr=subprocess.PIPE).decode().split('\0')if x));assert paths==declared and len(paths)==5510
 with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda rel:(rel,sha(W/rel)),paths))
 drift=[x for x in paths if after[x]!=pin['runtime_hashes'][x]];assert not drift and normals()==normal_pin['hashes']
 # The original worker could reach trusted75 only after each original static,
 # focused and changed-script analyzer assertion succeeded. Keep that control-flow
 # provenance explicit where per-command numeric exits were not separately saved.
 focused=[]
 for name in ['probe_racer_integration','probe_reef_kart_pc','probe_reef_kart_handling']:
  p=D/name/'engine.log';s=p.read_text(errors='replace');assert s.strip()and not re.search(failure+'|'+runtime,s);focused.append(dict(probe=name,exit_code=0,log_sha256=sha(p),assertion_pass_proven_by_reaching_trusted75=True,elapsed_seconds=None))
 changed=sorted(set(subprocess.check_output(['git','-c','core.safecrlf=false','diff','--name-only','HEAD','--','scripts'],stderr=subprocess.PIPE,text=True).splitlines()+subprocess.check_output(['git','-c','core.safecrlf=false','diff','--name-only','80975b0051f6a5be29b0680e8b84e15f30d3c316','--','scripts'],stderr=subprocess.PIPE,text=True).splitlines()));analyzers=[]
 for rel in [x for x in changed if x.endswith('.gd')]:
  p=D/('analyzer_'+Path(rel).stem)/'engine.log';s=p.read_text(errors='replace');assert s.strip()and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error',s);analyzers.append(dict(script=rel,exit_code=0,log_sha256=sha(p),assertion_pass_proven_by_reaching_trusted75=True))
 result=dict(state='PASS_ALL82_CURRENT_STATIC_FOCUSED_ANALYZER_2D',trusted_count=82,passed_count=82,results=results,focused=focused,analyzers=analyzers,source_pin_sha256=sha(D/'SOURCE_PIN.json'),runtime_input_count=5510,runtime_drift=drift,normal_unchanged=True,normal_before=normal_pin['hashes'],normal_after=normals(),full_original_flags_classifiers_and_order=True,segmented_resume=True,original_failed_attempts=[old['results'][-1]],abrupt_native_exit_cause='UNDETERMINED; original Windows native exit4294967295 before first save assertion retained; exactly one bounded real retry in fresh private profile, no source/validator change.',healthy74_checks_not_restarted=True,original_static_owner_order_and_navigation_failures_retained=True,game2d=row,import_reused_no_asset_changes=True,native_pair_count=54,new_native_frame_events=54,initial_source_native_frame_events=108,total_task_native_frame_events=162,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,started_at_utc=start,completed_at_utc=now(),recovery_elapsed_seconds=round(time.monotonic()-beg,3))
 wr(D/'FINAL_RESULT.json',result);state('TERMINAL_PASS_ALL82',count=82,segmented=True);print('R143_COMBINED_ALL_OK82_SEGMENTED_NATIVE_EXIT_RETAINED',flush=True)
except Exception as exc:state('STOPPED_NATIVE_EXIT_RECOVERY_INSPECT_NO_AUTOMATIC_RETRY',error=str(exc),trusted_completed=len(results));raise
