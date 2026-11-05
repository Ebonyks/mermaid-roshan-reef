"""Anonymous byte verification of the published corrected v8 seed."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request,urllib.parse
P=Path(__file__).resolve().parents[1]
REV='b700b846d1d2f4b1843279f268e2bb12e4b1f4ec'
BASE='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+REV+'/'
PATH='assets_src/animation/native_rig_costumes_20261031/replacement_v6/evidence/frozen_inputs_v8.json'
def fetch(path):
    req=urllib.request.Request(BASE+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'Mermaid-Roshan-source-review'})
    with urllib.request.urlopen(req,timeout=40) as response:return response.status,response.read()
status,data=fetch(PATH)
manifest=json.loads(data)
expected=hashlib.sha256((P/'fixtures/frozen_inputs_v8.json').read_bytes()).hexdigest()
def check(item):
    path,wanted=item
    try:
        code,raw=fetch(path);actual=hashlib.sha256(raw).hexdigest()
        return dict(path=path,status=code,expected_sha256=wanted,actual_sha256=actual,passed=code==200 and actual==wanted)
    except Exception as exc:return dict(path=path,passed=False,error=str(exc))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(check,sorted(manifest['files'].items())))
result=dict(revision=REV,manifest=BASE+PATH,manifest_sha256=hashlib.sha256(data).hexdigest(),local_frozen_manifest_sha256=expected,access_mode='anonymous HTTPS, no credentials or authenticated session',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=rows,passed=status==200 and hashlib.sha256(data).hexdigest()==expected and all(x['passed'] for x in rows),limits='Published frozen v8 source prototype verified, not artistic/runtime/device/child/owner acceptance. Rejected 26bd6d1f overlay predecessor excluded; shared rig contract v1 remains its separate owner’s locally frozen artifact.')
(P/'evidence/upstream_seed_remote_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('UPSTREAM V8 REMOTE',result['passed'],len(rows),'files',REV)
raise SystemExit(0 if result['passed'] else 1)
