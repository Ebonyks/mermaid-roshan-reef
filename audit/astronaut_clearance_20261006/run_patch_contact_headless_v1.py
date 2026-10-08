from pathlib import Path
from datetime import datetime, timezone
import ctypes
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from PIL import Image, ImageStat

root = Path(__file__).resolve().parents[2]
packet = Path(__file__).resolve().parent
engine = Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
fixture = 'audit/astronaut_clearance_20261006/verify_birthday_patch_contact_v1.gd'
job = root / 'tmp/astronaut_birthday_patch_contact_v1_20261007'
log = packet / 'PATCH_CONTACT_HEADLESS_V1_LOG.txt'
receipt = packet / 'PATCH_CONTACT_HEADLESS_V1_RECEIPT.json'
preflight = packet / 'PATCH_CONTACT_HEADLESS_V1_PREFLIGHT.json'
TIME_CAP = 220
OUTPUT_CAP = 64 * 1024**2
CACHE_CAP = 64 * 1024**2
FLOOR = 3 * 1024**3


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


def dir_bytes(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file()) if path.exists() else 0


class MemoryStatus(ctypes.Structure):
    _fields_ = [('length', ctypes.c_uint32), ('load', ctypes.c_uint32),
        ('total_phys', ctypes.c_uint64), ('avail_phys', ctypes.c_uint64),
        ('total_page', ctypes.c_uint64), ('avail_page', ctypes.c_uint64),
        ('total_virtual', ctypes.c_uint64), ('avail_virtual', ctypes.c_uint64),
        ('avail_extended', ctypes.c_uint64)]


def resources(cache=False):
    m = MemoryStatus()
    m.length = ctypes.sizeof(m)
    assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    d = {'C_free_bytes': shutil.disk_usage('C:/').free, 'physical_available_bytes': m.avail_phys}
    if cache:
        d['cache_bytes'] = dir_bytes(root / '.godot')
    return d


def occupancy():
    command = '@(Get-CimInstance Win32_Process -Filter "Name=\'Godot_v4.7.2-stable_win64.exe\'" | Select-Object ProcessId,ExecutablePath) | ConvertTo-Json -Compress'
    q = subprocess.run(['powershell', '-NoProfile', '-Command', command], capture_output=True, text=True, timeout=15)
    assert q.returncode == 0
    value = json.loads(q.stdout) if q.stdout.strip() else []
    return value if isinstance(value, list) else [value]


def inventory():
    files = {root / 'project.godot', root / 'tools/godot_baseline.json', Path(__file__),
        root / fixture, packet / 'PATCH_CONTACT_PLAN.json',
        root / 'tmp/astronaut_partial_save_repair_20261006/reef_save.json'}
    for tree in ['assets', 'scenes', 'scripts', 'shaders']:
        files.update(p for p in (root / tree).rglob('*') if p.is_file())
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files)]


assert not any(p.exists() for p in [log, receipt, preflight]), 'Preserve prior attempts; no automatic retry.'
assert not job.exists(), 'Unique isolated save required.'
job.mkdir(parents=True)
version = subprocess.check_output([str(engine), '--version'], text=True).strip()
assert version == '4.7.2.stable.official.ed1daf0bf'
assert sha(engine) == 'ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
before = resources(True)
occupied = occupancy()
assert not occupied and before['C_free_bytes'] >= FLOOR and before['physical_available_bytes'] >= FLOOR
sources = inventory()
candidate = (root / fixture).read_text()
original = (packet / 'verify_birthday_valve_contact_v1.gd').read_text()
original_checks = [line.strip() for line in original.splitlines() if '_check(' in line and not line.startswith('func _check')]
assert all(line in candidate for line in original_checks)
assert 'astronaut_birthday_patch_contact_v1_20261007' in candidate
commands = []
for script in [fixture, 'scripts/opera_astronaut_patch_work.gd', 'scripts/opera_astronaut_valve_work.gd', 'scripts/opera_astronaut_surface.gd', 'scripts/opera_career_world_2d.gd']:
    commands.append(('Analyzer ' + script, [str(engine), '--headless', '--path', str(root), '--script', 'res://' + script, '--check-only']))
commands.append(('Birthday patch141', [str(engine), '--headless', '--path', str(root), '--script', 'res://' + fixture]))
started = utc()
start = time.monotonic()
preflight.write_text(json.dumps({'started_utc': started, 'baseline': '96274aab9cebd563b10846a4a48de5d017588563', 'engine_version': version, 'engine_sha256': sha(engine), 'sources': sources, 'commands': commands, 'resource_before': before, 'approved_executable_occupancy': occupied, 'combined_cap_seconds': TIME_CAP, 'original121_assertion_lines_preserved': len(original_checks), 'expected_checks': 141, 'no_automatic_retry': True, 'scope': 'Dirty owned current-source headless genuine birthday four-mechanic/save/finish/return after explicit prior-six-jobs fixture;20additional PATCH queue/contact/cancel/observed-commit checks; no native/strictQA11/fullsuite/independent/device/child/owner acceptance.'}, indent=2) + '\n')
steps = []
abort = None
with log.open('xb') as output:
    for label, command in commands:
        assert not occupancy(), 'Another approved engine is active; no launch.'
        output.write(('\nSTEP ' + label + '\n').encode())
        output.flush()
        offset = log.stat().st_size
        begin = time.monotonic()
        process = subprocess.Popen(command, cwd=root, stdout=output, stderr=subprocess.STDOUT)
        print(json.dumps({'step': label, 'owned_pid': process.pid}), flush=True)
        last_resource = begin
        while process.poll() is None:
            if time.monotonic() - start > TIME_CAP:
                abort = 'combined engine wall cap'
            elif dir_bytes(job) + log.stat().st_size > OUTPUT_CAP:
                abort = 'output cap'
            elif time.monotonic() - last_resource >= 10:
                current = resources()
                last_resource = time.monotonic()
                if current['C_free_bytes'] < FLOOR or current['physical_available_bytes'] < FLOOR:
                    abort = 'actual disk/memory floor'
            with log.open('rb') as tail:
                tail.seek(offset)
                content = tail.read()
            if any(word in content for word in [b'ERROR:', b'SCRIPT ERROR', b'Parse Error', b'Compile Error']):
                abort = 'engine error; stop this owned process immediately'
            if abort:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                break
            time.sleep(0.25)
        steps.append({'label': label, 'command': command, 'owned_pid': process.pid, 'exit_code': process.returncode, 'elapsed_seconds': round(time.monotonic() - begin, 3), 'abort': abort})
        print(json.dumps(steps[-1]), flush=True)
        if abort or process.returncode:
            break
engine_seconds = round(time.monotonic() - start, 3)
lines = log.read_text(encoding='utf-8', errors='replace').splitlines()
errors = [s for s in lines if any(w in s for w in ['ERROR:', 'SCRIPT ERROR', 'Parse Error', 'Compile Error'])]
evidence = [json.loads(s.split('|', 1)[1]) for s in lines if s.startswith('ASTRO_BIRTHDAY_RESULT|')]
after = resources(True)
after['output_bytes'] = dir_bytes(job) + log.stat().st_size
after['cache_growth_bytes'] = max(0, after['cache_bytes'] - before['cache_bytes'])
source_match = inventory() == sources
resource_ok = not abort and after['output_bytes'] <= OUTPUT_CAP and after['cache_growth_bytes'] <= CACHE_CAP and after['C_free_bytes'] >= FLOOR
passed = len(steps) == len(commands) and all(x['exit_code'] == 0 and not x['abort'] for x in steps) and not errors and len(evidence) == 1 and evidence[0]['checks'] == 141 and evidence[0]['failures'] == 0 and bool(evidence[0].get('valve_contacts')) and all(x['valid'] for x in evidence[0]['valve_contacts']) and len(evidence[0].get('patch_contacts', [])) == 5 and all(x['valid'] for x in evidence[0]['patch_contacts']) and source_match and resource_ok
result = {'result': 'PASS' if passed else 'FAIL', 'started_utc': started, 'finished_utc': utc(), 'combined_engine_seconds': engine_seconds, 'cap_seconds': TIME_CAP, 'steps': steps, 'errors': errors, 'abort': abort, 'evidence': evidence, 'sources': sources, 'source_bindings_still_match': source_match, 'resource_before': before, 'resource_after': after, 'resource_limits_pass': resource_ok, 'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log), 'preflight_sha256': sha(preflight), 'meaning': 'Scoped current-source headless diagnostics only; no native/strict visual/full-suite/integration/device/child/owner acceptance. Prior attempts/costs retained.'}
receipt.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'result': result['result'], 'checks': [x['checks'] for x in evidence], 'failed_checks': [x for e in evidence for x in e['rows'] if not x['pass']], 'valve_contacts': len(evidence[0].get('valve_contacts', [])) if evidence else 0, 'errors': errors[:8], 'seconds': engine_seconds, 'source_match': source_match, 'resource_limits_pass': resource_ok, 'receipt_sha256': sha(receipt)}), flush=True)
sys.exit(0 if passed else 1)
