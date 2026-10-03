from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys,time,urllib.request,urllib.parse
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=R/'tmp/nursery_review_s_publish_v432';out.mkdir(exist_ok=False)
verify=R/'tmp/nursery_review_s_remote_v432';verify.mkdir(exist_ok=False)
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
seal=read(R/'tmp/nursery_review_s_sealed_v428.json')
assert seal['status']=='EXACT_SCOPED_MOTION_SOURCE_S_BLOBS_SEALED'
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
for label in ('game2d','authority','development','document_tests'):
 assert read(R/'assets_src/local_motion/nursery_connected_scrub_v4_20261002/gates'/(label+'_v1.receipt.json'))['status']=='PASS',label
assert read(R/'assets_src/local_motion/nursery_connected_scrub_v4_20261002/REVIEW_STATUS.json')['status']=='MACHINE_RENDER_COMPLETE_VISUAL_REJECTED'
assert len(read(R/'audit/job_artwork_refinement_live/ALL_ITEMS.json')['items'])==1802
run('fetch',['git','fetch','origin',branch])
assert git('rev-parse','origin/'+branch).decode().strip()==seal['base_revision'],'Topic advanced remotely; reconcile before publication.'
msg=out/'COMMIT_MESSAGE.txt';msg.write_text('Preserve complete rejected Nursery motion and eight source reviews\n\nRecord every41 native fresh-source A3 frame and every41 prompt-only A4 frame, all component/action opinions, prompt/input/model/workflow provenance, receipt and original-size QA boards. A3 action2.7 rejected. A4 action3.2 removes the tall white arch but still fails two reciprocal rubbing strokes2.8 and fixture material3.4; attention4.6 remains separate. Same source/input/seed/settings/developed workflow for prompt-only A4. No current-game score transfer or binding.\n\nDirectly review eight previously unassigned Day One discovery source originals: seven inclusive priorities/six below4.5; painted star4.5 and crystal texture4.6 provisional. Record exact literal dungeon/Ember fallback roles separately from unverified job use and source names; do not replace a bird beak with a leafy carrot. Library V39 remains1802 known entries,713 source-cell-region priorities and377 source reviews outstanding. Preserve all dated history and original bytes.\n\nPreserve immutable R15802 anonymous verified remote files, every literal journal row in bounded reconstructible shards and exact receipt. Add actual temporary browser proofs with no deliverable/handoff status mark. Existing authority, coverage,52 document tests/6 stress tests and staged2D no-regression pass. Fresh postcommit2D/authority/coverage gates run before this topic draft push. Current official4.7.2 local82/82 remains independently qualified against all783 unchanged literal production members and all53 raw diagnostics. Hosted R and the new exact revision are independent; wait for R final state before pushing to avoid cancelling its active suite.\n\nPublish and anonymously verify every required immutable file in the new closed V16 map. No protected original, production code/art, security/workflow/gate change, rejected reference upload/browser status action, current-action/cinematic/device/child/owner/all-job acceptance, finding lifecycle closure, dev/master integration or release.\n',encoding='utf-8',newline='\n')
run('commit',['git','commit','--quiet','--file',str(msg)],1800)
revision=git('rev-parse','HEAD').decode().strip();tree=git('rev-parse','HEAD^{tree}').decode().strip();assert git('rev-parse','HEAD^').decode().strip()==seal['base_revision']
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
for label,args in [('game2d',[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate']),('authority',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'])]:run(label,args,1800 if label=='game2d' else 600)
# A new topic push must not cancel the still-running exact R validation.
gh='C:/Program Files/GitHub CLI/gh.exe'
deadline=time.monotonic()+3600
while True:
 hosted=json.loads(subprocess.check_output([gh,'run','view','37083138864','--json','status,conclusion,headSha,url,jobs'],cwd=R))
 assert hosted['headSha']==seal['base_revision']
 if hosted['status']=='completed':
  hosted['captured_utc']=now();hosted['qualification']='Exact parent R hosted completion; separate from new S machine/visual/device/child/owner acceptance. Any failed/advisory result remains literal and unwaived.';write(out/'HOSTED_R_FINAL.json',hosted)
  print('EXACT_PARENT_R_HOSTED_FINAL',hosted['conclusion'],flush=True);break
 assert time.monotonic()<deadline,'Exact parent R hosted suite remains active; no cancelling push made.'
 print('WAITING_EXACT_PARENT_R_HOSTED_COMPLETION_NO_CANCEL',now(),flush=True)
 time.sleep(60)
run('push',['git','push','origin','HEAD:refs/heads/'+branch],1800)
assert git('rev-parse','origin/'+branch).decode().strip()==revision
pub={'status':'TOPIC_CANDIDATE_PUBLISHED_REMOTE_VERIFICATION_PENDING','revision':revision,'tree':tree,'branch':branch,'map_path':mp,'map_sha256':seal['map_sha256'],'payload_sha256':m['payload_sha256'],'payload_files':m['required_files'],'payload_bytes':m['required_payload_bytes'],'local_ci_members':783,'revision_source_members':543,'auxiliary_generated_uid_members':240,'checked_utc':now(),'qualification':'Durable topic review checkpoint only. Visual/current-action/all-job/device/child/owner/integration/release remain open; blocked imagegen reference upload remains blocked.'};write(out/'RECEIPT.json',pub)
print('PUBLISHED_NURSERY_SOURCE_TOPIC_REVISION',revision,flush=True)
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
