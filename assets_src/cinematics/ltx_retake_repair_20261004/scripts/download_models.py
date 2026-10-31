from pathlib import Path
import concurrent.futures,hashlib,json,time,urllib.request
packet=Path(__file__).resolve().parents[1]
plan=json.loads((packet/'environment/download_plan.json').read_text())
def download(item):
 target=Path(item['destination']);target.parent.mkdir(parents=True,exist_ok=True);start=time.monotonic()
 if target.exists():
  with target.open('rb') as s: actual=hashlib.file_digest(s,'sha256').hexdigest()
  if actual==item['sha256']:return dict(item,status='VERIFIED_EXISTING',elapsed_seconds=0)
  raise RuntimeError('Existing destination differs: '+str(target))
 part=target.with_suffix(target.suffix+'.part')
 for attempt in range(3):
  offset=part.stat().st_size if part.exists() else 0
  request=urllib.request.Request(item['url'],headers={'Range':f'bytes={offset}-'} if offset else {})
  try:
   with urllib.request.urlopen(request,timeout=90) as response:
    with part.open('ab' if offset and response.status==206 else 'wb') as stream:
     while block:=response.read(8*1024*1024):stream.write(block)
   break
  except Exception:
   if attempt==2:raise
   time.sleep(3)
 if part.stat().st_size!=item['bytes']:raise RuntimeError('Size mismatch: '+str(part))
 with part.open('rb') as stream:actual=hashlib.file_digest(stream,'sha256').hexdigest()
 if actual!=item['sha256']:raise RuntimeError('Hash mismatch: '+str(part))
 part.rename(target);result=dict(item,status='VERIFIED_DOWNLOADED',elapsed_seconds=round(time.monotonic()-start,3));print('VERIFIED',target.name,result['elapsed_seconds'],flush=True);return result
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 jobs={pool.submit(download,item):item for item in plan['files']}
 for future in concurrent.futures.as_completed(jobs):
  try:results.append(future.result())
  except Exception as error:results.append(dict(jobs[future],status='FAILED',error=str(error)))
  (packet/'environment/download_receipt.json').write_text(json.dumps({'files':results},indent=2)+'\n')
if any(r['status']=='FAILED' for r in results):raise SystemExit(1)
