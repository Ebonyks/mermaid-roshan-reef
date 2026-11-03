"""Run the complete existing project gate unchanged, preserving exact logs."""
from pathlib import Path
import datetime
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--resume-at-game2d',action='store_true')
    args=parser.parse_args()
    source = REPO/'scripts/ci.sh'
    canonical = source.read_bytes().replace(b'\r\n', b'\n')
    executed=canonical
    if args.resume_at_game2d:
        checkpoint=json.loads((ROOT/'evidence/project_ci_checkpoint.json').read_text())
        assert checkpoint['source_ci_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
        prefix=(ROOT/'evidence/history/ci_archive_gate/project_ci.log').read_bytes()
        assert hashlib.sha256(prefix).hexdigest()==checkpoint['prefix_log_sha256']
        changed=subprocess.check_output(['git','diff','HEAD','--name-only','--','scripts','scenes','assets','project.godot','tools/audit_game_2d.py'],cwd=REPO,text=True).strip()
        assert not changed,'Production/gate inputs changed; checkpoint reuse is invalid'
        marker=b'python3 tools/audit_game_2d.py --regression-gate'
        context=canonical[canonical.index(b'RUNTIME_ERROR_RE='):canonical.index(b'import_log=')]
        assert b'FAILURE_RE=' in context
        executed=canonical[:canonical.index(b'export GODOT\n')+len(b'export GODOT\n')]+context+canonical[canonical.index(marker):]
    helper = REPO/'tmp/shared_swim_full_ci.sh'
    helper.write_bytes(executed)
    shim = REPO/'tmp/shared_swim_ci_bin'
    shim.mkdir(exist_ok=True)
    (shim/'python3').write_text('#!/bin/sh\nexec "'+Path(sys.executable).as_posix()+'" "$@"\n', encoding='utf-8', newline='\n')
    env = os.environ.copy()
    env.update(PYTHONUTF8='1', PYTHONIOENCODING='utf-8', GODOT='C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe')
    evidence = ROOT/'evidence'
    command = ['C:/Program Files/Git/bin/bash.exe', '-c', 'export PATH="$PWD/tmp/shared_swim_ci_bin:$PATH"; exec bash tmp/shared_swim_full_ci.sh']
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (evidence/'project_ci.log').open('wb') as out, (evidence/'project_ci.err').open('wb') as err:
        result = subprocess.run(command, cwd=REPO, env=env, stdout=out, stderr=err, timeout=14400, creationflags=subprocess.CREATE_NO_WINDOW)
    receipt = {'exit': result.returncode, 'start_utc': start, 'end_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'source_ci_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'executed_lf_sha256': hashlib.sha256(executed).hexdigest(),
               'commands_classifiers_deadlines_unchanged': True, 'command': command, 'single_uninterrupted_run': not args.resume_at_game2d,
               'resumed_at_game2d':args.resume_at_game2d,'checkpoint':'evidence/project_ci_checkpoint.json' if args.resume_at_game2d else None,
               'coverage_claim':'Retained full-prefix evidence plus unchanged failed-stage-and-all-following commands' if args.resume_at_game2d else 'Single complete invocation'}
    (evidence/'project_ci_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8', newline='\n')
    print('CANONICAL_CI_EXIT', result.returncode, flush=True)
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
