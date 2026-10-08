from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import threading
import time

root = Path(__file__).resolve().parents[2]
packet = Path(__file__).resolve().parent
log = packet / 'PIPE_MATERIAL_DOCUMENT_TAIL_V3_LOG.txt'
receipt = packet / 'PIPE_MATERIAL_DOCUMENT_TAIL_V3_RECEIPT.json'
seal = packet / 'PIPE_MATERIAL_STAGED_PROVENANCE_V3.json'
assert not any(p.exists() for p in [log, receipt, seal]), 'Preserve every attempt; no automatic retry.'
plan = json.loads((packet / 'PIPE_MATERIAL_DOCUMENT_TAIL_V3_PLAN.json').read_text(encoding='utf-8'))
head_path = packet / 'PIPE_MATERIAL_HEADLESS_V1_RECEIPT.json'
head = json.loads(head_path.read_text(encoding='utf-8'))
assert head['result'] == 'PASS' and all(s['exit_code'] == 0 for s in head['steps'])
impact_path = root / 'design/audit_impacts/astronaut-clearance-20261006.json'
impact = json.loads(impact_path.read_text(encoding='utf-8'))
walk = json.loads((root / 'design/audit_impacts/astronaut-walkthrough-20261007.json').read_text(encoding='utf-8'))
CAP = plan['tail_cap_seconds']
start = time.monotonic()
started = datetime.now(timezone.utc).isoformat()
steps = []
rows = []
failure = None

def utc():
    return datetime.now(timezone.utc).isoformat()

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()

def remaining():
    value = CAP - (time.monotonic() - start)
    assert value > 0, 'Declared60second tail exhausted.'
    return value

receipt.write_text(json.dumps({'result': 'RUNNING', 'started_utc': started, 'cap_seconds': CAP}, indent=2) + '\n', encoding='utf-8')
seal.write_text(json.dumps({'result': 'PENDING', 'scope': 'Current byte seal after the missed final checks.'}, indent=2) + '\n', encoding='utf-8')

def owned_paths():
    return sorted({p for p in impact['files'] + walk['files'] if (root / p).exists()})

def stage_changed(output):
    paths = set(owned_paths())
    tracked = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=root, timeout=remaining()).decode('utf-8').split('\0'))
    changed = set(subprocess.check_output(['git', 'diff', '--name-only', '-z'], cwd=root, timeout=remaining()).decode('utf-8').split('\0'))
    selected = sorted((paths - tracked) | (paths & changed))
    if selected:
        subprocess.run(['git', 'add', '-f', '--', *selected], cwd=root, stdout=output,
                       stderr=subprocess.STDOUT, check=True, timeout=remaining())
    return selected

def run(label, command, output):
    begin = time.monotonic()
    output.write(('\nSTEP ' + label + '\n' + json.dumps(command) + '\n').encode('utf-8'))
    output.flush()
    result = subprocess.run(command, cwd=root, stdout=output, stderr=subprocess.STDOUT, timeout=remaining())
    steps.append({'label': label, 'command': command, 'exit_code': result.returncode,
                  'elapsed_seconds': round(time.monotonic() - begin, 3)})
    print(json.dumps({k: steps[-1][k] for k in ['label', 'exit_code', 'elapsed_seconds']}), flush=True)
    assert result.returncode == 0, label

try:
    # The old8command result is retained at its source; unchanged GDScript checks transfer.
    old_path = packet / 'PIPE_MATERIAL_DOCUMENT_GATES_V1_RECEIPT.json'
    old = json.loads(old_path.read_text(encoding='utf-8'))
    assert old['result'] == 'FAIL' and len(old['steps']) == 8 and all(s['exit_code'] == 0 for s in old['steps'])
    assert sha(root / old['log_path']) == old['log_sha256']
    gd_bindings = [b for b in old['source_bindings'] if b['path'].endswith('.gd')]
    assert all(sha(root / b['path']) == b['sha256'] for b in gd_bindings)
    assert all(sha(root / b['path']) == b['sha256'] for b in head['sources'])
    with log.open('xb') as output:
        initial_staging = stage_changed(output)
        run('Final development coverage', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto'], output)
        status_path = packet / 'STATUS.json'
        status = json.loads(status_path.read_text(encoding='utf-8'))
        status['pipe_material_candidate']['document_tail'] = {
            'result': 'PASS_TWO_MISSED_RECHECKS', 'receipt': receipt.name,
            'original_document_result': 'FAIL', 'original_charge_seconds': (plan['original_charged_source_document_seconds'] + plan['spent_v2_seconds']),
            'meaning': 'Original8individual commands passed; source unchanged, no repeat. Staged seal and final post-record coverage outcome are in tail receipt.'}
        status_path.write_text(json.dumps(status, indent=2) + '\n', encoding='utf-8')
        impact['validation'].append({'command': 'PIPE bounded changed-method final rechecks',
            'result': 'PASS', 'evidence': receipt.name + '; authority/development final commands return0. OriginalV1FAILand181.92scharge retained. No8command rerun, native/full-suite/4.6acceptance. Byte seal and post-record coverage bound in the receipt.'})
        impact_path.write_text(json.dumps(impact, indent=2) + '\n', encoding='utf-8')
        stage_changed(output)
        run('Post-record development coverage', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto'], output)
    current_sources = [{'path': p, 'sha256': sha(root / p)} for p in [
        'scripts/opera_astronaut_surface.gd', 'scripts/opera_career_world_2d.gd',
        'audit/MASTER_AUDIT_2026-08-09.md', 'audit/findings/ACTIVE_FINDINGS_2026-08-13.md',
        'design/05_DOC_LEDGER.md', 'design/audit_impacts/astronaut-clearance-20261006.json',
        'audit/astronaut_clearance_20261006/STATUS.json']]
    result = {'result': 'PASS', 'started_utc': started, 'finished_utc': utc(),
        'steps': steps, 'cap_seconds': CAP, 'elapsed_before_seal_seconds': round(time.monotonic() - start, 3),
        'original_failed_receipt_sha256': sha(old_path),
        'original_charged_source_document_seconds': (plan['original_charged_source_document_seconds'] + plan['spent_v2_seconds']),
        'unchanged_gd_bindings': gd_bindings, 'headless_receipt_sha256': sha(head_path),
        'source_bindings': current_sources, 'log_path': log.relative_to(root).as_posix(), 'log_sha256': sha(log),
        'scope': 'Only remaining development rechecks; V2authority returned0; V1FAILremains, native/visual/fulltrusted/independent/device/child/owner acceptance pending.'}
    receipt.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    stage_changed(subprocess.DEVNULL)
    paths = [p for p in owned_paths() if p != seal.relative_to(root).as_posix()]
    git = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=root, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    timer = threading.Timer(remaining(), lambda: git.kill() if git.poll() is None else None)
    timer.start()
    try:
        for path in paths:
            remaining()
            git.stdin.write((':' + path + '\n').encode('utf-8'))
            git.stdin.flush()
            header = git.stdout.readline().decode('utf-8').strip().split()
            assert len(header) == 3 and header[1] == 'blob', (path, header)
            staged_hash = hashlib.sha256()
            count = int(header[2])
            while count:
                block = git.stdout.read(min(count, 1024**2))
                assert block, 'Owned Git stopped before blob completion.'
                staged_hash.update(block)
                count -= len(block)
            assert git.stdout.read(1) == b'\n', path
            raw_hash = sha(root / path)
            staged = staged_hash.hexdigest()
            equivalence = 'LITERAL_BYTES'
            if raw_hash != staged:
                assert not path.startswith('audit/astronaut_'), 'Literal packet mismatch: ' + path
                normalized = (root / path).read_bytes().replace(b'\r\n', b'\n')
                assert hashlib.sha256(normalized).hexdigest() == staged, 'Unexplained staged difference: ' + path
                equivalence = 'DECLARED_CRLF_TO_LF'
            rows.append({'path': path, 'bytes': (root / path).stat().st_size,
                         'working_sha256': raw_hash, 'staged_sha256': staged, 'equivalence': equivalence})
        git.stdin.close()
        assert git.wait(timeout=remaining()) == 0
    finally:
        timer.cancel()
        if git.poll() is None:
            git.kill()
            git.wait(timeout=5)
    assert all(sha(root / b['path']) == b['sha256'] for b in current_sources)
    out = {'result': 'PASS', 'checked_utc': utc(), 'baseline': impact['baseline'],
        'tail_seconds': round(time.monotonic() - start, 3), 'tail_cap_seconds': CAP,
        'original_failed_document_charge_seconds': plan['original_charged_source_document_seconds'],
        'cumulative_document_seconds': round((plan['original_charged_source_document_seconds'] + plan['spent_v2_seconds']) + time.monotonic() - start, 3),
        'tail_receipt_sha256': sha(receipt), 'headless_receipt_sha256': sha(head_path),
        'surface_sha256': sha(root / 'scripts/opera_astronaut_surface.gd'),
        'declared_paths_verified': len(rows), 'files': rows,
        'scope': 'Current literal staged source/evidence; V1FAILand PENDINGseal preserved. AllV8native/walkthrough pixels remain historical. No fresh native,4.6,fulltrusted,commit/push/integration/release acceptance.'}
    seal.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    subprocess.run(['git', 'add', '-f', '--', seal.relative_to(root).as_posix()], cwd=root, check=True, timeout=remaining())
    assert subprocess.check_output(['git', 'show', ':' + seal.relative_to(root).as_posix()], cwd=root, timeout=remaining()) == seal.read_bytes()
    print(json.dumps({'result': 'PASS', 'tail_seconds': out['tail_seconds'],
        'paths_including_seal': len(rows) + 1, 'tail_receipt_sha256': sha(receipt),
        'seal_sha256': sha(seal), 'original_document_result': 'FAIL', 'native_runs': 0}), flush=True)
except Exception as exc:
    failure = type(exc).__name__ + ': ' + str(exc)
    out = {'result': 'FAIL', 'started_utc': started, 'finished_utc': utc(),
        'elapsed_seconds': round(time.monotonic() - start, 3), 'cap_seconds': CAP,
        'steps': steps, 'failure': failure, 'verified_paths_before_failure': len(rows),
        'original_failed_document_charge_seconds': plan['original_charged_source_document_seconds'],
        'log_sha256': sha(log) if log.exists() else None,
        'meaning': 'Tail failure retained; no automatic retry or clearance.'}
    receipt.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'result': 'FAIL', 'failure': failure[:1200], 'seconds': out['elapsed_seconds'], 'receipt_sha256': sha(receipt)}), flush=True)
    sys.exit(1)
