from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,os,sys,json,re,hashlib,time,datetime
W=Path.cwd();T=Path(__file__).parent;D=T/'r145_dev58b_validation_resume_cast';assert not D.exists(),'Resume live recorded handle, never duplicate';D.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def git(*a):return subprocess.check_output(['git','-c','core.safecrlf=false',*a],stderr=subprocess.PIPE)
BASE='cafce6e857ef1ba60a3d9a033b5fe5f889f3dce5';DEV='58b29d1014d27b29e7e5313d4dcff5f8beffc14b'
assert git('rev-parse','HEAD').decode().strip()==BASE and git('rev-parse','MERGE_HEAD').decode().strip()==DEV
old=json.loads((T/'r145_dev58b_validation/SOURCE_PIN.json').read_text(encoding='utf-8'));assert git('write-tree').decode().strip()==old['staged_tree']
E=Path(old['engine']);assert sha(E.read_bytes())==old['engine_sha256']=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
paths=sorted(old['runtime_hashes']);assert len(paths)==5580
with ThreadPoolExecutor(max_workers=4)as pool:before=dict(pool.map(lambda p:(p,sha((W/p).read_bytes())),paths))
normalizations_before=[]
for p in paths:
 if before[p]!=old['runtime_hashes'][p]:
  assert p.endswith('.import'),p
  blob=git('show',':'+p);assert (W/p).read_bytes()==blob and sha(blob.replace(b'\n',b'\r\n'))==old['runtime_hashes'][p],p
  normalizations_before.append({'path':p,'kind':'Only CRLF to canonical staged Git LF','before':old['runtime_hashes'][p],'after':before[p]})
fixture=old['fixture'];assert sha((W/fixture).read_bytes())==old['fixture_sha256']
np=json.loads((T/'NORMAL_SAVE_PIN.json').read_text(encoding='utf-8'));nb=Path(np['normal_base'])
def normal_hashes():return{s:sha(Path(str(nb)+s).read_bytes())if Path(str(nb)+s).is_file()else'absent'for s in np['hashes']}
assert normal_hashes()==old['normal_before'],'Normal save differs since original stream; inspect, never reset or attribute silently'
first=json.loads((T/'R145_DEV58B_VALIDATION_STATE.json').read_text(encoding='utf-8'));assert first['stage']=='STOPPED_INSPECT_NO_AUTOMATIC_RESTART';wr(T/'R145_DEV58B_FIRST_FAILURE_STATE.json',first)
passed=[]
for p in (T/'r145_dev58b_validation').glob('*/RESULT.json'):
 r=json.loads(p.read_text(encoding='utf-8'))
 if r['passed']:passed.append(r)
assert len(passed)==6 and all(r['exit_code']==0 for r in passed)
failed=json.loads((T/'r145_dev58b_validation/focused_probe_bubble_duel_cast/RESULT.json').read_text(encoding='utf-8'));assert failed['exit_code']==2 and not failed['passed']
ci=(W/'scripts/ci.sh').read_text(encoding='utf-8');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
wr(D/'SOURCE_PIN.json',{'tested_prior_Racer_source':BASE,'incoming_current_Dev':DEV,'staged_tree':old['staged_tree'],'runtime_hashes':before,'runtime_input_count':5580,'fixture':fixture,'fixture_sha256':old['fixture_sha256'],'engine':str(E),'engine_sha256':old['engine_sha256'],'normal_before':old['normal_before'],'prior_passed_results':passed,'first_failed_cast_result':failed,'import_text_only_normalizations_before_resume':normalizations_before,'scope':'Resume corrected cast invocation and never-started82trusted/final2D only. No source, probe or design-bank change; no new physics parameter variant.'})
results=[]
def state(stage,**kw):wr(T/'R145_DEV58B_RESUME_STATE.json',{'stage':stage,'runner_pid':os.getpid(),'baseline':BASE,'incoming':DEV,'staged_tree':old['staged_tree'],'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':len(results),**kw})
def run(label,cmd,timeout=480,classifier=True):
 d=D/label;d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E))
 for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
  q=d/key;q.mkdir();assert q.resolve().is_relative_to(T.resolve());env[key]=str(q)
 with(d/'engine.log').open('wb')as log:
  proc=subprocess.Popen(cmd,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);started=time.monotonic();state('RUNNING_'+label,pid=proc.pid,command=cmd,log=str(d/'engine.log'))
  try:rc=proc.wait(timeout=timeout)
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15);proc.wait(timeout=10);raise RuntimeError('Strict timeout, no verdict-only pass: '+label)
 out=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in out.splitlines()if classifier and re.search(failure+'|'+runtime,l)]
 row={'label':label,'command':cmd,'exit_code':rc,'elapsed_seconds':round(time.monotonic()-started,3),'failure_lines':bad,'log_sha256':sha((d/'engine.log').read_bytes()),'passed':rc==0 and not bad and(bool(out.strip())if classifier else True)};wr(d/'RESULT.json',row);results.append(row);assert row['passed'],(label,rc,bad,out[-3000:]);print('R145_RESUME_PASS',label,flush=True)
try:
 cast_output=D/'focused_cast_isolated'/'cast_result.json'
 run('focused_cast_isolated',[sys.executable,'-B','tools/run_bubble_duel_stress.py','--cast','--cycles','4','--output',str(cast_output)],2100)
 cast=json.loads(cast_output.read_text(encoding='utf-8'));reload_file=cast_output.with_name('cast_result-reload.json');reloaded=json.loads(reload_file.read_text(encoding='utf-8'));assert len(cast['cycles'])==4 and cast['failures']==0 and all(r['passed']for r in cast['cycles']) and reloaded['failures']==0
 wr(D/'CAST_INVOCATION_REPAIR.json',{'state':'PASS_USING_PUBLISHED_ISOLATED_DRIVER_AND_FRESH_PROCESS_RELOAD','original_failure':failed,'cause':'Direct cast probe extends stress harness and requires BUBBLE_DUEL_STRESS_ROOT to contain actual user-data directory. Missing env guard correctly stopped before trial.','repair':'Use unchanged tools/run_bubble_duel_stress.py --cast --cycles4 with owned isolated temporary profile, fixture report and new-process reload.','source_or_probe_changes':0,'new_physics_design_variants':0,'prior_75_vs_50_cap_overrun_preserved':True,'actual_bouts':4,'modes':['versus','duel','coop','practice'],'cast_result':str(cast_output),'reload_result':str(reload_file),'no_passed_prefix_repeated':True})
 for index,name in enumerate(names):
  flag='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test'
  run('%02d_%s'%(index+1,name),[str(E),'--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch',flag])
 run('post_game2d',[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],1800,False)
 with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda p:(p,sha((W/p).read_bytes())),paths))
 normalizations_after=[]
 for p in paths:
  if after[p]!=before[p]:
   assert p.endswith('.import'),p
   blob=git('show',':'+p);assert (W/p).read_bytes()==blob and sha(blob.replace(b'\n',b'\r\n'))==before[p],p
   normalizations_after.append({'path':p,'kind':'Only CRLF to staged Git LF','before':before[p],'after':after[p]})
 assert normal_hashes()==old['normal_before'];assert sha((W/fixture).read_bytes())==old['fixture_sha256'];assert git('write-tree').decode().strip()==old['staged_tree']
 wr(D/'FINAL_RESULT.json',{'state':'PASS_ACTUAL_COMBINED_SOURCE_AFTER_RETAINED_CAST_SETUP_FAILURE','baseline':BASE,'incoming_current_Dev':DEV,'staged_tree':old['staged_tree'],'runtime_input_count':5580,'prior_successful_commands':passed,'prior_setup_failure':failed,'resumed_results':results,'trusted_commands':82,'assertion_probes':81,'headless_capture_skip':1,'successful_gate_commands':len(passed)+len(results),'total_recorded_command_attempts':len(passed)+1+len(results),'cast_bouts':4,'cast_fresh_process_reload':True,'source_changes_for_repair':0,'new_physics_design_variants':0,'normalizations_before_resume':normalizations_before,'normalizations_after_resume':normalizations_after,'normal_save_unchanged':True,'fixture_unchanged':True,'no_new_native_frames':True,'prior17_Racer_images_keep_CAF_provenance':True,'formal_QA11':None,'device':None,'child':None,'owner':None,'Dev_integrated':False,'accepted_removed':0})
 state('TERMINAL_PASS');print('R145_COMBINED_ALL_REQUIRED_MACHINE_GATES_PASS_AFTER_RETAINED_SETUP_FAILURE',flush=True)
except Exception as exc:state('STOPPED_INSPECT_NO_AUTOMATIC_RESTART',error=str(exc));raise
