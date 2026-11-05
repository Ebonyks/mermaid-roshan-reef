from pathlib import Path
import os,sys,subprocess,tempfile,re,json,time,hashlib
R=Path(__file__).resolve().parents[1];REPO=R.parents[2];OUT=R/'evidence/runtime';OUT.mkdir(exist_ok=True);(R/'evidence/scratch').mkdir(exist_ok=True)
GODOT='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'
ci=(REPO/'scripts/ci.sh').read_text();probes=re.search(r'for p in (probe_reef_districts .*?); do',ci).group(1).split();failure=re.compile(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error');runtime=re.compile(r'SCRIPT ERROR|Invalid assignment of property or key|The tweened property .* does not exist|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)');rows=[]
def write():
 (OUT/'receipt.json').write_text(json.dumps({'scope':'Unchanged trusted CI runtime import and every probe, exact flags/home isolation and failure expressions; static lanes recorded separately','ci_sha256':hashlib.sha256((REPO/'scripts/ci.sh').read_bytes()).hexdigest(),'planned_probes':len(probes),'complete':len(rows)==len(probes)+1,'rows':rows},indent=2)+'\n')
def run(name,args,timeout):
 start=time.monotonic()
 with tempfile.TemporaryDirectory(prefix=name+'-',dir=R/'evidence/scratch') as home:
  env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
  for key,d in [('APPDATA','appdata'),('LOCALAPPDATA','localappdata'),('XDG_DATA_HOME','data'),('XDG_CONFIG_HOME','config')]:p=Path(home)/d;p.mkdir();env[key]=str(p)
  with (OUT/(name+'.log')).open('w',encoding='utf-8') as f:
   try:proc=subprocess.run(args,cwd=REPO,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=timeout,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));code=proc.returncode
   except subprocess.TimeoutExpired:code=124
 text=(OUT/(name+'.log')).read_text(encoding='utf-8',errors='replace');errors=(re.compile(r'SCRIPT ERROR|Parse Error|Compile Error|ERR_FILE_CORRUPT|Error importing|Cannot load resource|ERROR:.*(Failed loading resource|Cannot open file|No loader found|Resource file not found)') if name=='import' else failure)
 verdict=(code==0 or (code==124 and re.search(r'ALL OK|RESULT','\n'.join(text.splitlines()[-5:])))) and bool(text) and not errors.search(text) and not runtime.search(text)
 row={'name':name,'args':args,'exit':code,'seconds':round(time.monotonic()-start,2),'pass':bool(verdict),'log':name+'.log','sha256':hashlib.sha256((OUT/(name+'.log')).read_bytes()).hexdigest()};rows.append(row);write();print(name,code,bool(verdict),flush=True)
run('import',[GODOT,'--headless','--path',str(REPO),'--import','--verbose'],720)
if not rows[0]['pass']:raise SystemExit('Production import failed; probes not attempted')
for name in probes:
 mode='--hybrid-touch-test' if name in ['probe_passive','probe_touch_router','probe_touch_stress','probe_interaction','probe_touch_adversary'] else '--classic-touch-test'
 run(name,[GODOT,'--headless','--path',str(REPO),'-s','scripts/'+name+'.gd','--','--touch',mode],480)
raise SystemExit(0 if all(x['pass'] for x in rows) else 1)
