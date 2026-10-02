from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys, urllib.parse, urllib.request
b = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
baseline = '9df7340c9821c905bc618347ff95dcb498f3d058'
branch = 'codex/job-art-review-v2-20261001'
f = b / 'audit/job_review_v2_20261001/supported_geode_remote_verified_v12'
out = b / 'tmp/supported_geode_remote_receipt_v341'
assert f.is_dir() and not out.exists()
out.mkdir()
read = lambda p: json.loads(p.read_text(encoding='utf-8-sig'))
sha = lambda raw: hashlib.sha256(raw).hexdigest()
def write(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')
def git(*args, input=None):
    return subprocess.run(['git', *args], cwd=b, input=input, capture_output=True, check=True).stdout
def run(label, command, directory=out):
    p = subprocess.run(command, cwd=b, capture_output=True, timeout=600, creationflags=subprocess.CREATE_NO_WINDOW)
    (directory / (label + '.stdout.log')).write_bytes(p.stdout)
    (directory / (label + '.stderr.log')).write_bytes(p.stderr)
    assert p.returncode == 0, p.stderr.decode(errors='replace')[-1200:]
    print(label, 'PASS', flush=True)
    return p
assert git('rev-parse', 'HEAD').decode().strip() == baseline
assert git('branch', '--show-current').decode().strip() == branch
assert not git('diff', '--cached', '--name-only').strip()
receipt = read(f / 'RESULT.json')
assert receipt['status'] == 'PASS_ALL_ANONYMOUS_REMOTE_BYTES' and receipt['revision'] == baseline
bridge = read(b / 'audit/job_geode_supported_celebration_v1_20261002/PUBLICATION_SOURCE_NEWLINE_BRIDGE_FINAL_V337.json')
assert len(bridge['checks']) == 377
def check_sources():
    ordered = bridge['checks']
    data = git('cat-file', '--batch', input=''.join('HEAD:' + x['path'] + '\n' for x in ordered).encode())
    offset = 0
    for item in ordered:
        end = data.index(b'\n', offset)
        header = data[offset:end].split()
        assert header[1] == b'blob', item['path']
        length = int(header[2]); offset = end + 1
        raw = data[offset:offset + length]; offset += length + 1
        assert sha(raw) == item['exact_git_blob_sha256'], item['path']
        assert sha((b / item['path']).read_bytes()) == item['literal_local_sha256'], item['path']
    assert offset == len(data)
check_sources()
impact_path = b / 'design/audit_impacts/job-geode-remote-verification-receipt-20261002.json'
manifest_path = f / 'FILES_V12.json'
assert read(manifest_path)['status'] == 'EXACT_RECEIPT_MANIFEST_PREPARED'
for source, name in [(impact_path, 'IMPACT_PRE_RETRY.original.json'), (f / 'PLAN.json', 'PLAN_PRE_RETRY.original.json')]:
    assert not (f / name).exists()
    shutil.copyfile(source, f / name)
gate = f / 'gates'
assert 'missing acceptance_gaps' in (gate / 'development.stdout.log').read_text()
write(gate / 'development.receipt.json', {
    'status': 'FAIL_PRESERVED', 'wrapper_process_exit': 1,
    'underlying_process_exit': None,
    'diagnostics': ['Impact record missing required acceptance_gaps string'],
    'stdout_sha256': sha((gate / 'development.stdout.log').read_bytes()),
    'stderr_sha256': sha((gate / 'development.stderr.log').read_bytes()),
    'qualification': 'Original wrapper stopped on the nonzero audit-development result; its exact underlying exit number was not persisted. Raw result and original deficient impact record are preserved. No runtime or artwork failure.'
})
impact = read(impact_path)
impact['acceptance_gaps'] = 'Publication evidence only; no new visual, runtime, phone, child, owner or full all-job acceptance. Hosted CI remains separate. All 377 current production/test sources remain unchanged.'
impact['validation'].extend([
    {'command': 'Original document-authority gate', 'result': 'PASS', 'evidence': (gate / 'authority.receipt.json').relative_to(b).as_posix()},
    {'command': 'Original development-coverage gate', 'result': 'FAIL', 'evidence': (gate / 'development.receipt.json').relative_to(b).as_posix()}
])
plan = read(f / 'PLAN.json')
plan['document_gate_retry'] = {'reason': 'Required acceptance_gaps string absent from first sidecar impact record', 'original_impact': 'IMPACT_PRE_RETRY.original.json', 'failed_receipt': 'gates/development.receipt.json', 'qualification': 'Documentation metadata correction only; no new application defect, lifecycle or source change.'}
write(f / 'PLAN.json', plan)
write(f / 'SOURCE_RECHECK_V341.json', {'status': 'PASS_ALL377_LOCAL_AND_GIT_SOURCE_HASHES_UNCHANGED', 'reference': '../../job_geode_supported_celebration_v1_20261002/PUBLICATION_SOURCE_NEWLINE_BRIDGE_FINAL_V337.json', 'source_count': 377, 'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'qualification': 'Same exact local literal and canonical Git production/test blobs as verified checkpoint M; no fresh full-suite or visual acceptance inferred.'})
shutil.copyfile(__file__, f / Path(__file__).name)
for label in ['authorityv2', 'developmentv2']:
    (gate / (label + '.stdout.log')).write_bytes(b'')
    (gate / (label + '.stderr.log')).write_bytes(b'')
    write(gate / (label + '.receipt.json'), {'status': 'PREPARED_CURRENT_DOCUMENT_GATE'})
scope = set(impact['files']) | {p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}
impact['files'] = sorted(scope)
write(impact_path, impact)
for label, command in [
    ('authorityv2', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_document_authority.py']),
    ('developmentv2', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto'])
]:
    process = run(label, command, directory=gate)
    gate_receipt = gate / (label + '.receipt.json')
    write(gate_receipt, {'status': 'PASS', 'command': command, 'process_exit': process.returncode,
        'stdout_sha256': sha(process.stdout), 'stderr_sha256': sha(process.stderr),
        'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'qualification': 'Fresh publication document gate; no application or creative acceptance.'})
    impact['validation'].append({'command': ' '.join(command), 'result': 'PASS', 'evidence': gate_receipt.relative_to(b).as_posix()})
    write(impact_path, impact)
check_sources()
paths = ''.join(p + '\0' for p in sorted(scope)).encode()
git('add', '-f', '--pathspec-from-file=-', '--pathspec-file-nul', input=paths)
git('add', '--renormalize', '-f', '--pathspec-from-file=-', '--pathspec-file-nul', input=paths)
changed = {x.decode() for x in git('diff', '--cached', '--name-only', '-z').split(b'\0') if x}
assert changed == scope
mp = manifest_path.relative_to(b).as_posix()
files = {}
for path in sorted(scope - {mp}):
    raw = git('show', ':' + path)
    files[path] = [len(raw), sha(raw)]
write(manifest_path, {
    'schema': 'reef.remote-verification-receipt.v1',
    'base_revision': baseline,
    'verified_review_revision': baseline,
    'verified_review_manifest_url': receipt['manifest_url'],
    'verified_review_manifest_sha256': receipt['map_sha256'],
    'required_files': len(files),
    'files': files,
    'qualification': 'Publication-only verification sidecar for immutable checkpoint M; M receipt independently covers all 6,366 review files at its own exact revision. No new creative or runtime claim.'
})
git('add', '-f', '--', mp)
rawmap = git('show', ':' + mp)
files_with_map = dict(files)
files_with_map[mp] = [len(rawmap), sha(rawmap)]
run('fetch', ['git', 'fetch', 'origin'])
assert git('rev-parse', 'origin/' + branch).decode().strip() == baseline
message = out / 'COMMIT_MESSAGE.txt'
message.write_text('Publish supported geode remote-verification receipt\n\nSave the exact 9df7340c anonymous all-6366-file receipt and complete lossless journal beside the illustrated review on the established GitHub topic branch. Link the evidence from the master planning entry and document ledger. Record every payload/reference/manifest hash and normal TLS access interval.\n\nAll 377 literal local/canonical Git production and test sources are unchanged. Existing 82-probe local verification remains scoped to those exact sources; this revision adds publication evidence only. Audit-authority and development-coverage gates pass. No artwork edit, finding closure, all-job/owner acceptance, integration or release.\n', encoding='utf-8')
run('commit', ['git', 'commit', '--file', str(message)])
revision = git('rev-parse', 'HEAD').decode().strip()
assert git('rev-parse', 'HEAD^').decode().strip() == baseline
for label, command in [
    ('postcommit_authority', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_document_authority.py']),
    ('postcommit_development', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto'])
]:
    run(label, command)
check_sources()
run('push', ['git', 'push', 'origin', 'HEAD:refs/heads/' + branch])
prefix = 'https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/' + revision + '/'
checks = []
for path, expected in sorted(files_with_map.items()):
    request = urllib.request.Request(prefix + urllib.parse.quote(path, safe='/'), headers={'User-Agent': 'MermaidReef-Anonymous-Receipt-QA'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
        assert response.status == 200
    assert [len(data), sha(data)] == expected, path
    checks.append({'path': path, 'bytes': len(data), 'sha256': sha(data), 'matches': True})
with urllib.request.urlopen(receipt['manifest_url'], timeout=60) as response:
    assert response.status == 200 and sha(response.read()) == receipt['map_sha256']
result = {
    'status': 'PASS_DURABLE_REMOTE_RECEIPT_PUBLICATION',
    'receipt_revision': revision,
    'review_revision': baseline,
    'receipt_url': 'https://github.com/Ebonyks/mermaid-roshan-reef/blob/' + revision + '/' + (f / 'RESULT.json').relative_to(b).as_posix(),
    'entry_url': 'https://github.com/Ebonyks/mermaid-roshan-reef/blob/' + revision + '/' + (f / 'index.html').relative_to(b).as_posix(),
    'sidecar_manifest_url': prefix + mp,
    'sidecar_manifest_sha256': sha(rawmap),
    'published_sidecar_files': len(checks),
    'checks': checks,
    'access_mode': 'Anonymous GET; normal TLS verification; no Authorization header',
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_count': 377,
    'source_unchanged': True,
    'qualification': 'Durable receipt confirms exact immutable checkpoint M 6,366-file verification. Sidecar changes documents/provenance only; no dev/master, visual/owner or release acceptance.'
}
write(out / 'RESULT.json', result)
print(json.dumps(result), flush=True)
