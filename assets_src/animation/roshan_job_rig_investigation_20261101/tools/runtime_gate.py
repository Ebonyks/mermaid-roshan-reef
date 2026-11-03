from pathlib import Path
import subprocess,sys,os,re,json,time,hashlib,tempfile
R=Path(__file__).resolve().parents[1];REPO=R.parents[2];E=R/'evidence';G='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'
def call(args,name,env=None,timeout=720):
 p=E/(name+'.log');start=time.monotonic()
 with p.open('w',encoding='utf-8') as f:
  try: q=subprocess.run(args,cwd=REPO,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=timeout);code=q.returncode
  except subprocess.TimeoutExpired: code=124
 s=p.read_text(encoding='utf-8',errors='replace');return {'name':name,'args':args,'exit':code,'seconds':time.monotonic()-start,'log':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'runtime_error':bool(re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)',s)),'text':s}
def main():
 env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=G)
 rows=[]
 probe_only='--probes-only' in sys.argv
 report_name='runtime_probe_gate.json' if probe_only else 'runtime_gate.json'
 def save(): (E/report_name).write_text(json.dumps({'source':'scripts/ci.sh','source_sha256':hashlib.sha256((REPO/'scripts/ci.sh').read_bytes()).hexdigest(),'status':'RUNNING','rows':[{k:v for k,v in x.items() if k!='text'} for x in rows]},indent=2)+'\n')
 for args,name in ([] if probe_only else [([sys.executable,'-B','tools/resolve_godot.py','--godot',G],'resolve'),([G,'--headless','--path',str(REPO),'--import'],'project_import'),([sys.executable,'-B','tools/audit_game_2d.py','--regression-gate'],'game2d')]):
  d=call(args,name,env);rows.append(d);save()
  if d['exit'] or d['runtime_error']:raise SystemExit('BLOCKED '+name)
 ci=(REPO/'scripts/ci.sh').read_text();probes=re.search(r'for p in (.*?); do',ci).group(1).split();(E/'scratch').mkdir(exist_ok=True)
 for p in probes:
  with tempfile.TemporaryDirectory(prefix='probe-',dir=E/'scratch') as home:
   e=env.copy()
   for key,child in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:
    dest=Path(home)/child;dest.mkdir();e[key]=str(dest)
   mode='--hybrid-touch-test' if p in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'] else '--classic-touch-test'
   d=call([G,'--headless','--path',str(REPO),'-s','scripts/'+p+'.gd','--','--touch',mode],p,e,480);d['failure_regex']=bool(re.search(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error',d['text']));d['pass']=not d['failure_regex'] and not d['runtime_error'] and bool(d['text']) and (d['exit']==0 or (d['exit']==124 and re.search(r'ALL OK|RESULT','\n'.join(d['text'].splitlines()[-5:])) is not None));rows.append(d);save();print(p,d['pass'],round(d['seconds'],1),flush=True)
 report=json.loads((E/report_name).read_text());report['status']='PASS' if all(x.get('pass',x['exit']==0 and not x['runtime_error']) for x in rows) else 'FAIL';report['probe_count']=len(probes);report['scope']='All trusted probes only; separate import/2D/authority/static lanes remain required.' if probe_only else 'Runtime plus import/2D lane';(E/report_name).write_text(json.dumps(report,indent=2)+'\n');print('FULL_RUNTIME',report['status'],len(probes));raise SystemExit(0 if report['status']=='PASS' else 1)
if __name__=='__main__':main()

