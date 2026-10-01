"""Anonymous HTTPS verification of the manifest and every required exact-revision file."""
from pathlib import Path
import argparse,hashlib,json,urllib.request,urllib.parse,concurrent.futures,datetime,time
ap=argparse.ArgumentParser();ap.add_argument('revision');ap.add_argument('--receipt',type=Path,required=True);a=ap.parse_args()
V=Path(__file__).resolve().parent;R=V.parents[4]
manifest_path=V.relative_to(R).as_posix()+'/manifest.json'
base='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+a.revision+'/'
def fetch(path):
 url=base+urllib.parse.quote(path,safe='/');request=urllib.request.Request(url,headers={'User-Agent':'Mermaid-Roshan-book-review-verifier'})
 for attempt in range(3):
  try:
   with urllib.request.urlopen(request,timeout=120) as response:
    h=hashlib.sha256();size=0;chunks=[]
    while True:
     data=response.read(1024*1024)
     if not data:break
     size+=len(data);h.update(data)
     if path==manifest_path:chunks.append(data)
   return dict(path=path,bytes=size,sha256=h.hexdigest(),url=url,data=b''.join(chunks) if chunks else None)
  except Exception:
   if attempt==2:raise
   time.sleep(1+attempt)
remote=fetch(manifest_path)
assert remote['data']==(V/'manifest.json').read_bytes().replace(b'\r\n',b'\n'),'Remote manifest bytes differ'
manifest=json.loads(remote['data']);expected={r['path']:r for r in manifest['files']};checked=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 futures={pool.submit(fetch,p):p for p in expected}
 for i,f in enumerate(concurrent.futures.as_completed(futures),1):
  r=f.result();e=expected[r['path']]
  assert r['sha256']==e['sha256'] and r['bytes']==e['bytes'],(r['path'],r['sha256'],e['sha256'])
  r.pop('data',None);checked.append(r)
  if i%20==0:print(f'Verified {i}/{len(expected)} files',flush=True)
remote.pop('data',None)
record=dict(status='ALL_REQUIRED_REMOTE_BYTES_VERIFIED',revision=a.revision,checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),access_mode='Anonymous HTTPS; no GitHub credentials or cookies used',manifest=remote,payload_sha256=manifest['payload_sha256'],files_verified=len(checked),bytes_verified=sum(r['bytes'] for r in checked),files=sorted(checked,key=lambda x:x['path']),acceptance='Publication and byte identity only; owner/child/print acceptance remains open.')
a.receipt.parent.mkdir(parents=True,exist_ok=True);a.receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps({k:v for k,v in record.items() if k not in ['files','manifest']},indent=2))
