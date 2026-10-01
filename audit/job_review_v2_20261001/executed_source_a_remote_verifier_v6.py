from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from urllib.parse import quote
import argparse,datetime,hashlib,json,subprocess,time,urllib.request

root=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
families=['audit/day_one_pool_live_refinement_v2_20261001','assets_src/imagegen/day1_playroom_sign_v2_20261001','audit/day_two_boxing_puff_reuse_v1_20261001','assets_src/imagegen/day2_boxing_single_gloves_v1_20261001','audit/day_two_boxing_live_refinement_v1_20261001']
parser=argparse.ArgumentParser();parser.add_argument('--revision',required=True);parser.add_argument('--resume',action='store_true');args=parser.parse_args()
revision=subprocess.check_output(['git','rev-parse',args.revision+'^{commit}'],cwd=root,text=True).strip()
assert revision=='8e41deaf34f925869395cd8ab0affefe89f89ab5'
out=root/'tmp/current_public_remote_v6'
if args.resume:assert out.exists()
else:assert not out.exists();out.mkdir()
attempt=out/('attempt_%02d'%(len(list(out.glob('attempt_*')))+1));attempt.mkdir()
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def fetch(path):
    url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+quote(path,safe='/')
    request=urllib.request.Request(url,headers={'User-Agent':'MermaidRoshan-public-byte-verification'})
    for index in range(3):
        try:
            with urllib.request.urlopen(request,timeout=45) as response:
                assert response.status==200
                return response.read()
        except Exception:
            if index==2:raise
            time.sleep(index+1)
def blob(path):return subprocess.check_output(['git','show',revision+':'+path],cwd=root)
manifests=[];files={}
for prefix in families:
    path=prefix+'/MANIFEST.json';data=fetch(path);assert data==blob(path),path;manifest=json.loads(data)
    assert sha('\n'.join(r['path']+'\t'+r['sha256'] for r in manifest['files']).encode())==manifest['packet_payload_sha256']
    manifests.append((prefix,manifest,sha(data)))
    for row in manifest['files']+manifest['dependencies']:
        previous=files.get(row['path']);assert previous is None or (previous['sha256'],previous['bytes'])==(row['sha256'],row['bytes'])
        files[row['path']]=row
    print('PUBLIC_MANIFEST_MATCH',prefix,sha(data),flush=True)
metadata={'revision':revision,'manifests':{p:h for p,m,h in manifests},'declared_unique_files':len(files),'map_sha256':sha(json.dumps(files,sort_keys=True).encode()),'access_mode':'Anonymous public HTTPS with normal TLS verification; no credentials or Authorization header'}
meta_path=out/'CHECKPOINT_IDENTITY.json'
if args.resume:assert json.loads(meta_path.read_text())==metadata
else:meta_path.write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
verified={};checkpoint=out/'VERIFIED_FILES.jsonl'
if checkpoint.exists():
    for line in checkpoint.read_text(encoding='utf-8').splitlines():
        row=json.loads(line);wanted=files[row['path']]
        assert (row['sha256'],row['bytes'],row['result'])==(wanted['sha256'],wanted['bytes'],'MATCH')
        verified[row['path']]=row
def verify(row):
    raw=fetch(row['path']);assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['path']
    return {'path':row['path'],'sha256':row['sha256'],'bytes':len(raw),'result':'MATCH','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
failures=[]
with checkpoint.open('a',encoding='utf-8') as journal,ThreadPoolExecutor(max_workers=6) as workers:
    jobs={workers.submit(verify,r):r['path'] for r in files.values() if r['path'] not in verified}
    for job in as_completed(jobs):
        try:
            row=job.result();verified[row['path']]=row
            journal.write(json.dumps(row)+'\n');journal.flush()
            if len(verified)%100==0:print('PUBLIC_BYTE_PROGRESS',len(verified),'/',len(files),flush=True)
        except Exception as error:
            failures.append({'path':jobs[job],'error':type(error).__name__+': '+str(error)})
            print('PUBLIC_BYTE_FAILURE',jobs[job],type(error).__name__,flush=True)
finished=datetime.datetime.now(datetime.timezone.utc).isoformat()
complete=set(verified)==set(files) and not failures
result={'status':'PASS_ALL_IMMUTABLE_REMOTE_BYTES' if complete else 'FAIL_PRESERVED_INCOMPLETE','revision':revision,'started_utc':started,'checked_utc':finished,'unique_files_verified':len(verified),'unique_files_required':len(files),'bytes_verified':sum(r['bytes'] for r in verified.values()),'failures':failures,'qualification':'Every MATCH was actually fetched anonymously and size/SHA256 checked at this immutable revision. Resume records preserve the original check time; no accepted receipt is written unless every declared file and all five manifests match. Hosted CI and creative acceptance are separate.'}
(attempt/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
if not complete:print(json.dumps(result),flush=True);raise SystemExit(1)
assert all(not (root/p/'REMOTE_VERIFICATION.json').exists() for p in families)
for prefix,manifest,manifest_sha in manifests:
    ordered=sorted({r['path'] for r in manifest['files']+manifest['dependencies']})
    receipt={'schema':'reef.public-remote-verification.v1','revision':revision,'repository':'https://github.com/Ebonyks/mermaid-roshan-reef','entry':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+manifest['entry'],'immutable_tree':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,'manifest':'https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'+prefix+'/MANIFEST.json','manifest_sha256':manifest_sha,'packet_payload_sha256':manifest['packet_payload_sha256'],'started_utc':min(verified[p]['checked_utc'] for p in ordered),'checked_utc':finished,'access_mode':metadata['access_mode'],'result':'PASS','files_verified':len(ordered),'bytes_verified':sum(verified[p]['bytes'] for p in ordered),'joint_verification':'Five immutable manifests independently fetched and compared to exact Git blobs; every9583 declared unique payload/dependency path size and SHA256 checked. Checkpoint records retain per-file fetch times.','files':[verified[p] for p in ordered],'qualification':'Published review archive accessibility and exact bytes at8e41deaf only. Later receipt/review changes do not silently rebind this original payload revision. Source/static/contact opinions, complete action, device/child/owner approval, comprehensive acceptance, integration and release remain separate and unfinished.'}
    (root/prefix/'REMOTE_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result),flush=True)
