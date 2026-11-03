"""Run exact approved Godot and reject stale receipts or swallowed native errors."""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
DEFAULT_ENGINE = Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64_console.exe')


def inputs():
    paths = [p for base in ['rig', 'geometry', 'skins', 'textures'] for p in (ROOT/base).rglob('*')
             if p.is_file() and p.suffix not in {'.import', '.uid'}]
    paths += list(ROOT.glob('*.gd')) + list(ROOT.glob('*.gdshader')) + [ROOT/'project.godot', ROOT/'study.tscn']
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['import', 'check', 'pose', 'verify', 'capture'], required=True)
    parser.add_argument('--godot', type=Path, default=DEFAULT_ENGINE)
    args = parser.parse_args()
    subprocess.run([sys.executable, '-B', str(REPO/'tools/resolve_godot.py'), '--godot', str(args.godot)], check=True, stdout=subprocess.DEVNULL)
    run_id = uuid.uuid4().hex
    source = inputs()
    command = [str(args.godot), '--path', str(ROOT)]
    if args.mode == 'import':
        command += ['--headless', '--import']
    elif args.mode == 'check':
        command += ['--headless', '--check-only', '-s', 'res://study.gd']
    else:
        if args.mode == 'verify':
            command += ['--headless']
        else:
            command += ['--rendering-method', 'mobile', '--resolution', '1280x720', '--position', '240,120']
        flag = {'pose': '--pose-preview', 'verify': '--verify-only', 'capture': '--capture'}[args.mode]
        command += ['--', flag, '--run-id='+run_id]
    start = time.time()
    log = ROOT/'evidence'/('native_'+args.mode+'.log')
    previous = ROOT/'evidence'/('native_'+args.mode+'_receipt.json')
    if previous.exists():
        old = json.loads(previous.read_text(encoding='utf-8'))
        history = ROOT/'evidence/history'
        history.mkdir(exist_ok=True)
        stem = args.mode+'_'+old['run_id']
        shutil.copy2(previous, history/(stem+'.json'))
        if log.exists():
            shutil.copy2(log, history/(stem+'.log'))
    with log.open('wb') as out:
        process = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        timed_out = False
        while process.poll() is None:
            time.sleep(.25)
            fatal = re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:', log.read_text(encoding='utf-8', errors='replace'))
            timed_out = time.time()-start > (900 if args.mode == 'capture' else 300)
            if fatal or timed_out:
                process.terminate()
                process.wait(timeout=15)
                break
    text = log.read_text(encoding='utf-8', errors='replace')
    errors = [line for line in text.splitlines() if re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:|SHAREDSWIM\|.*\|FAIL', line)]
    receipt = None
    if args.mode in ['pose', 'verify', 'capture']:
        name = {'pose': 'pose_preview.json', 'verify': 'native_swap_tests.json', 'capture': 'native_capture_complete.json'}[args.mode]
        path = ROOT/'evidence'/name
        if path.exists() and path.stat().st_mtime >= start:
            receipt = json.loads(path.read_text(encoding='utf-8'))
        if receipt is None or receipt.get('run_id') != run_id or receipt.get('pass', True) is not True:
            errors.append('Missing, stale or rejected completion receipt')
    if args.mode == 'capture' and receipt and receipt.get('counts') != {'ballet': 229, 'magician': 229, 'live_swaps': 229}:
        errors.append('Native frame coverage differs from the declared three full229-frame captures')
    if source != inputs():
        errors.append('Inputs changed during native run')
    if timed_out:
        errors.append('Native process exceeded the declared deadline')
    record = {'pass': process.returncode == 0 and not errors, 'mode': args.mode, 'exit': process.returncode,
              'run_id': run_id, 'command': command, 'elapsed_seconds': round(time.time()-start, 3),
              'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'inputs': source,
              'errors': errors, 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest()}
    (ROOT/'evidence'/('native_'+args.mode+'_receipt.json')).write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'inputs'}, indent=2))
    return 0 if record['pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
