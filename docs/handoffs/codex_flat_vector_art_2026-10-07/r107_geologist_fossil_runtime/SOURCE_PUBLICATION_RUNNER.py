from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime,shutil,urllib.request,urllib.parse,concurrent.futures,sys
S=Path(__file__).parent;R=Path.cwd();BR='codex/flat-vector-geologist-pan-runtime-20261017';BASE='44da99ba5c68153fa247e0794425b5f6d7d3cc79';CAN='cfcadc966bc2f3d9962243589d8a820c19ac2b0d';H='docs/handoffs/codex_flat_vector_art_2026-10-07';P=R/H/'r107_geologist_fossil_runtime';A=R/'assets_src/imagegen/geologist_fossil_slab_wide_20261029';IP=R/'design/audit_impacts/flat-vector-geologist-fossil-runtime-20261029.json'
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
  if p.endswith('.import')and entry[:2]!='??':
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
 stage('WAITING_EXISTING_VALIDATION58344_NO_RESTART');start=time.monotonic()
 while not(S/'full_validation/FINAL_RESULT.json').exists():
  if(S/'VALIDATION_STOP.json').exists():raise RuntimeError('Existing validation stopped; inspect exact failure, no restart')
  assert time.monotonic()-start<7200;time.sleep(10)
 result=rd(S/'full_validation/FINAL_RESULT.json');assert result['status']=='PASS_ALL_82_AND_CURRENT_STATIC'and result['probe_count']==82 and result['normal_unchanged']
 assert rd(S/'FRAME_REVIEW.json')['all_16_current_frames_inspected'];assert gs('branch','--show-current')==BR and gs('rev-parse','HEAD')==BASE
 pin=rd(S/'SOURCE_PIN.json');assert all(sha(R/p)==h for p,h in pin['runtime_hashes'].items())
 cleanup=eol_cleanup('DELIVERY_EOL_CLEANUP');shutil.copyfile(S/'DELIVERY_EOL_CLEANUP.json',P/'DELIVERY_EOL_CLEANUP.json')
 for a,b in [('full_validation/FINAL_RESULT.json','LOCAL_82_RESULT.json'),('full_validation/LAUNCH.json','LOCAL_82_LAUNCH.json'),('full_validation/STATIC_RESULT.json','STATIC_RESULT.json'),('full_validation/STATIC_PREFIX.log','STATIC_PREFIX.log'),('full_validation/GAME2D.log','GAME2D.log'),('validate_candidate.py','VALIDATION_RUNNER.py'),('current_ci_static_prefix.sh','CURRENT_STATIC_PREFIX.sh'),('publish_source.py','SOURCE_PUBLICATION_RUNNER.py')]:shutil.copyfile(S/a,P/b)
 combined=bytearray();index=[]
 for row in result['results']:
  b=Path(row['log']).read_bytes();assert digest(b)==row['log_sha256'];combined.extend(('=== '+row['probe']+' ===\n').encode());offset=len(combined);combined.extend(b);combined.extend(b'\n');index.append({'probe':row['probe'],'offset':offset,'bytes':len(b),'sha256':digest(b),'exit_code':row['exit_code'],'passed':row['passed']})
 (P/'TRUSTED_PROBES.log').write_bytes(combined);wr(P/'TRUSTED_LOG_INDEX.json',{'combined_log_sha256':digest(combined),'preserves_every_original_probe_log_byte':True,'entries':index})
 plan=rd(A/'PLAN.json');plan['current_machine']='PASS current owned-worktree static/import and all82trusted with exact source/normal11 guards;114configured native checks and16directly inspected candidate frames.';wr(A/'PLAN.json',plan);wr(P/'PLAN.json',plan)
 status={'state':'PAINTED_FOSSIL_SOURCE_LOCAL82_STATIC_NATIVE114_PASS_EXACT_CI_PENDING','stable_id':'FV-4CD5292EEE1D','baseline':BASE,'new_generation_calls':1,'new_runtime_images':4,'new_bounded_implementation_artifacts':1,'implementation_unit':'One coherent fossil whole/three-fragment implementation; not four role removals.','new_frame_events':{'bounded':16,'excluded':0,'retained_total':16},'native_checks':114,'candidate_frames_reviewed':16,'baseline_frames_reused':6,'primitive_calls':rd(P/'PRIMITIVE_CENSUS.json'),'functions_byte_identical':53,'Dev_integrated':False,'formal_QA11':None,'device':None,'child':None,'owner':None,'accepted_removed':0,'mission_complete':False,'checked_at_utc':now()};wr(P/'STATUS.json',status)
 wt(P/'README.md','# Painted fossil and matching fragments candidate\n\nStable item `FV-4CD5292EEE1D`, source baseline `'+BASE+'`. A painted golden ammonite on lavender stone and three exact matching fragments replace the stretched SVG and two flat arc fallbacks in the existing fossil activity. Uniform whole-source drawing and registered fragments preserve all gesture, hit, snap and save behavior;53other functions are byte-identical. The final assembly draws one whole parent to avoid independently filtered seams. The separate flat soil cover, cave/UI, other art and original completion actor overlap remain open.\n\nOne built-in ImageGen static edit extends the existing fossil backing; no model/version, request ID, seed or usage was returned. Native Aseprite source and four technical exports are preserved. No animation budget used. [Plan](PLAN.json), [manifest](MANIFEST.json), [derivation](DERIVATION.json), [ten-axis comparison](FRAME_REVIEW.json), [source binding](DELIVERY_SOURCE_BINDING.json), [machine result](LOCAL_82_RESULT.json) and [audit impact](../../../../design/audit_impacts/flat-vector-geologist-fossil-runtime-20261029.json).\n\nExact4.7.2Mobile/Speedy import/currentstatic/all82trusted and114configured native checks pass with normal saves unchanged. All16candidate frames across covered/reveal/loose/held/wrongdrop/snapping/completed states at1280/1600 were directly inspected against current immutable scene references. Six existing source frames are reused, adding no frame events. Exact-source CI and Dev are pending. Formal QA11, natural/training/all-route, device, child and owner acceptance remain separate and open. Accepted artwork removals remain zero.\n')
 for file,marker,paragraph in [('audit/MASTER_AUDIT_2026-08-09.md','| Geologist painted fossil and fragments |','| Geologist painted fossil and fragments | [R107 candidate](../'+P.relative_to(R).as_posix()+'/README.md) | [Impact](../'+IP.relative_to(R).as_posix()+'); currentstatic/import/all82/native114 and16directlyreviewed frames PASS. One coherent whole/three-fragment source,53other functions unchanged; soil/otherart/CI/Dev/formal/external remain open. |')]:
  p=R/file;lines=p.read_text(encoding='utf-8').splitlines();i=next(i for i,l in enumerate(lines)if l.startswith(marker));lines[i]=paragraph;wt(p,'\n'.join(lines)+'\n')
 ch=R/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';wt(ch,ch.read_text(encoding='utf-8')+'\nR107 CHG-113 verification: exactcurrentstatic/import/all82trusted and114configurednativechecks/16directlyreviewed frames pass. One static edit, four technicalexports, one implementation;16newbounded frameevents, noexcluded events,6priorframes reused immutably. SourceCI/Dev/formal/device/child/owner/global gaps remain.\n')
 impact=rd(IP);impact['validation'].append({'command':'Exact frozen candidate currentstatic/import/all82trusted, native114/16reviewedframes','result':'PASS','evidence':P.relative_to(R).as_posix()+'/LOCAL_82_RESULT.json; SOURCE_PIN.json; FRAME_REVIEW.json; actual sourceCI/Dev/formal/external stay separate.'})
 files=set(gs('diff','--name-only').splitlines())|{p.relative_to(R).as_posix()for parent in[P,A]for p in parent.rglob('*')if p.is_file()}|{row['path']for row in rd(A/'DERIVATION.json')['exports']}|{row['path']+'.import'for row in rd(A/'DERIVATION.json')['exports']}|{(P/'DELIVERY_SOURCE_BINDING.json').relative_to(R).as_posix()};files.discard(IP.relative_to(R).as_posix());impact['files']=sorted(files);wr(IP,impact);files.add(IP.relative_to(R).as_posix());existing=sorted(p for p in files if(R/p).is_file()and not p.endswith(('/MANIFEST.json','/DELIVERY_SOURCE_BINDING.json')));subprocess.run(['git','add','-f','--',*existing],cwd=R,check=True,capture_output=True)
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
  b=git('show',':'+p);rows.append({'revision':None,'path':p,'bytes':len(b),'sha256':digest(b),'role':'Actual painted fossil whole/fragments, source/editable masters, context/review/current machine evidence; no global acceptance inferred'})
 historical=[(CAN,'assets/opera/worlds/geology/painted_work_v1_20261001/fossil.png','Historical painted appearance source, original acceptance scope retained')]
 for width in[1280,1600]:
  for n in['01_initial','02_assembly_loose_pieces','03_complete']:historical.append((BASE,H+'/r106_geologist_workbench_runtime/candidate/'+str(width)+'/1/'+n+'.png','Same-scene source context reused immutably; zero new frameevent credit'))
 for rev,p,role in historical:
  b=git('show',rev+':'+p);rows.append({'revision':rev,'path':p,'bytes':len(b),'sha256':digest(b),'role':role})
 manifest={'schema':'reef.runtime_trial_delivery/1','revision':'FV-AUDIT-20261029-R107','baseline':BASE,'stable_id':'FV-4CD5292EEE1D','files':rows,'required_files':len(rows),'required_bytes':sum(x['bytes']for x in rows),'scope':'One coherent painted fossil source plus three exact fragments, native source/master,16newactual contextframes and applicable validation. Historical dependency bounded to appearance source and6current same-scene context images, no recursive archive.','new_generation_calls':1,'new_runtime_images':4,'new_bounded_implementation_artifacts':1,'new_frame_events':{'bounded':16,'excluded':0,'retained':16},'whole_role_closed':False,'accepted_removed':0,'mission_complete':False};wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',(P/'MANIFEST.json').relative_to(R).as_posix()],cwd=R,check=True,capture_output=True)
 gates=[gate('FINAL_AUTHORITY',[sys.executable,'-B','tools/audit_document_authority.py']),gate('FINAL_DEVELOPMENT',[sys.executable,'-B','tools/audit_development.py','--base','auto'])];wr(S/'FINAL_PRECOMMIT_GATES.json',gates)
 assert set(gs('diff','--cached','--name-only').splitlines())<=files;assert not gs('diff','--name-only'),'Unexpected unstaged semantic edits'
 subprocess.run(['git','fetch','origin'],cwd=R,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE,'Owned topic advanced';dev=gs('rev-parse','origin/dev');assert dev==BASE,'Dev advanced; reconcile and validate applicable delta first'
 subprocess.run(['git','commit','-m','Replace flat fossil with painted whole and matching fragments'],cwd=R,check=True,capture_output=True);rev=gs('rev-parse','HEAD');stage('SOURCE_COMMITTED_PUSH_PENDING',source_revision=rev);eol_cleanup('POSTCOMMIT_EOL_CLEANUP');assert not gs('status','--porcelain'),'Unexpected dirty file after commit'
 subprocess.run(['git','push','origin',BR],cwd=R,check=True,capture_output=True);stage('SOURCE_PUSHED_ANONYMOUS_VERIFICATION',source_revision=rev)
 mp=(P/'MANIFEST.json').relative_to(R).as_posix();mb=git('show',rev+':'+mp);code,b=fetch(mp,rev);assert code==200 and b==mb
 def verify(row):
  rr=row['revision']or rev;code,b=fetch(row['path'],rr);assert code==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return {**row,'revision':rr,'http_status':code,'verified':True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 wr(S/'SOURCE_REMOTE_VERIFICATION.json',{'schema':'reef.remote_delivery_verification/1','repository':'Ebonyks/mermaid-roshan-reef','revision':rev,'manifest':mp,'manifest_sha256':digest(mb),'manifest_bytes':len(mb),'required_files':len(rows),'required_bytes':manifest['required_bytes'],'files':verified,'access_mode':'Anonymous HTTPS GET, no Authorization/cookies; exact immutable bytes/SHA256 for manifest and every required file.','checked_at_utc':now(),'state':'ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED','limits':'Transport/provenance only; not formal/device/child/owner acceptance.'})
 runs=json.loads(subprocess.check_output(['gh','run','list','--repo','Ebonyks/mermaid-roshan-reef','--branch',BR,'--limit','8','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=R,text=True,encoding='utf-8'));wr(S/'SOURCE_CI_HANDLES.json',[x for x in runs if x['headSha']==rev]);final={'state':'SOURCE_DELIVERED_ANONYMOUSLY_VERIFIED_EXACT_CI_PENDING','source_revision':rev,'branch':BR,'manifest':mp,'required_files':len(rows),'required_bytes':manifest['required_bytes'],'receipt':str(S/'SOURCE_REMOTE_VERIFICATION.json'),'source_clean':True,'origin_dev_at_publication':dev,'Dev_integrated':False,'PR_created':False,'completed_at_utc':now()};wr(S/'SOURCE_PUBLICATION_FINAL.json',final);stage('TERMINAL_SOURCE_DELIVERY_SUCCESS',**final);print('R107_SOURCE_DELIVERED',rev,len(rows),flush=True)
except Exception as e:
 wr(S/'PUBLICATION_STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect exact handle/source/log; no healthy restart, no force push.'});stage('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
