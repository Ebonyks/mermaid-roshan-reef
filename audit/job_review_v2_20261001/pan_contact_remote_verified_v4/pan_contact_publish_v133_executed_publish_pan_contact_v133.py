from pathlib import Path
import subprocess,json,hashlib,datetime,sys,urllib.request,concurrent.futures,time,shutil
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');out=b/'tmp/pan_contact_publish_v133';out.mkdir(exist_ok=False)
branch='codex/job-art-review-v2-20261001'
def run(name,args,timeout=600):
 p=subprocess.run(args,cwd=b,capture_output=True,timeout=timeout);(out/(name+'.stdout.log')).write_bytes(p.stdout);(out/(name+'.stderr.log')).write_bytes(p.stderr);print(name,p.returncode,flush=True);assert p.returncode==0,p.stderr.decode(errors='replace')[-900:];return p.stdout
def git(*args):return subprocess.run(['git',*args],cwd=b,capture_output=True,check=True).stdout
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
seal=json.loads((b/'tmp/pan_contact_v131_sealed.json').read_text());assert git('rev-parse','HEAD').decode().strip()==seal['base_revision'];assert git('branch','--show-current').decode().strip()==branch
mp=seal['map_path'];raw=git('show',':'+mp);assert hashlib.sha256(raw).hexdigest()==seal['map_sha256'];m=json.loads(raw);expected=dict(m['files']);expected[mp]=[len(raw),hashlib.sha256(raw).hexdigest()]
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(expected)
ordered=sorted(expected);data=subprocess.run(['git','cat-file','--batch'],cwd=b,input=''.join(':'+p+'\n' for p in ordered).encode(),capture_output=True,check=True).stdout;offset=0
for path in ordered:
 end=data.index(b'\n',offset);header=data[offset:end].split();size=int(header[2]);offset=end+1;raw=data[offset:offset+size];offset+=size+1;assert [len(raw),hashlib.sha256(raw).hexdigest()]==expected[path],path
assert offset==len(data)
snapshot=json.loads((b/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files'];assert len(snapshot)==325 and all(hashlib.sha256((b/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in snapshot)
msg=out/'COMMIT_MESSAGE.txt';msg.write_text('Refine geologist pan proportions and generate a readable two-hand grip\n\nPreserve every native comparison and earlier failed support/contact draft. Add a painted grain and a connected static gripping pose; both-screen hand contact4.6 is separate from tabletop support4.3 and missing articulated panning. Extend the illustrated known-item register to1559 entries and292 directly inspected teacher/geology/pan comparisons.\n\nAll325 production sources, game input/rewards/save and prior closed maps remain unchanged. Parser, inference, official4.7.2 import, contract/authority/development and2D no-regression gates pass; strict2D and ordinary complete route/device/child/owner/final audit acceptance remain open. Publish a reversible269-file topic supplement only.\n',encoding='utf-8');run('commit',['git','commit','--file',str(msg)])
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
for name,cmd in [('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:run(name,cmd)
run('fetch',['git','fetch','origin']);run('push',['git','push','origin','HEAD:refs/heads/'+branch],1800);assert git('rev-parse','origin/'+branch).decode().strip()==revision
pub=dict(status='TOPIC_REVIEW_PUBLISHED_VERIFICATION_PENDING',revision=revision,tree=tree,branch=branch,map_path=mp,map_sha256=seal['map_sha256'],payload_sha256=m['payload_sha256'],files=m['required_files'],bytes=m['required_payload_bytes'],source_count=325,production_source_unchanged=True,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),qualification='Reversible review checkpoint only; no dev/master integration, production replacement or comprehensive owner acceptance.');write(out/'RECEIPT.json',pub);shutil.copyfile(__file__,out/'executed_publish_pan_contact_v133.py')
verify=b/'tmp/pan_contact_remote_v133';verify.mkdir(exist_ok=False);prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
started=utc()
def fetch(path):
 for attempt in range(1,4):
  try:
   req=urllib.request.Request(prefix+path,headers={'User-Agent':'Mermaid-Roshan-review-verification/1'})
   with urllib.request.urlopen(req,timeout=120) as response:assert response.status==200;raw=response.read()
   return dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),attempt=attempt,status='FETCHED_ANONYMOUS_TLS_GET',checked_utc=utc()),raw
  except Exception as e:
   if attempt==3:return dict(path=path,status='FETCH_FAILED',error=str(e),checked_utc=utc()),None
   time.sleep(attempt)
map_row,map_raw=fetch(mp);assert map_raw is not None and map_row['sha256']==pub['map_sha256'];rm=json.loads(map_raw);assert rm==m
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(m['files'].items())).encode();assert hashlib.sha256(formula).hexdigest()==m['payload_sha256']
rows=[];fail=[]
with (verify/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  futures={pool.submit(fetch,p):p for p in m['files']}
  for future in concurrent.futures.as_completed(futures):
   row,raw=future.result();p=row['path'];row['expected_bytes'],row['expected_sha256']=m['files'][p];row['matches']=raw is not None and [row['bytes'],row['sha256']]==m['files'][p];journal.write(json.dumps(row)+'\n');journal.flush();rows.append(row)
   if not row['matches']:fail.append(row)
   if len(rows)%100==0:print('verified',len(rows),'failures',len(fail),flush=True)
 map_row['matches']=True;journal.write(json.dumps(map_row)+'\n')
result=dict(status='PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED',revision=revision,tree=tree,branch=branch,entry_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_review_v2_20261001/index.html',tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,manifest_url=prefix+mp,map_sha256=pub['map_sha256'],payload_sha256=m['payload_sha256'],payload_files=len(rows),files_including_manifest=len(rows)+1,payload_bytes=sum(v[0] for v in m['files'].values()),access_mode='Anonymous GET, normal TLS certificate verification, no Authorization header',started_utc=started,finished_utc=utc(),failed_files=fail,qualification='Published reversible review bytes only; static source/contact scores do not confer complete motion/route/device/child/owner/release acceptance.');write(verify/'RESULT.json',result);print(json.dumps(result),flush=True);raise SystemExit(0 if not fail else 1)
