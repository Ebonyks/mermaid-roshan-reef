from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.parse,urllib.request
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
BASE='79f20126e01454132fe245fb3b8a03e700b9ca31';BRANCH='codex/job-art-review-v2-20261001';MAP='audit/job_review_v2_20261001/CANDY_LOCAL_WRAP_CONTINUITY_FILES_V20.json';PRIOR='audit/job_review_v2_20261001/CANDY_WRAPPER_AND_FOSSIL_REVEAL_FILES_V19.json'
OUT=B/'tmp/candy_local_publish_v558';VERIFY=B/'tmp/candy_local_remote_v558';PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda raw:hashlib.sha256(raw).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d,compact=False):
 n=p.with_name(p.name+'.v558_next');n.write_bytes((json.dumps(d,ensure_ascii=False,indent=None if compact else 2,separators=(',',':') if compact else None)+'\n').encode());n.replace(p)
def git(*args,data=None):return subprocess.run(['git',*args],cwd=B,input=data,capture_output=True,check=True).stdout
def blobs(ref,paths):
 values={};p=subprocess.Popen(['git','cat-file','--batch'],cwd=B,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for path in sorted(paths):
  p.stdin.write((ref+':'+path+'\n').encode());p.stdin.flush();head=p.stdout.readline().split();assert len(head)==3 and head[1]==b'blob',path
  n=int(head[2]);left=n;h=hashlib.sha256()
  while left:
   chunk=p.stdout.read(min(left,65536));assert chunk;left-=len(chunk);h.update(chunk)
  assert p.stdout.read(1)==b'\n';values[path]=[n,h.hexdigest()]
 p.stdin.close();assert p.wait(timeout=30)==0;return values
def checks():
 for label in ['authority','development','document_tests','game2d']:assert read(P/'gates_v1'/(label+'.receipt.json'))['status']=='PASS',label
 assert read(P/'previous_v_hosted_complete/VERIFICATION.json')['status']=='PREVIOUS_V_EXACT_HOSTED_JOBS_COMPLETED_SUCCESS'
 assert read(P/'previous_v_remote_verified/RESULT.json')['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES'
 assert read(P/'attempt01/DIRECT_REVIEW.json')['whole_reference_action_score']==2.4 and read(P/'comparison_a2/attempt01/DIRECT_REVIEW.json')['whole_component_score']==1.8
 reg=read(B/'audit/job_artwork_refinement_live/ALL_ITEMS.json');assert len(reg['items'])==2044 and reg['counts']['inclusive_current_source_priorities']==894
 source=read(P/'PRODUCTION_BOUNDARY.json')['members'];assert len(source)==783 and all(sha((B/x['path']).read_bytes())==x['sha256'] for x in source)
 ci=read(B/'audit/job_candy_workflow_current_v1_20261003/full_ci_v1/RECEIPT.json');assert ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
 assert len(read(B/'assets_src/imagegen/candy_wrap_contact_v1_20261003/COMPLETE_SOURCE_REVIEW.json')['sources'])==13
 assert read(B/'assets_src/imagegen/nursery_palm_attention_v1_20261002/REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
def run(label,args):
 p=subprocess.run(args,cwd=B,capture_output=True,timeout=1800,creationflags=subprocess.CREATE_NO_WINDOW);(OUT/(label+'.stdout.log')).write_bytes(p.stdout);(OUT/(label+'.stderr.log')).write_bytes(p.stderr);print(label,p.returncode,flush=True);assert p.returncode==0,p.stderr.decode(errors='replace')[-1000:]
if sys.argv[1:]==['--prepare']:
 assert git('rev-parse','HEAD').decode().strip()==BASE;target=P/'review_tools'/Path(__file__).name;shutil.copyfile(__file__,target)
 attrs=B/'.gitattributes';raw=attrs.read_bytes()
 for path in [MAP,'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json','audit/job_artwork_refinement_live/ALL_ITEMS_V45.original.json','audit/job_artwork_refinement_live/all_items_V45.original.html','audit/job_artwork_refinement_live/BOUNDARY_V45.original.json']:
  line=(path+' -text').encode()
  if line not in raw:raw+=b'\n'+line+b'\n'
 n=attrs.with_name(attrs.name+'.v558_next');n.write_bytes(raw);n.replace(attrs)
 write(B/MAP,dict(status='PENDING_EXACT_REVIEW_BYTE_SEAL',base_revision=BASE,qualification='Placeholder only; no published/current-remote claim.'))
 write(P/'PUBLICATION_BOUNDARY_V558.json',dict(status='PENDING_STAGED_REVIEW_BYTES_AND_UNCHANGED_PRODUCTION_CHECK'))
 d=read(IP);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()}|{target.relative_to(B).as_posix(),MAP,(P/'PUBLICATION_BOUNDARY_V558.json').relative_to(B).as_posix(),'.gitattributes'});write(IP,d);print('New review-only publication scope prepared.');sys.exit(0)
if sys.argv[1:]==['--seal']:
 assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()==BRANCH;checks()
 source=read(P/'PRODUCTION_BOUNDARY.json')['members'];tracked={x.decode() for x in git('ls-files','-z').split(b'\0') if x};published={x['path'] for x in source if x['path'] in tracked};aux=[x for x in source if x['path'] not in tracked];assert len(published)==543 and len(aux)==240 and all(x['path'].endswith('.gd.uid') for x in aux)
 pv=blobs('HEAD',published);bridge=[]
 for x in source:
  path=x['path'];raw=(B/path).read_bytes()
  if path in published:
   prior=git('show','HEAD:'+path);exact=raw==prior;normalized=not exact and prior==raw.replace(b'\r\n',b'\n');assert exact or normalized,path;bridge.append(dict(path=path,literal_sha256=sha(raw),published_sha256=sha(prior),exact_bytes=exact,whole_text_crlf_to_lf_only=normalized))
 write(P/'PUBLICATION_BOUNDARY_V558.json',dict(status='PASS_NO_PRODUCTION_DELTA_FROM_V_ALL783_LITERALS_UNCHANGED',checked_utc=now(),revision_source_members=543,auxiliary_generated_uid_members=240,source_bridge=bridge,qualification='Source-only local reference and audit/library changes. Exact prior V hosted/local82/82 applies only to unchanged production; new review gates and hosted status remain separate.'))
 d=read(IP);scope=set(d['files'])|{IP.relative_to(B).as_posix()};assert all((B/x).is_file() for x in scope)
 assert not any(x.startswith(('assets/','scripts/','.github/','.secrets/','.codex/','.claude/','.git/')) for x in scope)
 assert max(len('D:/a/mermaid-roshan-reef/mermaid-roshan-reef/'+x) for x in scope)<260
 staged={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert staged<=scope
 paths=b''.join(x.encode()+b'\0' for x in sorted(scope-{MAP}));git('add','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths);git('add','--renormalize','-f','--pathspec-from-file=-','--pathspec-file-nul',data=paths)
 changed={x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x};assert changed<=scope and not git('diff','--cached','--name-only','--diff-filter=D','-z');files=blobs('',changed-{MAP})
 for path,value in files.items():
  if path.startswith(('assets_src/','audit/job_artwork_refinement_live/')) or path in [IP.relative_to(B).as_posix()]:assert value==[(B/path).stat().st_size,sha((B/path).read_bytes())],path
 oldraw=git('show','HEAD:'+PRIOR);old=json.loads(oldraw);refs=(set(old['files'])|set(old['unchanged_required_files'])|{PRIOR})-set(files)-{MAP}
 assert not any(x.startswith(('.secrets/','.git/','.codex/','.claude/')) for x in refs);unchanged=blobs('HEAD',refs);formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(files.items())).encode()
 manifest=dict(schema='reef.immutable-review-supplement.v1',base_revision=BASE,prior_closed_map=PRIOR,prior_closed_map_sha256=sha(oldraw),required_files=len(files),required_payload_bytes=sum(v[0] for v in files.values()),payload_sha256=sha(formula),payload_hash_formula='SHA256 UTF8 sorted path TAB bytes TAB SHA256 LF',files=files,required_unchanged_files=len(unchanged),unchanged_required_files=unchanged,archived_prior_paths=[],qualification='V46 known2044 entries,894 source-cell-region priorities,605 unique source priorities,359 pending sources. Every82 local A1/A2 native canvases,14 original-size boards,six details and20 component opinions reviewed: whole wrapping2.4/far-fold1.8 rejected. Three new complete ImageGen contact poses; A11 far-start4.5/near-role4.0; A12 grip4.3 rejected; A13 partial-fold4.5/exact coverage4.2. All13 contact natives/43 authored states reviewed;55 Candy states including12 wrapper states. No source-score transfer or source-frame census inflation. All783 current production literal members unchanged; prior V exact hosted success and local82/82 apply only to identical production. Preserve all23323 previous anonymous remote byte rows in12 bounded lossless shards and all prior failures. No production binding, protected originals, 3D, gate/security/workflow changes, upload/status rejection retry, finding closure, owner/device/child/all-job acceptance, dev/master integration or release.')
 write(B/MAP,manifest,True);assert (B/MAP).stat().st_size<4194304;git('add','-f','--',MAP);raw=git('show',':'+MAP);assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(files)|{MAP}
 write(B/'tmp/candy_local_sealed_v558.json',dict(status='EXACT_SOURCE_ONLY_CANDY_LOCAL_REVIEW_SEALED',base_revision=BASE,map_path=MAP,map_sha256=sha(raw),payload_sha256=manifest['payload_sha256'],files=files,map_bytes=len(raw),unchanged=len(unchanged),checked_utc=now()));print('SEALED',len(files),'payload files',len(unchanged),'unchanged dependencies','map bytes',len(raw),flush=True);sys.exit(0)
assert sys.argv[1:]==['--publish'];assert git('rev-parse','HEAD').decode().strip()==BASE;checks();seal=read(B/'tmp/candy_local_sealed_v558.json');assert seal['status']=='EXACT_SOURCE_ONLY_CANDY_LOCAL_REVIEW_SEALED';raw=git('show',':'+MAP);assert sha(raw)==seal['map_sha256'];manifest=json.loads(raw);expected=dict(seal['files']);expected[MAP]=[len(raw),sha(raw)]
assert blobs('',set(expected))==expected;assert {x.decode() for x in git('diff','--cached','--name-only','-z').split(b'\0') if x}==set(expected);OUT.mkdir(exist_ok=False);VERIFY.mkdir(exist_ok=False);shutil.copyfile(__file__,OUT/Path(__file__).name)
run('fetch',['git','fetch','origin',BRANCH]);assert git('rev-parse','origin/'+BRANCH).decode().strip()==BASE
for prefix in ['precommit']:
 for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto']),('game2d',['tools/audit_game_2d.py','--regression-gate'])]:run(prefix+'_'+name,[PY,'-X','utf8','-B',*args])
message=OUT/'COMMIT_MESSAGE.txt';message.write_text('Review Candy golden-paper hand motion and regenerate fold sources\n\nInspect every82 native Comfy reference canvas,14 original-size boards,six details and20 components. Whole wrapping2.4 and far-edge fold1.8 remain rejected: the sweet is never covered. Preserve exact inputs/prompts/workflow/model/native outputs and all failed helper/preview evidence.\n\nGenerate three complete reversible ImageGen poses. Preserve near-role and free-edge grip failures; A13 partial fold reaches source-only4.5 while exact coverage4.2 remains weak. Review every13 contact original and43 authored states, plus12 wrapper states. Extend the illustrated register to2044 items with894 inclusive source priorities,605 unique source priorities and359 source reviews pending. No motion frames inflate source census.\n\nAll783 production members remain unchanged. Preserve previous V exact hosted success and every23323 anonymous remote verification row in12 lossless bounded shards. Keep current runtime WRAP2.8 and whole4.1 contact study separate from new static-source opinions. New review gates pass; strict zero-2D, ordinary action, all jobs, device, child, owner and final report acceptance remain open.\n\nNo production binding, protected original, 3D, security/workflow/gate or finding lifecycle change. Publish a reversible topic review checkpoint only, with full immutable anonymous byte verification; no dev/master integration or release.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(message)]);revision=git('rev-parse','HEAD').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==BASE;tree=git('rev-parse','HEAD^{tree}').decode().strip()
# The commit preserves the fully checked staged bytes. Recheck Git-range coverage;
# repeat no unchanged inventory scan. The fresh precommit inventory still gates push.
for name,args in [('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto'])]:run('postcommit_'+name,[PY,'-X','utf8','-B',*args])
run('push',['git','push','origin','HEAD:refs/heads/'+BRANCH]);assert git('rev-parse','origin/'+BRANCH).decode().strip()==revision;write(OUT/'RECEIPT.json',dict(status='TOPIC_REVIEW_PUBLISHED_ANONYMOUS_BYTE_VERIFICATION_PENDING',revision=revision,tree=tree,map_path=MAP,map_sha256=seal['map_sha256'],checked_utc=now(),qualification='Review-only, no production/integration/release/owner acceptance.'));print('PUBLISHED',revision,flush=True)
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
targets=dict(manifest['files']);targets.update(manifest['unchanged_required_files']);targets[MAP]=expected[MAP];fail=[];count=0
with (VERIFY/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for future in concurrent.futures.as_completed([pool.submit(fetch,p,v) for p,v in targets.items()]):
   row=future.result();journal.write(json.dumps(row)+'\n');journal.flush();count+=1
   if not row['matches']:fail.append(row)
   if count%500==0:print('ANONYMOUS_REMOTE_BYTES',count,'FAILURES',len(fail),flush=True)
result=dict(status='PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED',revision=revision,tree=tree,branch=BRANCH,entry_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/'+P.relative_to(B).as_posix()+'/index.html',library_url='https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_artwork_refinement_live/all_items.html',tree_url='https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,manifest_url=url+MAP,map_sha256=seal['map_sha256'],payload_sha256=manifest['payload_sha256'],payload_files=len(manifest['files']),required_unchanged_files=len(manifest['unchanged_required_files']),files_including_manifest=count,access_mode='Anonymous GET; normal TLS; no Authorization header',started_utc=started,finished_utc=now(),failed_files=fail,qualification='All closed review payload/reference bytes verified. New exact-head hosted CI, all action/device/child/owner/all-job acceptance, integration and release remain separate.');write(VERIFY/'RESULT.json',result);print(json.dumps(result),flush=True);sys.exit(0 if not fail else 1)
