from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote
import datetime, hashlib, json, shutil, subprocess, time, urllib.request
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
revision='6edb4ca8c57bfbfe3123636863a29c95165ac23f'
index_path='audit/job_review_v2_20261001/CURRENT_NATIVE_JOB_ART_SUPPLEMENT_FILES_V2.json'
out=r/'tmp/native_supplement_remote_v84';assert not out.exists();out.mkdir()
shutil.copyfile(__file__,out/'executed_verify_native_supplement_remote_v84.py')
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
base='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'
def fetch(path,collect=False):
    req=urllib.request.Request(base+quote(path,safe='/'),headers={'User-Agent':'MermaidRoshan-public-immutable-byte-verification'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=45) as response:
                assert response.status==200
                sha=hashlib.sha256();size=0;parts=[]
                while True:
                    block=response.read(1024*1024)
                    if not block:break
                    sha.update(block);size+=len(block)
                    if collect:parts.append(block)
                return size,sha.hexdigest(),b''.join(parts) if collect else None
        except Exception:
            if attempt==2:raise
            time.sleep(attempt+1)
size,hash_value,data=fetch(index_path,True)
assert hash_value=='402e68d7b75e6d00bd7027b6b767af89ba89616c4043132538d5bb90f13e2d85'
assert data==subprocess.check_output(['git','show',revision+':'+index_path],cwd=r)
m=json.loads(data);files=m['files']
assert len(files)==m['required_files']==444 and list(files)==sorted(files)
assert sum(v[0] for v in files.values())==m['required_payload_bytes']==43281662
digest=hashlib.sha256(''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in files.items()).encode()).hexdigest()
assert digest==m['payload_sha256']
tree=subprocess.check_output(['git','rev-parse',revision+'^{tree}'],cwd=r,text=True).strip()
assert tree=='394ca93b5b5d4f3bc29c79fdf0e5dea30b183576'
metadata=dict(revision=revision,tree=tree,index=index_path,index_sha256=hash_value,index_bytes=size,payload_sha256=digest,required_files=len(files),required_bytes=m['required_payload_bytes'],access_mode='Anonymous public HTTPS with normal TLS verification. No credentials or Authorization header. Complete GET of every immutable mapped path and map itself.',base_revision=m['base_revision'],prior_closed_map=m['prior_closed_map'])
(out/'CHECKPOINT_IDENTITY.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
def verify(p,v):
    count,sha,_=fetch(p);assert [count,sha]==v,p
    return [p,count,sha,datetime.datetime.now(datetime.timezone.utc).isoformat()]
verified={};failures=[]
print('NATIVE_SUPPLEMENT_INDEX_MATCH',revision,hash_value,len(files),flush=True)
with (out/'FETCH_JOURNAL.jsonl').open('w',encoding='utf-8') as journal, ThreadPoolExecutor(max_workers=8) as workers:
    jobs={workers.submit(verify,p,v):p for p,v in files.items()}
    for job in as_completed(jobs):
        try:
            row=job.result();verified[row[0]]=row
            journal.write(json.dumps(row,separators=(',',':'))+'\n');journal.flush()
            if len(verified)%100==0:print('NATIVE_SUPPLEMENT_BYTES',len(verified),'/',len(files),flush=True)
        except Exception as error:
            failures.append(dict(path=jobs[job],error=type(error).__name__+': '+str(error)))
            print('NATIVE_SUPPLEMENT_FAILURE',jobs[job],type(error).__name__,flush=True)
complete=set(verified)==set(files) and not failures
result=dict(status='PASS_ALL_IMMUTABLE_NATIVE_SUPPLEMENT_BYTES' if complete else 'FAIL_PRESERVED_INCOMPLETE',**metadata,entry='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_review_v2_20261001/index.html',tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,manifest=base+index_path,manifest_bytes=size,manifest_sha256=hash_value,started_utc=started,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),verified_files=len(verified),verified_bytes=sum(x[1] for x in verified.values()),failures=failures,journal_value_schema=['path','bytes','sha256','checked_utc'],qualification='444 native supplement payloads and its self-map at exact6edb4ca8. Earlier c211 full and239-file C maps/receipts remain immutable. Hosted, source/context/action/device/child/owner, integration and release claims remain separate.')
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result),flush=True)
raise SystemExit(0 if complete else 1)
