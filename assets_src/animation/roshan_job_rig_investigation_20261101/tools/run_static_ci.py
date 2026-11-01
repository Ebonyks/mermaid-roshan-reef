"""Run the unchanged static section of scripts/ci.sh under Git Bash.

Import, medium inventory and every trusted probe are separate retained lanes.
Only working-directory and Python executable plumbing differs on Windows.
"""
from pathlib import Path
import subprocess,os,sys,json,hashlib,time
R=Path(__file__).resolve().parents[1];REPO=R.parents[2]
source=(REPO/'scripts/ci.sh').read_text()
prefix=source.split("RUNTIME_ERROR_RE=",1)[0]
prefix=prefix.replace('cd "$(dirname "$0")/.."','cd "$REVIEW_REPO"',1)
native_python=sys.executable.replace('\\','/')
prefix='python3() { "'+native_python+'" "$@"; }\nexport -f python3\n'+prefix
env=os.environ.copy();env.update(REVIEW_REPO=str(REPO).replace('\\','/'),GODOT='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe',PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
start=time.monotonic()
script=R/'evidence/scratch/static_ci_input.sh'
script.parent.mkdir(parents=True,exist_ok=True)
script.write_text(prefix,encoding='utf8',newline='\n')
with (R/'evidence/static_ci.log').open('w',encoding='utf8') as out:
    run=subprocess.run(['C:/Program Files/Git/bin/bash.exe',str(script)],stdin=subprocess.DEVNULL,text=True,cwd=REPO,env=env,stdout=out,stderr=subprocess.STDOUT)
report={'source':'scripts/ci.sh prefix before RUNTIME_ERROR_RE','source_sha256':hashlib.sha256((REPO/'scripts/ci.sh').read_bytes()).hexdigest(),'exit':run.returncode,'seconds':time.monotonic()-start,'pass':run.returncode==0,'plumbing':'Git Bash, same installed native Python, source-only working directory; all gate commands/classifiers unmodified.','other_required_lanes':['project_import.log','game2d_retry.log','trusted_probe_completion.json'],'source_quality':'strict_regression.json remains FAIL; this is an archive review draft, not an accepted performance.'}
(R/'evidence/static_ci_result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(run.returncode)
