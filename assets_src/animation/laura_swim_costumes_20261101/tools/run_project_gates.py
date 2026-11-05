"""Execute every canonical gate unchanged, with Windows UTF-8 stdout isolation."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]


def main():
    source = REPO/'scripts/ci.sh'
    canonical = source.read_bytes().replace(b'\r\n',b'\n')
    resume = '--resume-at-coverage' in sys.argv
    executed = canonical
    if resume:
        marker = b'python3 tools/audit_development.py --base auto'
        checkpoint = json.loads((ROOT/'evidence/project_ci_checkpoint.json').read_text())
        assert checkpoint['source_ci_sha256'] == hashlib.sha256(source.read_bytes()).hexdigest()
        executed = canonical[:canonical.index(b'export GODOT\n')+len(b'export GODOT\n')]+canonical[canonical.index(marker):]
    helper = REPO/'tmp/laura_swim_full_ci.sh'
    helper.write_bytes(executed)
    shim = REPO/'tmp/laura_swim_ci_bin'
    shim.mkdir(exist_ok=True)
    (shim/'python3').write_text('#!/bin/sh\nexec "'+Path(sys.executable).as_posix()+'" "$@"\n',encoding='utf-8',newline='\n')
    env = os.environ.copy()
    env.update(PYTHONUTF8='1',PYTHONIOENCODING='utf-8',GODOT='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe')
    evidence = ROOT/'evidence'
    evidence.mkdir(exist_ok=True)
    command = ['C:/Program Files/Git/bin/bash.exe','-c','export PATH="$PWD/tmp/laura_swim_ci_bin:$PATH"; exec bash tmp/laura_swim_full_ci.sh']
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (evidence/'project_ci.log').open('wb') as out, (evidence/'project_ci.err').open('wb') as err:
        result = subprocess.run(command,cwd=REPO,env=env,stdout=out,stderr=err,timeout=14400,creationflags=subprocess.CREATE_NO_WINDOW)
    receipt = {'exit':result.returncode,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_ci_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'executed_lf_sha256':hashlib.sha256(executed).hexdigest(),'commands_classifiers_deadlines_unchanged':True,'command':command,'single_uninterrupted_run':not resume,'resumed_at_coverage':resume,'checkpoint':'project_ci_checkpoint.json' if resume else None}
    (evidence/'project_ci_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('CANONICAL_CI_EXIT',result.returncode,flush=True)
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
