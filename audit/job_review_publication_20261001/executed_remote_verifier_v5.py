from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, datetime, hashlib, json, subprocess, time, urllib.request
root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
families=['audit/day_one_pool_live_refinement_v2_20261001', 'assets_src/imagegen/day1_playroom_sign_v2_20261001', 'audit/day_two_boxing_puff_reuse_v1_20261001', 'assets_src/imagegen/day2_boxing_single_gloves_v1_20261001', 'audit/day_two_boxing_live_refinement_v1_20261001']
parser=argparse.ArgumentParser();parser.add_argument('--revision',required=True);parser.add_argument('--receipt-only',action='store_true');args=parser.parse_args()
revision=subprocess.check_output(['git','rev-parse',args.revision+'^{commit}'],cwd=root,text=True).strip()
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def fetch(path):
    url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+path
    request=urllib.request.Request(url,headers={'User-Agent':'MermaidRoshan-public-byte-verification'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request,timeout=60) as response:
                assert response.status==200;return response.read()
        except Exception:
            if attempt==2:raise
            time.sleep(2)
def blob(path):return subprocess.check_output(['git','show',revision+':'+path],cwd=root)
if args.receipt_only:
    for prefix in families:
        for name in ['MANIFEST.json','REMOTE_VERIFICATION.json']:
            path=prefix+'/'+name;data=fetch(path);assert data==blob(path),path
            print('PUBLIC_RECEIPT|MATCH|'+path+'|sha256='+sha(data),flush=True)
    print('PUBLIC_RECEIPTS|PASS|revision='+revision,flush=True);raise SystemExit(0)
manifests=[];files={}
for prefix in families:
    path=prefix+'/MANIFEST.json';data=fetch(path);assert data==blob(path),path;manifest=json.loads(data)
    assert sha('\n'.join(r['path']+'\t'+r['sha256'] for r in manifest['files']).encode())==manifest['packet_payload_sha256']
    manifests.append((prefix,manifest,sha(data)))
    for row in manifest['files']+manifest['dependencies']:
        previous=files.get(row['path']);assert previous is None or (previous['sha256'],previous['bytes'])==(row['sha256'],row['bytes'])
        files[row['path']]=row
    print('PUBLIC_MANIFEST|MATCH|'+path+'|sha256='+sha(data),flush=True)
def verify(row):
    raw=fetch(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['path']
    return {'path':row['path'],'sha256':row['sha256'],'bytes':len(raw),'result':'MATCH'}
verified={}
with ThreadPoolExecutor(max_workers=6) as workers:
    jobs=[workers.submit(verify,r) for r in files.values()]
    for job in as_completed(jobs):
        row=job.result();verified[row['path']]=row
        if len(verified)%100==0:print(f'PUBLIC_REVIEW_PROGRESS|{len(verified)}/{len(files)}',flush=True)
finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
for prefix,manifest,manifest_sha in manifests:
    path=root/prefix/'REMOTE_VERIFICATION.json';assert not path.exists(),'Preserve prior remote receipt.'
    ordered=sorted({r['path'] for r in manifest['files']+manifest['dependencies']})
    receipt={'schema':'reef.public-remote-verification.v1','revision':revision,'repository':'https://github.com/Ebonyks/mermaid-roshan-reef',
      'entry':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+manifest['entry'],
      'immutable_tree':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,
      'manifest':'https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+prefix+'/MANIFEST.json',
      'manifest_sha256':manifest_sha,'packet_payload_sha256':manifest['packet_payload_sha256'],'started_utc':started,'checked_utc':finished,
      'access_mode':'Anonymous public HTTPS with normal TLS verification; no credentials or Authorization header',
      'result':'PASS','files_verified':len(ordered),'bytes_verified':sum(verified[p]['bytes'] for p in ordered),
      'joint_verification':'Five manifests independently fetched and compared to exact immutable Git blobs; identical payload/dependency maps verified once per unique path.',
      'files':[verified[p] for p in ordered],
      'qualification':'Published review archive accessibility and exact bytes only. Source/static/contact opinions, complete action, device/child/owner acceptance, comprehensive approval, integration and release remain separate and unfinished.'}
    path.write_text(json.dumps(receipt,indent=2)+'\n')
print(f'PUBLIC_REVIEW|PASS|revision={revision}|unique={len(verified)}|bytes={sum(r["bytes"] for r in verified.values())}',flush=True)
