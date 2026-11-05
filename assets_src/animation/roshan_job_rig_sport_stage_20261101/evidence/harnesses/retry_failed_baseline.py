from pathlib import Path
import subprocess,sys,os,json,hashlib,time,tempfile,re
R=Path(__file__).resolve().parents[2];repo=R.parents[2];out=R/'evidence/baseline_retry_after_native';out.mkdir(exist_ok=True);g='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe';rows=[];err=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error');envbase=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=g,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
for name,args,limit,kind in [('probe_opera_2d',[g,'--headless','--path',str(repo),'-s','scripts/probe_opera_2d.gd','--','--touch','--classic-touch-test'],480,'probe'),('probe_chapter2',[g,'--headless','--path',str(repo),'-s','scripts/probe_chapter2.gd','--','--touch','--classic-touch-test'],480,'probe'),('probe_audit',[g,'--headless','--path',str(repo),'-s','scripts/probe_audit.gd','--','--touch','--classic-touch-test'],480,'probe'),('audit_audio_quality',[sys.executable,'tools/audit_audio_quality.py','--check'],900,'static'),('visual_contract_unittest',[sys.executable,'-m','unittest','tools.tests.test_audit_visual_design'],900,'static')]:
 env=dict(envbase)
 if kind=='probe':
  home=Path(tempfile.mkdtemp(prefix='sport-stage-retry-'))
  for n in ['appdata','localappdata','data','config']:(home/n).mkdir()
  env.update(APPDATA=str(home/'appdata'),LOCALAPPDATA=str(home/'localappdata'),XDG_DATA_HOME=str(home/'data'),XDG_CONFIG_HOME=str(home/'config'))
 start=time.monotonic();log=out/(name+'.log')
 with log.open('w',encoding='utf-8') as f:
  proc=subprocess.Popen(args,cwd=repo,stdout=f,stderr=subprocess.STDOUT,env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));(out/'active_process.json').write_text(json.dumps({'pid':proc.pid,'args':args,'active':True},indent=2)+'\n')
  try:code=proc.wait(timeout=limit)
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True);code=124
 text=log.read_text(errors='replace');ok=code==0 and (not err.search(text) if kind=='probe' else True)
 rows.append({'name':name,'kind':kind,'args':args,'exit':code,'pass':ok,'seconds':round(time.monotonic()-start,2),'log':log.name,'sha256':hashlib.sha256(log.read_bytes()).hexdigest(),'isolated_probe_home_retained':kind=='probe'});(out/'receipt.json').write_text(json.dumps({'scope':'Only5failed/timed-out unchanged baseline gates retried after native render jobs finish; exact flags/floors unchanged, original failures retained. A retry does not accept source attachment/visual failures.','rows':rows,'complete':len(rows)==5,'pass':len(rows)==5 and all(x['pass'] for x in rows)},indent=2)+'\n');print(name,code,ok,flush=True)
(out/'active_process.json').write_text('{"active":false,"status":"complete"}\n')
