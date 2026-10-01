from pathlib import Path
import datetime,hashlib,json,os,re,shutil,subprocess,sys,time
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001/failed_probe_diagnostics_v1'
assert not out.exists();out.mkdir()
shutil.copyfile(Path(__file__),out/'executed_run_v2_failed_probe_diagnostics_v1.py')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
snap=json.loads((r/'audit/job_review_v2_20261001/full_ci_candidate_v1/SOURCE_BEFORE.json').read_text())
assert all(sha(r/x['path'])==x['sha256'] for x in snap['source_files'])
results=[]
engine='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe'
for probe in ['probe_mg2d','probe_audit']:
 home=r/'tmp'/('v2_probe_diagnostic_'+probe+'_20261001');assert not home.exists();home.mkdir()
 for name in ['data','config','appdata','localappdata']:(home/name).mkdir()
 env=dict(os.environ,APPDATA=str(home/'appdata'),LOCALAPPDATA=str(home/'localappdata'),XDG_DATA_HOME=str(home/'data'),XDG_CONFIG_HOME=str(home/'config'))
 command=[engine,'--headless','--path',str(r),'-s','scripts/'+probe+'.gd','--','--touch','--classic-touch-test']
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
 with (out/(probe+'.stdout.log')).open('wb') as stdout,(out/(probe+'.stderr.log')).open('wb') as stderr:
  try:
   process=subprocess.run(command,cwd=r,env=env,stdout=stdout,stderr=stderr,timeout=480,creationflags=subprocess.CREATE_NO_WINDOW)
   code=process.returncode;timeout=False
  except subprocess.TimeoutExpired:code=None;timeout=True
 text=(out/(probe+'.stdout.log')).read_text(errors='replace')+'\n'+(out/(probe+'.stderr.log')).read_text(errors='replace')
 result={'probe':probe,'command':command,'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-tick,'exit_code':code,'timeout':timeout,'failure_lines':[x for x in text.splitlines() if re.search(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error',x)],'last_12_lines':text.splitlines()[-12:],'stdout_sha256':sha(out/(probe+'.stdout.log')),'stderr_sha256':sha(out/(probe+'.stderr.log'))}
 results.append(result);print(json.dumps(result),flush=True)
 (out/'PROCESS_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
checks=[{'path':x['path'],'sha256':sha(r/x['path']),'match':sha(r/x['path'])==x['sha256']} for x in snap['source_files']]
passed=all(x['exit_code']==0 and not x['failure_lines'] for x in results) and all(x['match'] for x in checks)
receipt={'status':'PASS_TARGETED_DIAGNOSTIC_RETRY' if passed else 'FAIL_TARGETED_DIAGNOSTIC_RETRY','results':results,'source_unchanged':all(x['match'] for x in checks),'source_checks':checks,'prior_full_suite':'audit/job_review_v2_20261001/full_ci_candidate_v1/RECEIPT.json','qualification':'Official Godot4.7.2 direct targeted retries with isolated save homes. Unmodified probe and production sources. This does not replace or turn the preserved failed full-CI result into a pass, or establish hosted/visual/device/child/owner acceptance.'}
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
p=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files']+[x.relative_to(r).as_posix() for x in out.rglob('*') if x.is_file()]));d['validation'].append({'command':'Unmodified failed probes direct diagnostic retry','result':'PASS' if passed else 'FAIL','evidence':'audit/job_review_v2_20261001/failed_probe_diagnostics_v1/RECEIPT.json; preserved full CI remains failed, no gate or script altered.'});p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
sys.exit(0 if passed else 1)
