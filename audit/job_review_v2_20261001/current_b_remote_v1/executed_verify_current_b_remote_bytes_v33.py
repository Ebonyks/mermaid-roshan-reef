from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import quote
import argparse,datetime,hashlib,json,subprocess,time,urllib.request
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
parser=argparse.ArgumentParser();parser.add_argument('--resume',action='store_true');args=parser.parse_args()
revision='c2116877de10202c40e1d939c77eb3646b5f202f';index_path='audit/job_review_v2_20261001/CURRENT_B_FILES_V1.json'
out=r/'tmp/current_b_remote_v33'
if args.resume:assert out.is_dir()
else:assert not out.exists();out.mkdir()
attempt=out/('attempt_%02d'%(len(list(out.glob('attempt_*')))+1));attempt.mkdir()
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
base='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'
def fetch(path,collect=False):
 request=urllib.request.Request(base+quote(path,safe='/'),headers={'User-Agent':'MermaidRoshan-public-immutable-byte-verification'})
 for try_index in range(3):
  try:
   with urllib.request.urlopen(request,timeout=45) as response:
    assert response.status==200
    sha=hashlib.sha256();size=0;parts=[]
    while True:
     block=response.read(1024*1024)
     if not block:break
     sha.update(block);size+=len(block)
     if collect:parts.append(block)
    return size,sha.hexdigest(),b''.join(parts) if collect else None
  except Exception:
   if try_index==2:raise
   time.sleep(try_index+1)
index_size,index_sha,index_data=fetch(index_path,True)
assert index_data==subprocess.check_output(['git','show',revision+':'+index_path],cwd=r)
m=json.loads(index_data);assert m['file_count']==13534 and index_sha=='76f46664a2e4967161593fe831ef9024dad9a8dfc4a191b34652b6d512691798'
files=m['files'];assert len(files)==m['file_count']
digest=hashlib.sha256(''.join(path+'\0'+str(value[0])+'\0'+value[1]+'\n' for path,value in files.items()).encode('utf-8')).hexdigest();assert digest==m['sorted_payload_sha256']
tree=subprocess.check_output(['git','rev-parse',revision+'^{tree}'],cwd=r,text=True).strip()
metadata={'revision':revision,'tree':tree,'index':index_path,'index_sha256':index_sha,'index_bytes':index_size,'payload_sha256':digest,'required_files':len(files),'required_bytes':m['payload_bytes'],'access_mode':'Anonymous public HTTPS with normal TLS verification. No credentials or Authorization header. Every exact immutable path must be fetched.'}
metapath=out/'CHECKPOINT_IDENTITY.json'
if args.resume:assert json.loads(metapath.read_text(encoding='utf-8'))==metadata
else:metapath.write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
verified={};journalpath=out/'FETCH_JOURNAL.jsonl'
if journalpath.exists():
 for line in journalpath.read_text(encoding='utf-8').splitlines():
  row=json.loads(line);assert row[0] in files and row[1:3]==files[row[0]];verified[row[0]]=row
def verify(path,value):
 size,sha,_=fetch(path);assert [size,sha]==value,path
 return [path,size,sha,datetime.datetime.now(datetime.timezone.utc).isoformat()]
failures=[]
print('CURRENT_B_INDEX_MATCH',revision,index_sha,len(files),flush=True)
with journalpath.open('a',encoding='utf-8') as journal,ThreadPoolExecutor(max_workers=8) as workers:
 jobs={workers.submit(verify,path,value):path for path,value in files.items() if path not in verified}
 for job in as_completed(jobs):
  try:
   row=job.result();verified[row[0]]=row;journal.write(json.dumps(row,separators=(',',':'))+'\n');journal.flush()
   if len(verified)%250==0:print('CURRENT_B_BYTES',len(verified),'/',len(files),flush=True)
  except Exception as error:
   failures.append({'path':jobs[job],'error':type(error).__name__+': '+str(error)});print('CURRENT_B_FAILURE',jobs[job],type(error).__name__,flush=True)
finished=datetime.datetime.now(datetime.timezone.utc).isoformat();complete=set(verified)==set(files) and not failures
result={'status':'PASS_ALL_IMMUTABLE_CURRENT_B_BYTES' if complete else 'FAIL_PRESERVED_INCOMPLETE','revision':revision,'tree':tree,'entry':base.replace('raw.githubusercontent.com','github.com').replace('/'+revision+'/', '/blob/'+revision+'/')+m['entry'],'manifest':base+index_path,'manifest_sha256':index_sha,'manifest_bytes':index_size,'payload_sha256':digest,'started_utc':started,'checked_utc':finished,'required_files':len(files),'verified_files':len(verified),'verified_bytes':sum(row[1] for row in verified.values()),'failures':failures,'access_mode':metadata['access_mode'],'journal_value_schema':['path','bytes','sha256','checked_utc'],'qualification':'Every MATCH is a complete real anonymous GET at the exact currentB revision; resume records keep original check times. SourceA history remains separately pinned. Hosted CI, all-source/complete-action/device/child/owner acceptance, integration and release remain separate.'}
(attempt/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result),flush=True);raise SystemExit(0 if complete else 1)
