from pathlib import Path
import concurrent.futures, datetime, hashlib, json, shutil, subprocess, sys, time, urllib.request

b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=b/'tmp/geology_checkpoint_l_publish_v297';out.mkdir(exist_ok=False)
verify=b/'tmp/geology_checkpoint_l_remote_v297';verify.mkdir(exist_ok=False)
branch='codex/job-art-review-v2-20261001'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):return subprocess.run(['git',*args],cwd=b,capture_output=True,check=True).stdout
def run(name,args,timeout=600):
 p=subprocess.run(args,cwd=b,capture_output=True,timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(name+'.stdout.log')).write_bytes(p.stdout);(out/(name+'.stderr.log')).write_bytes(p.stderr)
 print(name,p.returncode,flush=True);assert p.returncode==0,p.stderr.decode(errors='replace')[-1400:];return p.stdout
seal=json.loads((b/'tmp/geology_checkpoint_l_sealed.json').read_text())
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
snapshot=json.loads((b/'audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v1/SOURCE_BEFORE.json').read_text())['source_files']
assert len(snapshot)==372 and all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in snapshot)
ci=json.loads((b/'audit/job_geode_route_emblem_runtime_v1_20261002/full_ci_v1/RECEIPT.json').read_text())
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
run('fetch',['git','fetch','origin'])
assert git('rev-parse','origin/'+branch).decode().strip()==seal['base_revision'],'Topic changed remotely; reconcile before publication.'
msg=out/'COMMIT_MESSAGE.txt'
msg.write_text('Reuse painted geode throughout its actual job route\n\nThe end specimen opens into two stone halves with crystals rooted inside. Reuse that same unchanged source for Library crest, closed invitation, normal earned celebration and existing shared developer menu; preserve input, progress, save and rewards. Three production script bindings and one new AtlasTexture resource. Strict catalog/cache check and exact function-body preservation recorded; initial unused-metadata failure retained and repaired without weakening validators.\n\nEvery58 current native stills/316 consecutive frames/37 complete boards/eight native details and23 individual opinions reviewed. Library/invitation4.5 provisional; developer80px4.6; celebration material4.6 but unsupported placement4.2/composition3.3. Room2.8/contact2.7/fossil clearing3.9/pan3.8/caption4.0 and native-resolution background gap remain. V31 known register1726 entries,676 source priorities/385 unassigned, with material/mounting separated and earlierV30 bytes/labels preserved.\n\nAlso review every256 preservedOctober1 Doctor1280 training WASH frames on22 complete boards plus eight native details and12 individual opinions. Workflow2.7/contact2.3/subject2.2/basin2.9 remain weak; dated capture freshness470/475, not a new current rerender. Other1818 captured case frames and ordinary story/device/child/owner acceptance remain open.\n\nFresh officialGodot4.7.2 unmodified full suite1 82/82 on372 unchanged literal source files, raw diagnostics retained. Topic review candidate; no all-job acceptance, finding closure, dev/master integration or release. Every new payload and259 required unchanged native reference files anonymously verified at immutable revision. Earlier closed maps unchanged.\n',encoding='utf-8')
run('commit',['git','commit','--file',str(msg)])
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip()
assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
for name,cmd in [('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:run(name,cmd)
run('push',['git','push','origin','HEAD:refs/heads/'+branch],1800)
assert git('rev-parse','origin/'+branch).decode().strip()==revision
pub={'status':'TOPIC_RUNTIME_CANDIDATE_PUBLISHED_VERIFICATION_PENDING','revision':revision,'tree':tree,'branch':branch,'map_path':mp,'map_sha256':seal['map_sha256'],'payload_sha256':m['payload_sha256'],'payload_files':m['required_files'],'payload_bytes':m['required_payload_bytes'],'source_count':372,'production_binding_changed':True,'checked_utc':utc(),'qualification':'Reversible topic candidate; no dev/master integration or all-job, device, child, owner, cinematic or release acceptance.'}
write(out/'RECEIPT.json',pub);shutil.copyfile(__file__,out/'publish_geology_checkpoint_l_v297.py')
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
targets=dict(m['files']);targets.update(m.get('unchanged_required_files',{}))
rows=[];fail=[]
with (verify/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for future in concurrent.futures.as_completed([pool.submit(fetch,p) for p in targets]):
   row,raw=future.result();row['expected_bytes'],row['expected_sha256']=targets[row['path']]
   row['matches']=raw is not None and [row['bytes'],row['sha256']]==targets[row['path']]
   journal.write(json.dumps(row)+'\n');journal.flush();rows.append(row)
   if not row['matches']:fail.append(row)
   if len(rows)%100==0:print('verified',len(rows),'failures',len(fail),flush=True)
 map_row['matches']=True;journal.write(json.dumps(map_row)+'\n')
result={'status':'PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED','revision':revision,'tree':tree,'branch':branch,
 'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_geode_route_emblem_runtime_v1_20261002/index.html',
 'tree_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,'manifest_url':prefix+mp,'map_sha256':pub['map_sha256'],'payload_sha256':m['payload_sha256'],
 'payload_files':len(m['files']),'required_unchanged_files':len(m.get('unchanged_required_files',{})),'files_including_manifest':len(rows)+1,'payload_bytes':sum(v[0] for v in m['files'].values()),
 'access_mode':'Anonymous GET, normal TLS certificate verification, no Authorization header','started_utc':started,'finished_utc':utc(),'failed_files':fail,
 'qualification':'Published reversible production candidate bytes and qualified reviews; no all-job, full timed motion, device, child, owner, integration, cinematic or release acceptance.'}
write(verify/'RESULT.json',result);print(json.dumps(result),flush=True);raise SystemExit(0 if not fail else 1)
