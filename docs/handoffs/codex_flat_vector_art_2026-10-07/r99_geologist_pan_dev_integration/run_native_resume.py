from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime
S=Path(__file__).parent;R=Path.cwd();OLD=S/'merged_validation';W=S/'native_resume';W.mkdir(exist_ok=False)
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
pin=rd(OLD/'SOURCE_PIN.json');first=rd(OLD/'FINAL_RESULT.json');assert first['status']=='FAIL'and first['probe_count']==3 and first['passed_count']==2
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==first['baseline']
assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],text=True).strip()==first['incoming_dev']
assert subprocess.check_output(['git','write-tree'],text=True).strip()==first['index_tree']
for k in ['runtime_hashes','sidecars']:assert all((R/p).is_file()and sha(R/p)==h for p,h in pin[k].items()),k
assert sha(R/'scripts/ci.sh')==pin['ci_script_sha256']
normal=Path(rd(R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r95_geologist_pan_runtime/CANDIDATE_SOURCE_PIN.json')['normal_base'])
def normals():return {x:sha(Path(str(normal)+x))if Path(str(normal)+x).is_file()else'absent' for x in first['normal_before']}
assert normals()==first['normal_before'];before=normals()
engine=Path(pin['engine']).with_name('godot.exe');assert sha(engine)=='ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
assert subprocess.check_output([str(engine),'--version'],text=True).strip()=='4.7.2.stable.official.ed1daf0bf'
ci=(R/'scripts/ci.sh').read_text(encoding='utf-8-sig');names=re.search(r'for p in (.*?); do',ci).group(1).split();assert len(names)==82
failure=re.search(r"^FAILURE_RE='(.*?)'",ci,re.M).group(1);runtime=re.search(r"^RUNTIME_ERROR_RE='(.*?)'",ci,re.M).group(1)
wr(W/'LAUNCH.json',{'started_at_utc':now(),'source':first['baseline'],'incoming_dev':first['incoming_dev'],'index_tree':first['index_tree'],'method':'Retain the two healthy original checks, diagnose failed third and continue remaining unchanged scripts through exact native Godot executable. No original result rewritten.','reason':'Original console wrapper exited -1 mid-Slide assertions with no failure line or final verdict; exact cause UNKNOWN. Native executable removes intermediate console wrapper as a bounded launcher diagnostic; source/sidecars/CI and normal-save pins unchanged.','prior_failure':'../merged_validation/FINAL_RESULT.json','native_engine':str(engine),'native_sha256':sha(engine),'engine_version':'4.7.2.stable.official.ed1daf0bf','static_import':'Retained current merged five gates/import; no runtime or checker changes since freeze.','failure_regex':failure,'runtime_error_regex':runtime,'normal_before':before})
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8');results=[];start=time.monotonic()
for i,name in enumerate(names[2:],2):
 d=W/name;d.mkdir();e=env.copy()
 for k,n in [('APPDATA','appdata'),('LOCALAPPDATA','local'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=d/n;p.mkdir();e[k]=str(p)
 touch='--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary']else'--classic-touch-test';cmd=[str(engine),'--headless','--path',str(R),'-s','scripts/'+name+'.gd','--','--touch',touch];t=time.monotonic();timed=False
 with(d/'engine.log').open('wb')as log:
  proc=subprocess.Popen(cmd,cwd=R,env=e,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=0x08000000)
  wr(W/'RUNNING.json',{'probe':name,'index':i+1,'count':82,'pid':proc.pid,'started_at_utc':now(),'command':cmd,'log':str(d/'engine.log')})
  try:rc=proc.wait(timeout=480)
  except subprocess.TimeoutExpired:proc.kill();rc=proc.wait();timed=True
 text=(d/'engine.log').read_text(encoding='utf-8',errors='replace');bad=[l for l in text.splitlines()if re.search(failure+'|'+runtime,l)];verdict=bool(re.search(r'ALL OK|RESULT|done|DONE|result',text));tail_verdict=bool(re.search(r'ALL OK|RESULT','\n'.join(text.splitlines()[-5:])));exit_ok=rc==0 or(timed and tail_verdict)
 row={'probe':name,'command':cmd,'exit_code':rc,'timeout_after_verdict_accepted':timed and tail_verdict,'elapsed_seconds':round(time.monotonic()-t,3),'failure_lines':bad,'output_nonempty':bool(text.strip()),'positive_verdict_observed':verdict,'passed':exit_ok and not bad and bool(text.strip()),'log':str(d/'engine.log'),'log_sha256':sha(d/'engine.log')};results.append(row);wr(W/'RESULTS_PROGRESS.json',{'completed':len(results)+2,'passed':sum(x['passed']for x in results)+2,'results':results});print('R99_NATIVE_RESUME',i+1,name,'PASS'if row['passed']else'FAIL',row['elapsed_seconds'],flush=True)
 if not row['passed']:break
changed=[p for p,v in pin['runtime_hashes'].items()if not(R/p).is_file()or sha(R/p)!=v];changed_side=[p for p,v in pin['sidecars'].items()if not(R/p).is_file()or sha(R/p)!=v];after=normals();all_results=first['results'][:2]+results;passed=len(all_results)==82 and all(x['passed']for x in all_results)and not changed and not changed_side and before==after
out={'status':'PASS_ALL_82_PROBE_BY_PROBE'if passed else'FAIL','baseline':first['baseline'],'incoming_dev':first['incoming_dev'],'index_tree':first['index_tree'],'started_at_utc':rd(W/'LAUNCH.json')['started_at_utc'],'completed_at_utc':now(),'elapsed_probe_seconds':round(time.monotonic()-start,3),'probe_count':len(all_results),'passed_count':sum(x['passed']for x in all_results),'retained_healthy_initial_probes':2,'native_resume_probes':len(results),'results':all_results,'runtime_changes':changed,'sidecar_changes':changed_side,'normal_before':before,'normal_after':after,'normal_unchanged':before==after,'original_console_run':'FAIL at third check before verdict; exact cause UNKNOWN, preserved untouched.','qualification':'Machine validation only. FormalQA11/device/child/owner/global closure remain open.'};wr(W/'FINAL_RESULT.json',out);print('R99_NATIVE_RESUME_ALL_OK'if passed else'R99_NATIVE_RESUME_FAIL',len(all_results),flush=True);assert passed
