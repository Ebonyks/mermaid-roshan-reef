from pathlib import Path
import subprocess,os,json,time
p=Path(__file__).resolve().parents[4];q=Path(__file__).resolve().parents[1]
env=os.environ.copy();env['GODOT']='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1'
start=time.monotonic()
with (q/'environment/project_ci.log').open('w',encoding='utf-8') as log:r=subprocess.run([r'C:\Program Files\Git\bin\bash.exe','scripts/ci.sh'],cwd=p,env=env,stdout=log,stderr=subprocess.STDOUT)
(q/'environment/project_ci.json').write_text(json.dumps({'command':'Git Bash scripts/ci.sh','exit_code':r.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'status':'PASS' if r.returncode==0 else 'FAIL'},indent=2)+'\n')
print('FULL_CI_EXIT',r.returncode,flush=True)
raise SystemExit(r.returncode)
