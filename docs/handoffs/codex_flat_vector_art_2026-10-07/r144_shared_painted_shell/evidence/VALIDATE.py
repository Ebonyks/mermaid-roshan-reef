from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,os,sys,json,re,hashlib,time,datetime
W=Path.cwd();T=Path(__file__).parent;D=T/'validation';assert not D.exists(),'Resume recorded validation, do not duplicate';D.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
wr=lambda p,x:p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.check_output(['git','-c','core.safecrlf=false',*args],stderr=subprocess.PIPE)
base=git('rev-parse','HEAD').decode().strip();assert base=='a7e1faefc09b3303494a5499cce5fe120cb2dcb2'
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],text=True).strip());assert sha(E)=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
pin=json.loads((T/'NORMAL_SAVE_PIN.json').read_text());nb=Path(pin['normal_base'])
def normals():return{s:sha(Path(str(nb)+s))if Path(str(nb)+s).is_file()else'absent'for s in pin['hashes']}
assert normals()==pin['hashes']
ci=(W/'scripts/ci.sh').read_text(encoding='utf-8');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
paths=sorted(p for p in git('ls-files','-z','--','scripts','assets','scenes','shaders','addons','project.godot','export_presets.cfg').decode().split('\0')if p)
with ThreadPoolExecutor(max_workers=4)as pool:before=dict(pool.map(lambda p:(p,sha(W/p)),paths))
fixture='docs/handoffs/codex_flat_vector_art_2026-10-07/r144_shared_painted_shell/capture_context.gd'
wr(D/'SOURCE_PIN.json',{'baseline':base,'runtime_hashes':before,'fixture':fixture,'fixture_sha256':sha(W/fixture),'engine_sha256':sha(E),'normal_before':pin['hashes']})
results=[]
def state(stage,**kw):
 wr(T/'VALIDATION_STATE.json',dict(stage=stage,runner_pid=os.getpid(),source_sha256=sha(W/'scripts/shell_ornament.gd'),baseline=base,at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw))
def run(label,cmd,timeout=480,classifier=True):
 d=D/label;d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E))
 for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
  q=d/key;q.mkdir();env[key]=str(q)
 with(d/'engine.log').open('wb')as log:
  p=subprocess.Popen(cmd,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);started=time.monotonic();state('RUNNING_'+label,pid=p.pid,command=cmd,log=str(d/'engine.log'),completed=len(results))
  try:rc=p.wait(timeout=timeout)
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15);p.wait(timeout=10);raise RuntimeError('Strict timeout; no verdict-only pass: '+label)
 text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in text.splitlines()if classifier and re.search(failure+'|'+runtime,l)]
 row={'label':label,'command':cmd,'exit_code':rc,'elapsed_seconds':round(time.monotonic()-started,3),'failure_lines':bad,'log_sha256':sha(d/'engine.log'),'passed':rc==0 and not bad and(bool(text.strip())if classifier else True)};wr(d/'RESULT.json',row);results.append(row)
 assert row['passed'],(label,rc,bad,text[-3000:]);print('R144_PASS',label,flush=True);return text
try:
 text=run('static_import',[r'C:/Program Files/Git/bin/bash.exe',str(T/'ci_static_prefix.sh')],5400,False);assert 'R144_STATIC_IMPORT_ALL_OK'in text
 run('changed_parser',[sys.executable,'-B','-m','gdtoolkit.parser','scripts/shell_ornament.gd',fixture],600,False)
 run('changed_inference',[sys.executable,'-B','tools/lint_inference.py','scripts/shell_ornament.gd',fixture],600,False)
 for label,path in [('shell_analyzer','scripts/shell_ornament.gd'),('fixture_analyzer',fixture)]:run(label,[str(E),'--headless','--path',str(W),'--check-only','--script','res://'+path],180)
 for index,name in enumerate(names):
  flag='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test'
  run('%02d_%s'%(index+1,name),[str(E),'--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch',flag])
 run('post_game2d',[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],1800,False)
 with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda p:(p,sha(W/p)),paths))
 drift=[p for p in paths if before[p]!=after[p]];normalizations=[]
 for p in drift:
  assert p.endswith('.import')
  blob=git('show','HEAD:'+p);assert(W/p).read_bytes()==blob
  assert hashlib.sha256(blob.replace(b'\n',b'\r\n')).hexdigest()==before[p]
  normalizations.append({'path':p,'before_raw':before[p],'after':after[p],'canonical_git_sha256':hashlib.sha256(blob).hexdigest(),'kind':'CRLF to canonical Git LF only'})
 assert normals()==pin['hashes'] and sha(W/fixture)==json.loads((D/'SOURCE_PIN.json').read_text())['fixture_sha256']
 wr(D/'FINAL_RESULT.json',{'state':'PASS_ACTUAL_R144_STATIC_IMPORT_ANALYZERS_AND82_STRICT_COMMAND_EXITS','baseline':base,'candidate_source_sha256':sha(W/'scripts/shell_ornament.gd'),'results':results,'trusted_commands':82,'assertion_probes':81,'headless_capture_skip':1,'runtime_input_count':len(paths),'runtime_drift':drift,'canonical_text_only_import_normalization':normalizations,'normal_unchanged':True,'formal_QA11':None,'device':None,'child':None,'owner':None,'Dev_integrated':False,'accepted_removed':0})
 state('TERMINAL_PASS',completed=len(results));print('R144_ALL_MACHINE_GATES_PASS',flush=True)
except Exception as exc:state('STOPPED_INSPECT_NO_AUTOMATIC_RESTART',error=str(exc),completed=len(results));raise
