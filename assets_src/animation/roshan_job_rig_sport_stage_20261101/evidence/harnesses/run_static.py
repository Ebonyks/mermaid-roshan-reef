from pathlib import Path
import subprocess,re,os,sys,json,time,hashlib
R=Path(__file__).resolve().parents[2];repo=R.parents[2];out=R/'evidence/static_gates';out.mkdir(exist_ok=True);source=(repo/'scripts/ci.sh').read_text();prefix=source.split("RUNTIME_ERROR_RE=")[0];lines=prefix.replace('\\\n',' ').splitlines();commands=[]
g='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe'
for line in lines:
 if not line.startswith('python3 '):continue
 line=line.split('||')[0].strip();line=line.replace('python3 ',sys.executable+' ',1).replace('"$GODOT"',g)
 if 'audit_development.py' in line or line.endswith('tools/audit_document_authority.py'):continue # run after exact final coverage is populated
 if "$(find scripts -name '*.gd')" in line:args=[sys.executable,'-m','gdtoolkit.parser',*[str(p.relative_to(repo)) for p in (repo/'scripts').rglob('*.gd')]]
 else:
  import shlex,glob
  args=shlex.split(line,posix=False);args=[a.strip('"') for a in args]
  expanded=[]
  for a in args:expanded.extend(glob.glob(a,root_dir=repo) if '*' in a else [a])
  args=expanded
 commands.append((args,'audit_visual_design.py' in line and '--stress' not in line))
commands.append(([sys.executable,'tools/audit_game_2d.py','--regression-gate'],False))
rows=[]
for i,(args,advisory) in enumerate(commands):
 name=str(i+1).zfill(2)+'_'+Path(args[1] if len(args)>1 else 'check').stem;log=out/(name+'.log');start=time.monotonic();env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT=g,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
 with log.open('w',encoding='utf-8') as f:
  try:p=subprocess.run(args,cwd=repo,stdout=f,stderr=subprocess.STDOUT,env=env,timeout=900,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0));code=p.returncode
  except subprocess.TimeoutExpired:code=124
 rows.append({'name':name,'args':args,'exit':code,'seconds':round(time.monotonic()-start,2),'pass':code==0,'advisory_in_unmodified_ci':advisory,'log':log.name,'sha256':hashlib.sha256(log.read_bytes()).hexdigest()});(out/'receipt.json').write_text(json.dumps({'ci_sha256':hashlib.sha256((repo/'scripts/ci.sh').read_bytes()).hexdigest(),'scope':'Unmodified CI static gate commands with Windows Python/glob expansion; final impact/authority gates run separately. Failures/timeouts never waived.','rows':rows},indent=2)+'\n');print(name,code,flush=True)
