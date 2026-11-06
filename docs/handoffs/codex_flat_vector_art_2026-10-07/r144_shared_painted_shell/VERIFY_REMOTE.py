from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,sys,json,hashlib,urllib.request,urllib.parse,time,datetime
W=Path.cwd();T=Path(__file__).parent;commit=sys.argv[1];manifest_path=sys.argv[2];label=sys.argv[3]
assert len(commit)==40 and all(c in '0123456789abcdef'for c in commit)
D=T/('remote_'+label+'_'+commit);assert not(D/'REMOTE_VERIFICATION.json').exists(),'Reuse completed immutable receipt, do not duplicate';D.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'
def fetch(url):
 assert url.startswith(prefix)
 last=None
 for attempt in range(4):
  try:
   request=urllib.request.Request(url,headers={'User-Agent':'reef-r144-anonymous-byte-verifier'})
   with urllib.request.urlopen(request,timeout=90)as response:
    assert response.status==200
    return response.read(),response.status
  except Exception as exc:last=exc;time.sleep(0.5*(attempt+1))
 raise last
local=subprocess.check_output(['git','show',commit+':'+manifest_path],stderr=subprocess.PIPE)
url=prefix+commit+'/'+urllib.parse.quote(manifest_path,safe='/');raw,status=fetch(url);assert raw==local
manifest=json.loads(raw);rows=manifest['files'];results=[]
def verify(row):
 revision=row.get('revision',commit);revision=commit if revision=='SELF'else revision
 assert len(revision)==40
 url=row.get('url',prefix+revision+'/'+urllib.parse.quote(row['path'],safe='/'))
 raw,status=fetch(url);actual=sha(raw);assert actual==row['sha256'],(row['path'],actual,row['sha256']);assert len(raw)==row['bytes']
 return {'path':row['path'],'revision':revision,'url':url,'sha256':actual,'bytes':len(raw),'http_status':status,'access_mode':'anonymous_no_authorization_no_cookies','checked_at_utc':now()}
with ThreadPoolExecutor(max_workers=4)as pool:
 futures=[pool.submit(verify,row)for row in rows]
 for future in as_completed(futures):
  results.append(future.result())
  if len(results)%25==0:print('ANON_VERIFIED',label,len(results),'/',len(rows),flush=True)
results.append({'path':manifest_path,'revision':commit,'url':url,'sha256':sha(raw),'bytes':len(raw),'http_status':status,'access_mode':'anonymous_no_authorization_no_cookies','checked_at_utc':now()})
receipt={'state':'PASS_ALL_REQUIRED_MANIFEST_BYTES_ANONYMOUSLY_VERIFIED','revision':commit,'manifest_path':manifest_path,'manifest_sha256':sha(raw),'required_files_including_manifest':len(results),'access_mode':'anonymous_no_authorization_no_cookies','checked_at_utc':now(),'files':sorted(results,key=lambda r:(r['revision'],r['path']))}
(D/'REMOTE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print('ALL_REQUIRED_BYTES_PASS',label,len(results),commit,flush=True)
