from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[2]
packet = Path(__file__).resolve().parent
python = sys.executable
receipt = packet / 'PATCH_READABILITY_DOCUMENT_GATES_V1_RECEIPT.json'
log = packet / 'PATCH_READABILITY_DOCUMENT_GATES_V1_LOG.txt'
assert not receipt.exists() and not log.exists(), 'Preserve a previous attempt; no automatic retry.'
impact = root / 'design/audit_impacts/astronaut-clearance-20261006.json'
record = json.loads(impact.read_text(encoding='utf-8'))
gd_files = sorted(p for p in record['files'] if p.endswith('.gd') and (root / p).exists())
bindings = gd_files + [
    'audit/MASTER_AUDIT_2026-08-09.md',
    'audit/findings/ACTIVE_FINDINGS_2026-08-13.md',
    'design/05_DOC_LEDGER.md',
    'audit/astronaut_clearance_20261006/PIPE_CONTACT_REVIEW.json',
    'audit/astronaut_clearance_20261006/CURRENT_ROUTE_CONTACT_RECHECK_PLAN.json',
    'audit/astronaut_clearance_20261006/CURRENT_ROUTE_CONTACT_RECHECK_REVIEW.json',
    'audit/astronaut_clearance_20261006/PIPE_CORRECTION_ASPECT_PLAN.json',
    'audit/astronaut_clearance_20261006/PIPE_CORRECTION_ASPECT_REVIEW.json',
    'audit/astronaut_clearance_20261006/NATIVE_BIRTHDAY_CAPTURE_V4_REVIEW.json',
    'audit/astronaut_clearance_20261006/RELEASE_OWNERSHIP_REVIEW.json',
    'audit/astronaut_clearance_20261006/PIPE_RELEASE_OWNERSHIP_PLAN.json',
    'audit/astronaut_clearance_20261006/NATIVE_BIRTHDAY_CAPTURE_V1_REVIEW.json',
    'audit/astronaut_clearance_20261006/NATIVE_BIRTHDAY_CAPTURE_V2_REVIEW.json',
    'audit/astronaut_clearance_20261006/PIPE_CONTACT_IMPLEMENTATION_PLAN.json',
    'audit/astronaut_clearance_20261006/run_patch_readability_document_gates_v1.py',
    'audit/astronaut_clearance_20261006/PIPE_TRAVEL_PLAN.json',
    'audit/astronaut_clearance_20261006/PIPE_TRAVEL_REVIEW.json',
    'audit/astronaut_clearance_20261006/VALVE_CONTACT_REVIEW.json',
    'audit/astronaut_clearance_20261006/VALVE_CONTACT_PLAN.json',
    'audit/astronaut_clearance_20261006/VALVE_CONTACT_NATIVE_V2_PLAN.json',
    'audit/astronaut_clearance_20261006/VALVE_CONTACT_DOCUMENT_GATES_V2_PLAN.json',
    'audit/astronaut_clearance_20261006/PATCH_CONTACT_PLAN.json',
    'audit/astronaut_clearance_20261006/PATCH_CONTACT_REVIEW.json',
    'audit/astronaut_clearance_20261006/PATCH_READABILITY_PLAN.json',
    'audit/astronaut_clearance_20261006/PATCH_READABILITY_REVIEW.json',
    'audit/astronaut_clearance_20261006/PATCH_READABILITY_NATIVE_RECOVERY_V1_PLAN.json',
    'audit/astronaut_clearance_20261006/run_patch_readability_native_recovery_v1.py',
    'audit/astronaut_clearance_20261006/PATCH_READABILITY_NATIVE_V1_RECEIPT.json',
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc():
    return datetime.now(timezone.utc).isoformat()


sources = [{'path': p, 'sha256': sha(root / p)} for p in bindings]
started = utc()
start = time.monotonic()
receipt.write_text(json.dumps({'result': 'RUNNING', 'started_utc': started,
    'scope': 'Non-engine source/document gates; no import/capture/fullCI.'}, indent=2) + '\n')
provenance = packet / 'PATCH_READABILITY_STAGED_PROVENANCE_V1.json'
if provenance.exists():
    assert json.loads(provenance.read_text())["result"] == "PENDING", "Preserve a sealed provenance receipt."
else:
    provenance.write_text(json.dumps({'result': 'PENDING',
    'scope': 'Literal staged-byte verification will be sealed after source/document gates.'}, indent=2) + '\n')
steps = []
commands = [
    ('Changed GDScript parser', [python, '-X', 'utf8', '-B', '-m', 'gdtoolkit.parser', *gd_files]),
    ('Changed GDScript inference', [python, '-X', 'utf8', '-B', 'tools/lint_inference.py', *gd_files]),
    ('Document authority', [python, '-X', 'utf8', '-B', 'tools/audit_document_authority.py']),
    ('Authority/development units', [python, '-X', 'utf8', '-B', '-m', 'unittest',
        'tools.tests.test_audit_document_authority', 'tools.tests.test_audit_development']),
    ('Authority stress', [python, '-X', 'utf8', '-B', 'tools/audit_document_authority.py', '--stress']),
    ('Shrinking 2D regression', [python, '-X', 'utf8', '-B', 'tools/audit_game_2d.py', '--regression-gate']),
    ('Development coverage', [python, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto']),
    ('Staged whitespace', ['git', 'diff', '--cached', '--check']),
]
with log.open('xb') as output:
    for label, command in commands:
        if label in ['Development coverage', 'Staged whitespace']:
            paths = [p for p in record['files'] if (root / p).exists()]
            staged = subprocess.run(['git', 'add', '-f', '--', *paths], cwd=root,
                capture_output=True, text=True, timeout=30)
            assert staged.returncode == 0, staged.stderr[-2000:]
        output.write(('\nSTEP ' + label + '\n').encode())
        output.flush()
        begin = time.monotonic()
        process = subprocess.run(command, cwd=root, stdout=output,
            stderr=subprocess.STDOUT, timeout=max(1, 120.0 - (time.monotonic() - start)))
        steps.append({'label': label, 'command': command, 'exit_code': process.returncode,
            'elapsed_seconds': round(time.monotonic() - begin, 3)})
        output.flush()
        print(json.dumps({'step': label, 'exit_code': process.returncode,
            'elapsed_seconds': steps[-1]['elapsed_seconds']}), flush=True)
        if process.returncode != 0:
            break
current_receipts = []
headpath = packet / 'PATCH_READABILITY_HEADLESS_V1_RECEIPT.json'
head = json.loads(headpath.read_text())
assert head['result'] == 'PASS' and [x['checks'] for x in head['evidence']] == [143]
assert all(x['failures'] == 0 and all(r['pass'] for r in x['rows']) for x in head['evidence'])
assert len(head['evidence'][0]['patch_contacts']) == 5 and all(r['valid'] for r in head['evidence'][0]['patch_contacts'])
assert all(sha(root / b['path']) == b['sha256'] for b in head['sources'])
assert sha(root / head['log_path']) == head['log_sha256']
current_receipts.append({'path': headpath.relative_to(root).as_posix(), 'sha256': sha(headpath), 'checks': [143], 'source_log_bindings_match': True, 'headless_contact_coverage': 'Five actual accepted patch commits before/after reload, including rapid remaining-three queue completion; sampled pre-reload valve rows plus final-contact checks both circle portions. Not full temporal review.'})
path = packet / 'PATCH_READABILITY_NATIVE_RECOVERY_V1_RECEIPT.json'
data = json.loads(path.read_text())
assert data['result'] == 'PASS'
parent = json.loads((packet / 'PATCH_READABILITY_NATIVE_V1_RECEIPT.json').read_text())
assert parent['result'] == data['original_native_parent_result'] == 'FAIL'
assert sha(packet / 'PATCH_READABILITY_NATIVE_V1_RECEIPT.json') == data['retained_failed_parent_sha256']
assert data['original_second_native_exit_code'] == 'UNRECORDED'
assert data['original_native_resource_continuity'] == 'UNVERIFIED_AFTER_MONITOR_FAILURE'
assert [x['checks'] for x in data['evidence']] == [127, 127, 17]
assert all(x['failures'] == 0 and all(row['pass'] for row in x['rows']) for x in data['evidence'])
assert [len(e['patch_contacts']) for e in data['evidence'][:2]] == [5, 5]
assert all(row['valid'] for e in data['evidence'][:2] for row in e['patch_contacts'])
assert all(row['valid'] for e in data['evidence'][:2] for row in e['valve_contacts'])
assert all(sha(root / b['path']) == b['sha256'] for b in data['sources'])
assert sha(root / data['log_path']) == data['log_sha256']
assert sha(root / data['capture_log_path']) == data['capture_log_sha256']
for native in data['native']:
    assert sha(root / native['manifest_path']) == native['manifest_sha256']
    assert all(sha(root / row['path']) == row['sha256'] for row in native['pixel_checks'])
    assert native['actual_native_mobile'] and native['settled_return'] and native['direction_and_scale_match'] and native['patch_trace_bindings_match']
current_receipts.append({'path': path.relative_to(root).as_posix(), 'sha256': sha(path),
    'checks': [x['checks'] for x in data['evidence']], 'aspects': [x['width'] for x in data['native']],
    'source_log_native_pixel_bindings_match': True,
    'original_native_parent': 'FAIL', 'second_native_exit_code': 'UNRECORDED',
    'original_native_resource_continuity': 'UNVERIFIED_AFTER_MONITOR_FAILURE',
    'recovery_scope': 'Only missed17negative checks newly supervised; preserved native subruns reconciled.'})
failed = json.loads((packet / 'VALVE_CONTACT_NATIVE_V1_RECEIPT.json').read_text())
assert failed['result'] == 'FAIL'
assert sha(packet / 'PATCH_READABILITY_BEFORE_SURFACE_SOURCE.txt') == '4c6f460f03d6b9610cb3d14305cf069f6841e122f200cdaa2f59f49120906c63'
assert sha(packet / 'PATCH_BEFORE_WORLD_SOURCE.txt') == '9368b7f398bbc57ec646c6068cda1ebafb8fee5a570d60049bd7ce9c04532d25'
assert sha(packet / 'PATCH_BEFORE_SURFACE_SOURCE.txt') == 'a8b1e12c6bfaecd5dda07c74ff2fdf2f373adcb7bb92f61b28fb5998d2887368'
assert sha(packet / 'VALVE_BEFORE_WORLD_SOURCE.txt') == '6f61646adc21cc2392fa18d3b3624f7c5f2bb4de050a6b858a7705980f5d2590'
assert sha(packet / 'VALVE_BEFORE_SURFACE_SOURCE.txt') == '84b0806ee388e1d0150629c872318c92fd3f614e949385a26f97eac0c0d82809'
assert sha(packet / 'PIPE_TRAVEL_BEFORE_SOURCE.txt') == '654504436f9ba3040edfd3cbdf277aed2337a7799f9de5b8d5573369bdacdc39'
assert sha(packet / 'PIPE_RELEASE_BEFORE_SOURCE.txt') == 'd39bbed5c738535167ce9c526596fee32b4cfc369a5a2d376f1a7cf58e841d44'
snapshot = json.loads((packet / 'PIPE_CONTACT_V4_SOURCE_SNAPSHOT.json').read_text())
assert sha(root / snapshot['literal_snapshot']) == snapshot['sha256']
matched = all(sha(root / p['path']) == p['sha256'] for p in sources)
passed = len(steps) == len(commands) and all(s['exit_code'] == 0 for s in steps) and matched
result = {'result': 'PASS' if passed else 'FAIL', 'started_utc': started, 'finished_utc': utc(),
    'elapsed_seconds': round(time.monotonic() - start, 3), 'time_cap_seconds': 120.0, 'prior_patch_document_seconds': 69.653, 'prior_valve_document_seconds': 86.111,
    'steps': steps, 'gd_files': gd_files, 'source_bindings': sources,
    'source_bindings_match': matched, 'current_runtime_receipts': current_receipts,
    'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log),
    'meaning': 'Source syntax, authority, coverage, 2D no-regression and literal runtime-log binding only. '
        'Historical failing fixtures remain literal data under audit, outside ci.sh production scripts parser scope. '
        'NativeV8 both-aspect pixels, source/draw/alpha PATCH trace, five actual patch contact commits peraspect, valve contact and pipe direction rows are byte-verified diagnostics; previous world/surface receipts are historical and every complete action remains below4.6. Original PATCH readability native parent remains FAIL after the save-rotation accounting race; second native exit code and continuous resource monitoring remain unverified. The recovery supervises only missed17negatives. The earlier VALVE nativeV1prelaunch failure is an operator tool record, not a runner engine log. '
        'No full trusted suite, strict clean/fresh runtime, independent/device/child/owner or integration acceptance.'}
receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'result': result['result'], 'steps': len(steps),
    'gd_files': len(gd_files), 'elapsed_seconds': result['elapsed_seconds'],
    'receipt_sha256': sha(receipt), 'source_bindings_match': matched}), flush=True)
sys.exit(0 if passed else 1)
