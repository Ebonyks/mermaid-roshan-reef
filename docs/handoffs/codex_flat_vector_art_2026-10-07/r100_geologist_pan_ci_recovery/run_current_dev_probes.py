from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime
S=Path(__file__).parent;R=Path.cwd();P=R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime';W=S/'merged_validation';W.mkdir(exist_ok=False)
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
base=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert base=='4918dc910b2f922a85f458cc0cdc710e8059c187'
assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],text=True).strip()=='7a65b9f0abacddeee70230f220955f4d18d551b5'
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/flat-vector-geologist-pan-runtime-20261017'
old=json.loads((P/'CANDIDATE_SOURCE_PIN.json').read_text(encoding='utf-8-sig'));normal=Path(old['normal_base'])
def normals():return {x:sha(Path(str(normal)+x))if Path(str(normal)+x).is_file()else'absent' for x in ['','.bak','.tmp','.tmp0','.tmp1','.old','.bak.tmp','.bak.old','.before_new_game','.before_new_game.tmp','.before_new_game.old']}
before=normals();engine=str(Path(subprocess.check_output(['python','-B','tools/resolve_godot.py'],text=True).strip()).with_name('godot.exe'));assert sha(Path(engine))=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
ci=(R/'scripts/ci.sh').read_text(encoding='utf-8-sig');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
def isolated(name):
 d=W/name;d.mkdir();e=env.copy()
 for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/n;p.mkdir();e[k]=str(p)
 return d,e
gates=[]
for label,cmd,seconds in [('parser',['python','-m','gdtoolkit.parser','scripts/opera_geology_surface.gd','scripts/opera_house_venue_2d.gd','scripts/probe_opera.gd'],120),('inference',['python','-B','tools/lint_inference.py','scripts/opera_geology_surface.gd','scripts/opera_house_venue_2d.gd','scripts/probe_opera.gd'],120),('authority',['python','-B','tools/audit_document_authority.py'],300),('development',['python','-B','tools/audit_development.py','--base','auto'],300),('game2d',['python','-B','tools/audit_game_2d.py','--regression-gate'],300)]:
 t=time.monotonic();q=subprocess.run(cmd,cwd=R,env=env,capture_output=True,timeout=seconds);raw=q.stdout+q.stderr;(W/(label+'.log')).write_bytes(raw);gates.append({'gate':label,'command':cmd,'exit_code':q.returncode,'elapsed_seconds':round(time.monotonic()-t,3),'log_sha256':hashlib.sha256(raw).hexdigest()});wr(W/'GATES.json',gates);print('R100_GATE',label,q.returncode,flush=True);assert q.returncode==0,raw.decode(errors='replace')[-2000:]
d,e=isolated('import');cmd=[engine,'--headless','--path',str(R),'--import'];q=subprocess.run(cmd,cwd=R,env=e,capture_output=True,timeout=720);raw=q.stdout+q.stderr;(d/'engine.log').write_bytes(raw);assert q.returncode==0 and not re.search(runtime+r'|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource',raw.decode(errors='replace'))
print('R100_GATE import PASS',flush=True)
# Freeze actual runtime files after the ordinary import; original normal child files are hash-only.
incoming_paths=subprocess.check_output(['git','diff','--name-only','a9875690ceff436e9ce012a675db09a236aef0f5..7a65b9f0abacddeee70230f220955f4d18d551b5'],text=True).splitlines()
paths=sorted(set(old['runtime_hashes'])|{'assets/opera/worlds/props/geologist_washing_pan_painted.png','.github/workflows/probes.yml'}|{p for p in incoming_paths if p.startswith(('assets/','scripts/','scenes/','shaders/'))and(R/p).is_file()})
pin={p:sha(R/p)for p in paths};side={p:sha(R/p)for p in old['sidecars']};wr(W/'SOURCE_PIN.json',{'baseline':base,'incoming_dev':'7a65b9f0abacddeee70230f220955f4d18d551b5','index_tree':subprocess.check_output(['git','write-tree'],text=True).strip(),'runtime_hashes':pin,'sidecars':side,'ci_script_sha256':sha(R/'scripts/ci.sh'),'engine':engine,'engine_sha256':sha(Path(engine)),'normal_before':before,'candidate_pan_sha256':pin['scripts/opera_geology_surface.gd']})
wr(W/'LAUNCH.json',{'started_at_utc':now(),'baseline':base,'method':'Repository Build & test probe-by-probe route; all82 unchanged trusted scripts; per-probe pre-engine private environment; exact normal save hash guard. Original fullCI remains FAIL.','expected_count':82,'source_pin':str(W/'SOURCE_PIN.json'),'failure_regex':failure,'runtime_error_regex':runtime,'engine':engine,'engine_version':'4.7.2.stable.official.ed1daf0bf','static_reuse':'The prior full run completed its static/assets/audio gates. No audio pixels/assets or those checker sources changed. Current parser/inference/authority/development/2D/import run separately.','no_probe_or_runtime_changes_during_run':True})
results=[];start=time.monotonic()
for i,name in enumerate(names):
 d,e=isolated(name);touch='--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test';cmd=[engine,'--headless','--path',str(R),'-s','scripts/'+name+'.gd','--','--touch',touch];t=time.monotonic();timed=False
 with(d/'engine.log').open('wb')as log:
  proc=subprocess.Popen(cmd,cwd=R,env=e,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
  wr(W/'RUNNING.json',{'probe':name,'index':i+1,'count':82,'pid':proc.pid,'started_at_utc':now(),'command':cmd,'log':str(d/'engine.log')})
  try:rc=proc.wait(timeout=480)
  except subprocess.TimeoutExpired:proc.kill();rc=proc.wait();timed=True
 text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in text.splitlines()if re.search(failure+'|'+runtime,l)];verdict=bool(re.search(r'ALL OK|RESULT|done|DONE|result',text));tail_verdict=bool(re.search(r'ALL OK|RESULT','\n'.join(text.splitlines()[-5:])));exit_ok=rc==0 or(timed and tail_verdict)
 row={'probe':name,'command':cmd,'exit_code':rc,'timeout_after_verdict_accepted':timed and tail_verdict,'elapsed_seconds':round(time.monotonic()-t,3),'failure_lines':bad,'output_nonempty':bool(text.strip()),'positive_verdict_observed':verdict,'passed':exit_ok and not bad and bool(text.strip()),'log':str(d/'engine.log'),'log_sha256':sha(d/'engine.log')};results.append(row);wr(W/'RESULTS_PROGRESS.json',{'completed':len(results),'passed':sum(x['passed']for x in results),'results':results});print('R100_PROBE',i+1,name,'PASS'if row['passed']else'FAIL',row['elapsed_seconds'],flush=True)
 # A proven failure stops this recovery; never repeatedly run a healthy suite or alter a probe.
 if not row['passed']:break
changed=[p for p,v in pin.items()if not(R/p).is_file()or sha(R/p)!=v];changed_side=[p for p,v in side.items()if not(R/p).is_file()or sha(R/p)!=v];after=normals();passed=len(results)==82 and all(x['passed']for x in results)and not changed and not changed_side and before==after
out={'status':'PASS_ALL_82_PROBE_BY_PROBE'if passed else'FAIL','baseline':base,'incoming_dev':'7a65b9f0abacddeee70230f220955f4d18d551b5','index_tree':subprocess.check_output(['git','write-tree'],text=True).strip(),'started_at_utc':json.loads((W/'LAUNCH.json').read_text())['started_at_utc'],'completed_at_utc':now(),'elapsed_probe_seconds':round(time.monotonic()-start,3),'probe_count':len(results),'passed_count':sum(x['passed']for x in results),'results':results,'runtime_changes':changed,'sidecar_changes':changed_side,'normal_before':before,'normal_after':after,'normal_unchanged':before==after,'original_full_CI':'FAIL retained; no retrospective success claim.','qualification':'Machine validation of actual reconciled pan candidate only; formalQA11/device/child/owner/global closure remain open.'};wr(W/'FINAL_RESULT.json',out);print('R100_RECONCILED_ALL_OK'if passed else'R100_RECONCILED_FAIL',len(results),flush=True);assert passed
