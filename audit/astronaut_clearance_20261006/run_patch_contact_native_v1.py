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
fixture = 'audit/astronaut_clearance_20261006/capture_birthday_native_v7.gd'
negative = 'audit/astronaut_clearance_20261006/verify_pipe_contact_negative_v5.gd'
job = root / 'tmp/astronaut_native_birthday_capture_v7_20261007'
negative_job = root / 'tmp/astronaut_pipe_contact_negative_v5_20261007'
log = packet / 'PATCH_CONTACT_NATIVE_V1_LOG.txt'
receipt = packet / 'PATCH_CONTACT_NATIVE_V1_RECEIPT.json'
preflight = packet / 'PATCH_CONTACT_NATIVE_V1_PREFLIGHT.json'
manifests = {w: packet / f'NATIVE_BIRTHDAY_CAPTURE_V7_{w}_MANIFEST.json' for w in [1280, 1600]}
TIME_CAP = 300
OUTPUT_CAP = 512 * 1024**2
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
        root / fixture, root / negative, packet / 'PATCH_CONTACT_PLAN.json',
        root / 'tmp/astronaut_partial_save_repair_20261006/reef_save.json'}
    for tree in ['assets', 'scenes', 'scripts', 'shaders']:
        files.update(p for p in (root / tree).rglob('*') if p.is_file())
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files)]


assert not any(p.exists() for p in [log, receipt, preflight, *manifests.values()]), 'Preserve prior attempts; no automatic retry.'
assert not job.exists(), 'Unique PATCH native save/output leaves required.'
assert not negative_job.exists(), 'Unique negative save parent required.'
for width in manifests:
    (job / f'{width}x720/frames').mkdir(parents=True, exist_ok=True)
negative_job.mkdir(parents=True, exist_ok=True)
version = subprocess.check_output([str(engine), '--version'], text=True).strip()
assert version == '4.7.2.stable.official.ed1daf0bf'
assert sha(engine) == 'ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
before = resources(True)
occupied = occupancy()
assert not occupied and before['C_free_bytes'] >= FLOOR and before['physical_available_bytes'] >= FLOOR
sources = inventory()
candidate = (root / fixture).read_text()
original = (packet / 'capture_birthday_native_v6.gd').read_text()
original_checks = [line.strip() for line in original.splitlines() if '_check(' in line and not line.startswith('func _check')]
assert all(line in candidate for line in original_checks)
assert candidate.count('_check(') == original.count('_check(') + 1
assert 'capture_v6_20261007' not in candidate and 'V6_%d_MANIFEST' not in candidate
assert 'capture_v7_20261007/%dx720' in candidate and 'V7_%d_MANIFEST' in candidate
assert (root / negative).read_text().replace('negative_v5_20261007', 'negative_v4_20261007') == (packet / 'verify_pipe_contact_negative_v4.gd').read_text()
commands = []
for script in [fixture, negative, 'scripts/opera_astronaut_pipe_work.gd']:
    commands.append(('Analyzer ' + script, [str(engine), '--headless', '--path', str(root), '--script', 'res://' + script, '--check-only'], None))
for width in manifests:
    commands.append((f'Native birthday {width}x720', [str(engine), '--windowed', '--resolution', f'{width}x720', '--position', '64,64', '--rendering-method', 'mobile', '--rendering-driver', 'vulkan', '--audio-driver', 'Dummy', '--path', str(root), '--script', 'res://' + fixture], width))
commands.append(('Live contact negatives17', [str(engine), '--headless', '--path', str(root), '--script', 'res://' + negative], None))
started = utc()
start = time.monotonic()
preflight.write_text(json.dumps({'started_utc': started, 'baseline': '96274aab9cebd563b10846a4a48de5d017588563', 'branch': 'codex/astronaut-clearance-20261006', 'origin_dev': '6238934447cf28834874396dfbaff65effafda46', 'engine_version': version, 'engine_sha256': sha(engine), 'sources': sources, 'commands': commands, 'resource_before': before, 'approved_executable_occupancy': occupied, 'combined_cap_seconds': TIME_CAP, 'output_cap_bytes': OUTPUT_CAP, 'cache_growth_cap_bytes': CACHE_CAP, 'original126_assertion_lines_preserved': len(original_checks), 'expected_per_aspect_checks': 127, 'negative_checks': 17, 'no_automatic_retry': True, 'prior_valve_prelaunch_setup_seconds': 8.6128821, 'scope': 'Current-source native PATCH contact candidate. Original126birthday assertions plus1five-commit contact-observation check peraspect; headless negative proof separate. Dirty owned local source; explicit prior-six-birthday-jobs/DayOne fixture; genuine Continue/card/object/four-phase/save/finish/return. Read-only postdraw direction observations. Dummy audio. Not strict QA11, full natural Chapter2, full suite, independent/device/child/owner acceptance.', 'prior_native_and_analyzer_seconds': 471.786, 'prior_valve_headless_seconds': 97.711, 'prior_valve_native_seconds': 227.677, 'previous_slice_engine_seconds': 595.844}, indent=2) + '\n')
steps = []
abort = None
with log.open('xb') as output:
    for label, command, width in commands:
        assert not occupancy(), 'Another approved engine is active; no launch.'
        output.write(('\nSTEP ' + label + '\n').encode())
        output.flush()
        offset = log.stat().st_size
        env = os.environ.copy()
        if width:
            env['ASTRO_NATIVE_WIDTH'] = str(width)
        begin = time.monotonic()
        process = subprocess.Popen(command, cwd=root, env=env, stdout=output, stderr=subprocess.STDOUT)
        print(json.dumps({'step': label, 'owned_pid': process.pid}), flush=True)
        last_resource = begin
        while process.poll() is None:
            if time.monotonic() - start > TIME_CAP:
                abort = 'combined engine wall cap'
            elif dir_bytes(job) + dir_bytes(negative_job) + log.stat().st_size > OUTPUT_CAP:
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
        steps.append({'label': label, 'command': command, 'owned_pid': process.pid, 'exit_code': process.returncode, 'elapsed_seconds': round(time.monotonic() - begin, 3), 'width': width, 'abort': abort})
        print(json.dumps(steps[-1]), flush=True)
        if abort or process.returncode:
            break
engine_seconds = round(time.monotonic() - start, 3)
lines = log.read_text(encoding='utf-8', errors='replace').splitlines()
errors = [s for s in lines if any(w in s for w in ['ERROR:', 'SCRIPT ERROR', 'Parse Error', 'Compile Error'])]
evidence = [json.loads(s.split('|', 1)[1]) for s in lines if s.startswith(('ASTRO_BIRTHDAY_RESULT|', 'ASTRO_PIPE_RESULT|'))]
native = []
for width, path in manifests.items():
    if not path.exists():
        continue
    data = json.loads(path.read_text())
    pixels = []
    for frame in data['frames']:
        p = root / frame['path']
        with Image.open(p) as im:
            dims = list(im.size)
            nonblank = max(ImageStat.Stat(im.convert('RGB')).stddev) > 1.0
        ok = sha(p) == frame['sha256'] and p.stat().st_size == frame['bytes'] and dims == frame['dimensions'] == [width, 720] and nonblank
        pixels.append({'path': frame['path'], 'sha256': frame['sha256'], 'dimensions': dims, 'pass': ok})
    labels = {x['label'] for x in data['frames']}
    required = {f'phase{i}_open' for i in range(4)} | {'phase0_pipe_approach', 'phase0_pipe_contact_a', 'phase0_pipe_contact_b', 'phase0_pipe_release', 'phase0_pipe_return', 'phase2_valve_approach', 'phase2_valve_anticipation', 'phase2_valve_contact', 'phase2_valve_turn', 'phase2_valve_release', 'phase2_valve_return', 'phase1_patch_approach', 'phase1_patch_anticipation', 'phase1_patch_contact_a', 'phase1_patch_contact_b', 'phase1_patch_release', 'phase1_patch_return', 'room_return'}
    settled = [x for x in data['frames'] if x['label'] == 'room_return']
    direction = data.get('direction_observations', [])
    native.append({'width': width, 'manifest_path': path.relative_to(root).as_posix(), 'manifest_sha256': sha(path), 'frames': len(pixels), 'pixel_checks': pixels, 'missing_views': sorted(required - labels), 'errors': data['errors'], 'actual_native_mobile': data['display_server'] != 'headless' and data['rendering_method'] == 'mobile' and data['rendering_driver'] == 'vulkan' and data['viewport'] == [width, 720], 'settled_return': len(settled) == 1 and settled[0]['return_fade_alpha'] <= 0.02 and settled[0]['castle_room'] == 'mermaid_pool', 'direction_samples': len(direction), 'direction_and_scale_match': bool(direction) and all(x['flip_h'] == x['expected_flip'] and x['scale_preserved'] for x in direction)})
after = resources(True)
after['output_bytes'] = dir_bytes(job) + dir_bytes(negative_job) + log.stat().st_size
after['cache_growth_bytes'] = max(0, after['cache_bytes'] - before['cache_bytes'])
source_match = inventory() == sources
resource_ok = not abort and after['output_bytes'] <= OUTPUT_CAP and after['cache_growth_bytes'] <= CACHE_CAP and after['C_free_bytes'] >= FLOOR
passed = len(steps) == len(commands) and all(x['exit_code'] == 0 and not x['abort'] for x in steps) and not errors and [x['checks'] for x in evidence] == [127, 127, 17] and all(x['failures'] == 0 for x in evidence) and all(len(e.get('patch_contacts', [])) == 5 and all(r['valid'] for r in e['patch_contacts']) for e in evidence[:2]) and len(native) == 2 and all(all(x['pass'] for x in n['pixel_checks']) and not n['missing_views'] and not n['errors'] and n['actual_native_mobile'] and n['settled_return'] and n['direction_and_scale_match'] for n in native) and source_match and resource_ok
result = {'result': 'PASS' if passed else 'FAIL', 'started_utc': started, 'finished_utc': utc(), 'combined_engine_seconds': engine_seconds, 'cap_seconds': TIME_CAP, 'steps': steps, 'errors': errors, 'abort': abort, 'evidence': evidence, 'native': native, 'sources': sources, 'source_bindings_still_match': source_match, 'resource_before': before, 'resource_after': after, 'resource_limits_pass': resource_ok, 'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log), 'preflight_sha256': sha(preflight), 'meaning': 'Scoped dirty-local native/headless diagnostics only; no strict visual or full-suite/integration/device/child/owner acceptance. Prior attempts/costs retained.'}
receipt.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'result': result['result'], 'checks': [x['checks'] for x in evidence], 'failed_checks': [x for e in evidence for x in e['rows'] if not x['pass']], 'frames': [x['frames'] for x in native], 'errors': errors[:8], 'seconds': engine_seconds, 'source_match': source_match, 'resource_limits_pass': resource_ok, 'receipt_sha256': sha(receipt)}), flush=True)
sys.exit(0 if passed else 1)
