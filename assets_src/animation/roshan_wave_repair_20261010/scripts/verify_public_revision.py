"""Anonymous immutable GitHub byte verification; no credentials or upload."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, datetime, hashlib, json, time, urllib.request
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--revision',required=True);p.add_argument('--workers',type=int,default=8)
 a=p.parse_args()
 if len(a.revision)!=40 or any(c not in '0123456789abcdef' for c in a.revision):raise ValueError('Immutable40hex revision required')
 packet=Path(__file__).resolve().parent.parent
 root=next(x for x in packet.parents if (x/'project.godot').is_file())
 base=f'https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/{a.revision}/'
 manifest_path=(packet/'packet_manifest.json').relative_to(root).as_posix()
 def fetch(path):
  for attempt in range(3):
   try:
    with urllib.request.urlopen(urllib.request.Request(base+path,headers={'User-Agent':'reef-public-byte-verifier/1'}),timeout=60) as r:return r.read()
   except Exception:
    if attempt==2:raise
    time.sleep(attempt+1)
 raw=fetch(manifest_path)
 if raw!=(packet/'packet_manifest.json').read_bytes():raise ValueError('Published manifest differs from frozen local bytes')
 manifest=json.loads(raw);rows=manifest['files']+manifest.get('required_external_files',[])
 if manifest['file_count']!=len(manifest['files']) or len({r['path'] for r in rows})!=len(rows):raise ValueError('Manifest count/duplicate path mismatch')
 def verify(row):
  data=fetch(row['path']);digest=hashlib.sha256(data).hexdigest()
  if digest!=row['sha256'] or len(data)!=row['bytes']:raise ValueError('Byte/hash mismatch: '+row['path'])
  return {'path':row['path'],'sha256':digest,'bytes':len(data),'status':'ANONYMOUS_HTTP_BYTES_PASS'}
 results=[];failures=[]
 with ThreadPoolExecutor(max_workers=a.workers) as pool:
  futures={pool.submit(verify,row):row['path'] for row in rows}
  for future in as_completed(futures):
   try:results.append(future.result())
   except Exception as e:failures.append({'path':futures[future],'error':str(e)})
 results.sort(key=lambda r:r['path'])
 packet_paths={r['path'] for r in manifest['files']}
 packet_results=sorted((r for r in results if r['path'] in packet_paths),key=lambda r:r['path'].encode('utf-8'))
 payload=''.join(f"{r['path']}\t{r['sha256']}\t{r['bytes']}\n" for r in packet_results).encode('utf-8')
 measured_payload=hashlib.sha256(payload).hexdigest()
 if not failures and measured_payload!=manifest['payload_sha256']:raise ValueError('Fetched packet payload algorithm/hash mismatch')
 record={'schema':'reef.public-revision-verification.v1','revision':a.revision,
  'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'access_mode':'Anonymous HTTPS raw.githubusercontent.com; no authentication or cookies',
  'manifest_path':manifest_path,'manifest_sha256':hashlib.sha256(raw).hexdigest(),
  'payload_sha256':manifest['payload_sha256'],'fetched_payload_sha256':measured_payload,'required_files':len(rows),'verified_files':len(results),
  'verified_bytes':sum(r['bytes'] for r in results),'files':results,'failures':failures,
  'ANONYMOUS_TRANSPORT_VERIFIED':not failures and len(results)==len(rows),
  'ARCHIVE_COMPLETE':not failures and len(results)==len(rows) and manifest['claims'].get('derivation_archive_complete',True),
  'known_archive_limits':manifest.get('known_archive_limits',[]),'DELIVERY_ACCEPTED':False}
 (packet/'remote_verification.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
 print(json.dumps({k:v for k,v in record.items() if k not in ['files']}))
 if failures:raise SystemExit(1)

if __name__=='__main__':main()
