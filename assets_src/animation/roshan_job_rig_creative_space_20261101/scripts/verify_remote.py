"""Anonymous byte verification of an exact published review revision, never acceptance."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,datetime,hashlib,json,time,urllib.request,urllib.parse

P=Path(__file__).resolve().parents[1];R=P.parents[2]
parser=argparse.ArgumentParser();parser.add_argument('revision');parser.add_argument('--receipt',required=True);args=parser.parse_args()
assert len(args.revision)==40 and all(c in '0123456789abcdef' for c in args.revision)
prefix=P.relative_to(R).as_posix();sha=lambda b:hashlib.sha256(b).hexdigest()
def fetch(revision,path):
    url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+urllib.parse.quote(path,safe='/')
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Roshan-source-review-byte-verification'}),timeout=45) as response:return response.read(),response.status,url
        except Exception:
            if attempt==2:raise
            time.sleep(attempt+1)
manifest_bytes,code,url=fetch(args.revision,prefix+'/manifest.json')
manifest=json.loads(manifest_bytes);local=(P/'manifest.json').read_bytes();assert sha(local)==sha(manifest_bytes),'remote manifest differs from exact local payload'
canonical=''.join(x['path']+'\0'+x['sha256']+'\n' for x in sorted(manifest['files'],key=lambda x:x['path'])).encode('utf8');assert sha(canonical)==manifest['payload_sha256']
def check(item,revision=args.revision):
    try:
        data,status,url=fetch(revision,item['path']);actual=sha(data)
        return dict(path=item['path'],revision=revision,url=url,status=status,expected_sha256=item['sha256'],actual_sha256=actual,bytes=len(data),passed=actual==item['sha256'] and ('bytes' not in item or len(data)==item['bytes']))
    except Exception as exc:return dict(path=item['path'],revision=revision,passed=False,error=str(exc))
rows=[]
with ThreadPoolExecutor(max_workers=6) as pool:
    jobs=[pool.submit(check,x) for x in manifest['files']]
    for future in as_completed(jobs):
        rows.append(future.result())
        if len(rows)%50==0:print('ANONYMOUS PAYLOAD',len(rows),'/',len(jobs),flush=True)
inventory=json.loads((P/'source_inventory.json').read_text(encoding='utf8'));backlog=json.loads((P/'coverage_backlog.json').read_text(encoding='utf8'))
references={x['path']:x for x in inventory['sources']}
for x in backlog['career_families']:references[x['source']]=dict(path=x['source'],sha256=x['sha256'])
with ThreadPoolExecutor(max_workers=6) as pool:source_rows=list(pool.map(lambda x:check(x,inventory['baseline']),references.values()))
passed=code==200 and all(x['passed'] for x in rows+source_rows)
result=dict(request_id='CREATIVE_SPACE_20261101_REJECTED_REVIEW_V1',payload_revision=args.revision,repository='Ebonyks/mermaid-roshan-reef',branch='codex/roshan-job-rig-creative-space-20261101',entry='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+args.revision+'/'+prefix+'/README.md',tree='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+args.revision+'/'+prefix,manifest_url=url,manifest_sha256=sha(manifest_bytes),payload_sha256=manifest['payload_sha256'],access_mode='Anonymous HTTPS with no credentials, cookies, token or authenticated session',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ARCHIVE_COMPLETE=passed,GENERATION_READY=False,DELIVERY_ACCEPTED=False,classification=manifest['classification'],human_device_child_owner_acceptance='PENDING; numerical/provenance/shared-contract gaps remain blocking',passed=passed,files=sorted(rows,key=lambda x:x['path']),historical_source_references=sorted(source_rows,key=lambda x:x['path']),upstream_seed_receipt=prefix+'/evidence/upstream_seed_remote_verification.json',shared_contract='Exact owner-local freeze b2a5dfe9; owner publication remains pending')
target=Path(args.receipt).resolve();assert target.is_relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print('REMOTE REVIEW ARCHIVE',passed,len(rows),'payload files;',len(source_rows),'historical source references',flush=True)
raise SystemExit(0 if passed else 1)
