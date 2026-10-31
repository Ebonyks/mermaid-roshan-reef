from pathlib import Path
import subprocess, json, hashlib, time, re
from datetime import datetime, timezone
root = Path(__file__).resolve().parents[4]
out = Path(__file__).resolve().parent
sources = [root/'project.godot']
for folder in ['scripts','scenes','shaders','assets/opera/worlds/chef_quality_20261019','assets/opera/worlds/widgets']:
    sources += [p for p in (root/folder).rglob('*') if p.is_file() and p.suffix not in ['.import','.uid']]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sources += [root/'tools/prepare_opera_minigame_art.py',root/'tools/tests/test_prepare_opera_minigame_art.py']
pins = {p.relative_to(root).as_posix(): sha(p) for p in sources}
started = datetime.now(timezone.utc).isoformat()
clock = time.monotonic()
command = ['C:/Program Files/Git/bin/bash.exe','--noprofile','--norc',str(out/'run_ci_native_capture_02.sh')]
with (out/'full_ci_native_capture_02.log').open('w',encoding='utf-8') as f:
    run = subprocess.run(command,cwd=root,stdout=f,stderr=subprocess.STDOUT)
transcript = (out/'full_ci_native_capture_02.log').read_text(encoding='utf-8',errors='replace')
completed = re.findall(r'^PROBE (\S+) process exit: (\d+)$',transcript,re.M)
expected = re.search(r'for p in (.+?); do',(root/'scripts/ci.sh').read_text()).group(1).split()
drift = [name for name,h in pins.items() if not (root/name).is_file() or sha(root/name)!=h]
status = 'PASS' if run.returncode==0 and [p for p,c in completed]==expected and all(c=='0' for p,c in completed) and not drift else 'FAIL'
receipt = {'status':status,'baseline':'6fb96aeb441952c1053cc5ce18435fc57fc1d1ab','command':command,
    'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
    'elapsed_seconds':round(time.monotonic()-clock,3),'process_exit':run.returncode,
    'expected_probes':len(expected),'completed_probes':completed,'source_drift':drift,
    'source_sha256_raw_checkout':pins,'log_sha256':sha(out/'full_ci_native_capture_02.log')}
(out/'full_ci_native_capture_02.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k not in ['source_sha256_raw_checkout','completed_probes']}))
raise SystemExit(0 if status=='PASS' else 1)
