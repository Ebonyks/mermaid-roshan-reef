from pathlib import Path
from datetime import datetime, timezone
import ctypes
import hashlib
import json
import os
import subprocess
import sys
import time
import shutil

setup_start = time.monotonic()
root = Path(__file__).resolve().parents[2]
packet = Path(__file__).resolve().parent
engine = Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/godot-4.7.2/editor/Godot_v4.7.2-stable_win64.exe')
script = 'audit/astronaut_clearance_20261006/verify_pipe_correction_aspects_v1.gd'
job = root / 'tmp/astronaut_pipe_correction_aspects_v1_20261007'
log = packet / 'PIPE_CORRECTION_ASPECT_V1_LOG.txt'
preflight = packet / 'PIPE_CORRECTION_ASPECT_V1_PREFLIGHT.json'
receipt = packet / 'PIPE_CORRECTION_ASPECT_V1_RECEIPT.json'
assert not job.exists() and not any(p.exists() for p in [log, preflight, receipt]), 'Preserve earlier artifacts; no automatic retry.'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def utc():
    return datetime.now(timezone.utc).isoformat()

def directory_bytes(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file()) if path.exists() else 0

class MemoryStatus(ctypes.Structure):
    _fields_ = [('length', ctypes.c_uint32), ('load', ctypes.c_uint32),
        ('total_phys', ctypes.c_uint64), ('avail_phys', ctypes.c_uint64),
        ('total_page', ctypes.c_uint64), ('avail_page', ctypes.c_uint64),
        ('total_virtual', ctypes.c_uint64), ('avail_virtual', ctypes.c_uint64),
        ('avail_extended', ctypes.c_uint64)]

memory = MemoryStatus()
memory.length = ctypes.sizeof(memory)
assert ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory))
before = {'C_free_bytes': shutil.disk_usage('C:/').free,
    'physical_available_bytes': memory.avail_phys, 'cache_bytes': directory_bytes(root / '.godot')}
assert before['C_free_bytes'] >= 3 * 1024**3 and before['physical_available_bytes'] >= 3 * 1024**3
version = subprocess.check_output([str(engine), '--version'], text=True).strip()
assert version == '4.7.2.stable.official.ed1daf0bf'
for width in [1280, 1600]:
    (job / f'{width}x720').mkdir(parents=True)
names = [script, 'audit/astronaut_clearance_20261006/run_pipe_correction_aspects_v1.py',
    'audit/astronaut_clearance_20261006/PIPE_CORRECTION_ASPECT_PLAN.json',
    'scripts/main.gd', 'scripts/save_state.gd', 'scripts/opera_house.gd', 'scripts/opera_act.gd',
    'scripts/opera_career_world_2d.gd', 'scripts/opera_astronaut_surface.gd',
    'scripts/opera_astronaut_pipe_work.gd', 'scripts/opera_gesture_surface.gd',
    'scripts/opera_roshan_actor.gd', 'scripts/castle_career_routes.gd',
    'scripts/opera_world_hotspot_2d.gd', 'scripts/day_one_director.gd',
    'scripts/chapter_two_director.gd', 'scripts/chapter_two_career_scene_adapter.gd',
    'scripts/chapter_two_party_plan.gd', 'project.godot',
    'assets/opera/worlds/actors/animation/roshan_astronaut_sheet_a.png',
    'design/CHAPTER2_EIGHT_CAREER_PRODUCTION_SPINE_2026-08-30.md']
sources = [{'path': n, 'sha256': sha(root / n)} for n in names]
base = [str(engine), '--headless', '--path', str(root), '--script', 'res://' + script]
started = utc()
start = time.monotonic()
commands = [('Godot analyzer', base + ['--check-only'], None),
    ('1280x720 real-input correction', base, 1280), ('1600x720 real-input correction', base, 1600)]
preflight.write_text(json.dumps({'started_utc': started, 'engine_version': version,
    'engine_sha256': sha(engine), 'sources': sources, 'commands': commands,
    'combined_time_cap_seconds': 150, 'resource_before': before,
    'setup_seconds': round(start - setup_start, 3), 'fixture': 'Explicit prior-six-jobs story fixture and isolated saves. Real card/object/touches, no placement/phase/progress injection.',
    'allocation': 'Small headless diagnostic only, serial aspects, no import/native capture/fullCI and no automatic retry. Prior141.03s pipe/159.35s route costs retained separately.'}, indent=2) + '\n', encoding='utf-8')
steps = []
with log.open('xb') as output:
    for label, command, width in commands:
        env = os.environ.copy()
        if width is not None:
            env['ASTRO_PIPE_WIDTH'] = str(width)
        output.write(('\nSTEP ' + label + '\n').encode())
        output.flush()
        process = subprocess.Popen(command, cwd=root, env=env, stdout=output, stderr=subprocess.STDOUT)
        print(json.dumps({'step': label, 'owned_pid': process.pid, 'combined_time_cap_seconds': 150}), flush=True)
        begin = time.monotonic()
        timed_out = False
        try:
            process.wait(timeout=max(1, 150 - (time.monotonic() - start)))
        except subprocess.TimeoutExpired:
            timed_out = True
            process.terminate()
            process.wait(timeout=15)
        steps.append({'label': label, 'command': command, 'width': width,
            'owned_pid': process.pid, 'exit_code': process.returncode,
            'timed_out': timed_out, 'elapsed_seconds': round(time.monotonic() - begin, 3)})
        if timed_out or process.returncode != 0:
            break
lines = log.read_text(encoding='utf-8', errors='replace').splitlines()
errors = [line for line in lines if any(s in line for s in ['ERROR:', 'SCRIPT ERROR', 'Parse Error', 'Compile Error'])]
records = [json.loads(line.split('|', 1)[1]) for line in lines if line.startswith('ASTRO_PIPE_RESULT|')]
required = {'wrong fueled pipe can be lifted toward correct cell',
    'pending relocation snapshot restores source not target',
    'actual saved pending relocation preserves source and credit',
    'actual pause restores original wrong piece without credit',
    'off-grid drag returns wrong piece to selected tray',
    'selected-tile tap requests owned contact',
    'genuine correction finishes board2 exactly once'}
matrix_ok = len(records) == 2 and {d['width'] for d in records} == {1280, 1600}
for d in records:
    matrix_ok = matrix_ok and d['failures'] == 0 and len(d['contacts']) == 7 and required <= {x['label'] for x in d['rows'] if x['pass']}
after = {'C_free_bytes': shutil.disk_usage('C:/').free, 'cache_bytes': directory_bytes(root / '.godot'),
    'artifact_bytes': directory_bytes(job) + log.stat().st_size + preflight.stat().st_size}
after['cache_growth_bytes'] = max(0, after['cache_bytes'] - before['cache_bytes'])
resource_ok = after['C_free_bytes'] >= 3 * 1024**3 and after['artifact_bytes'] <= 32 * 1024**2 and after['cache_growth_bytes'] <= 16 * 1024**2
matched = all(sha(root / x['path']) == x['sha256'] for x in sources)
passed = len(steps) == 3 and all(x['exit_code'] == 0 and not x['timed_out'] for x in steps) and not errors and matrix_ok and resource_ok and matched
data = {'result': 'PASS' if passed else 'FAIL', 'started_utc': started, 'finished_utc': utc(),
    'engine_version': version, 'engine_sha256': sha(engine), 'steps': steps,
    'elapsed_seconds': round(time.monotonic() - start, 3), 'combined_time_cap_seconds': 150,
    'setup_seconds': round(start - setup_start, 3), 'total_observed_seconds': round(time.monotonic() - setup_start, 3),
    'resource_before': before, 'resource_after': after, 'resource_limits_pass': resource_ok,
    'errors': errors, 'evidence': records, 'required_matrix_pass': matrix_ok,
    'sources': sources, 'source_bindings_still_match': matched,
    'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log),
    'preflight_path': preflight.relative_to(root).as_posix(), 'preflight_sha256': sha(preflight),
    'isolated_save_files': [{'path': f.relative_to(root).as_posix(), 'sha256': sha(f), 'size_bytes': f.stat().st_size} for f in sorted(job.rglob('*')) if f.is_file()],
    'meaning': 'Genuine headless wrong-plan/lifting/save/pause/selected-tile recovery and actual shared-transform bounds at both aspects. No native pixels, action appearance/body proportions,>=4.6, fullsuite/fullchapter, independent/device/child/owner acceptance.'}
receipt.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'result': data['result'], 'aspect_checks': {str(x['width']): x['checks'] for x in records},
    'errors': errors[:8], 'failed_checks': [x for d in records for x in d['rows'] if not x['pass']],
    'elapsed_seconds': data['elapsed_seconds'], 'receipt_sha256': sha(receipt), 'sources_match': matched}), flush=True)
sys.exit(0 if passed else 1)
