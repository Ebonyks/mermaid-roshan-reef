"""Verify the exact published game packet without credentials or private access."""
import argparse, concurrent.futures, datetime, hashlib, json, urllib.request, urllib.parse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--revision',required=True);p.add_argument('--manifest',default='audit/cycles/reef-kart-zones-20261105/DELIVERY_MANIFEST.json');p.add_argument('--out',required=True);a=p.parse_args()
base='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+a.revision+'/'
def fetch(path):
 request=urllib.request.Request(base+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'ReefKart-Anonymous-Packet-Verification/1'})
 with urllib.request.urlopen(request,timeout=60) as response:
  return response.read(),response.status
raw,status=fetch(a.manifest)
local_manifest=Path(a.manifest).read_bytes()
if hashlib.sha256(raw).hexdigest()!=hashlib.sha256(local_manifest).hexdigest():
 raise RuntimeError('Published manifest differs from the local literal manifest')
manifest=json.loads(raw)
paths=[entry['path'] for entry in manifest['files']]
if len(paths)!=len(set(paths)) or paths!=sorted(paths):
 raise RuntimeError('Manifest paths must be unique and sorted')
payload=hashlib.sha256(''.join(entry['path']+'\t'+entry['sha256']+'\n' for entry in manifest['files']).encode()).hexdigest()
if payload!=manifest['payload_sha256']:
 raise RuntimeError('Manifest payload checksum mismatch')
def check(entry):
 raw,status=fetch(entry['path']);actual=hashlib.sha256(raw).hexdigest()
 return {'path':entry['path'],'http_status':status,'expected_sha256':entry['sha256'],'actual_sha256':actual,'bytes':len(raw),'pass':status==200 and actual==entry['sha256'] and len(raw)==entry['bytes']}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
 checks=list(executor.map(check,manifest['files']))
receipt={'schema':'reef.kart.remote-verification.v1','repository':'Ebonyks/mermaid-roshan-reef','revision':a.revision,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'access_mode':'Anonymous public raw HTTPS; no Authorization header, GitHub app, token, signed or expiring URL','manifest_path':a.manifest,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'payload_sha256':manifest['payload_sha256'],'checked_files':len(checks),'pass':all(x['pass'] for x in checks),'files':checks,'creative_acceptance':'Not supplied. Human audio/visual, device, child and owner gates remain separate.'}
Path(a.out).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'}))
if not receipt['pass']:raise SystemExit(1)
