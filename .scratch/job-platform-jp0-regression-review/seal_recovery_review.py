"""Read-only project inspection; write a recovery receipt in this review directory."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
PROJECT = Path('H:/CodexWorktrees/mermaid-roshan-reef-job-platform-jp0-20260930')
EVIDENCE = Path('H:/CodexWorktrees/job-platform-jp0-evidence-20260930')
ENGINE = Path('C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot.exe')
BASELINE = '7f068cb80766edd52a110cc1cb3958158f829822'
CASES = {
    'probe_audit': 'probe-audit-core-20261001',
    'probe_audio': 'probe-audio-core-20261001',
    'probe_dust_boss_balance': 'probe-dust-boss-balance-core-20261001',
}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

payload_path = EVIDENCE / 'full-ci3-source-payload.json'
payload = read_json(payload_path)
for row in payload['files']:
    raw = (PROJECT / row['path']).read_bytes()
    assert sha(raw) == row['sha256'], row['path']
    assert sha(raw.replace(b'\r\n', b'\n')) == row['canonical_lf_sha256'], row['path']

full_log = (EVIDENCE / 'full-ci3.log').read_bytes()
full_result = read_json(EVIDENCE / 'full-ci3-result.json')
processes = re.findall(r'^PROBE (\w+) process exit: (-?\d+)\s*$', full_log.decode('utf-8'), re.MULTILINE)
failed = {name: int(code) for name, code in processes if int(code)}
assert len(processes) == 82
assert failed == {name: 127 for name in CASES}
assert full_result['exit_code'] == 1

recovery = []
for name, directory in CASES.items():
    case = HERE / directory
    result = read_json(case / 'result.json')
    assert result['actual_engine_exit_code'] == 0, name
    stdout = (case / 'stdout.raw.txt').read_bytes()
    stderr = (case / 'stderr.raw.txt').read_bytes()
    text = stdout.decode('utf-8')
    assert not re.search(r'FAIL|FAILED|ISSUE|TIMEOUT|STUCK|DID NOT|MISSING|SCRIPT ERROR|Parse Error|Compile Error', text), name
    assert not re.search(r'SCRIPT ERROR|Parse Error|Compile Error|ERROR:', stderr.decode('utf-8')), name
    assert ('AUDIT|persisted wins: 5/5' in text if name == 'probe_audit' else 'ALL OK' in text), name
    source_path = f'scripts/{name}.gd'
    current = (PROJECT / source_path).read_bytes().replace(b'\r\n', b'\n')
    baseline = subprocess.run(['git', 'show', f'{BASELINE}:{source_path}'], cwd=PROJECT, check=True, capture_output=True).stdout.replace(b'\r\n', b'\n')
    assert current == baseline, name
    recovery.append({
        'probe': name,
        'source_path': source_path,
        'canonical_source_sha256': sha(current),
        'canonical_source_equals_immutable_baseline': BASELINE,
        'result': result,
        'stdout': str(case / 'stdout.raw.txt'),
        'stdout_sha256': sha(stdout),
        'stderr': str(case / 'stderr.raw.txt'),
        'stderr_sha256': sha(stderr),
        'stderr_classification': 'Existing raw-image import warnings only' if name == 'probe_audit' else 'Empty',
    })

engine_sha = sha(ENGINE.read_bytes())
assert engine_sha == 'ab1824f85bfd8e0e4128182c000c4003a3e042245b2967848d089b2a04b22424'
receipt = {
    'schema': 'reef.jp0-native-recovery-review.v1',
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'tested_source_base': payload['base_commit'],
    'functional_source_files_verified_unchanged': len(payload['files']),
    'deterministic_source_payload_sha256': payload['deterministic_payload_sha256'],
    'source_payload_raw_sha256': sha(payload_path.read_bytes()),
    'full_ci3': {
        'result': 'FAIL',
        'execution': full_result,
        'log_sha256': sha(full_log),
        'stderr_sha256': sha((EVIDENCE / 'full-ci3-errors.log').read_bytes()),
        'process_records': len(processes),
        'original_zero_exits': 79,
        'incomplete_pipeline_exits': failed,
        'cause': 'Unproven; no missing-command or specific Windows exception claim',
    },
    'native_recovery': recovery,
    'engine_path': str(ENGINE),
    'engine_sha256': engine_sha,
    'engine_version': '4.7.2.stable.official.ed1daf0bf',
    'claim': 'Three unchanged probes complete under direct native supervision with actual engine exit 0; together with the 79 original zero-exit probes this supplies per-probe evidence at the frozen candidate.',
    'limitations': [
        'The original aggregate remains FAIL and is not relabeled as uninterrupted green regression.',
        'Incoming dev 549ea956 must be reconciled and tested before integration.',
        'JP1 final checker application, full50 tests and final full/exact-head CI remain pending.',
        'Automatic approval review blocked H worktree writes; explicit authorization is pending.',
        'No GitHub publication, integration, device/child/owner or game-wide acceptance claim.',
        'The earlier attached core observation returned a null exit code and is retained as failed observation; only the direct native result is used here.',
    ],
}
out = HERE / 'native-recovery-receipt.json'
assert not out.exists(), 'Refusing to overwrite a sealed receipt'
out.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'receipt': str(out), 'sha256': sha(out.read_bytes()), 'native_recovery': '3 actual engine exits 0', 'original_aggregate': 'FAIL', 'source_files_unchanged': len(payload['files'])}))
