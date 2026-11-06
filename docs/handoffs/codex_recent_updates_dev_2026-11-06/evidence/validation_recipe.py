from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,os,sys,json,re,hashlib,time,datetime
W=Path.cwd();T=Path(__file__).parent;D=T/'recent_updates_validation_resume_audio';assert not D.exists(),'Resume recorded handle, never duplicate';D.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def git(*a):return subprocess.check_output(['git','-c','core.safecrlf=false',*a],stderr=subprocess.PIPE)
base=git('rev-parse','HEAD').decode().strip();assert base=='f1cced56d299695580509b0d3c96e75f7f5e75ce'
assert git('rev-parse','MERGE_HEAD').decode().strip()=='8c9bc130766725965a76eca876ef683b92242334'
E=Path(subprocess.check_output([sys.executable,'-B','tools/resolve_godot.py'],text=True).strip());assert sha(E.read_bytes())=='c8f0a6bc45a19b33541501e57f6f7cd972ab18453743266339d495cbbe846643'
ci=(W/'scripts/ci.sh').read_text(encoding='utf-8');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
allprefix=ci[:ci.index('for p in ')]
audio_at=allprefix.index('python3 tools/audit_audio_quality.py --check')
prelude=allprefix[:allprefix.index('python3 -m unittest tools.tests.test_audit_godot_baseline')]
prefix=prelude+allprefix[audio_at:]
assert 'cd "$(dirname "$0")/.."' in prefix
prefix=prefix.replace('cd "$(dirname "$0")/.."','cd "'+W.as_posix()+'"',1)+'\necho RECENT_STATIC_IMPORT_ALL_OK\n'
(D/'ci_static_prefix.sh').write_text(prefix,encoding='utf-8',newline='\n')
paths=sorted(p for p in git('ls-files','-z','--','scripts','assets','scenes','shaders','addons','project.godot','export_presets.cfg').decode().split('\0')if p)
with ThreadPoolExecutor(max_workers=4)as pool:before=dict(pool.map(lambda p:(p,sha((W/p).read_bytes())),paths))
fixture='assets_src/review/recent_updates_dev_20261106/capture_review.gd';fixture_pin=sha((W/fixture).read_bytes())
np=json.loads((T/'NORMAL_SAVE_PIN.json').read_text());nb=Path(np['normal_base'])
def normal_hashes():return{s:sha(Path(str(nb)+s).read_bytes())if Path(str(nb)+s).is_file()else'absent' for s in np['hashes']}
normal_before=normal_hashes()
wr(D/'SOURCE_PIN.json',dict(current_Dev=base,incoming_Racer='8c9bc130766725965a76eca876ef683b92242334',runtime_hashes=before,fixture=fixture,fixture_sha256=fixture_pin,engine=str(E),engine_sha256=sha(E.read_bytes()),normal_before=normal_before))
results=[]
def state(stage,**kw):wr(T/'RECENT_RESUME_VALIDATION_STATE.json',dict(stage=stage,runner_pid=os.getpid(),baseline=base,incoming='8c9bc130766725965a76eca876ef683b92242334',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),completed=len(results),**kw))
def run(label,cmd,timeout=480,classifier=True):
 d=D/label;d.mkdir();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=str(E))
 for key in ['APPDATA','LOCALAPPDATA','XDG_DATA_HOME','XDG_CONFIG_HOME','TEMP','TMP']:
  q=d/key;q.mkdir();env[key]=str(q)
 with(d/'engine.log').open('wb')as log:
  p=subprocess.Popen(cmd,cwd=W,env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000);started=time.monotonic();state('RUNNING_'+label,pid=p.pid,command=cmd,log=str(d/'engine.log'))
  try:rc=p.wait(timeout=timeout)
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15);p.wait(timeout=10);raise RuntimeError('Strict timeout; no verdict-only pass: '+label)
 output=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in output.splitlines()if classifier and re.search(failure+'|'+runtime,l)]
 row=dict(label=label,command=cmd,exit_code=rc,elapsed_seconds=round(time.monotonic()-started,3),failure_lines=bad,log_sha256=sha((d/'engine.log').read_bytes()),passed=rc==0 and not bad and(bool(output.strip())if classifier else True));wr(d/'RESULT.json',row);results.append(row)
 assert row['passed'],(label,rc,bad,output[-2600:]);print('RECENT_PASS',label,flush=True);return output
try:
 output=run('static_import',[r'C:/Program Files/Git/bin/bash.exe',str(D/'ci_static_prefix.sh')],5400,False);assert 'RECENT_STATIC_IMPORT_ALL_OK' in output
 changed=[p for p in git('diff','--cached','--name-only','--','scripts').decode().splitlines()if p.endswith('.gd')]
 run('changed_parser',[sys.executable,'-B','-m','gdtoolkit.parser',*changed,fixture],600,False)
 run('changed_inference',[sys.executable,'-B','tools/lint_inference.py',*changed,fixture],600,False)
 for name in ['probe_racer_integration','probe_reef_kart_pc']:
  run('focused_'+name,[str(E),'--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch','--classic-touch-test'])
 for index,name in enumerate(names):
  flag='--hybrid-touch-test'if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test'
  run('%02d_%s'%(index+1,name),[str(E),'--headless','--path',str(W),'-s','scripts/'+name+'.gd','--','--touch',flag])
 run('post_game2d',[sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],1800,False)
 with ThreadPoolExecutor(max_workers=4)as pool:after=dict(pool.map(lambda p:(p,sha((W/p).read_bytes())),paths))
 drift=[p for p in paths if before[p]!=after[p]];normalizations=[]
 for p in drift:
  assert p.endswith('.import'),p
  blob=git('show',':'+p);actual=(W/p).read_bytes();assert actual==blob and sha(blob.replace(b'\n',b'\r\n'))==before[p],p
  normalizations.append(dict(path=p,before_raw=before[p],after=after[p],canonical_git_sha256=sha(blob),kind='CRLF to canonical staged LF only'))
 assert normal_hashes()==normal_before,'Normal child save hashes changed; inspect external activity, no silent attribution or reset'
 assert sha((W/fixture).read_bytes())==fixture_pin
 wr(D/'FINAL_RESULT.json',dict(state='PASS_REPAIRED_AUDIO_REMAINING_STATIC_IMPORT_FOCUSED_AND82_STRICT_EXITS_CHAINED_TO_RETAINED_FIRST_FAILURE',baseline=base,incoming='8c9bc130766725965a76eca876ef683b92242334',results=results,trusted_commands=82,assertion_probes=81,headless_capture_skip=1,runtime_input_count=len(paths),runtime_drift=drift,canonical_text_only_import_normalizations=normalizations,normal_unchanged=True,formal_QA11=None,device=None,child=None,owner=None,Dev_integrated=False,accepted_removed=0,first_failed_validation='recent_updates_validation/static_import/RESULT.json',repair='RECENT_AUDIO_SUMMARY_REPAIR.json',previously_passed_pre_audio_prefix_not_repeated=True))
 state('TERMINAL_PASS');print('RECENT_RESUMED_REMAINING_MACHINE_GATES_PASS',flush=True)
except Exception as exc:state('STOPPED_INSPECT_NO_AUTOMATIC_RESTART',error=str(exc));raise
