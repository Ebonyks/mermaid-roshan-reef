"""Anonymous HTTPS checks for every output and all pinned incoming dependencies."""
from pathlib import Path
import argparse,json,hashlib,urllib.request,urllib.parse,concurrent.futures,datetime,time
a=argparse.ArgumentParser();a.add_argument('revision');a.add_argument('--receipt',type=Path,required=True);a=a.parse_args();V=Path(__file__).resolve().parent;R=V.parents[4]
mp=V.relative_to(R).as_posix()+'/manifest.json'
def fetch(rev,path,keep=False):
 url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+urllib.parse.quote(path,safe='/')
 for n in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mermaid-Roshan-V45-anonymous-verifier'}),timeout=100) as z:
    digest=hashlib.sha256();size=0;parts=[]
    while True:
     data=z.read(1048576)
     if not data:break
     digest.update(data);size+=len(data)
     if keep:parts.append(data)
   row=dict(revision=rev,path=path,url=url,bytes=size,sha256=digest.hexdigest())
   if keep:row['data']=b''.join(parts)
   return row
  except Exception:
   if n==2:raise
   time.sleep(1+n)
mr=fetch(a.revision,mp,True);assert mr['data']==(V/'manifest.json').read_bytes().replace(b'\r\n',b'\n');m=json.loads(mr.pop('data'))
jobs=[dict(q,revision=a.revision,lane='output') for q in m['files']]+[dict(q,lane='pinned_input') for q in m['required_external_inputs']];rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 fs={pool.submit(fetch,q['revision'],q['path']):q for q in jobs}
 for f in concurrent.futures.as_completed(fs):
  q=fs[f];r=f.result();assert r['bytes']==q['bytes'] and r['sha256']==q['sha256'],q['path'];r['lane']=q['lane'];rows.append(r)
  if len(rows)%20==0:print('Verified',len(rows),'/',len(jobs),flush=True)
record=dict(status='ALL_REQUIRED_REMOTE_BYTES_VERIFIED',revision=a.revision,checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),access_mode='Anonymous HTTPS; no credentials or cookies',manifest=mr,payload_sha256=m['payload_sha256'],external_inputs_sha256=m['external_inputs_sha256'],output_files_verified=len(m['files']),pinned_input_files_verified=len(m['required_external_inputs']),total_bytes_verified=sum(q['bytes'] for q in rows),files=sorted(rows,key=lambda q:(q['revision'],q['path'])),acceptance='Byte availability/identity only.23/25draft,11/15held and owner/child/SLP/print limits unchanged.')
a.receipt.write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps({k:v for k,v in record.items() if k not in ['files','manifest']},indent=2))
