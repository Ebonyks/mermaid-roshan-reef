from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime,shutil,urllib.request,urllib.parse,concurrent.futures,sys
S=Path(__file__).parent;R=Path.cwd();BR='codex/flat-vector-geologist-pan-runtime-20261017';BASE='803dbac68705d46bcb4a5da4d060a0ae8cf09d6d';CAN='cfcadc966bc2f3d9962243589d8a820c19ac2b0d';H='docs/handoffs/codex_flat_vector_art_2026-10-07';P=R/H/'r113_geologist_crest_runtime';A=R/'assets_src/imagegen/geologist_crest_20261030';IP=R/'design/audit_impacts/flat-vector-geologist-crest-runtime-20261030.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def wt(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def gs(*a):return git(*a).decode('utf-8').strip()
def stage(n,**kw):wr(S/'PUBLICATION_STATE.json',{'state':n,'updated_at_utc':now(),**kw})
def gate(label,cmd):
 q=subprocess.run(cmd,cwd=R,capture_output=True,env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8'));b=q.stdout+q.stderr;(S/(label+'.log')).write_bytes(b);assert q.returncode==0,label+' '+b.decode(errors='replace')[-2200:];return {'gate':label,'command':cmd,'exit_code':0,'log_sha256':digest(b)}
def eol_cleanup(label):
 rows=[]
 for entry in git('status','--porcelain','-z').decode().split('\0'):
  if not entry:continue
  p=entry[3:]
  if p.endswith('.import')and entry[:2]!='??'and(R/p).is_file():
   cur=(R/p).read_bytes();idx=git('show',':'+p)
   if cur.replace(b'\r\n',b'\n')==idx.replace(b'\r\n',b'\n'):rows.append({'path':p,'before_raw_sha256':digest(cur),'index_sha256':digest(idx),'lf_sha256':digest(cur.replace(b'\r\n',b'\n'))})
 if rows:
  f=S/(label+'_PATHS.txt');wt(f,'\n'.join(x['path']for x in rows)+'\n');subprocess.run(['git','restore','--worktree','--pathspec-from-file='+str(f)],cwd=R,check=True,capture_output=True);assert all(digest((R/x['path']).read_bytes().replace(b'\r\n',b'\n'))==x['lf_sha256']for x in rows)
 wr(S/(label+'.json'),{'files':rows,'count':len(rows),'semantics_or_pixels_changed':False,'scope':'Only LF-equivalent import sidecars against current owned index; no runtime/pixel reset.','checked_at_utc':now()});return rows
def fetch(p,rev):
 url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+urllib.parse.quote(p,safe='/');req=urllib.request.Request(url,headers={'User-Agent':'MermaidReef-anonymous-delivery-verifier'})
 for attempt in range(5):
  try:
   with urllib.request.urlopen(req,timeout=90)as response:return response.status,response.read()
  except Exception:
   if attempt==4:raise
   time.sleep(2*(attempt+1))
try:
 stage('WAITING_EXISTING_VALIDATION9212_NO_RESTART');start=time.monotonic()
 while not(S/'full_validation/FINAL_RESULT.json').exists():
  if(S/'VALIDATION_STOP.json').exists():raise RuntimeError('Existing validation stopped; inspect exact failure, no restart')
  assert time.monotonic()-start<7200;time.sleep(10)
 result=rd(S/'full_validation/FINAL_RESULT.json');assert result['status']=='PASS_ALL_82_AND_CURRENT_STATIC'and result['probe_count']==82 and result['normal_unchanged']
 assert rd(S/'FRAME_REVIEW.json')['all_10_current_frames_inspected'];assert gs('branch','--show-current')==BR and gs('rev-parse','HEAD')==BASE
 pin=rd(S/'SOURCE_PIN.json');assert all(sha(R/p)==h for p,h in pin['runtime_hashes'].items())
 cleanup=eol_cleanup('DELIVERY_EOL_CLEANUP');shutil.copyfile(S/'DELIVERY_EOL_CLEANUP.json',P/'DELIVERY_EOL_CLEANUP.json')
 for a,b in [('full_validation/FINAL_RESULT.json','LOCAL_82_RESULT.json'),('full_validation/LAUNCH.json','LOCAL_82_LAUNCH.json'),('full_validation/STATIC_RESULT.json','STATIC_RESULT.json'),('full_validation/STATIC_PREFIX.log','STATIC_PREFIX.log'),('full_validation/GAME2D.log','GAME2D.log'),('validate_candidate.py','VALIDATION_RUNNER.py'),('current_ci_static_prefix.sh','CURRENT_STATIC_PREFIX.sh'),('publish_source.py','SOURCE_PUBLICATION_RUNNER.py')]:shutil.copyfile(S/a,P/b)
 combined=bytearray();index=[]
 for row in result['results']:
  b=Path(row['log']).read_bytes();assert digest(b)==row['log_sha256'];combined.extend(('=== '+row['probe']+' ===\n').encode());offset=len(combined);combined.extend(b);combined.extend(b'\n');index.append({'probe':row['probe'],'offset':offset,'bytes':len(b),'sha256':digest(b),'exit_code':row['exit_code'],'passed':row['passed']})
 (P/'TRUSTED_PROBES.log').write_bytes(combined);wr(P/'TRUSTED_LOG_INDEX.json',{'combined_log_sha256':digest(combined),'preserves_every_original_probe_log_byte':True,'entries':index})
 plan=rd(A/'PLAN.json');plan['current_machine']='PASS frozen currentstatic/import/all82trusted, source34checks/2baselineframes and candidate70checks/10directlyreviewedframes. No excluded runs; native/formal/device/child/owner separate.';wr(A/'PLAN.json',plan);wr(P/'PLAN.json',plan)
 status=dict(state='PAINTED_GEOLOGIST_CREST_SOURCE_LOCAL82_STATIC_NATIVE70_PASS_EXACT_CI_PENDING',stable_id='FV-8C7C289334A2',baseline=BASE,new_generation_calls=1,rejected_takes=0,new_runtime_images=1,new_bounded_implementation_artifacts=1,implementation_unit='One complete painted route-card crest implementation; no role acceptance/removal.',new_frame_events=dict(bounded=12,excluded=0,retained_total=12),native_checks=70,baseline_checks=34,candidate_frames_reviewed=10,baseline_frames_reviewed=2,retired_source=rd(P/'RETIRED_SOURCE.json'),functions_byte_identical=23,Dev_integrated=False,formal_QA11=None,device=None,child=None,owner=None,accepted_removed=0,mission_complete=False,checked_at_utc=now());wr(P/'STATUS.json',status)
 wt(P/'README.md','# Painted Geologist career crest candidate\n\n`FV-8C7C289334A2`, baseline `'+BASE+'`. One whole painted crystal-and-ammonite shell medallion replaces the flatSVG on the Library Geologist picture card. Original50x50 crest box/offset52,98,154x154button/input/callback/reward/save/route and23otherfunctions unchanged; only resourceconstant and Geologist-only mipmapfilter change. OldSVG/import retired with nonruntime originals; separate goalSVG and other art remain open.\n\nOne built-in static take within cap2, native1254square/Aseprite/roundtrip0visibleRGBAchanged; complete uniform216/1254 and20pxpadding to256, CUTOUT_OK. Model/version/requestID/seed/usage notexposed;0animationcalls. [Plan](PLAN.json), [manifest](MANIFEST.json), [derivation](DERIVATION.json), [ten-axisreview](FRAME_REVIEW.json), [retired source](RETIRED_SOURCE.json), [machine](LOCAL_82_RESULT.json), [sourcebinding](DELIVERY_SOURCE_BINDING.json), [impact](../../../../design/audit_impacts/flat-vector-geologist-crest-runtime-20261030.json).\n\nExact4.7.2 Mobile/Speedy import/currentstatic/all82trusted PASS; normal11save files unchanged. Sourcebaseline34checks/2frames and candidate70checks/10frames at1280/1600 directlyviewed: unearned/focused/earned/reentry/original Geologist launch. Noexcludedruns,12newboundedframeevents. Tiny fossil spiral recognition, natural/training/allroutes, fullspeed/device/performance/child/owner/formalQA11 and exactsourceCI/Dev remain separate. Actor identities/flatcave/goalSVG and inherited roommessage unchanged; acceptedremoved0/globalcompletionfalse.\n')
 master=R/'audit/MASTER_AUDIT_2026-08-09.md';lines=master.read_text(encoding='utf-8').splitlines();i=next(i for i,l in enumerate(lines)if l.startswith('| Geologist painted route-card crest |'));lines[i]='| Geologist painted route-card crest | [R113 candidate](../'+P.relative_to(R).as_posix()+'/README.md) | [Impact](../'+IP.relative_to(R).as_posix()+'); currentstatic/import/all82/native70/10candidate and34/2source frames PASS,23otherfunctions unchanged. ExactsourceCI/Dev/formal/external/otherart open. |';wt(master,'\n'.join(lines)+'\n')
 ch=R/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';wt(ch,ch.read_text(encoding='utf-8')+'\nR113 CHG-119 verification: actualcandidate currentstatic/import/all82trusted/native70/10directlyreviewedframes pass, plus sourcebaseline34/2frames. One static take/onewhole256/noexcludedruns/oneimplementation/12newboundedframeevents; oldSVG5paths retired with originals preserved nonruntime.23otherroutefunctions/input/save/geometry and allgeologycode unchanged. ExactsourceCI/Dev/formal/device/child/owner/otherart/global gaps open.\n')
 impact=rd(IP);impact['validation'].append(dict(command='Frozen actualcandidate currentstatic/import/all82trusted, originalMain Library native70/10candidate and34/2baselineframes',result='PASS',evidence=P.relative_to(R).as_posix()+'/LOCAL_82_RESULT.json; SOURCE_PIN.json; FRAME_REVIEW.json; RETIRED_SOURCE.json; actualsourceCI/Dev/formal/external separate.'))
 files=set(gs('diff','--name-only').splitlines())|{p.relative_to(R).as_posix()for parent in[P,A]for p in parent.rglob('*')if p.is_file()}|{row['path']for row in rd(A/'DERIVATION.json')['exports']}|{row['path']+'.import'for row in rd(A/'DERIVATION.json')['exports']}|{(P/'DELIVERY_SOURCE_BINDING.json').relative_to(R).as_posix()};files.discard(IP.relative_to(R).as_posix());impact['files']=sorted(files);wr(IP,impact);files.add(IP.relative_to(R).as_posix());existing=sorted(p for p in files if(R/p).is_file()and not p.endswith(('/MANIFEST.json','/DELIVERY_SOURCE_BINDING.json')));subprocess.run(['git','add','-f','--',*existing],cwd=R,check=True,capture_output=True);deleted=pin['runtime_deletions'];assert all(not(R/p).exists()for p in deleted);subprocess.run(['git','add','-u','--',*deleted],cwd=R,check=True,capture_output=True)
 clean_by_path={x['path']:x for x in cleanup};binding=[]
 for p,tested in sorted(pin['runtime_hashes'].items()):
  b=(R/p).read_bytes();blob=git('show',':'+p)
  if digest(b)!=tested:assert p in clean_by_path and clean_by_path[p]['before_raw_sha256']==tested and digest(b.replace(b'\r\n',b'\n'))==clean_by_path[p]['lf_sha256'],p
  assert b==blob or b.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n'),p
  binding.append({'path':p,'tested_filesystem_sha256':tested,'current_filesystem_sha256':digest(b),'staged_blob_sha256':digest(blob),'binding':'EXACT_BYTES'if b==blob and digest(b)==tested else'EXPLICIT_CRLF_LF_EQUIVALENCE_ONLY'})
 wr(P/'DELIVERY_SOURCE_BINDING.json',{'source_pin':'SOURCE_PIN.json','files':binding,'no_gameplay_or_pixel_change':True});subprocess.run(['git','add','--',(P/'DELIVERY_SOURCE_BINDING.json').relative_to(R).as_posix()],cwd=R,check=True,capture_output=True)
 rows=[]
 for p in sorted(files):
  if p==(P/'MANIFEST.json').relative_to(R).as_posix():continue
  if p in pin['runtime_deletions']:continue
  b=git('show',':'+p);rows.append({'revision':None,'path':p,'bytes':len(b),'sha256':digest(b),'role':'Actual whole painted Geologist crest/source/master/baseline/candidate/current machine evidence; no global acceptance inferred'})
 historical=[(BASE,'assets/opera/worlds/ui/crests/opera_crest_chef.png','Neighboring painted shellmedallion style reference; approvalscope unchanged'),(BASE,'assets/opera/worlds/props/geologist_mineral_lavender_painted.png','Current Geologist lavender material reference, provisionalscope retained'),(BASE,'assets/opera/worlds/props/geologist_fossil_painted.png','Current Geologist ammonite identity reference, provisionalscope retained')]
 for rev,p,role in historical:
  b=git('show',rev+':'+p);rows.append({'revision':rev,'path':p,'bytes':len(b),'sha256':digest(b),'role':role})
 manifest=dict(schema='reef.runtime_trial_delivery/1',revision='FV-AUDIT-20261030-R113',baseline=BASE,stable_id='FV-8C7C289334A2',files=rows,required_files=len(rows),required_bytes=sum(x['bytes']for x in rows),scope='One whole painted Geologist route-card crest; native/master/provenance,2sourcebaseline and10candidateframes, exact actualmachine logs. Three bounded immutable appearance references, no recursive historical archive.',runtime_deletions=pin['runtime_deletions'],new_generation_calls=1,rejected_takes=0,new_runtime_images=1,new_bounded_implementation_artifacts=1,new_frame_events=dict(bounded=12,excluded=0,retained=12),whole_role_closed=False,accepted_removed=0,mission_complete=False);wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',(P/'MANIFEST.json').relative_to(R).as_posix()],cwd=R,check=True,capture_output=True)
 gates=[gate('FINAL_AUTHORITY',[sys.executable,'-B','tools/audit_document_authority.py']),gate('FINAL_DEVELOPMENT',[sys.executable,'-B','tools/audit_development.py','--base','auto'])];wr(S/'FINAL_PRECOMMIT_GATES.json',gates)
 assert set(gs('diff','--cached','--name-only').splitlines())<=files;assert not gs('diff','--name-only'),'Unexpected unstaged semantic edits'
 subprocess.run(['git','fetch','origin'],cwd=R,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE,'Owned topic advanced';dev=gs('rev-parse','origin/dev');assert dev==BASE,'Dev advanced; reconcile and validate applicable delta first'
 subprocess.run(['git','commit','-m','Replace flat Geologist route crest with whole painted medallion'],cwd=R,check=True,capture_output=True);rev=gs('rev-parse','HEAD');stage('SOURCE_COMMITTED_PUSH_PENDING',source_revision=rev);eol_cleanup('POSTCOMMIT_EOL_CLEANUP');assert not gs('status','--porcelain'),'Unexpected dirty file after commit'
 subprocess.run(['git','push','origin',BR],cwd=R,check=True,capture_output=True);stage('SOURCE_PUSHED_ANONYMOUS_VERIFICATION',source_revision=rev)
 mp=(P/'MANIFEST.json').relative_to(R).as_posix();mb=git('show',rev+':'+mp);code,b=fetch(mp,rev);assert code==200 and b==mb
 def verify(row):
  rr=row['revision']or rev;code,b=fetch(row['path'],rr);assert code==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return {**row,'revision':rr,'http_status':code,'verified':True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 wr(S/'SOURCE_REMOTE_VERIFICATION.json',{'schema':'reef.remote_delivery_verification/1','repository':'Ebonyks/mermaid-roshan-reef','revision':rev,'manifest':mp,'manifest_sha256':digest(mb),'manifest_bytes':len(mb),'required_files':len(rows),'required_bytes':manifest['required_bytes'],'files':verified,'access_mode':'Anonymous HTTPS GET, no Authorization/cookies; exact immutable bytes/SHA256 for manifest and every required file.','checked_at_utc':now(),'state':'ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED','limits':'Transport/provenance only; not formal/device/child/owner acceptance.'})
 runs=json.loads(subprocess.check_output(['gh','run','list','--repo','Ebonyks/mermaid-roshan-reef','--branch',BR,'--limit','8','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=R,text=True,encoding='utf-8'));wr(S/'SOURCE_CI_HANDLES.json',[x for x in runs if x['headSha']==rev]);final={'state':'SOURCE_DELIVERED_ANONYMOUSLY_VERIFIED_EXACT_CI_PENDING','source_revision':rev,'branch':BR,'manifest':mp,'required_files':len(rows),'required_bytes':manifest['required_bytes'],'receipt':str(S/'SOURCE_REMOTE_VERIFICATION.json'),'source_clean':True,'origin_dev_at_publication':dev,'Dev_integrated':False,'PR_created':False,'completed_at_utc':now()};wr(S/'SOURCE_PUBLICATION_FINAL.json',final);stage('TERMINAL_SOURCE_DELIVERY_SUCCESS',**final);print('R113_SOURCE_DELIVERED',rev,len(rows),flush=True)
except Exception as e:
 wr(S/'PUBLICATION_STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect exact handle/source/log; no healthy restart, no force push.'});stage('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
