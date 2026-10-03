from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.parse,urllib.request
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';S=B/'audit/job_shared_background_review_v1_20261003';T=B/'assets_src/imagegen/playroom_stacking_toy_painted_v1_20261003';L=B/'audit/job_artwork_refinement_live';IP=B/'design/audit_impacts/job-candy-shared-library-continuation-20261003.json'
BASE='ae3880df4244139a4f681034b530a5ee2c68895d';BRANCH='codex/job-art-review-v2-20261001';MAP='audit/job_review_v2_20261001/CANDY_SHARED_TOY_REVIEW_FILES_V21.json';PRIOR='audit/job_review_v2_20261001/CANDY_LOCAL_WRAP_CONTINUITY_FILES_V20.json';SHARDS='audit/job_review_v2_20261001/v21_unchanged_dependency_shards'
PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe';OUT=B/'tmp/candy_shared_publish_v573';VERIFY=B/'tmp/candy_shared_remote_v573'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d,compact=False):
 p.parent.mkdir(parents=True,exist_ok=True);n=p.with_name(p.name+'.v573_next');n.write_bytes((json.dumps(d,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)+'\n').encode());n.replace(p)
def git(*args,data=None):return subprocess.run(['git',*args],cwd=B,input=data,capture_output=True,check=True).stdout
def blobs(ref,paths):
 values={};p=subprocess.Popen(['git','cat-file','--batch'],cwd=B,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for path in sorted(paths):
  p.stdin.write((ref+':'+path+'\n').encode());p.stdin.flush();head=p.stdout.readline().split();assert len(head)==3 and head[1]==b'blob',path;n=int(head[2]);left=n;h=hashlib.sha256()
  while left:
   chunk=p.stdout.read(min(left,65536));assert chunk;left-=len(chunk);h.update(chunk)
  assert p.stdout.read(1)==b'\n';values[path]=[n,h.hexdigest()]
 p.stdin.close();assert p.wait(timeout=30)==0;return values
def checks():
 assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()==BRANCH
 for label in ['authority','development','document_tests','game2d']:assert read(P/'gates_v2'/(label+'.receipt.json'))['status']=='PASS',label
 assert read(P/'previous_w_remote_verified/RESULT.json')['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES'
 assert read(P/'previous_w_hosted_complete_v573/VERIFICATION.json')['status']=='EXACT_W_HOSTED_JOBS_COMPLETED_SUCCESS'
 reg=read(L/'ALL_ITEMS.json');assert reg['display_revision']=='V48' and len(reg['items'])==2047 and reg['counts']['inclusive_current_source_priorities']==950 and reg['counts']['unique_source_file_priorities']==661 and reg['counts']['unreviewed_current_source']==294
 assert read(T/'attempt03/DIRECT_REVIEW.json')['actual_ring_count']==7 and read(T/'attempt03/DIRECT_REVIEW.json')['whole_source_score']==4.5
 assert read(P/'comparison_a3/attempt01/DIRECT_REVIEW.json')['whole_component_score']==1.5 and read(P/'comparison_a4/attempt01/DIRECT_REVIEW.json')['whole_component_score']==0.8
 boundary=read(P/'PRODUCTION_BOUNDARY.json');assert len(boundary['members'])==783 and all(sha((B/x['path']).read_bytes())==x['sha256'] for x in boundary['members'])
def run(label,args):
 r=subprocess.run(args,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=1800);(OUT/(label+'.stdout.log')).write_bytes(r.stdout);(OUT/(label+'.stderr.log')).write_bytes(r.stderr);print(label,r.returncode,flush=True);assert r.returncode==0,r.stderr.decode(errors='replace')[-1000:]
phase=sys.argv[1];assert phase in ['--prepare','--seal','--publish']
if phase=='--prepare':
 assert git('rev-parse','HEAD').decode().strip()==BASE
 shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
 host=P/'previous_w_hosted_complete_v573';assert not host.exists();host.mkdir()
 for endpoint,name in [('actions/runs/37108271815','RUN.json'),('actions/runs/37108271815/jobs?per_page=100','JOBS.json')]:
  r=subprocess.run(['C:/Program Files/GitHub CLI/gh.exe','api','repos/Ebonyks/mermaid-roshan-reef/'+endpoint],cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW);(host/name).write_bytes(r.stdout);(host/(name+'.stderr.log')).write_bytes(r.stderr);assert r.returncode==0
 h=read(host/'RUN.json');jobs=read(host/'JOBS.json')['jobs'];assert h['head_sha']==BASE and h['status']=='completed' and h['conclusion']=='success' and jobs and all(j['status']=='completed' and j['conclusion']=='success' for j in jobs)
 write(host/'VERIFICATION.json',dict(status='EXACT_W_HOSTED_JOBS_COMPLETED_SUCCESS',checked_utc=now(),revision=BASE,run_id=h['id'],url=h['html_url'],job_count=len(jobs),jobs=[dict(name=j['name'],status=j['status'],conclusion=j['conclusion']) for j in jobs],steps_with_failed_conclusion=[dict(job=j['name'],step=s['name'],conclusion=s['conclusion']) for j in jobs for s in j.get('steps',[]) if s.get('conclusion')=='failure'],qualification='Actual exact-head completed hosted job statuses. Advisory failures, if any, remain explicit; machine success is not live visual, strict zero-2D, device/child/owner/all-job or new-revision acceptance.'))
 screenshot=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/SHARED_REVIEW_BROWSER_V572.jpg');assert screenshot.is_file();shutil.copyfile(screenshot,S/'BROWSER_REPORT_V572.jpg')
 write(S/'BROWSER_FINAL_VERIFY_V572.json',dict(status='FIXED_REPORT_DESKTOP_WRAP_AND_FILTERS_PASS',checked_utc=now(),url='http://127.0.0.1:8880/audit/job_shared_background_review_v1_20261003/index.html?revision=v48-fixed',native_sources=65,inclusive_priorities=53,context_images=6,filter_counts=[53,65],horizontal_overflow=False,viewport_width=1280,document_scroll_width=1265,screenshot_path=(S/'BROWSER_REPORT_V572.jpg').relative_to(B).as_posix(),screenshot_sha256=sha((S/'BROWSER_REPORT_V572.jpg').read_bytes()),library_original_toy_search=dict(query='D2X-0065',matches=1,current_original_score=3.0,replacement_link_present=True,horizontal_overflow=False),qualification='Actual desktop UI/report controls and source loading only. Initial overflow evidence preserved separately; no current game/device/child/owner acceptance.'))
 licenses=B/'ASSET_LICENSES.md';raw=licenses.read_bytes();path=(S/'BROWSER_REPORT_V572.jpg').relative_to(B).as_posix();assert ('| `'+path+'` |').encode() not in raw;raw+=('\n| `'+path+'` | Actual browser screenshot of the local shared source-review report | Original project review layout and inherited displayed artwork attribution | BROWSER_FINAL_VERIFY_V572.json records exact screenshot hash and observed UI state | QA proof only; no generated replacement/cinematic/gameplay pixels or owner acceptance. |\n').encode();n=licenses.with_name(licenses.name+'.v573_next');n.write_bytes(raw);n.replace(licenses)
 attrs=B/'.gitattributes';raw=attrs.read_bytes()
 paths=[S.relative_to(B).as_posix()+'/**',T.relative_to(B).as_posix()+'/**',MAP,SHARDS+'/**']+[('audit/job_artwork_refinement_live/'+x) for x in ['ALL_ITEMS_V46.original.json','all_items_V46.original.html','BOUNDARY_V46.original.json','ALL_ITEMS_V47.original.json','all_items_V47.original.html','BOUNDARY_V47.original.json']]
 for path in paths:
  line=(path+' -text').encode()
  if line not in raw:raw+=b'\n'+line+b'\n'
 n=attrs.with_name(attrs.name+'.v573_next');n.write_bytes(raw);n.replace(attrs)
 write(B/MAP,dict(status='PENDING_EXACT_SHARDED_REVIEW_SEAL',base_revision=BASE,qualification='Placeholder only; bounded dependency manifests will preserve the existing4MiB scanner ceiling.'))
 write(P/'PUBLICATION_BOUNDARY_V573.json',dict(status='PENDING_EXACT_STAGED_REVIEW_BYTE_SEAL'))
 d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for folder in [P,S,T] for p in folder.rglob('*') if p.is_file()}|{MAP,'.gitattributes'})
 for v in d['validation']:
  if 'Fresh authority' in v['command']:v.update(result='PASS',evidence='gates_v2/authority,development,document_tests,game2d.receipt.json: all exit0;52 document tests. 2D NO_REGRESSION only, debt remains UNSATISFIED.')
 d['validation'].append(dict(command='Exact W hosted jobs terminal status and repaired report browser verification',result='PASS',evidence='previous_w_hosted_complete_v573/VERIFICATION.json; shared BROWSER_FINAL_VERIFY_V572.json. Structural/UI success only, no source/action acceptance transfer.'));write(IP,d)
 print('PREPARED_EXACT_W_HOSTED_SUCCESS_AND_BOUNDED_PUBLICATION_SCOPE',len(d['files']),flush=True);sys.exit(0)
if phase=='--seal':
 checks();source=read(P/'PRODUCTION_BOUNDARY.json')['members'];tracked={x.decode() for x in git('ls-files','-z').split(b'\0') if x};published={x['path'] for x in source if x['path'] in tracked};aux=[x for x in source if x['path'] not in tracked];assert len(published)==543 and len(aux)==240 and all(x['path'].endswith('.gd.uid') for x in aux)
 bridge=[]
 for x in source:
  path=x['path'];raw=(B/path).read_bytes()
  if path in published:
   prior=git('show','HEAD:'+path);exact=raw==prior;normalized=not exact and prior==raw.replace(b'\r\n',b'\n');assert exact or normalized,path;bridge.append(dict(path=path,literal_sha256=sha(raw),published_sha256=sha(prior),exact_bytes=exact,whole_text_crlf_to_lf_only=normalized))
 write(P/'PUBLICATION_BOUNDARY_V573.json',dict(status='PASS_NO_PRODUCTION_DELTA_ALL783_LITERALS_UNCHANGED',checked_utc=now(),source_revision=BASE,published_members=543,auxiliary_uid_members=240,source_bridge=bridge,qualification='Review-only sources/QA/illustrated reports. Prior exact hosted success and82/82 local production checks remain bound to unchanged production; new review gates/hosted status and acceptance are independent.'))
 ips=[IP]+[B/'design/audit_impacts'/x for x in ['job-candy-local-far-fold-a3-20261003.json','job-candy-local-far-fold-a4-20261003.json','job-shared-background-source-review-20261003.json','job-playroom-painted-stacking-toy-20261003.json']]
 scope=set(read(IP)['files'])|{p.relative_to(B).as_posix() for p in ips};assert all((B/p).is_file() for p in scope)
 assert not any(p.startswith(('assets/','scripts/','.github/','.secrets/','.codex/','.claude/','.git/')) for p in scope)
 assert max(len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+p) for p in scope)<260
 staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=scope
 def stage(paths):
  raw=b''.join(p.encode()+b'\0' for p in sorted(paths));git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=raw);git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',data=raw)
 stage(scope-{MAP});changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope and not git('diff','--cached','--name-only','--diff-filter=D','-z')
 oldraw=git('show','HEAD:'+PRIOR);old=json.loads(oldraw);refs=(set(old['files'])|set(old['unchanged_required_files'])|{PRIOR})-changed-{MAP};unchanged=blobs('HEAD',refs)
 assert not any(p.startswith(('.secrets/','.git/','.codex/','.claude/')) for p in refs)
 shard_dir=B/SHARDS;assert not shard_dir.exists();shard_dir.mkdir(parents=True);desc=[];part={};estimate=250
 def emit(part):
  path=SHARDS+f'/PART_{len(desc)+1:03d}.json';write(B/path,dict(schema='reef.unchanged-review-dependency-shard.v1',base_revision=BASE,files=part),True);raw=(B/path).read_bytes();assert len(raw)<=900000;desc.append(dict(path=path,bytes=len(raw),sha256=sha(raw),entries=len(part)))
 for path,value in sorted(unchanged.items()):
  entry=len(json.dumps(path,ensure_ascii=False).encode())+len(json.dumps(value,separators=(',',':')).encode())+2
  if part and estimate+entry>899000:emit(part);part={};estimate=250
  part[path]=value;estimate+=entry
 if part:emit(part)
 assert sum(x['entries'] for x in desc)==len(unchanged)
 d=read(IP);d['files']=sorted(set(d['files'])|{x['path'] for x in desc});write(IP,d);scope|={x['path'] for x in desc};stage(scope-{MAP})
 changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};files=blobs('',changed-{MAP})
 assert not set(files)&set(unchanged)
 for path,value in files.items():
  if path.startswith(('assets_src/','audit/job_artwork_refinement_live/','audit/job_shared_background_review_v1_20261003/',SHARDS)):
   assert value==[(B/path).stat().st_size,sha((B/path).read_bytes())],path
 formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
 manifest=dict(schema='reef.immutable-review-supplement.sharded.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_dependency_shards=desc,shard_max_bytes=900000,qualification='V48 known2047 entries/950 source-cell-region priorities/661 unique source priorities/294 unreviewed primary sources. All65 omitted current primary sources and six exact joins reviewed;53 inclusive priorities/37 below4.5. Every164 A1-A4 native reference canvas and40 components scored;A3 1.5/A4 0.8 rejected. Three painted toy natives/21 components preserve6-ring A1/A2 failures4.1 and7-ring assembled A3 still4.5 provisional. Exact W23578 anonymous remote journal rows retained in12 lossless bounded shards and exact W hosted jobs successful. All783 production literal members unchanged; no protected original,3D,gate/security/workflow/finding lifecycle/production binding/integration/release or owner/device/child/all-job acceptance. Dependency manifests bounded; existing scanner ceiling unchanged.')
 write(B/MAP,manifest,True);assert (B/MAP).stat().st_size<4194304;git('add','-f','--',MAP);raw=git('show',':'+MAP);assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{MAP}
 write(B/'tmp/candy_shared_sealed_v573.json',dict(status='EXACT_SHARDED_REVIEW_BYTES_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=manifest['payload_sha256'],files=files,unchanged=unchanged,dependency_shards=desc,map_bytes=len(raw),checked_utc=now()));print('SEALED',len(files),'changed payloads',len(unchanged),'unchanged dependencies',len(desc),'bounded shards','root bytes',len(raw),flush=True);sys.exit(0)
checks();seal=read(B/'tmp/candy_shared_sealed_v573.json');assert seal['status']=='EXACT_SHARDED_REVIEW_BYTES_SEALED';raw=git('show',':'+MAP);assert sha(raw)==seal['map_sha256'];manifest=json.loads(raw);expected=dict(seal['files']);expected[MAP]=[len(raw),sha(raw)];assert blobs('',set(expected))==expected
assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(expected);OUT.mkdir(exist_ok=False);VERIFY.mkdir(exist_ok=False);shutil.copyfile(__file__,OUT/Path(__file__).name)
run('fetch',['git','fetch','origin',BRANCH,'dev']);assert git('rev-parse','origin/'+BRANCH).decode().strip()==BASE
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto']),('game2d',['tools/audit_game_2d.py','--regression-gate'])]:run('precommit_'+name,[PY,'-X','utf8','-B',*args])
message=OUT/'COMMIT_MESSAGE.txt';message.write_text('Review shared job artwork and reject Candy motion continuity failures\n\nIndividually inspect65 omitted shared originals and six unchanged-pixel context joins;53 inclusive priorities/37 below4.5. Preserve original sources and all current game bytes. Review every164 native A1-A4 motion canvas and40 components; new A3 1.5/A4 0.8 fail for extra hands and character distortion, no wrapper closure or release.\n\nReversibly regenerate only the named flat stacking toy after six-source reuse inventory. Preserve both six-ring failures4.1; the third seven-ring assembled native reaches static4.5 provisional, independent of all atlas/action/runtime acceptance. Show all three originals and21 component opinions. RegisterV48 retains2047 known items,950 source-cell-region priorities,661 unique source priorities,294 unreviewed primary sources.\n\nPreserve all23578 exact W anonymous remote verification rows in12 lossless bounded shards and actual successful exact-head hosted jobs. Keep document authority/findings/ledger facts synchronized without closing findings. Fix the observed review-page path overflow and retain browser proof. Preserve literal artifact bytes with scoped .gitattributes entries. Bound the new closed dependency manifests without raising the scanner ceiling.\n\nAll783 production members remain unchanged. Fresh structural gates and52 document tests pass;2D no-regression remains distinct from UNSATISFIED debt. No protected originals,3D,gate/security/workflow/production binding changes, blocked upload/status retry, owner/device/child/all-job acceptance, dev/master integration or release. Review checkpoint only.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(message)]);revision=git('rev-parse','HEAD').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==BASE;tree=git('rev-parse','HEAD^{tree}').decode().strip()
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto'])]:run('postcommit_'+name,[PY,'-X','utf8','-B',*args])
run('push',['git','push','origin','HEAD:refs/heads/'+BRANCH]);assert git('rev-parse','origin/'+BRANCH).decode().strip()==revision;write(OUT/'RECEIPT.json',dict(status='TOPIC_REVIEW_PUBLISHED_ANONYMOUS_BYTE_VERIFICATION_PENDING',revision=revision,tree=tree,map_path=MAP,map_sha256=seal['map_sha256'],checked_utc=now(),qualification='Review-only; no production/integration/release/owner acceptance.'));print('PUBLISHED',revision,flush=True)
url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/';started=now()
def fetch(path,value):
 for attempt in range(1,4):
  try:
   request=urllib.request.Request(url+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'MermaidReef-Anonymous-Review-QA'});h=hashlib.sha256();n=0
   with urllib.request.urlopen(request,timeout=60) as response:
    assert response.status==200
    while True:
     chunk=response.read(65536)
     if not chunk:break
     h.update(chunk);n+=len(chunk)
   return dict(path=path,bytes=n,sha256=h.hexdigest(),expected_bytes=value[0],expected_sha256=value[1],matches=[n,h.hexdigest()]==value,attempt=attempt,checked_utc=now(),status='FETCHED_ANONYMOUS_TLS_GET')
  except Exception as exc:
   if attempt==3:return dict(path=path,matches=False,error=str(exc),checked_utc=now(),status='FETCH_FAILED')
   time.sleep(attempt)
targets=dict(seal['files']);targets.update(seal['unchanged']);targets[MAP]=expected[MAP];failed=[];count=0
with (VERIFY/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for future in concurrent.futures.as_completed([pool.submit(fetch,p,v) for p,v in targets.items()]):
   row=future.result();journal.write(json.dumps(row)+'\n');journal.flush();count+=1
   if not row['matches']:failed.append(row)
   if count%500==0:print('ANONYMOUS_REMOTE_BYTES',count,'FAILURES',len(failed),flush=True)
result=dict(status='PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not failed else 'FAIL_PRESERVED',revision=revision,tree=tree,branch=BRANCH,entry_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+P.relative_to(B).as_posix()+'/index.html',library_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+L.relative_to(B).as_posix()+'/all_items.html',tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,manifest_url=url+MAP,map_sha256=seal['map_sha256'],payload_sha256=manifest['payload_sha256'],payload_files=len(manifest['files']),required_unchanged_files=len(seal['unchanged']),bounded_dependency_shards=len(manifest['unchanged_dependency_shards']),files_including_manifest=count,access_mode='Anonymous GET; normal TLS; no Authorization header',started_utc=started,finished_utc=now(),failed_files=failed,qualification='All closed review payload/reference bytes verified at exact immutable revision. New exact-head hosted CI, ordinary action/device/child/owner/all-job acceptance, integration and release remain separate.');write(VERIFY/'RESULT.json',result);print(json.dumps(result),flush=True);sys.exit(0 if not failed else 1)
