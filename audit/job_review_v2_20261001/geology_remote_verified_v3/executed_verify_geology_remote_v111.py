from pathlib import Path
import json, hashlib, urllib.request, time, datetime, concurrent.futures
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=b/'tmp/geology_supplement_remote_v111';out.mkdir(exist_ok=False)
pub=json.loads((b/'tmp/geology_supplement_publish_v110/RECEIPT.json').read_text())
revision=pub['revision'];prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
started=utc()
def fetch(path):
    for attempt in range(1,4):
        try:
            req=urllib.request.Request(prefix+path,headers={'User-Agent':'Mermaid-Roshan-review-verification/1'})
            with urllib.request.urlopen(req,timeout=120) as response:
                assert response.status==200
                raw=response.read()
            return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),attempt=attempt,status='FETCHED_ANONYMOUS_TLS_GET',checked_utc=utc()),raw
        except Exception as e:
            if attempt==3:return dict(path=path,status='FETCH_FAILED',error=str(e),checked_utc=utc()),None
            time.sleep(attempt)
map_row,map_raw=fetch(pub['map_path']);assert map_raw is not None
assert map_row['sha256']==pub['map_sha256'];m=json.loads(map_raw)
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(m['files'].items())).encode()
assert hashlib.sha256(formula).hexdigest()==m['payload_sha256']==pub['payload_sha256']
rows=[];fail=[]
with (out/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures={pool.submit(fetch,p):p for p in m['files']}
        for future in concurrent.futures.as_completed(futures):
            row,raw=future.result();p=row['path'];row['expected_bytes'],row['expected_sha256']=m['files'][p]
            row['matches']=raw is not None and [row['bytes'],row['sha256']]==m['files'][p]
            journal.write(json.dumps(row)+'\n');journal.flush();rows.append(row)
            if not row['matches']:fail.append(row)
            if len(rows)%100==0:print('verified',len(rows),'failures',len(fail),flush=True)
    map_row['matches']=True;journal.write(json.dumps(map_row)+'\n')
result=dict(status='PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED',revision=revision,tree=pub['tree'],branch=pub['branch'],entry_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_review_v2_20261001/index.html',tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,manifest_url=prefix+pub['map_path'],map_sha256=pub['map_sha256'],payload_sha256=m['payload_sha256'],payload_files=len(rows),files_including_manifest=len(rows)+1,payload_bytes=sum(v[0] for v in m['files'].values()),access_mode='Anonymous GET, normal TLS certificate verification, no Authorization header',started_utc=started,finished_utc=utc(),failed_files=fail,qualification='Published reversible review bytes only; source scores and isolated fixtures do not confer runtime, complete action, device, child, owner or release acceptance.')
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result),flush=True)
raise SystemExit(0 if not fail else 1)
