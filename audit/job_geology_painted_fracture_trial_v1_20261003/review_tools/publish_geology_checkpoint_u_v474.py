from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.request,urllib.parse
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=R/'tmp/geology_review_u_publish_v474';out.mkdir(exist_ok=False)
verify=R/'tmp/geology_review_u_remote_v474';verify.mkdir(exist_ok=False)
F=R/'audit/job_nursery_wash_connected_v1_20261002';branch='codex/job-art-review-v2-20261001'
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):return subprocess.run(['git',*args],cwd=R,capture_output=True,check=True).stdout
def run(label,args,timeout=600):
 p=subprocess.run(args,cwd=R,capture_output=True,timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/(label+'.stdout.log')).write_bytes(p.stdout);(out/(label+'.stderr.log')).write_bytes(p.stderr)
 print(label,p.returncode,flush=True)
 assert p.returncode==0,p.stderr.decode(errors='replace')[-1200:]
 return p.stdout
shutil.copyfile(Path(__file__),out/Path(__file__).name)
seal=read(R/'tmp/geology_review_u_sealed_v473.json')
assert seal['status']=='EXACT_SCOPED_GEOLOGY_U_BLOBS_SEALED'
assert git('rev-parse','HEAD').decode().strip()==seal['base_revision'] and git('branch','--show-current').decode().strip()==branch
mp=seal['map_path'];raw=git('show',':'+mp);assert sha(raw)==seal['map_sha256'];m=json.loads(raw)
expected=dict(m['files']);expected[mp]=[len(raw),sha(raw)]
assert {p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==set(expected)|set(m['archived_prior_paths'])
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for path in sorted(expected):
 proc.stdin.write((':'+path+'\n').encode());proc.stdin.flush();header=proc.stdout.readline().split();assert header[1]==b'blob',path
 n=int(header[2]);left=n;digest=hashlib.sha256()
 while left:
  chunk=proc.stdout.read(min(left,65536));assert chunk;left-=len(chunk);digest.update(chunk)
 assert proc.stdout.read(1)==b'\n' and [n,digest.hexdigest()]==expected[path],path
proc.stdin.close();assert proc.wait(timeout=30)==0
ci=read(F/'full_ci_v1/RECEIPT.json');assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['overall_process_exit']==0 and len(ci['probe_results'])==82 and all(r['process_exit']==0 for r in ci['probe_results'])
assert len(ci['source_checks'])==783 and all(sha((R/r['path']).read_bytes())==r['before_sha256'] for r in ci['source_checks'])
bridge=read(F/'PUBLICATION_SOURCE_NEWLINE_BRIDGE_V381.json');assert bridge['status']=='PASS_ALL783_PUBLICATION_BOUNDARY_MEMBERS' and bridge['revision_source_members']==543 and bridge['auxiliary_generated_uid_members']==240
assert read(R/'assets_src/imagegen/nursery_palm_attention_v1_20261002/REFERENCE_UPLOAD_BLOCK.json')['reference_uploaded'] is False
J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'
for label in ('game2d','authority','development','document_tests'):assert read(J/'gates'/(label+'.receipt.json'))['status']=='PASS',label
for attempt in (1,2):
 cr=read(J/f'DIRECT_REVIEW_ATTEMPT0{attempt}.json');assert cr['consecutive_frames']==(433 if attempt==1 else 435) and cr['selected_views']==58 and len(cr['opinions'])==12 and cr['production_binding'] is False
 assert all(x['direct_review'] for x in read(J/f'QA_BOARD_MANIFEST_A{attempt}.json')['boards'])
assert len(read(R/'audit/job_artwork_refinement_live/ALL_ITEMS.json')['items'])==1821
run('fetch',['git','fetch','origin',branch])
assert git('rev-parse','origin/'+branch).decode().strip()==seal['base_revision'],'Topic advanced remotely; reconcile before publication.'
msg=out/'COMMIT_MESSAGE.txt';msg.write_text('Record reversible painted fossil fracture trials and complete individual review\n\nReuse the unchanged1024-square painted ammonite source rather than regenerate suitable artwork. In a non-runtime inherited geology surface, partition its original atlas into three complementary irregular textured Canvas polygons with conserved UVs, mechanics and touch margins. Preserve exact A1 draw/capture fixtures before adding A2 restrained plum exposed-edge contours, bounded by read-only original alpha and suppressed after neighboring snaps. All production files remain unchanged.\n\nCapture actual intentional Library four-phase route, earned return and separate Opera elevator replay/Back at1280/1600 for each trial. Directly inspect every868 consecutive native input/wait frame (864 fossil and4 next-phase endpoints),116 selected canvases,94 full-aspect ordered boards and40 original native details. Record24 individual source/material/object/contact/transition/action opinions. A1 exposed cuts4.4 rejected; A2 fragments and join4.5 provisional, whole3.6 remains weak. Current production fossil3.2/pan3.4/contact2.7/room2.8 remain separate; the rooted geode opening is unchanged.\n\nAppend candidate history to illustrated registerV41 without changing1821 items, current source/mounted/action scores or priority counts. Preserve exact V40 register/page/boundary. Display both trials, all frames, opinions, original texture/fixtures/proof and failures. All783 production hashes unchanged. Preserve every18803 prior T anonymous remote journal row in10 bounded lossless shards, exact revision receipt and hosted snapshot.\n\nBoth trials pass parser/inference/officialGodot4.7.2 analyzers and fresh actual-input captures at both widths. Existing unchanged authority/coverage/52 document tests/2D no-regression and postcommit gates remain required; machine results do not pass graphics or strict-zero2D debt. Preserve pre-capture runner and report helper errors plus bounded corrections; no gate waiver. Topic publication waits for exact parent T hosted success and anonymously byte-verifies every new/unchanged closed-map dependency.\n\nNo runtime/protected original/source bitmap/security/workflow change, rejected reference upload/browser-persistence retry, owner approval, finding lifecycle closure, complete all-job/device/child acceptance, dev/master integration or release.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(msg)],1800)
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
for label,args in [('game2d',[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate']),('authority',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:run(label,args,1800 if label=='game2d' else 600)
# A new topic push must not cancel the still-running exact R validation.
gh='C:/Program Files/GitHub CLI/gh.exe'
deadline=time.monotonic()+3600
while True:
 hosted=json.loads(subprocess.check_output([gh,'run','view','37090563245','--json','status,conclusion,headSha,url,jobs'],cwd=R))
 assert hosted['headSha']==seal['base_revision']
 if hosted['status']=='completed':
  hosted['captured_utc']=now();hosted['qualification']='Exact parent T hosted completion; separate from new U machine/visual/device/child/owner acceptance. Any failed/advisory result remains literal and unwaived.';write(out/'HOSTED_T_FINAL.json',hosted)
  assert hosted['conclusion']=='success';print('EXACT_PARENT_T_HOSTED_FINAL',hosted['conclusion'],flush=True);break
 assert time.monotonic()<deadline,'Exact parent T hosted suite remains active; no cancelling push made.'
 print('WAITING_EXACT_PARENT_T_HOSTED_COMPLETION_NO_CANCEL',now(),flush=True)
 time.sleep(45)
run('push',['git','push','origin','HEAD:refs/heads/'+branch],1800)
assert git('rev-parse','origin/'+branch).decode().strip()==revision
pub={'status':'TOPIC_CANDIDATE_PUBLISHED_REMOTE_VERIFICATION_PENDING','revision':revision,'tree':tree,'branch':branch,'map_path':mp,'map_sha256':seal['map_sha256'],'payload_sha256':m['payload_sha256'],'payload_files':m['required_files'],'payload_bytes':m['required_payload_bytes'],'local_ci_members':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'checked_utc':now(),'qualification':'Durable dual fossil-fracture review checkpoint only. All783 production bytes unchanged. A1 fragment4.4 rejected;A2 fragments/join4.5 provisional,whole3.6 weak. Current fossil3.2/pan3.4/contact2.7/room2.8 remain independent. Complete all-job/device/child/owner/integration/release and both exact rejected upload/browser-status actions remain open.'};write(out/'RECEIPT.json',pub)
print('PUBLISHED_GEOLOGY_REVIEW_TOPIC_REVISION',revision,flush=True)
prefix='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+revision+'/'
started=now()
def fetch(path,expected_value,return_raw=False):
 for attempt in range(1,4):
  try:
   request=urllib.request.Request(prefix+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'MermaidReef-Anonymous-Review-QA'})
   digest=hashlib.sha256();size=0;parts=[]
   with urllib.request.urlopen(request,timeout=60) as response:
    assert response.status==200
    while True:
     chunk=response.read(65536)
     if not chunk:break
     digest.update(chunk);size+=len(chunk)
     if return_raw:parts.append(chunk)
   row={'path':path,'bytes':size,'sha256':digest.hexdigest(),'attempt':attempt,'status':'FETCHED_ANONYMOUS_TLS_GET','expected_bytes':expected_value[0],'expected_sha256':expected_value[1],'matches':[size,digest.hexdigest()]==expected_value,'checked_utc':now()}
   return row,b''.join(parts) if return_raw else None
  except Exception as exc:
   if attempt==3:return {'path':path,'status':'FETCH_FAILED','error':str(exc),'expected_bytes':expected_value[0],'expected_sha256':expected_value[1],'matches':False,'checked_utc':now()},None
   time.sleep(attempt)
map_row,map_raw=fetch(mp,expected[mp],True);assert map_row['matches'] and json.loads(map_raw)==m
formula=''.join(p+'\t'+str(v[0])+'\t'+v[1]+'\n' for p,v in sorted(m['files'].items())).encode();assert sha(formula)==m['payload_sha256']
targets=dict(m['files']);targets.update(m.get('unchanged_required_files',{}));rows=[];fail=[]
with (verify/'VERIFICATION_JOURNAL.jsonl').open('w',encoding='utf-8',newline='\n') as journal:
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for future in concurrent.futures.as_completed([pool.submit(fetch,p,v) for p,v in targets.items()]):
   row,_=future.result();journal.write(json.dumps(row)+'\n');journal.flush();rows.append(row)
   if not row['matches']:fail.append(row)
   if len(rows)%250==0:print('REMOTE_BYTES_VERIFIED',len(rows),'FAILURES',len(fail),flush=True)
 journal.write(json.dumps(map_row)+'\n')
result={'status':'PASS_ALL_ANONYMOUS_REMOTE_BYTES' if not fail else 'FAIL_PRESERVED','revision':revision,'tree':tree,'branch':branch,'entry_url':'https://github.com/Ebonyks/mermaid-roshan-reef/blob/'+revision+'/audit/job_artwork_refinement_live/all_items.html','tree_url':'https://github.com/Ebonyks/mermaid-roshan-reef/tree/'+revision,'manifest_url':prefix+mp,'map_sha256':pub['map_sha256'],'payload_sha256':m['payload_sha256'],'payload_files':len(m['files']),'required_unchanged_files':len(m.get('unchanged_required_files',{})),'files_including_manifest':len(rows)+1,'payload_bytes':sum(v[0] for v in m['files'].values()),'access_mode':'Anonymous GET, normal TLS certificate verification, no Authorization header','started_utc':started,'finished_utc':now(),'failed_files':fail,'local_ci_members':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'qualification':'Every required immutable topic payload/reference byte checked. Publication evidence only; local/hosted/visual/action/device/child/owner/all-job/integration/release remain separate. No imagegen reference upload authorization.'}
write(verify/'RESULT.json',result);print(json.dumps(result),flush=True);raise SystemExit(0 if not fail else 1)
