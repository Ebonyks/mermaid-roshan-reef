from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,time,urllib.parse,urllib.request
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');c=b/'audit/job_candy_workflow_current_v1_20261003';branch='codex/job-art-review-v2-20261001'
out=b/'tmp/candy_review_v_publish_v538';verify=b/'tmp/candy_review_v_remote_v538';py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';gh='C:/Program Files/GitHub CLI/gh.exe'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda raw:hashlib.sha256(raw).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):return subprocess.run(['git',*args],cwd=b,capture_output=True,check=True).stdout
def run(label,args,timeout=1800):
 p=subprocess.run(args,cwd=b,capture_output=True,timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(label+'.stdout.log')).write_bytes(p.stdout);(out/(label+'.stderr.log')).write_bytes(p.stderr)
 print(label,p.returncode,flush=True);assert p.returncode==0,p.stderr.decode(errors='replace')[-1500:];return p.stdout
# All blocking checks precede any commit or push; preserve an uncertain publication.
seal=read(b/'tmp/candy_review_v_sealed_v537.json');assert seal['status']=='EXACT_SCOPED_CANDY_V_BLOBS_SEALED'
assert git('rev-parse','HEAD').decode().strip()==seal['base_revision'] and git('branch','--show-current').decode().strip()==branch
ci=read(c/'full_ci_v1/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results']) and ci['source_unchanged']
assert len(ci['source_checks'])==783 and all(sha((b/x['path']).read_bytes())==x['before_sha256'] for x in ci['source_checks'])
bridge=read(c/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V537.json');assert bridge['status']=='PASS_ALL783_PUBLICATION_BOUNDARY_MEMBERS' and bridge['revision_source_members']==543 and bridge['auxiliary_generated_uid_members']==240
for label in ['authority','development','document_tests','game2d']:assert read(b/'audit/job_shared_entrance_sources_v1_20261003/gates_v1'/(label+'.receipt.json'))['status']=='PASS'
assert read(b/'assets_src/imagegen/nursery_palm_attention_v1_20261002/REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
reg=read(b/'audit/job_artwork_refinement_live/ALL_ITEMS.json');assert len(reg['items'])==2038 and reg['counts']['inclusive_current_source_priorities']==888
mp=seal['map_path'];raw=git('show',':'+mp);assert sha(raw)==seal['map_sha256'];manifest=json.loads(raw)
expected=dict(manifest['files']);expected[mp]=[len(raw),sha(raw)]
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(expected)
assert {p for p in expected if p.startswith('scripts/')}=={'scripts/opera_career_world_2d.gd'}
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=b,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for path in sorted(expected):
 proc.stdin.write((':'+path+'\n').encode());proc.stdin.flush();head=proc.stdout.readline().split();assert head[1]==b'blob',path
 n=int(head[2]);left=n;h=hashlib.sha256()
 while left:
  chunk=proc.stdout.read(min(left,65536));assert chunk;left-=len(chunk);h.update(chunk)
 assert proc.stdout.read(1)==b'\n' and [n,h.hexdigest()]==expected[path],path
proc.stdin.close();assert proc.wait(timeout=30)==0
out.mkdir(exist_ok=False);verify.mkdir(exist_ok=False);shutil.copyfile(__file__,out/Path(__file__).name)
run('fetch',['git','fetch','origin',branch])
assert git('rev-parse','origin/'+branch).decode().strip()==seal['base_revision'],'Remote topic advanced; reconcile before committing.'
for label,args in [('precommit_authority',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('precommit_development',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('precommit_game2d',[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'])]:run(label,args)
hosted=json.loads(subprocess.check_output([gh,'run','view','37093610815','--json','status,conclusion,headSha,url,jobs'],cwd=b));assert hosted['headSha']==seal['base_revision'] and hosted['status']=='completed' and hosted['conclusion']=='success';hosted['checked_utc']=now();hosted['qualification']='Previous U exact hosted SUCCESS only; it does not cover the new Candy production repair.';write(out/'HOSTED_U_FINAL.json',hosted)
message=out/'COMMIT_MESSAGE.txt';message.write_text('Audit Candy contact, fossil continuity and shared entrance sources\n\nRepair four missing birthday physical-station bindings with existing painted invitation art in one shared 2D world source. Capture real Kitchen training and birthday workflows at1280/1600, including626 consecutive wrapping/glaze canvases and64 selected views. Record48 individual mounted/action opinions; current wrapping2.8, glazing2.6 and incorrect cake berry placement/accounting remain priorities. No new wrapping art is bound to production.\n\nPreserve three golden-wrapper and ten connected-hand native ImageGen sources, their exact prompts, references, hashes and52 individual state opinions. Actual unbound contact study reviews every412 captured canvas,32 views,42 boards and22 native details: static contact4.5-4.6, complete action4.1 rejected. Latest bridge sources4.1/4.1/4.2 improve release and loose pleats but still fail conserved candy size and sliding contact. Preserve all failures and revise the refreshable illustrated library history. V45 directly reviews18 unchanged shared Kitchen/Opera entrance natives and104 authored prop cells with122 written opinions:17 source and99 cell inclusive priorities. Current V2/V4 manifests independently match all13 atlases; two stale historical ownership hashes and the failed preparation are retained. No original source pixels or production binding change from this additional review. The library now has2038 items,888 source/cell/region priorities,602 unique source priorities and359 source reviews outstanding. Withhold old Geologist/Nursery current mounted claims after the shared source changes.\n\nAlso retain the separate reversible fossil reveal/home study, every437 frame,58 views,48 boards,20 native details and13 opinions; whole3.8 remains unbound. Preserve all20087 rows of prior U anonymous remote verification in bounded lossless shards and its exact hosted SUCCESS. Fresh official4.7.2 unmodified full suite passes82/82 with all783 frozen literal source hashes preserved; publication bridge proves543 revision members and240 auxiliary generated UIDs. Existing structural and2D no-regression gates pass; raw engine diagnostics remain explicit.\n\nNo protected art, 3D, security/workflow/gate change, rejected upload/browser-status retry, finding lifecycle closure, all-job/device/child/owner approval, dev/master integration or release. Publish a review checkpoint only; anonymously verify every closed-map byte at the immutable revision.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(message)])
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
for label,args in [('postcommit_authority',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('postcommit_development',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('postcommit_game2d',[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'])]:run(label,args)
run('push',['git','push','origin','HEAD:refs/heads/'+branch])
assert git('rev-parse','origin/'+branch).decode().strip()==revision
pub={'status':'TOPIC_REVIEW_PUBLISHED_REMOTE_BYTE_VERIFICATION_PENDING','revision':revision,'tree':tree,'branch':branch,'map_path':mp,'map_sha256':seal['map_sha256'],'payload_sha256':manifest['payload_sha256'],'payload_files':len(manifest['files']),'payload_bytes':manifest['required_payload_bytes'],'checked_utc':now(),'qualification':'Durable review checkpoint only. One station-binding repair; all wrapper/contact and fossil sources/studies remain unbound. Current whole WRAP2.8 and candidate4.1 do not meet4.5. Full hosted new-head, visual/device/child/owner/all-job/integration/release remain separate.'};write(out/'RECEIPT.json',pub);print('PUBLISHED_CANDY_REVIEW_TOPIC_REVISION',revision,flush=True)
prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/';started=now()
def fetch(path,value,return_raw=False):
 for attempt in range(1,4):
  try:
   request=urllib.request.Request(prefix+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'MermaidReef-Anonymous-Review-QA'})
   h=hashlib.sha256();n=0;parts=[]
   with urllib.request.urlopen(request,timeout=60) as response:
    assert response.status==200
    while True:
     chunk=response.read(65536)
     if not chunk:break
     h.update(chunk);n+=len(chunk)
     if return_raw:parts.append(chunk)
   return {'path':path,'bytes':n,'sha256':h.hexdigest(),'attempt':attempt,'status':'FETCHED_ANONYMOUS_TLS_GET','expected_bytes':value[0],'expected_sha256':value[1],'matches':[n,h.hexdigest()]==value,'checked_utc':now()},b''.join(parts) if return_raw else None
  except Exception as exc:
   if attempt==3:return {'path':path,'status':'FETCH_FAILED','error':str(exc),'expected_bytes':value[0],'expected_sha256':value[1],'matches':False,'checked_utc':now()},None
   time.sleep(attempt)
map_row,map_raw=fetch(mp,expected[mp],True);assert map_row['matches'] and json.loads(map_raw)==manifest
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(manifest['files'].items())).encode();assert sha(formula)==manifest['payload_sha256']
targets=dict(manifest['files']);targets.update(manifest['unchanged_required_files']);rows=[];fail=[]
with (verify/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for future in concurrent.futures.as_completed([pool.submit(fetch,p,v) for p,v in targets.items()]):
   row,_=future.result();journal.write(json.dumps(row)+'\n');journal.flush();rows.append(row)
   if not row['matches']:fail.append(row)
   if len(rows)%250==0:print('REMOTE_BYTES_VERIFIED',len(rows),'FAILURES',len(fail),flush=True)
 journal.write(json.dumps(map_row)+'\n')
result={'status':'PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED','revision':revision,'tree':tree,'branch':branch,'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_artwork_refinement_live/all_items.html','tree_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,'manifest_url':prefix+mp,'map_sha256':seal['map_sha256'],'payload_sha256':manifest['payload_sha256'],'payload_files':len(manifest['files']),'required_unchanged_files':len(manifest['unchanged_required_files']),'files_including_manifest':len(rows)+1,'payload_bytes':manifest['required_payload_bytes'],'access_mode':'Anonymous GET, normal TLS certificate verification, no Authorization header','started_utc':started,'finished_utc':now(),'failed_files':fail,'local_ci_members':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'qualification':'Every required immutable topic payload/reference byte checked. Publication only; new exact-head hosted, visual/action/device/child/owner/all-job/integration/release remain separate. No reference-upload or browser persistence approval claim.'};write(verify/'RESULT.json',result);print(json.dumps(result),flush=True);raise SystemExit(0 if not fail else 1)
