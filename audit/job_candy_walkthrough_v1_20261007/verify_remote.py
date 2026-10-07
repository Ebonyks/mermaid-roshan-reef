"""Anonymous immutable GitHub payload verification. No uploads or credentials.
Run after publication: python -B verify_remote.py --revision FULL_COMMIT_SHA
The resulting transport receipt is sealed separately from payload hashes.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse, datetime, hashlib, json, urllib.request

p=Path(__file__).resolve().parent
args=argparse.ArgumentParser();args.add_argument('--revision',required=True)
revision=args.parse_args().revision
assert len(revision)==40 and all(c in '0123456789abcdef' for c in revision)
m=json.loads((p/'MANIFEST.json').read_text(encoding='utf-8'))
prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/audit/job_candy_walkthrough_v1_20261007/'
def fetch(item):
    path=item['path'];assert '..' not in Path(path).parts
    request=urllib.request.Request(prefix+path,headers={'User-Agent':'CandyWalkthroughReadonlyVerifier/1.0'})
    with urllib.request.urlopen(request,timeout=45) as response:
        raw=response.read();code=response.status
    sha=hashlib.sha256(raw).hexdigest()
    assert code==200 and sha==item['sha256'] and len(raw)==item['bytes'],path
    return dict(path=path,url=prefix+path,http_status=code,bytes=len(raw),sha256=sha)
items=m['payload_files']+[dict(path='MANIFEST.json',sha256=hashlib.sha256((p/'MANIFEST.json').read_bytes()).hexdigest(),bytes=(p/'MANIFEST.json').stat().st_size)]
with ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(fetch,items))
receipt=dict(status='PASS_ANONYMOUS_IMMUTABLE_REMOTE_BYTES',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    repository='Ebonyks/mermaid-roshan-reef',branch='codex/candymaker-walkthrough-20261007',payload_revision=revision,
    access_mode='Unauthenticated public HTTPS; urllib uses no gh token, cookie or Authorization header',
    entry_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_candy_walkthrough_v1_20261007/README.md',
    immutable_tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision+'/audit/job_candy_walkthrough_v1_20261007',
    direct_manifest_url=prefix+'MANIFEST.json',payload_sha256=m['payload_sha256'],
    verified_files=len(results),verified_bytes=sum(r['bytes'] for r in results),files=results,
    scope='Published review packet only. No runtime/art/contact/device/child/owner or4.6 acceptance. Transport receipt is excluded from payload self-hash and sealed separately.')
(p/'REMOTE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'}))
