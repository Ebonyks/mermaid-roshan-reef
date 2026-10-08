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
fixture = 'audit/astronaut_clearance_20261006/capture_birthday_native_v8.gd'
negative = 'audit/astronaut_clearance_20261006/verify_pipe_contact_negative_v6.gd'
job = root / 'tmp/astronaut_native_birthday_capture_v8_20261007'
negative_job = root / 'tmp/astronaut_pipe_contact_negative_v6_20261007'
log = packet / 'PATCH_READABILITY_NATIVE_RECOVERY_V1_LOG.txt'
receipt = packet / 'PATCH_READABILITY_NATIVE_RECOVERY_V1_RECEIPT.json'
preflight = packet / 'PATCH_READABILITY_NATIVE_RECOVERY_V1_PREFLIGHT.json'
manifests = {w: packet / f'NATIVE_BIRTHDAY_CAPTURE_V8_{w}_MANIFEST.json' for w in [1280, 1600]}
TIME_CAP = 60
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
    total = 0
    if not path.exists():
        return total
    for p in path.rglob('*'):
        try:
            if p.is_file():
                total += p.stat().st_size
        except FileNotFoundError:
            # SaveState rotates tiny backup files atomically during observation.
            continue
    return total


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
        root / fixture, root / negative, packet / 'PATCH_READABILITY_PLAN.json',
        root / 'tmp/astronaut_partial_save_repair_20261006/reef_save.json'}
    for tree in ['assets', 'scenes', 'scripts', 'shaders']:
        files.update(p for p in (root / tree).rglob('*') if p.is_file())
    return [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(files)]



assert not any(p.exists() for p in [log, receipt, preflight]), 'Preserve attempts; no automatic retry.'
assert negative_job.exists() and not list(negative_job.iterdir()), 'Previously prepared but unused negative save parent must be empty.'
parent_path = packet / 'PATCH_READABILITY_NATIVE_V1_RECEIPT.json'
parent = json.loads(parent_path.read_text())
assert parent['result'] == 'FAIL' and parent['negative_process_launched'] is False
original_preflight = json.loads((packet / 'PATCH_READABILITY_NATIVE_V1_PREFLIGHT.json').read_text())
plan_path = packet / 'PATCH_READABILITY_NATIVE_RECOVERY_V1_PLAN.json'
plan = json.loads(plan_path.read_text())
assert sha(parent_path) == plan['parent_sha256']
assert all(sha(root / b['path']) == b['sha256'] for b in original_preflight['sources'])
assert all(sha(root / b['path']) == b['sha256'] for b in plan['immutable_native_manifests'])
capture_log = packet / 'PATCH_READABILITY_NATIVE_V1_LOG.txt'
assert sha(capture_log) == plan['capture_log_sha256']
capture_lines = capture_log.read_text(encoding='utf-8', errors='replace').splitlines()
capture_evidence = [json.loads(l.split('|', 1)[1]) for l in capture_lines if l.startswith('ASTRO_BIRTHDAY_RESULT|')]
assert [e['checks'] for e in capture_evidence] == [127, 127] and all(e['failures'] == 0 for e in capture_evidence)
before = resources(True)
occupied = occupancy()
assert not occupied and before['C_free_bytes'] >= FLOOR and before['physical_available_bytes'] >= FLOOR
version = subprocess.check_output([str(engine), '--version'], text=True).strip()
assert version == '4.7.2.stable.official.ed1daf0bf' and sha(engine) == 'ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
expected_paths = {b['path'] for b in original_preflight['sources']} | {Path(__file__).relative_to(root).as_posix()}
assert {b['path'] for b in inventory()} <= expected_paths, 'Unexpected runtime file; re-scope first.'
bindings = {b['path']: b for b in original_preflight['sources']}
for p in [Path(__file__), plan_path, parent_path]:
    bindings[p.relative_to(root).as_posix()] = {'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size, 'sha256': sha(p)}
sources = sorted(bindings.values(), key=lambda b: b['path'])
command = [str(engine), '--headless', '--path', str(root), '--script', 'res://' + negative]
started = utc()
start = time.monotonic()
preflight.write_text(json.dumps({'started_utc': started, 'baseline': original_preflight['baseline'], 'sources': sources, 'command': command, 'resource_before': before, 'approved_executable_occupancy': occupied, 'combined_cap_seconds': TIME_CAP, 'output_cap_bytes': OUTPUT_CAP, 'cache_growth_cap_bytes': CACHE_CAP, 'parent_failure_sha256': sha(parent_path), 'preserved_native_manifest_bindings': plan['immutable_native_manifests'], 'no_capture_process_or_retry': True, 'limits': plan['limits']}, indent=2) + '\n')
abort = None
with log.open('xb') as output:
    output.write(b'STEP Missed current-source pipe negatives17\n')
    output.flush()
    process = subprocess.Popen(command, cwd=root, stdout=output, stderr=subprocess.STDOUT)
    print(json.dumps({'step': 'Missed current-source pipe negatives17', 'owned_pid': process.pid}), flush=True)
    last_resource = time.monotonic()
    try:
        while process.poll() is None:
            if time.monotonic() - start > TIME_CAP:
                abort = 'recovery wall cap'
            elif dir_bytes(negative_job) + log.stat().st_size > OUTPUT_CAP:
                abort = 'recovery output cap'
            elif time.monotonic() - last_resource >= 10:
                current = resources()
                last_resource = time.monotonic()
                if current['C_free_bytes'] < FLOOR or current['physical_available_bytes'] < FLOOR:
                    abort = 'actual disk/memory floor'
            content = log.read_bytes()
            if any(w in content for w in [b'ERROR:', b'SCRIPT ERROR', b'Parse Error', b'Compile Error']):
                abort = 'engine error'
            if abort:
                break
            time.sleep(0.25)
    except Exception as e:
        abort = 'recovery monitor exception: ' + type(e).__name__ + ': ' + str(e)
    finally:
        if abort and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
engine_seconds = round(time.monotonic() - start, 3)
negative_lines = log.read_text(encoding='utf-8', errors='replace').splitlines()
negative_evidence = [json.loads(l.split('|', 1)[1]) for l in negative_lines if l.startswith('ASTRO_PIPE_RESULT|')]
evidence = capture_evidence + negative_evidence
errors = [l for l in capture_lines + negative_lines if any(w in l for w in ['ERROR:', 'SCRIPT ERROR', 'Parse Error', 'Compile Error'])]
steps = [{'label': 'Missed current-source pipe negatives17', 'command': command, 'owned_pid': process.pid, 'exit_code': process.returncode, 'elapsed_seconds': engine_seconds, 'abort': abort}]
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
    patch_frames = [f for f in data['frames'] if f.get('live_state', {}).get('phase_index') == 1 and f['live_state'].get('surface_mode') == 'tap']
    patch_trace = bool(patch_frames) and all(all(k in f['live_state'] for k in ['patch_state', 'patch_state_t', 'patch_queue', 'patch_generation', 'patch_last_contact', 'patch_draw_route', 'surface_alpha', 'panel_alpha']) and f['live_state']['patch_draw_route'] == 'target:patch_astronaut' and f['live_state']['widget_mover_path'] == 'res://assets/opera/worlds/widgets/widget_target_astronaut_mover.png' and f['live_state']['patch_repair_source'] == 'res://assets/opera/worlds/widgets/widget_target_astronaut_piece_2.png' for f in patch_frames)
    settled = [x for x in data['frames'] if x['label'] == 'room_return']
    direction = data.get('direction_observations', [])
    native.append({'width': width, 'manifest_path': path.relative_to(root).as_posix(), 'manifest_sha256': sha(path), 'frames': len(pixels), 'pixel_checks': pixels, 'missing_views': sorted(required - labels), 'errors': data['errors'], 'actual_native_mobile': data['display_server'] != 'headless' and data['rendering_method'] == 'mobile' and data['rendering_driver'] == 'vulkan' and data['viewport'] == [width, 720], 'settled_return': len(settled) == 1 and settled[0]['return_fade_alpha'] <= 0.02 and settled[0]['castle_room'] == 'mermaid_pool', 'patch_trace_frames': len(patch_frames), 'patch_trace_bindings_match': patch_trace, 'direction_samples': len(direction), 'direction_and_scale_match': bool(direction) and all(x['flip_h'] == x['expected_flip'] and x['scale_preserved'] for x in direction)})

after = resources(True)
after['output_bytes'] = dir_bytes(negative_job) + log.stat().st_size
after['preserved_native_output_bytes'] = dir_bytes(job) + capture_log.stat().st_size
after['cache_growth_bytes'] = max(0, after['cache_bytes'] - before['cache_bytes'])
source_match = all(sha(root / b['path']) == b['sha256'] for b in sources)
resource_ok = not abort and after['output_bytes'] <= OUTPUT_CAP and after['cache_growth_bytes'] <= CACHE_CAP and after['C_free_bytes'] >= FLOOR
passed = process.returncode == 0 and not abort and not errors and [e['checks'] for e in evidence] == [127, 127, 17] and all(e['failures'] == 0 and all(r['pass'] for r in e['rows']) for e in evidence) and all(len(e['patch_contacts']) == 5 and all(r['valid'] for r in e['patch_contacts']) for e in capture_evidence) and len(native) == 2 and all(all(f['pass'] for f in n['pixel_checks']) and not n['missing_views'] and not n['errors'] and n['actual_native_mobile'] and n['settled_return'] and n['direction_and_scale_match'] and n['patch_trace_bindings_match'] for n in native) and source_match and resource_ok and sha(capture_log) == plan['capture_log_sha256']
result = {'result': 'PASS' if passed else 'FAIL', 'claim': 'RECONCILED_CURRENT_SOURCE_SUBRUN_DIAGNOSTICS', 'started_utc': started, 'finished_utc': utc(), 'combined_engine_seconds': engine_seconds, 'cap_seconds': TIME_CAP, 'steps': steps, 'errors': errors, 'abort': abort, 'evidence': evidence, 'native': native, 'sources': sources, 'source_bindings_still_match': source_match, 'resource_before': before, 'resource_after': after, 'resource_limits_pass': resource_ok, 'resource_claim_scope': 'Additional missed-negative recovery process only; original interrupted native monitoring is not recovered.', 'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log), 'capture_log_path': capture_log.relative_to(root).as_posix(), 'capture_log_sha256': sha(capture_log), 'preflight_sha256': sha(preflight), 'retained_failed_parent_sha256': sha(parent_path), 'original_native_parent_result': 'FAIL', 'original_second_native_exit_code': 'UNRECORDED', 'original_native_resource_continuity': 'UNVERIFIED_AFTER_MONITOR_FAILURE', 'native_reports_terminal_observed_without_duplicate_launch': True, 'meaning': 'Both prior native fixture reports and every existing PNG/source/backend/patch trace are reconciled as literal diagnostics. Only the missed17negative run is newly supervised. No original-parent pass, missing exit/continuous monitoring reconstruction, visual4.6/fulltrusted/strictQA11/normal-cadence/independent/device/child/owner/integration acceptance.'}
receipt.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'result': result['result'], 'checks': [e['checks'] for e in evidence], 'frames': [n['frames'] for n in native], 'failed_checks': [r for e in evidence for r in e['rows'] if not r['pass']], 'engine_seconds': engine_seconds, 'source_match': source_match, 'resource_limits_pass_recovery_only': resource_ok, 'original_native_parent_result': 'FAIL', 'receipt_sha256': sha(receipt)}), flush=True)
sys.exit(0 if passed else 1)
