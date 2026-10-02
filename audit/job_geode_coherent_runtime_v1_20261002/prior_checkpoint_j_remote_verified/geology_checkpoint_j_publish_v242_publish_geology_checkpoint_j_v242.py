from pathlib import Path
import concurrent.futures, datetime, hashlib, json, shutil, subprocess, sys, time, urllib.request

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=b/'tmp/geology_checkpoint_j_publish_v242';out.mkdir(exist_ok=False)
verify=b/'tmp/geology_checkpoint_j_remote_v242';verify.mkdir(exist_ok=False)
branch='codex/job-art-review-v2-20261001'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):return subprocess.run(['git',*args],cwd=b,capture_output=True,check=True).stdout
def run(name,args,timeout=600):
 p=subprocess.run(args,cwd=b,capture_output=True,timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(name+'.stdout.log')).write_bytes(p.stdout);(out/(name+'.stderr.log')).write_bytes(p.stderr)
 print(name,p.returncode,flush=True);assert p.returncode==0,p.stderr.decode(errors='replace')[-1400:];return p.stdout
seal=json.loads((b/'tmp/geology_checkpoint_j_sealed.json').read_text())
assert git('rev-parse','HEAD').decode().strip()==seal['base_revision']
assert git('branch','--show-current').decode().strip()==branch
mp=seal['map_path'];raw=git('show',':'+mp);assert hashlib.sha256(raw).hexdigest()==seal['map_sha256']
m=json.loads(raw);expected=dict(m['files']);expected[mp]=[len(raw),hashlib.sha256(raw).hexdigest()]
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(expected)
ordered=sorted(expected);data=subprocess.run(['git','cat-file','--batch'],cwd=b,input=''.join(':'+p+'\n' for p in ordered).encode(),capture_output=True,check=True).stdout
offset=0
for path in ordered:
 end=data.index(b'\n',offset);size=int(data[offset:end].split()[2]);offset=end+1;raw=data[offset:offset+size];offset+=size+1
 assert [len(raw),hashlib.sha256(raw).hexdigest()]==expected[path],path
assert offset==len(data)
snapshot=json.loads((b/'audit/job_geology_river_runtime_v1_20261002/full_ci_v1/SOURCE_BEFORE.json').read_text())['source_files']
assert len(snapshot)==362 and all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in snapshot)
ci=json.loads((b/'audit/job_geology_river_runtime_v1_20261002/full_ci_v1/RECEIPT.json').read_text())
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
run('fetch',['git','fetch','origin'])
assert git('rev-parse','origin/'+branch).decode().strip()==seal['base_revision'],'Topic changed remotely; reconcile before publication.'
msg=out/'COMMIT_MESSAGE.txt'
msg.write_text('Audit painted river runtime and seven-state geode pilot\n\nBind six complete painted river images at reversible new paths; preserve actual input/path/flow/save methods. Include every162 isolated join studies and all46 current ordinary four-phase views/28 production network views. Current unmodified officialGodot4.7.2 full suite82/82 preserves362 literal source hashes and57 raw diagnostics.\n\nReview every312 actual continuous geode frame: opening4.2 exposes silhouette swaps. Preserve every failed regeneration, native original and exact reference hash; selected seven-state unbound pilot reaches provisional opening4.5, materials/rooted crystals4.6 after every312 frames on26 boards and8 native transition details. Current production geode remains unchanged. Room2.8/contact2.7/clap4.0 remain weak. V27 library has1712 individually addressable entries,666 inclusive priorities and388 unassigned.\n\nQualified reversible topic review checkpoint only; no complete training/story/return/device/child/owner/all-job acceptance, dev/master integration or release. Prior immutable source and review maps remain unchanged.\n',encoding='utf-8')
run('commit',['git','commit','--file',str(msg)])
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
for name,cmd in [('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:run(name,cmd)
run('push',['git','push','origin','HEAD:refs/heads/'+branch],1800)
assert git('rev-parse','origin/'+branch).decode().strip()==revision
pub={'status':'TOPIC_RUNTIME_CANDIDATE_PUBLISHED_VERIFICATION_PENDING','revision':revision,'tree':tree,'branch':branch,'map_path':mp,'map_sha256':seal['map_sha256'],'payload_sha256':m['payload_sha256'],'payload_files':m['required_files'],'payload_bytes':m['required_payload_bytes'],'source_count':362,'production_binding_changed':True,'checked_utc':utc(),'qualification':'Reversible topic candidate; no dev/master integration or all-job, device, child, owner, cinematic or release acceptance.'}
write(out/'RECEIPT.json',pub);shutil.copyfile(__file__,out/'publish_geology_checkpoint_j_v242.py')
prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'
started=utc()
def fetch(path):
 for attempt in range(1,4):
  try:
   req=urllib.request.Request(prefix+path,headers={'User-Agent':'MermaidReef-Anonymous-Review-QA'})
   with urllib.request.urlopen(req,timeout=60) as response:raw=response.read();status=response.status
   assert status==200
   return {'path':path,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'attempt':attempt,'status':'FETCHED_ANONYMOUS_TLS_GET','checked_utc':utc()},raw
  except Exception as e:
   if attempt==3:return {'path':path,'status':'FETCH_FAILED','error':str(e),'checked_utc':utc()},None
   time.sleep(attempt)
map_row,map_raw=fetch(mp);assert map_raw is not None and map_row['sha256']==pub['map_sha256'];assert json.loads(map_raw)==m
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(m['files'].items())).encode()
assert hashlib.sha256(formula).hexdigest()==m['payload_sha256']
rows=[];fail=[]
with (verify/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for future in concurrent.futures.as_completed([pool.submit(fetch,p) for p in m['files']]):
   row,raw=future.result();row['expected_bytes'],row['expected_sha256']=m['files'][row['path']]
   row['matches']=raw is not None and [row['bytes'],row['sha256']]==m['files'][row['path']]
   journal.write(json.dumps(row)+'\n');journal.flush();rows.append(row)
   if not row['matches']:fail.append(row)
   if len(rows)%100==0:print('verified',len(rows),'failures',len(fail),flush=True)
 map_row['matches']=True;journal.write(json.dumps(map_row)+'\n')
result={'status':'PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED','revision':revision,'tree':tree,'branch':branch,
 'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_geode_coherent_pilot_v1_20261002/index.html',
 'tree_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,'manifest_url':prefix+mp,'map_sha256':pub['map_sha256'],'payload_sha256':m['payload_sha256'],
 'payload_files':len(rows),'files_including_manifest':len(rows)+1,'payload_bytes':sum(v[0] for v in m['files'].values()),
 'access_mode':'Anonymous GET, normal TLS certificate verification, no Authorization header','started_utc':started,'finished_utc':utc(),'failed_files':fail,
 'qualification':'Published reversible production candidate bytes and qualified reviews; no all-job, full timed motion, device, child, owner, integration, cinematic or release acceptance.'}
write(verify/'RESULT.json',result);print(json.dumps(result),flush=True);raise SystemExit(0 if not fail else 1)
