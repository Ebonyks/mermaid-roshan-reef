from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[2]
packet = Path(__file__).resolve().parent
log = packet / 'PIPE_PATH_QUERY_V1_LOG.txt'
receipt = packet / 'PIPE_PATH_QUERY_V1_RECEIPT.json'
assert not log.exists() and not receipt.exists(), 'Preserve attempts; no automatic retry.'
plan = json.loads((packet / 'PIPE_PATH_QUERY_V1_PLAN.json').read_text(encoding='utf-8'))
records = [json.loads((root / name).read_text(encoding='utf-8')) for name in
    ['design/audit_impacts/astronaut-clearance-20261006.json', 'design/audit_impacts/astronaut-walkthrough-20261007.json']]
owned = {p for record in records for p in record['files'] if (root / p).exists()}
directories = ['audit/astronaut_clearance_20261006', 'audit/astronaut_walkthrough_20261007']
outside = sorted(p for p in owned if not any(p.startswith(d + '/') for d in directories))
scope = directories + outside
assert not any(p.startswith(('assets/', '.godot/')) for p in scope)
started = datetime.now(timezone.utc).isoformat()
start = time.monotonic()
steps = []
output_names = {}
failure = None
with log.open('xb') as stream:
    for label, command in [('tracked', ['git', 'ls-files', '--cached', '-z', '--', *scope]),
                           ('changed', ['git', 'diff', '--name-only', '-z', '--', *scope])]:
        begin = time.monotonic()
        remaining = plan['trial_cap_seconds'] - (begin - start)
        assert remaining > 0
        try:
            result = subprocess.run(command, cwd=root, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=remaining)
            names = [name for name in result.stdout.decode('utf-8').split('\0') if name]
            scoped = all(any(name == path or name.startswith(path + '/') for path in scope) for name in names)
            output_names[label] = names
            stream.write((json.dumps({'label': label, 'command': command,
                'stdout_paths': names}) + '\n').encode('utf-8'))
            stream.write(result.stderr)
            steps.append({'label': label, 'exit_code': result.returncode,
                'elapsed_seconds': round(time.monotonic() - begin, 3),
                'returned_paths': len(names), 'all_paths_scoped': scoped,
                'stderr_bytes': len(result.stderr),
                'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
                'stderr_sha256': hashlib.sha256(result.stderr).hexdigest()})
            if result.returncode != 0 or not scoped:
                failure = label + ': nonzero exit or out-of-scope path'
                break
        except subprocess.TimeoutExpired:
            failure = label + ': original15second trial cap exhausted'
            break
        stream.flush()
passed = failure is None and len(steps) == 2 and all(s['exit_code'] == 0 and s['all_paths_scoped'] for s in steps)
selected = sorted((owned - set(output_names.get('tracked', []))) | (owned & set(output_names.get('changed', []))))
out = {'result': 'PASS' if passed else 'FAIL', 'started_utc': started,
    'finished_utc': datetime.now(timezone.utc).isoformat(),
    'elapsed_seconds': round(time.monotonic() - start, 3), 'cap_seconds': plan['trial_cap_seconds'],
    'steps': steps, 'failure': failure, 'query_scope': scope, 'declared_existing_paths': len(owned),
    'candidate_paths_to_stage': selected, 'staging_performed': False,
    'auditor_or_engine_run': False, 'prior_source_document_seconds': plan['prior_source_document_seconds'],
    'log_path': log.relative_to(root).as_posix(), 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(),
    'meaning': 'Read-only preparation timing and scoping only. Final coverage, byte seal, native/visual/independent/device/child/owner clearance are not established.'}
receipt.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'result': out['result'], 'seconds': out['elapsed_seconds'],
    'steps': steps, 'candidate_staging_paths': len(selected),
    'receipt_sha256': hashlib.sha256(receipt.read_bytes()).hexdigest()}), flush=True)
sys.exit(0 if passed else 1)
