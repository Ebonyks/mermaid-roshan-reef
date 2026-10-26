from pathlib import Path
import json,hashlib,concurrent.futures,urllib.request,urllib.parse,datetime
V=Path(__file__).resolve().parent
rows=json.loads((V/'handoff_local_verification.json').read_text('utf8'))['files']
def check(q):
 url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+q['revision']+'/'+urllib.parse.quote(q['path'],safe='/')
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Book-V38-input-verification'}),timeout=90) as r:
  data=r.read()
 assert len(data)==q['bytes'] and hashlib.sha256(data).hexdigest()==q['sha256'],q['path']
 return dict(**q,url=url)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 result=list(pool.map(check,rows))
record=dict(status='ALL67_INPUT_FILES_VERIFIED',access_mode='Anonymous HTTPS; no credentials/cookies',checked_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files_verified=len(result),files=result)
(V/'handoff_remote_verification.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf8',newline='\n')
print(record['status'])
