from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[2]
packet = Path(__file__).resolve().parent
log = packet / 'PIPE_MATERIAL_DOCUMENT_GATES_V1_LOG.txt'
receipt = packet / 'PIPE_MATERIAL_DOCUMENT_GATES_V1_RECEIPT.json'
seal = packet / 'PIPE_MATERIAL_STAGED_PROVENANCE_V1.json'
assert not any(p.exists() for p in [log, receipt, seal]), 'Preserve all attempts; no automatic retry.'
impact_path = root / 'design/audit_impacts/astronaut-clearance-20261006.json'
record = json.loads(impact_path.read_text(encoding='utf-8'))
gd_files = sorted(p for p in record['files'] if p.endswith('.gd') and (root / p).exists())
prior_seconds = sum(json.loads((packet / name).read_text(encoding='utf-8'))['elapsed_seconds']
    for name in ['PIPE_MATERIAL_SOURCE_GATES_V1_RECEIPT.json', 'PIPE_MATERIAL_PREPARATION_V1_RECEIPT.json'])
CAP = 180.0 - prior_seconds
start = time.monotonic()

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()

started = utc()
bindings = gd_files + ['audit/MASTER_AUDIT_2026-08-09.md',
    'audit/findings/ACTIVE_FINDINGS_2026-08-13.md', 'design/05_DOC_LEDGER.md',
    *['audit/astronaut_clearance_20261006/' + name for name in [
        'PIPE_MATERIAL_PLAN.json', 'PIPE_MATERIAL_IMPLEMENTATION_START.json',
        'PIPE_MATERIAL_REVIEW.json', 'PIPE_MATERIAL_SOURCE_GATES_V1_RECEIPT.json',
        'PIPE_MATERIAL_PREPARATION_V1_RECEIPT.json', 'run_pipe_material_headless_v1.py',
        'run_pipe_material_native_v1.py', 'run_pipe_material_document_gates_v1.py']]]
sources = [{'path': p, 'sha256': sha(root / p)} for p in bindings]
receipt.write_text(json.dumps({'result': 'RUNNING', 'started_utc': started,
    'remaining_cap_seconds': CAP, 'prior_source_seconds': prior_seconds}, indent=2) + '\n', encoding='utf-8')
seal.write_text(json.dumps({'result': 'PENDING', 'scope': 'Literal staged bytes after source/document gates.'}, indent=2) + '\n', encoding='utf-8')
steps = []
commands = [
    ('Changed GDScript parser', [sys.executable, '-X', 'utf8', '-B', '-m', 'gdtoolkit.parser', *gd_files]),
    ('Changed GDScript inference', [sys.executable, '-X', 'utf8', '-B', 'tools/lint_inference.py', *gd_files]),
    ('Document authority', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_document_authority.py']),
    ('Authority/development units', [sys.executable, '-X', 'utf8', '-B', '-m', 'unittest',
        'tools.tests.test_audit_document_authority', 'tools.tests.test_audit_development']),
    ('Authority stress', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_document_authority.py', '--stress']),
    ('Shrinking2D regression', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_game_2d.py', '--regression-gate']),
    ('Development coverage', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto']),
    ('Staged whitespace', ['git', 'diff', '--cached', '--check']),
]

def stage(paths, output):
    for command in [['git', 'add', '-f', '--', *paths], ['git', 'add', '--renormalize', '--', *paths]]:
        result = subprocess.run(command, cwd=root, stdout=output, stderr=subprocess.STDOUT,
            timeout=max(1.0, CAP - (time.monotonic() - start)))
        assert result.returncode == 0, 'Owned-path staging failed.'

def run(label, command, output):
    begin = time.monotonic()
    output.write(('\nSTEP ' + label + '\n' + json.dumps(command) + '\n').encode('utf-8'))
    output.flush()
    try:
        process = subprocess.run(command, cwd=root, stdout=output, stderr=subprocess.STDOUT,
            timeout=max(1.0, CAP - (time.monotonic() - start)))
        exit_code, error = process.returncode, None
    except subprocess.TimeoutExpired:
        exit_code, error = -1, 'Original180s combined source/document cap exhausted.'
    steps.append({'label': label, 'command': command, 'exit_code': exit_code,
        'elapsed_seconds': round(time.monotonic() - begin, 3), 'error': error})
    print(json.dumps({k: steps[-1][k] for k in ['label', 'exit_code', 'elapsed_seconds', 'error']}), flush=True)
    return exit_code == 0

failure = None
paths = []
try:
    with log.open('xb') as output:
        paths = sorted(p for p in record['files'] if (root / p).exists())
        stage(paths, output)
        for label, command in commands:
            if not run(label, command, output):
                failure = label
                break
        if failure is None:
            record['validation'].append({'command': 'PIPE material source/document gates V1',
                'result': 'PASS_SCOPED8_COMMANDS',
                'evidence': 'PIPE_MATERIAL_DOCUMENT_GATES_V1_RECEIPT.json and literal log; parser/inference, authority,54units/6stress,2Dno-regression, development and staged whitespace. Exact-engine/native/fulltrusted/independent/device/child/owner still pending; historical evidence is preserved.'})
            impact_path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
            status_path = packet / 'STATUS.json'
            status = json.loads(status_path.read_text(encoding='utf-8'))
            status['pipe_material_candidate']['document_gates'] = {
                'receipt': receipt.name, 'result': 'SCOPED8_COMMANDS_PASS_FINAL_RECHECK_PENDING',
                'scope': 'No engine/native/fulltrusted or4.6acceptance.'}
            status_path.write_text(json.dumps(status, indent=2) + '\n', encoding='utf-8')
            stage(paths, output)
            for label, command in [
                ('Final document authority', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_document_authority.py']),
                ('Final development coverage', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto']),
            ]:
                if not run(label, command, output):
                    failure = label
                    break
except Exception as exc:
    failure = type(exc).__name__ + ': ' + str(exc)

matched = all(sha(root / binding['path']) == binding['sha256'] for binding in sources)
passed = failure is None and matched and len(steps) == 10 and all(s['exit_code'] == 0 for s in steps)
result = {'result': 'PASS' if passed else 'FAIL', 'started_utc': started, 'finished_utc': utc(),
    'elapsed_seconds': round(time.monotonic() - start, 3), 'remaining_cap_seconds': CAP,
    'original_source_document_cap_seconds': 180.0, 'prior_source_seconds': prior_seconds,
    'steps': steps, 'gd_files': gd_files, 'source_bindings': sources,
    'source_bindings_match': matched, 'failure': failure,
    'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log),
    'scope': 'Source/document gates only; cached Canvas material candidate has no engine/native/full-suite/strictQA11/4.6/independent/device/child/owner acceptance. Prior failures/costs retained.'}
receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
if not passed:
    print(json.dumps({'result': 'FAIL', 'failure': failure, 'seconds': result['elapsed_seconds'], 'receipt_sha256': sha(receipt)}), flush=True)
    sys.exit(1)

# Check staged blobs through one Git process; retain literal packet bytes.
begin = time.monotonic()
walk = json.loads((root / 'design/audit_impacts/astronaut-walkthrough-20261007.json').read_text(encoding='utf-8'))
paths = sorted(set(paths) | {p for p in walk['files'] if (root / p).exists()})
paths.remove(seal.relative_to(root).as_posix())
with subprocess.Popen(['git', 'cat-file', '--batch'], cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as git:
    stage(paths, subprocess.DEVNULL)
    rows = []
    for path in paths:
        assert time.monotonic() - start <= CAP, 'Original document cap exhausted during staged seal.'
        git.stdin.write((':' + path + '\n').encode('utf-8'))
        git.stdin.flush()
        header = git.stdout.readline().decode('utf-8').strip().split()
        assert len(header) == 3 and header[1] == 'blob', (path, header)
        remaining = int(header[2])
        blob = bytearray()
        while remaining:
            block = git.stdout.read(min(remaining, 1024**2))
            assert block, path
            blob.extend(block)
            remaining -= len(block)
        assert git.stdout.read(1) == b'\n', path
        working = (root / path).read_bytes()
        raw = hashlib.sha256(working).hexdigest()
        staged = hashlib.sha256(blob).hexdigest()
        mode = 'LITERAL_BYTES'
        if raw != staged:
            assert not path.startswith('audit/astronaut_'), 'A literal packet blob changed: ' + path
            assert working.replace(b'\r\n', b'\n') == blob, 'Unexplained staged difference: ' + path
            mode = 'DECLARED_CRLF_TO_LF'
        rows.append({'path': path, 'bytes': len(working), 'working_sha256': raw,
                     'staged_sha256': staged, 'equivalence': mode})
    git.stdin.close()
    assert git.wait(timeout=5) == 0
status_path = packet / 'STATUS.json'
# Keep the sealed status and receipt literal; final recheck result is in receipt.
out = {'result': 'PASS', 'checked_utc': utc(), 'baseline': record['baseline'],
       'surface_sha256': sha(root / 'scripts/opera_astronaut_surface.gd'),
       'document_receipt_sha256': sha(receipt), 'files': rows,
       'declared_paths_verified': len(rows), 'seal_seconds': round(time.monotonic() - begin, 3),
       'combined_source_document_seconds': round(time.monotonic() - start + prior_seconds, 3),
       'original_cap_seconds': 180.0,
       'meaning': 'Literal staged packet/source proof; all V8 captures and old staged receipts retain their historical source scope. No commit/push, fresh runtime/native/fulltrusted/4.6 acceptance.'}
seal.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
subprocess.run(['git', 'add', '-f', '--', seal.relative_to(root).as_posix()], cwd=root, check=True,
    timeout=max(1.0, CAP - (time.monotonic() - start)))
assert subprocess.check_output(['git', 'show', ':' + seal.relative_to(root).as_posix()], cwd=root) == seal.read_bytes()
print(json.dumps({'result': 'PASS', 'steps': len(steps), 'gd_files': len(gd_files),
    'declared_paths_verified_including_seal': len(rows) + 1,
    'combined_source_document_seconds': out['combined_source_document_seconds'],
    'receipt_sha256': sha(receipt), 'seal_sha256': sha(seal),
    'engine_runs': 0, 'native_runs': 0}), flush=True)
