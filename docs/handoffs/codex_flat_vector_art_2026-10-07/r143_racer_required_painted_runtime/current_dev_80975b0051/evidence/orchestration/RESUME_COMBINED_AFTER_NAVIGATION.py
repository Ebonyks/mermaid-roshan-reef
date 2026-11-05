from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,sys,os,re,hashlib,datetime,time
W=Path.cwd();T=Path(__file__).parent;D=W.parent/'combined_validation_80975b0051';assert D.exists() and not(D/'RESUME_NAVIGATION_LAUNCH.json').exists(),'Resume recorded healthy owner-order continuation';assert json.loads((T/'COMBINED_VALIDATION_STATE.json').read_text())['stage']=='STOPPED_INSPECT_EXACT_RESULT_NO_AUTOMATIC_RESTART';(D/'RESUME_NAVIGATION_LAUNCH.json').write_text('{}\n')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def state(stage,**k):wr(T/'COMBINED_VALIDATION_STATE.json',dict(stage=stage,at_utc=now(),runner_pid=os.getpid(),**k))
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],text=True).strip()).with_name('godot.exe');assert sha(E)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
assert json.loads((D/'NATIVE_COMPARISON.json').read_text())['new_current_candidate_frames']==54
assert json.loads((D/'import/RESULT.json').read_text())['exit_code']==0
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/flat-vector-racer-mount-fit-20261105'
normal_pin=json.loads((T/'NORMAL_SAVE_PIN.json').read_text());normal=Path(normal_pin['normal_base'])
def normals():return{s:sha(Path(str(normal)+s)) if Path(str(normal)+s).is_file() else 'absent'for s in normal_pin['hashes']}
assert normals()==normal_pin['hashes']
ci=(W/'scripts/ci.sh').read_text();names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82 and len(set(names))==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
assert sha(D/'SOURCE_PIN.json')=='0c0a9c2767abc404f366f7706d9df4786685300bed9db7ba11d516298fb0fa25'
pin=json.loads((D/'SOURCE_PIN.json').read_text());hashes=pin['runtime_hashes'];paths=sorted(hashes)
declared=sorted(set(x for x in subprocess.check_output(['git','ls-files','-z','--','scripts','assets','scenes','shaders','project.godot'],stderr=subprocess.PIPE).decode().split('\0')if x))
assert len(paths)==5510 and declared==paths,'Actual complete runtime closure must equal the original frozen source pin'
assert sha(W/'scripts/ci.sh')==pin['ci_sha256']


env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E));results=[];focused=[];analyzers=[];start=now();clock=time.monotonic()
def isolated(d):
 e=env.copy()
 for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
  p=d/key;p.mkdir();e[key]=str(p)
 return e
def execute(label,cmd,d,timeout):
 d.mkdir();e=isolated(d)
 with(d/'engine.log').open('wb')as log:
  p=subprocess.Popen(cmd,cwd=W,env=e,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);state(label,pid=p.pid,command=cmd,log=str(d/'engine.log'));beg=time.monotonic()
  try:rc=p.wait(timeout=timeout)
  except subprocess.TimeoutExpired:p.kill();rc=p.wait();raise RuntimeError('Recorded bounded command timed out: '+label)
 text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');return rc,text,round(time.monotonic()-beg,3),sha(d/'engine.log')
try:
 rc,text,elapsed,digest=execute('CURRENT_STATIC_PREFIX',[r'C:/Program Files/Git/bin/bash.exe',str(T/'combined_ci_static_resume_navigation.sh')],D/'static_resume_navigation',5400)
 assert rc==0 and 'R143_COMBINED_CURRENT_STATIC_PREFIX_ALL_OK'in text,text[-5000:]
 print('STATIC_PREFIX_ALL_OK',flush=True)
 for name in ['probe_racer_integration','probe_reef_kart_pc','probe_reef_kart_handling']:
  rc,text,elapsed,digest=execute('FOCUSED_'+name,[str(E),'--headless','--path',str(W),'-s','scripts/'+name+'.gd'],D/name,900)
  bad=[l for l in text.splitlines()if re.search(failure+'|'+runtime,l)];assert rc==0 and not bad and text.strip(),(name,rc,bad,text[-3500:]);focused.append(dict(probe=name,exit_code=rc,log_sha256=digest,elapsed_seconds=elapsed));print('FOCUSED_PASS',name,elapsed,flush=True)
 changed=sorted(set(subprocess.check_output(['git','-c','core.safecrlf=false','diff','--name-only','HEAD','--','scripts'],stderr=subprocess.PIPE,text=True).splitlines()+subprocess.check_output(['git','-c','core.safecrlf=false','diff','--name-only','80975b0051f6a5be29b0680e8b84e15f30d3c316','--','scripts'],stderr=subprocess.PIPE,text=True).splitlines()))
 for rel in [x for x in changed if x.endswith('.gd')]:
  rc,text,elapsed,digest=execute('ANALYZER_'+rel,[str(E),'--headless','--path',str(W),'--check-only','--script','res://'+rel],D/('analyzer_'+Path(rel).stem),180)
  assert rc==0 and not re.search(r'SCRIPT ERROR|Parse Error|Compile Error',text),(rel,text[-3000:]);analyzers.append(dict(script=rel,exit_code=0,log_sha256=digest))
 for index,name in enumerate(names):
  flag='--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test'
  cmd=[str(E),'--verbose','--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch',flag]
  rc,text,elapsed,digest=execute('TRUSTED_'+str(index+1)+'_'+name,cmd,D/name,480)
  bad=[l for l in text.splitlines()if re.search(failure+'|'+runtime,l)];row=dict(probe=name,exit_code=rc,elapsed_seconds=elapsed,failure_lines=bad,output_nonempty=bool(text.strip()),log_sha256=digest,passed=rc==0 and not bad and bool(text.strip()));results.append(row);wr(D/'RESULTS_PROGRESS.json',dict(completed=len(results),passed=sum(x['passed']for x in results),results=results));print('R143_PROBE',index+1,name,'PASS'if row['passed']else'FAIL',elapsed,flush=True);assert row['passed'],text[-5000:]
 rc,text,elapsed,digest=execute('GAME2D',[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],D/'game2d',1800);assert rc==0,text[-3500:]
 state('VERIFYING_FROZEN_RUNTIME_AND_NORMAL_SAVE')
 with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda rel:(rel,sha(W/rel)),paths))
 drift=[x for x in hashes if hashes[x]!=after[x]];assert not drift,drift
 assert normals()==normal_pin['hashes']
 wr(D/'FINAL_RESULT.json',dict(state='PASS_ALL82_CURRENT_STATIC_FOCUSED_ANALYZER_2D',trusted_count=82,passed_count=82,results=results,focused=focused,analyzers=analyzers,source_pin_sha256=sha(D/'SOURCE_PIN.json'),runtime_input_count=len(hashes),runtime_drift=drift,normal_unchanged=True,normal_before=normal_pin['hashes'],normal_after=normals(),full_original_flags_classifiers_and_order=True,import_reused_no_asset_changes=True,native_pair_count=54,new_native_frame_events=54,initial_source_native_frame_events=108,total_task_native_frame_events=162,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,static_resume=dict(original_failure='static/engine.log',original_failed_contract='owner decision append-only order',correction='Dev prefix preserved; three identical Racer decisions appended; candidate evidence routed outside Start with',healthy_preceding_static_checks_reused=True,rerun_from_original_failed_command=True),started_at_utc=start,completed_at_utc=now(),elapsed_seconds=round(time.monotonic()-clock,3)))
 state('TERMINAL_PASS_ALL82',count=82);print('R143_COMBINED_ALL_OK82',flush=True)
except Exception as exc:
 state('STOPPED_INSPECT_EXACT_RESULT_NO_AUTOMATIC_RESTART',error=str(exc),trusted_completed=len(results));raise
