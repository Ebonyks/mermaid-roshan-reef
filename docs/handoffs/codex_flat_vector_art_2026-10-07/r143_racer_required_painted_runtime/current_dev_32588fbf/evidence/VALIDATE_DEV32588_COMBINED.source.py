from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json,os,sys,hashlib,re,time,datetime
W=Path.cwd();T=Path(__file__).parent;D=W.parent/'combined_validation_32588fbf';DEV='32588fbfc6daaa0703d9ee95a526016fc995a38b';HEAD=DEV;MERGED='4b408d0d49ef05c9b852bc02c9d66270ce27bc6b'
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def g(*a):return subprocess.check_output(['git','-c','core.safecrlf=false',*a],cwd=W,stderr=subprocess.PIPE)
def state(stage,**k):
 x=dict(stage=stage,runner_pid=os.getpid(),head=HEAD,incoming_Dev=DEV,merged_source=MERGED,directory=str(D),at_utc=now(),**k);wr(T/'DEV32588_VALIDATION_STATE.json',x)
 s=rd(T/'CONTINUATION_STATE.json');s.update(active_operation=x,healthy_running_jobs=[x]if not stage.startswith(('TERMINAL','STOPPED'))else[]);wr(T/'CONTINUATION_STATE.json',s)
assert g('rev-parse','HEAD').decode().strip()==HEAD and g('rev-parse','MERGE_HEAD').decode().strip()==MERGED
assert g('branch','--show-current').decode().strip()=='codex/flat-vector-racer-dev-integration-20261105'
assert not (D/'LAUNCH.json').exists(),'Resume existing operation; no duplicate validation'
wr(D/'LAUNCH.json',dict(pid=os.getpid(),started_at_utc=now(),head=HEAD,merged=MERGED))
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],cwd=W,stderr=subprocess.PIPE,text=True).strip());assert E.name=='godot_console.exe'and sha(E)=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
assert rd(T/'STANDARD_LAUNCHER_CONTROL.json')['exit_code']==7
ci=(W/'scripts/ci.sh').read_text(encoding='utf-8');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82 and len(set(names))==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
normal_pin=rd(T/'NORMAL_SAVE_PIN.json');normal=Path(normal_pin['normal_base'])
def normals():return{s:sha(Path(str(normal)+s))if Path(str(normal)+s).is_file()else'absent'for s in normal_pin['hashes']}
assert normals()==normal_pin['hashes']
roots=['scripts','assets','scenes','shaders','addons','project.godot','export_presets.cfg'];paths=sorted(set(x for x in g('ls-files','-z','--',*roots).decode().split('\0')if x));state('FREEZING_EXPANDED_RUNTIME_CLOSURE',count=len(paths))
with ThreadPoolExecutor(max_workers=4)as pool:hashes=dict(pool.map(lambda p:(p,sha(W/p)),paths))
wr(D/'SOURCE_PIN.json',dict(head=HEAD,incoming_Dev=DEV,merged_source=MERGED,scope='Tracked production roots plus addon/configuration dependency closure for diagnostic machine validation; not formal QA11 closure',roots=roots,runtime_hashes=hashes,engine=str(E),engine_sha256=sha(E),ci_sha256=sha(W/'scripts/ci.sh'),normal_before=normal_pin['hashes'],version='4.7.2.stable.official.ed1daf0bf'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E));results=[];steps=[];focused=[];analyzers=[];start=now();beg=time.monotonic()
def execute(label,cmd,folder,timeout,classifier=True):
 d=D/folder;d.mkdir();e=env.copy()
 for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
  p=d/key;p.mkdir();e[key]=str(p)
 for key in ['BUBBLE_DUEL_STRESS_ROOT','BUBBLE_DUEL_STRESS_OUTPUT','BUBBLE_DUEL_CYCLES','BUBBLE_DUEL_VERIFY_RELOAD','BUBBLE_DUEL_RELOAD_OUTPUT']:
  e.pop(key,None)
 if any('scripts/probe_bubble_duel_'in str(arg)for arg in cmd):
  e['BUBBLE_DUEL_STRESS_ROOT']=str(d);e['BUBBLE_DUEL_STRESS_OUTPUT']=str(d/'probe_output.json')
 with(d/'engine.log').open('wb')as f:
  process=subprocess.Popen(cmd,cwd=W,env=e,stdin=subprocess.DEVNULL,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000);state(label,pid=process.pid,command=cmd,log=str(d/'engine.log'));clock=time.monotonic();stamp=now()
  try:rc=process.wait(timeout=timeout)
  except subprocess.TimeoutExpired:
   assert process.poll()is None
   subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15);process.wait(timeout=10);raise RuntimeError('Strict original bounded timeout; no verdict-based acceptance: '+label)
 text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in text.splitlines()if classifier and re.search(failure+'|'+runtime,l)];row=dict(label=label,command=cmd,exit_code=rc,pid=process.pid,started_at_utc=stamp,elapsed_seconds=round(time.monotonic()-clock,3),log_path=(d/'engine.log').relative_to(D).as_posix(),log_sha256=sha(d/'engine.log'),failure_lines=bad,output_nonempty=bool(text.strip()),passed=rc==0 and not bad and (bool(text.strip())if classifier else True));wr(d/'RESULT.json',row)
 return row,text
try:
 row,text=execute('CURRENT_STATIC_IMPORT_PREFIX',[r'C:/Program Files/Git/bin/bash.exe',str(D/'ci_static_prefix.sh')],'static',5400,False);steps.append(row);assert row['passed']and'R143_DEV32588_CURRENT_STATIC_PREFIX_ALL_OK'in text,text[-6000:];print('DEV32588_CURRENT_STATIC_IMPORT_ALL_OK',flush=True)
 row,text=execute('MCP_SCOPE_NEGATIVE_CONTROLS',[sys.executable,'-B','-m','unittest','tools.tests.test_godot_mcp_scope'],'mcp_scope',900,False);steps.append(row);assert row['passed'],text[-5000:];print('MCP_SCOPE_ALL_OK',flush=True)
 row,text=execute('MCP_NO_DEBUGGER_LIFECYCLE',[str(E),'--headless','--path',str(W),'-s','tools/godot_mcp/probe_inactive.gd'],'mcp_inactive',180);steps.append(row);assert row['passed'],text[-5000:];print('MCP_INACTIVE_ALL_OK',flush=True)
 changed=sorted(set(g('diff','--name-only','HEAD','--','scripts').decode().splitlines()+g('diff','--name-only',MERGED,'--','scripts').decode().splitlines()));changed=[p for p in changed if p.endswith('.gd')]
 row,text=execute('CHANGED_SCRIPT_PARSER',[sys.executable,'-B','-m','gdtoolkit.parser',*changed],'parser',600,False);steps.append(row);assert row['passed'],text[-4000:]
 row,text=execute('CHANGED_SCRIPT_INFERENCE',[sys.executable,'-B','tools/lint_inference.py',*changed],'inference',600,False);steps.append(row);assert row['passed'],text[-4000:]
 for rel in changed:
  row,text=execute('ANALYZER_'+rel,[str(E),'--headless','--path',str(W),'--check-only','--script','res://'+rel],'analyzer_'+Path(rel).stem,180);row['script']=rel;analyzers.append(row);assert row['passed'],text[-5000:]
 print('CHANGED_ANALYZERS_ALL_OK',len(analyzers),flush=True)
 for name in ['probe_racer_integration','probe_reef_kart_pc','probe_reef_kart_handling','probe_bubble_duel_cast','probe_bubble_duel_dual_active','probe_bubble_duel_stress']:
  row,text=execute('FOCUSED_'+name,[str(E),'--headless','--path',str(W),'-s','scripts/'+name+'.gd'],name,900);row['probe']=name;focused.append(row);assert row['passed'],text[-5000:];print('DEV32588_FOCUSED_PASS',name,row['elapsed_seconds'],flush=True)
 for index,name in enumerate(names):
  flag='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test'
  cmd=[str(E),'--verbose','--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch',flag];row,text=execute('TRUSTED_'+str(index+1)+'_'+name,cmd,name,480);row.update(probe=name,evidence_lane='HEADLESS_CAPTURE_SKIP'if name=='probe_human_art_audit'else'ASSERTION_PROBE');results.append(row);wr(D/'RESULTS_PROGRESS.json',dict(completed=len(results),passed_exits=sum(x['passed']for x in results),results=results));print('DEV32588_COMBINED_PROBE',index+1,name,'PASS_EXIT'if row['passed']else'FAIL',row['elapsed_seconds'],flush=True);assert row['passed'],text[-5000:]
 row,text=execute('POST_MATRIX_GAME2D',[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],'game2d',1800,False);steps.append(row);assert row['passed'],text[-5000:]
 state('VERIFYING_EXPANDED_FROZEN_SOURCE_AND_SAVES',count=len(paths))
 declared=sorted(set(x for x in g('ls-files','-z','--',*roots).decode().split('\0')if x));assert declared==paths
 with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda p:(p,sha(W/p)),paths))
 drift=[p for p in paths if hashes[p]!=after[p]];assert not drift,drift;assert normals()==normal_pin['hashes'];assert sha(W/'scripts/ci.sh')==rd(D/'SOURCE_PIN.json')['ci_sha256']
 wr(D/'FINAL_RESULT.json',dict(state='PASS_CURRENT_DEV32588_COMBINATION_82_COMMAND_EXITS',head=HEAD,incoming_Dev=DEV,merged_source=MERGED,trusted_command_count=82,passed_exit_count=82,assertion_probe_count=81,headless_capture_skip_count=1,results=results,steps=steps,focused=focused,analyzers=analyzers,source_pin_sha256=sha(D/'SOURCE_PIN.json'),runtime_input_count=len(paths),runtime_drift=drift,normal_unchanged=True,normal_before=normal_pin['hashes'],normal_after=normals(),original_flags_order_and_classifiers=True,strict_actual_zero_exit=True,timeout_verdict_acceptance=False,old_failed_attempts_retained_at_previous_pins=True,new_native_frames=0,previous_native_frames_reused_only_at_their_actual_source_pin=True,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,started_at_utc=start,completed_at_utc=now(),elapsed_seconds=round(time.monotonic()-beg,3)));state('TERMINAL_PASS_CURRENT_DEV32588_COMBINATION',passed_exits=82,assertion_probes=81,capture_skip=1);print('DEV32588_COMBINED_ALL_OK81_ASSERTION_PLUS1_CAPTURE_SKIP',flush=True)
except Exception as exc:state('STOPPED_INSPECT_NO_AUTOMATIC_RESTART',error=str(exc),trusted_completed=len(results));raise
