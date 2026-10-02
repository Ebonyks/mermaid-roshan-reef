from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
import datetime, hashlib, json, subprocess, time, urllib.request

r = Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
revision = '56d66f63e375b61cf02936b426a05a2b92c14d3b'
index_path = 'audit/job_review_v2_20261001/CURRENT_REVIEW_SUPPLEMENT_FILES_V1.json'
out = r / 'tmp/review_supplement_remote_v55'
assert not out.exists()
out.mkdir()
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
base = 'https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/' + revision + '/'

def fetch(path, collect=False):
    request = urllib.request.Request(base + quote(path, safe='/'), headers={'User-Agent': 'MermaidRoshan-public-immutable-byte-verification'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                assert response.status == 200
                sha = hashlib.sha256()
                size = 0
                parts = []
                while True:
                    block = response.read(1024 * 1024)
                    if not block:
                        break
                    sha.update(block)
                    size += len(block)
                    if collect:
                        parts.append(block)
                return size, sha.hexdigest(), b''.join(parts) if collect else None
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)

index_size, index_sha, index_data = fetch(index_path, True)
assert index_sha == '355f0371c764aec3d65f1fb6fd4505c23e201602aae51cf8e05c856ce369b13f'
assert index_data == subprocess.check_output(['git', 'show', revision + ':' + index_path], cwd=r)
m = json.loads(index_data)
files = m['files']
assert len(files) == m['required_files'] == 239
assert sum(v[0] for v in files.values()) == m['required_payload_bytes'] == 34451210
assert list(files) == sorted(files)
digest = hashlib.sha256(''.join(path + '\0' + str(value[0]) + '\0' + value[1] + '\n' for path, value in files.items()).encode('utf-8')).hexdigest()
assert digest == m['payload_sha256']
tree = subprocess.check_output(['git', 'rev-parse', revision + '^{tree}'], cwd=r, text=True).strip()
assert tree == '4596458379816725f0f014a5d18e03b304f8d4a9'
metadata = {'revision': revision, 'tree': tree, 'index': index_path, 'index_sha256': index_sha, 'index_bytes': index_size, 'payload_sha256': digest, 'required_files': len(files), 'required_bytes': m['required_payload_bytes'], 'access_mode': 'Anonymous public HTTPS with normal TLS verification. No credentials or Authorization header. Complete GET of every immutable mapped path and of the map itself.', 'base_revision': m['base_revision'], 'base_verified_content_commit': m['base_verified_content_commit']}
(out / 'CHECKPOINT_IDENTITY.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')

def verify(path, value):
    size, sha, _ = fetch(path)
    assert [size, sha] == value, path
    return [path, size, sha, datetime.datetime.now(datetime.timezone.utc).isoformat()]

verified = {}
failures = []
print('SUPPLEMENT_INDEX_MATCH', revision, index_sha, len(files), flush=True)
with (out / 'FETCH_JOURNAL.jsonl').open('w', encoding='utf-8') as journal, ThreadPoolExecutor(max_workers=8) as workers:
    jobs = {workers.submit(verify, path, value): path for path, value in files.items()}
    for job in as_completed(jobs):
        try:
            row = job.result()
            verified[row[0]] = row
            journal.write(json.dumps(row, separators=(',', ':')) + '\n')
            journal.flush()
            if len(verified) % 50 == 0:
                print('SUPPLEMENT_BYTES', len(verified), '/', len(files), flush=True)
        except Exception as error:
            failures.append({'path': jobs[job], 'error': type(error).__name__ + ': ' + str(error)})
            print('SUPPLEMENT_FAILURE', jobs[job], type(error).__name__, flush=True)
complete = set(verified) == set(files) and not failures
result = {'status': 'PASS_ALL_IMMUTABLE_REVIEW_SUPPLEMENT_BYTES' if complete else 'FAIL_PRESERVED_INCOMPLETE', **metadata, 'entry': 'https://github.com/Ebonyks/mermaid-roshan-reef/blob/' + revision + '/audit/job_review_v2_20261001/index.html', 'tree_url': 'https://github.com/Ebonyks/mermaid-roshan-reef/tree/' + revision, 'manifest': base + index_path, 'manifest_bytes': index_size, 'manifest_sha256': index_sha, 'started_utc': started, 'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'verified_files': len(verified), 'verified_bytes': sum(row[1] for row in verified.values()), 'failures': failures, 'journal_value_schema': ['path', 'bytes', 'sha256', 'checked_utc'], 'qualification': '239 changed payload blobs and self-map at this exact revision; earlier13534 c211 bytes remain pinned to their original receipt. Hosted CI, source/context/action/device/child/owner acceptance, integration and release remain separate.'}
(out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result), flush=True)
raise SystemExit(0 if complete else 1)
