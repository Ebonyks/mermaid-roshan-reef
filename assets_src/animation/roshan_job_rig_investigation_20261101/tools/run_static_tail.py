"""Run unchanged CI commands after the retained Windows stdin interruption.

The prefix through build_audio_quality_replacements passed in the first log;
final authority/development gates are repeated after all artifacts are closed.
"""
from pathlib import Path
import os,sys,subprocess,json,time,hashlib
R=Path(__file__).resolve().parents[1];REPO=R.parents[2]
source=(REPO/'scripts/ci.sh').read_text().split('RUNTIME_ERROR_RE=',1)[0]
tail=source[source.index('python3 tools/audit_audio_quality.py --check'):]
header='set -euo pipefail\npython3() { "'+sys.executable.replace('\\','/')+'" "$@"; }\nexport -f python3\n'
script=R/'evidence/scratch/static_tail.sh';script.write_text(header+tail,newline='\n')
env=os.environ.copy();env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8')
start=time.monotonic()
with (R/'evidence/static_tail.log').open('w') as log:
    run=subprocess.run(['C:/Program Files/Git/bin/bash.exe',str(script)],stdin=subprocess.DEVNULL,cwd=REPO,env=env,stdout=log,stderr=subprocess.STDOUT)
report={'source':'scripts/ci.sh unchanged static tail from audit_audio_quality.py --check','source_sha256':hashlib.sha256((REPO/'scripts/ci.sh').read_bytes()).hexdigest(),'exit':run.returncode,'seconds':time.monotonic()-start,'pass':run.returncode==0,'plumbing':'Native Python wrapper; script file and closed stdin; no gate/classifier/tolerance changes.'}
(R/'evidence/static_tail_result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));sys.exit(run.returncode)
