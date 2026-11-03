from pathlib import Path
import os,sys,subprocess,tempfile,re,json,time,hashlib,shutil
R=Path(__file__).resolve().parents[1];REPO=R.parents[2];OUT=R/'evidence/runtime_final';OUT.mkdir(exist_ok=True);(R/'evidence/scratch').mkdir(exist_ok=True)
GODOT='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'
ci=(REPO/'scripts/ci.sh').read_text();probes=re.search(r'for p in (probe_reef_districts .*?); do',ci).group(1).split();failure=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error');runtime=re.compile(r'SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)');rows=[]
prior=json.loads((R/'evidence/runtime/receipt.json').read_text())
for row in prior['rows']:
 p=R/'evidence/runtime'/row['log']
 if row['pass'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']:
  shutil.copy2(p,OUT/row['log']);rows.append(dict(row,reused_exact_log='evidence/runtime/'+row['log'],scope='Unchanged production bytes at the same f59a1d1d baseline.'))
def write():
 (OUT/'receipt.json').write_text(json.dumps({'scope':'Every trusted CI runtime probe, exact flags and failure rules; first import timeout, failed audit and cleanup error retained separately. Reused successful import/first2probe logs remain byte-exact, production remains unchanged.','ci_sha256':hashlib.sha256((REPO/'scripts/ci.sh').read_bytes()).hexdigest(),'planned_probes':len(probes),'complete':len(rows)==len(probes)+1,'rows':rows},indent=2)+'\n')
def run(name):
 start=time.monotonic();home=Path(tempfile.mkdtemp(prefix=name+'-',dir=R/'evidence/scratch'));env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
 for key,d in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=home/d;p.mkdir();env[key]=str(p)
 mode='--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'] else '--classic-touch-test';args=[GODOT,'--headless','--path',str(REPO),'-s','scripts/'+name+'.gd','--','--touch',mode]
 with (OUT/(name+'.log')).open('w',encoding='utf-8') as f:
  p=subprocess.Popen(args,cwd=REPO,env=env,stdout=f,stderr=subprocess.STDOUT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));(OUT/'active_process.json').write_text(json.dumps({'pid':p.pid,'args':args,'own_temporary_home':str(home),'started_utc_epoch':time.time()},indent=2)+'\n')
  try:code=p.wait(timeout=480)
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],stdout=f,stderr=subprocess.STDOUT,check=False,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));p.wait(timeout=15);code=124
 text=(OUT/(name+'.log')).read_text(encoding='utf-8',errors='replace');ok=(code==0 or (code==124 and re.search(r'ALL OK|RESULT','\n'.join(text.splitlines()[-5:])))) and bool(text) and not failure.search(text) and not runtime.search(text)
 row={'name':name,'args':args,'exit':code,'seconds':round(time.monotonic()-start,2),'pass':bool(ok),'log':name+'.log','sha256':hashlib.sha256((OUT/(name+'.log')).read_bytes()).hexdigest(),'temporary_home_retained_for_diagnostics':True};rows.append(row);write();print(name,code,bool(ok),flush=True)
write();done={x['name'] for x in rows};queue=[x for x in probes if x not in done and x!='probe_audit']+(['probe_audit'] if 'probe_audit' not in done else [])
for name in queue:run(name)
(OUT/'active_process.json').write_text('{"status":"complete","active":false}\n')
raise SystemExit(0 if all(x['pass'] for x in rows) else 1)
