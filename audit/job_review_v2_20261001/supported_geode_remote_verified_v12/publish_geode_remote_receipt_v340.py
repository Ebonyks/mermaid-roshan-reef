from pathlib import Path
import datetime, gzip, hashlib, json, shutil, subprocess, sys, urllib.parse, urllib.request

b = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
baseline = '9df7340c9821c905bc618347ff95dcb498f3d058'
branch = 'codex/job-art-review-v2-20261001'
f = b / 'audit/job_review_v2_20261001/supported_geode_remote_verified_v12'
out = b / 'tmp/supported_geode_remote_receipt_v340'
assert not f.exists() and not out.exists()
f.mkdir(parents=True)
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
original = b / 'tmp/supported_geode_checkpoint_m_remote_v338/RESULT.json'
receipt = read(original)
assert receipt['status'] == 'PASS_ALL_ANONYMOUS_REMOTE_BYTES' and receipt['revision'] == baseline
assert receipt['files_including_manifest'] == 6366 and receipt['failed_files'] == []
shutil.copyfile(original, f / 'RESULT.json')
journal = (original.parent / 'VERIFICATION_JOURNAL.jsonl').read_bytes()
assert len(journal.splitlines()) == 6366
assert all(json.loads(line)['matches'] for line in journal.splitlines())
(f / 'VERIFICATION_JOURNAL.jsonl.gz').write_bytes(gzip.compress(journal, compresslevel=9, mtime=0))
assert gzip.decompress((f / 'VERIFICATION_JOURNAL.jsonl.gz').read_bytes()) == journal
bridge = read(b / 'audit/job_geode_supported_celebration_v1_20261002/PUBLICATION_SOURCE_NEWLINE_BRIDGE_FINAL_V337.json')
assert bridge['status'] == 'PASS_ALL377_STAGED_SOURCE_EQUIVALENCE' and len(bridge['checks']) == 377
for item in bridge['checks']:
    assert sha((b / item['path']).read_bytes()) == item['literal_local_sha256'], item['path']
    assert sha(git('show', 'HEAD:' + item['path'])) == item['exact_git_blob_sha256'], item['path']

plan = {
    'status': 'VERIFIED_REVIEW_RECEIPT_PREPARED_FOR_DURABLE_PUBLICATION',
    'review_revision': baseline,
    'review_manifest_url': receipt['manifest_url'],
    'review_manifest_sha256': receipt['map_sha256'],
    'review_payload_sha256': receipt['payload_sha256'],
    'receipt_native_sha256': sha(original.read_bytes()),
    'journal_uncompressed_sha256': sha(journal),
    'journal_lines': 6366,
    'journal_method': 'Lossless gzip, deterministic mtime 0; literal HTTP verification journal bytes retained on decompression.',
    'qualification': 'Publication-only sidecar for the already verified immutable review revision. All 377 literal local and canonical Git production/test sources remain unchanged. No new runtime/image edit, fresh motion review, finding closure, owner acceptance, integration or release.'
}
write(f / 'PLAN.json', plan)
html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>Supported geode — published byte verification</title>
<style>body{{max-width:980px;margin:40px auto;padding:24px;font:18px/1.6 system-ui;background:#f2f5ff;color:#27364e}}a{{color:#434384}}code{{overflow-wrap:anywhere}}li{{margin:12px 0}}</style>
<h1>Supported geode review: every published file verified</h1>
<p>The opened specimen retains crystals rooted inside both halves and rests on the painted slab throughout the earned celebration. The mounted specimen/slab reaches provisional 4.5/5; material 4.6. Whole stage 4.1, room 2.8 and live contact 2.7 remain priorities.</p>
<p><a href="{receipt['entry_url']}">Immutable illustrated review entry</a> · <a href="{receipt['tree_url']}">Exact review revision</a> · <a href="{receipt['manifest_url']}">Direct closed manifest</a></p>
<p><strong>All 6,366 files match exact bytes and SHA-256.</strong> Anonymous GET used normal TLS certificate verification without an Authorization header. Check interval: {receipt['started_utc']} to {receipt['finished_utc']}. This covers 996 changed payload files, 5,369 required reference files and the manifest.</p>
<ul><li><a href="RESULT.json">Complete verification receipt</a></li><li><a href="VERIFICATION_JOURNAL.jsonl.gz">All 6,366 individual verification records, lossless gzip</a></li><li><a href="PLAN.json">Source preservation and journal provenance</a></li></ul>
<p>Review revision: <code>{baseline}</code><br>Manifest SHA-256: <code>{receipt['map_sha256']}</code><br>Sorted payload SHA-256: <code>{receipt['payload_sha256']}</code></p>
<p>The unmodified official Godot 4.7.2 local suite passes all 82 probes against 377 unchanged literal source files; 41 raw diagnostics remain recorded. This sidecar adds publication evidence only. Hosted CI, phone, child, owner and all-job visual acceptance remain separate. Neither dev nor master is changed.</p></html>'''
(f / 'index.html').write_text(html, encoding='utf-8', newline='\n')
shutil.copyfile(__file__, f / Path(__file__).name)
attrs = b / '.gitattributes'
attrs.write_text(attrs.read_text() + '\n# Literal published geode remote-verification sidecar.\n/audit/job_review_v2_20261001/supported_geode_remote_verified_v12/** -text\n', encoding='utf-8', newline='\n')
ledger = b / 'design/05_DOC_LEDGER.md'
ledger.write_text(ledger.read_text() + '\n| `audit/job_review_v2_20261001/supported_geode_remote_verified_v12/index.html` | 🔵 | `SUPPORTING_CURRENT`; immutable checkpoint 9df7340c remote verification: all 6,366 declared payload/reference/manifest files anonymously match exact bytes/SHA-256 at 2026-10-02 14:06:44–14:09:46 UTC. Lossless full journal and receipt preserve the checks. All 377 production/test sources unchanged; publication proof grants no visual, owner, integration or release acceptance. |\n', encoding='utf-8', newline='\n')
master = b / 'audit/MASTER_AUDIT_2026-08-09.md'
text = master.read_text()
marker = '# Mermaid Roshan: Reef of Light — game-wide master audit'
assert text.startswith(marker)
note = '\n\nSupported geode publication receipt (2026-10-02): [immutable review revision 9df7340c — all 6,366 remote files anonymously verified byte-for-byte](job_review_v2_20261001/supported_geode_remote_verified_v12/index.html). Receipt and complete lossless per-file journal record hashes, normal TLS access and 14:06:44–14:09:46 UTC check interval. All 377 production/test source bytes remain unchanged; this is publication evidence only, not creative/device/child/owner/all-job acceptance or a lifecycle change.\n'
master.write_text(marker + note + text[len(marker):], encoding='utf-8', newline='\n')
impact_path = b / 'design/audit_impacts/job-geode-remote-verification-receipt-20261002.json'
manifest_path = f / 'FILES_V12.json'
write(manifest_path, {'status': 'EXACT_RECEIPT_MANIFEST_PREPARED'})
gate = f / 'gates'
gate.mkdir()
for label in ['authority', 'development']:
    (gate / (label + '.stdout.log')).write_bytes(b'')
    (gate / (label + '.stderr.log')).write_bytes(b'')
    write(gate / (label + '.receipt.json'), {'status': 'PREPARED_CURRENT_DOCUMENT_GATE'})
scope = {'.gitattributes', 'audit/MASTER_AUDIT_2026-08-09.md', 'design/05_DOC_LEDGER.md', impact_path.relative_to(b).as_posix()}
scope.update(p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file())
impact = {
    'id': 'job-geode-remote-verification-receipt-20261002',
    'scope': 'Publish the completed immutable supported-geode checkpoint M anonymous byte-verification receipt and complete lossless journal to the established GitHub review destination; link it from canonical planning/ledger. No artwork, runtime, probe, source/test or lifecycle change.',
    'baseline': baseline,
    'rules': ['DL-AUTH-05', 'DL-AUTH-06', 'DL-AUTH-07', 'DL-ASSET-02', 'DL-ASSET-03', 'DL-QA-03'],
    'findings': [],
    'no_findings_reason': 'Publication evidence for the existing qualified review; no defect or finding lifecycle repaired or changed.',
    'files': sorted(scope),
    'validation': [
        {'command': 'Exact immutable checkpoint M anonymous TLS GET and SHA-256 of every manifest/payload/reference file', 'result': 'PASS', 'evidence': (f / 'RESULT.json').relative_to(b).as_posix()},
        {'command': 'Verify every 377 frozen local source hash and canonical Git source hash remains identical to checkpoint M', 'result': 'PASS', 'evidence': (f / 'PLAN.json').relative_to(b).as_posix()}
    ],
    'outstanding': ['No new runtime or art acceptance; full all-job audit/refinement and device/child/owner acceptance remain open. Hosted CI status is separate.']
}
write(impact_path, impact)
for label, command in [
    ('authority', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_document_authority.py']),
    ('development', [sys.executable, '-X', 'utf8', '-B', 'tools/audit_development.py', '--base', 'auto'])
]:
    process = run(label, command, directory=gate)
    gate_receipt = gate / (label + '.receipt.json')
    write(gate_receipt, {'status': 'PASS', 'command': command, 'process_exit': process.returncode,
        'stdout_sha256': sha(process.stdout), 'stderr_sha256': sha(process.stderr),
        'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'qualification': 'Publication-only document authority/coverage gate. Runtime sources remain unchanged; no new visual or owner acceptance.'})
    impact['validation'].append({'command': ' '.join(command), 'result': 'PASS', 'evidence': gate_receipt.relative_to(b).as_posix()})
write(impact_path, impact)
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
for item in bridge['checks']:
    assert sha((b / item['path']).read_bytes()) == item['literal_local_sha256']
    assert sha(git('show', 'HEAD:' + item['path'])) == item['exact_git_blob_sha256']
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
