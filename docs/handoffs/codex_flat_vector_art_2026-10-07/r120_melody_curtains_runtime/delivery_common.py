from pathlib import Path
import concurrent.futures, datetime, hashlib, json, os, subprocess, sys, time, urllib.parse, urllib.request

REPO = 'Ebonyks/mermaid-roshan-reef'
S = Path(__file__).parent
H = 'docs/handoffs/codex_flat_vector_art_2026-10-07'
REL = H + '/r120_melody_curtains_runtime'
ART = 'assets_src/imagegen/melody_curtains_20261101'
SOURCE_BASE = '27c88288bf6e39582072811443df79919e7bbb89'
SOURCE_BRANCH = 'codex/flat-vector-melody-curtains-20261101'
CANON_BASE = '3c3b39838b2ceacb13281a83957442662ca2f5b9'
CANON_BRANCH = 'codex/flat-vector-r6-20261012'
REVISION = 'FV-AUDIT-20261101-R120-SOURCE'
U = Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef')
R = Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-r6-20261012/mermaid-roshan-reef')

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rd(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def wt(p, x): p.write_text(x, encoding='utf-8', newline='\n')
def wr(p, x): wt(p, json.dumps(x, indent=2) + '\n')
def digest(b): return hashlib.sha256(b).hexdigest()
def sha(p): return digest(p.read_bytes())
def git(root, *args): return subprocess.check_output(['git', *args], cwd=root, stderr=subprocess.PIPE)
def gs(root, *args): return git(root, *args).decode('utf-8').strip()
def run(root, *args): subprocess.run(list(args), cwd=root, check=True, capture_output=True)
def state(kind, phase, **kw): wr(S/(kind+'_STATE.json'), dict(state=phase, at_utc=now(), **kw))

def index(root):
    result = {}
    for entry in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not entry: continue
        meta, path = entry.split(b'\t', 1)
        mode, oid, stage = meta.decode().split()
        assert stage == '0'
        result[path.decode()] = (mode, oid)
    return result

def blobs(root, paths, idx=None):
    idx = idx or index(root)
    paths = sorted(set(paths))
    q = subprocess.run(['git', 'cat-file', '--batch'], cwd=root,
        input=('\n'.join(idx[p][1] for p in paths)+'\n').encode(), capture_output=True, check=True)
    result = {}; at = 0
    for path in paths:
        end = q.stdout.index(b'\n', at)
        oid, typ, size = q.stdout[at:end].decode().split()
        assert typ == 'blob' and oid == idx[path][1]
        at = end + 1; size = int(size)
        result[path] = q.stdout[at:at+size]
        assert len(result[path]) == size and q.stdout[at+size:at+size+1] == b'\n'
        at += size + 1
    assert at == len(q.stdout)
    return result

def gate(root, label, command):
    q = subprocess.run(command, cwd=root, capture_output=True,
        env=dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8'))
    b = q.stdout + q.stderr; (S/(label+'.log')).write_bytes(b)
    assert q.returncode == 0, b.decode('utf-8', errors='replace')[-3500:]
    return dict(command=command, exit_code=q.returncode, log_sha256=digest(b))

def document_gates(root, label):
    return [gate(root, label+'_'+name, [sys.executable, '-B', 'tools/'+name+'.py', *args])
        for name, args in [('audit_document_authority', []), ('audit_development', ['--base', 'auto'])]]

def fetch(rev, path):
    req = urllib.request.Request('https://raw.githubusercontent.com/'+REPO+'/'+rev+'/'+urllib.parse.quote(path, safe='/'),
        headers={'User-Agent': 'MermaidReef-anonymous-R120-delivery-verifier'})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as q: return q.status, q.read()
        except Exception:
            if attempt == 4: raise
            time.sleep(2*(attempt+1))

def verify_manifest(root, rev, manifest_path, manifest):
    expected = git(root, 'show', rev+':'+manifest_path)
    status, b = fetch(rev, manifest_path)
    assert status == 200 and b == expected
    def one(row):
        rr = row.get('revision') or rev
        status, data = fetch(rr, row['path'])
        assert status == 200 and len(data) == row['bytes'] and digest(data) == row['sha256'], row['path']
        return dict(row, revision=rr, http_status=status, verified=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(one, manifest['files']))
    return dict(schema='reef.remote_delivery_verification/1', repository=REPO, revision=rev,
        manifest=manifest_path, manifest_sha256=digest(expected), manifest_bytes=len(expected),
        required_files=len(rows), required_bytes=sum(x['bytes'] for x in rows), files=rows,
        state='ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED_SOURCE_ONLY',
        access_mode='Anonymous immutable HTTPS GET without Authorization or cookies; exact bytes/SHA-256 of manifest and every required file.',
        checked_at_utc=now(), Dev_integrated=False, creative_acceptance=False)

def payload_rows(root, paths):
    return [dict(revision=None, path=p, bytes=len(b), sha256=digest(b), role='R120 current candidate, derivation, scene evidence or bounded registry delivery')
        for p, b in blobs(root, paths).items()]

def changed(root):
    return set(gs(root, 'diff', '--name-only', 'HEAD').splitlines()) | set(gs(root, 'ls-files', '--others', '--exclude-standard').splitlines())

def scope_files(paths):
    assert all(not p.startswith(('.secrets/', '.codex/', '.claude/', '.github/')) and p not in ['AGENTS.md','CLAUDE.md','SECURITY.md','project.godot'] for p in paths)

