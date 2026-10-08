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
receipt = packet / 'PIPE_CONTACT_DOCUMENT_GATES_V1_RECEIPT.json'
log = packet / 'PIPE_CONTACT_DOCUMENT_GATES_V1_LOG.txt'
assert not receipt.exists() and not log.exists(), 'Preserve a previous attempt; no automatic retry.'
impact = root / 'design/audit_impacts/astronaut-clearance-20261006.json'
record = json.loads(impact.read_text(encoding='utf-8'))
gd_files = sorted(p for p in record['files'] if p.endswith('.gd') and (root / p).exists())
bindings = gd_files + [
    'audit/MASTER_AUDIT_2026-08-09.md',
    'audit/findings/ACTIVE_FINDINGS_2026-08-13.md',
    'design/05_DOC_LEDGER.md',
    'audit/astronaut_clearance_20261006/PIPE_CONTACT_REVIEW.json',
    'audit/astronaut_clearance_20261006/PIPE_CONTACT_IMPLEMENTATION_PLAN.json',
    'audit/astronaut_clearance_20261006/run_pipe_contact_document_gates_v1.py',
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
provenance = packet / 'PIPE_CONTACT_STAGED_PROVENANCE_V1.json'
assert not provenance.exists()
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
            stderr=subprocess.STDOUT, timeout=max(1, 120 - (time.monotonic() - start)))
        steps.append({'label': label, 'command': command, 'exit_code': process.returncode,
            'elapsed_seconds': round(time.monotonic() - begin, 3)})
        output.flush()
        print(json.dumps({'step': label, 'exit_code': process.returncode,
            'elapsed_seconds': steps[-1]['elapsed_seconds']}), flush=True)
        if process.returncode != 0:
            break
current_receipts = []
for name in ['PIPE_CONTACT_V5_RECEIPT.json', 'PIPE_CONTACT_NEGATIVE_V1_RECEIPT.json']:
    path = packet / name
    data = json.loads(path.read_text())
    assert data['result'] == 'PASS'
    assert all(sha(root / p['path']) == p['sha256'] for p in data['sources'])
    assert sha(root / data['log_path']) == data['log_sha256']
    current_receipts.append({'path': path.relative_to(root).as_posix(), 'sha256': sha(path),
        'checks': data['evidence'][0]['checks'], 'source_and_native_log_bindings_match': True})
snapshot = json.loads((packet / 'PIPE_CONTACT_V4_SOURCE_SNAPSHOT.json').read_text())
assert sha(root / snapshot['literal_snapshot']) == snapshot['sha256']
matched = all(sha(root / p['path']) == p['sha256'] for p in sources)
passed = len(steps) == len(commands) and all(s['exit_code'] == 0 for s in steps) and matched
result = {'result': 'PASS' if passed else 'FAIL', 'started_utc': started, 'finished_utc': utc(),
    'elapsed_seconds': round(time.monotonic() - start, 3), 'time_cap_seconds': 120,
    'steps': steps, 'gd_files': gd_files, 'source_bindings': sources,
    'source_bindings_match': matched, 'current_runtime_receipts': current_receipts,
    'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log),
    'meaning': 'Source syntax, authority, coverage, 2D no-regression and literal runtime-log binding only. '
        'Historical failing fixture1 is data under audit, outside ci.sh production scripts parser scope. '
        'No full trusted suite, native pixels/action score, independent/device/child/owner or integration acceptance.'}
receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'result': result['result'], 'steps': len(steps),
    'gd_files': len(gd_files), 'elapsed_seconds': result['elapsed_seconds'],
    'receipt_sha256': sha(receipt), 'source_bindings_match': matched}), flush=True)
sys.exit(0 if passed else 1)
