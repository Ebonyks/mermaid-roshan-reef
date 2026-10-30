from pathlib import Path
import json,hashlib,subprocess,os,re,time,datetime,shutil,urllib.request,urllib.parse,concurrent.futures,sys
S=Path(__file__).parent;R=Path.cwd();BR='codex/flat-vector-geologist-pan-runtime-20261017';BASE='51b2e1ef7b32d155786277871fc3f5e941145ea6';CAN='cfcadc966bc2f3d9962243589d8a820c19ac2b0d';H='docs/handoffs/codex_flat_vector_art_2026-10-07';P=R/H/'r111_geologist_seam_runtime';A=R/'assets_src/imagegen/geologist_geode_seams_20261030';IP=R/'design/audit_impacts/flat-vector-geologist-seam-runtime-20261030.json'
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
 stage('WAITING_EXISTING_VALIDATION75978_NO_RESTART');start=time.monotonic()
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
 plan=rd(A/'PLAN.json');plan['current_machine']='PASS frozen currentstatic/import/all82trusted and108nativechecks/16directlyviewedframes,8immutable contextframes reused. Noexcluded currentruns, no gameplay/art assertion changes.';wr(A/'PLAN.json',plan);wr(P/'PLAN.json',plan)
 status=dict(state='PAINTED_GEODE_SEAM_SOURCE_LOCAL82_STATIC_NATIVE108_PASS_EXACT_CI_PENDING',stable_id='FV-4502C5860C45',baseline=BASE,new_generation_calls=1,new_runtime_images=2,new_bounded_implementation_artifacts=1,implementation_unit='One coherent closed/mint-cleft seam cue family implementation, not a complete role/removal.',new_frame_events=dict(bounded=16,excluded=0,retained_total=16),native_checks=108,candidate_frames_reviewed=16,baseline_frames_reused=8,primitive_calls=rd(P/'PRIMITIVE_CENSUS.json'),functions_byte_identical=56,Dev_integrated=False,formal_QA11=None,device=None,child=None,owner=None,accepted_removed=0,mission_complete=False,checked_at_utc=now());wr(P/'STATUS.json',status)
 wt(P/'README.md','# Painted geode seam cue candidate\n\nStable item `FV-4502C5860C45`, baseline `'+BASE+'`. Two whole painted mineral seam nodules, cream closed and mint-cleft completed, replace only five circle/arc markers. Common64logical-square canvas, same five centres/56px hitradius/120px pull. Whole states swap on existing tapbits.56otherfunctions/input/save/lifecycle remain byte-identical; shell/cavity/verticalseam/inheritedpointer and otherart remain debt.\n\nOne built-in ImageGen static two-state take, native1774x887/Aseprite and2whole512exports, no tint/deformation/objectpartcompositing. Model/version/requestID/seed/usage notexposed, animationcalls0. [Plan](PLAN.json), [manifest](MANIFEST.json), [derivation](DERIVATION.json), [ten-axisreview](FRAME_REVIEW.json), [machine](LOCAL_82_RESULT.json), [source binding](DELIVERY_SOURCE_BINDING.json), [prompt](../../../../assets_src/imagegen/geologist_geode_seams_20261030/PROMPT.txt), [impact](../../../../design/audit_impacts/flat-vector-geologist-seam-runtime-20261030.json).\n\nExact4.7.2 Mobile/Speedy currentstatic/import/all82trusted and108nativechecks PASS; normal saves unchanged. All16current states at1280/1600 directlyinspected against8immutable same-scene sourceframes, noexcluded currentruns. Wrongfinger/cancel/JSON seam restore pass. Ordinary100-to120pull completes; original119 terminalgap remains unchanged. Tinycontour/childrecognition/shellintegration, sourceCI/Dev/formalQA11/device/child/owner/natural/training/allroutes/global acceptance remain open; acceptedremoved0.\n')
 master=R/'audit/MASTER_AUDIT_2026-08-09.md';lines=master.read_text(encoding='utf-8').splitlines();i=next(i for i,l in enumerate(lines)if l.startswith('| Geologist painted geode seam cues |'));lines[i]='| Geologist painted geode seam cues | [R111 candidate](../'+P.relative_to(R).as_posix()+'/README.md) | [Impact](../'+IP.relative_to(R).as_posix()+'); currentstatic/import/all82/native108/16reviewedframes PASS,56otherfunctions unchanged. SourceCI/Dev/formal/external and remainingart open. |';wt(master,'\n'.join(lines)+'\n')
 ch=R/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';wt(ch,ch.read_text(encoding='utf-8')+'\nR111 CHG-117 verification: currentstatic/import/all82trusted/native108/16reviewedframes pass;8prior sourceframes reused withoutcredit,0excluded currentruns. One static take/2whole512exports/one coherent implementation,0animationcalls. ExactsourceCI/Dev/formal/device/child/owner/otherart/global gaps remain open; original119 terminalgap unchanged.\n')
 impact=rd(IP);impact['validation'].append(dict(command='Frozen actualcandidate currentstatic/import/all82trusted, native108/16reviewedframes',result='PASS',evidence=P.relative_to(R).as_posix()+'/LOCAL_82_RESULT.json; SOURCE_PIN.json; FRAME_REVIEW.json; actualsourceCI/Dev/formal/external separate.'))
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
  b=git('show',':'+p);rows.append({'revision':None,'path':p,'bytes':len(b),'sha256':digest(b),'role':'Actual complete painted seam cue states, source/editable master/native context/current machine evidence; no global acceptance inferred'})
 historical=[(BASE,'assets/opera/worlds/props/geologist_work_slab_painted.png','Neighboringbench appearance style; original provisional candidate scope unchanged'),(BASE,'assets/opera/worlds/props/geologist_mineral_mint_painted.png','Neighboring mint mineral palette/material reference; original approvalscope unchanged')]
 for width in[1280,1600]:
  for n in['01_initial','02_partial_seams','03_ready_to_pull','04_reveal_25']:historical.append(('0f4fad1901967b8cc536c6d894dd255f4a9bb786',H+'/r109_geologist_gallery_runtime/candidate/'+str(width)+'/'+n+'.png','Same-scene geode baseline reused immutably, zero newframecredit'))
 for rev,p,role in historical:
  b=git('show',rev+':'+p);rows.append({'revision':rev,'path':p,'bytes':len(b),'sha256':digest(b),'role':role})
 manifest=dict(schema='reef.runtime_trial_delivery/1',revision='FV-AUDIT-20261030-R111',baseline=BASE,stable_id='FV-4502C5860C45',files=rows,required_files=len(rows),required_bytes=sum(x['bytes']for x in rows),scope='One coherent two-whole-state painted seam cue implementation, complete native/source/master archive,16currentframes and8bounded immutable contextframes. No recursive history or excluded currentevents.',new_generation_calls=1,new_runtime_images=2,new_bounded_implementation_artifacts=1,new_frame_events=dict(bounded=16,excluded=0,retained=16),whole_role_closed=False,accepted_removed=0,mission_complete=False);wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',(P/'MANIFEST.json').relative_to(R).as_posix()],cwd=R,check=True,capture_output=True)
 gates=[gate('FINAL_AUTHORITY',[sys.executable,'-B','tools/audit_document_authority.py']),gate('FINAL_DEVELOPMENT',[sys.executable,'-B','tools/audit_development.py','--base','auto'])];wr(S/'FINAL_PRECOMMIT_GATES.json',gates)
 assert set(gs('diff','--cached','--name-only').splitlines())<=files;assert not gs('diff','--name-only'),'Unexpected unstaged semantic edits'
 subprocess.run(['git','fetch','origin'],cwd=R,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE,'Owned topic advanced';dev=gs('rev-parse','origin/dev');assert dev==BASE,'Dev advanced; reconcile and validate applicable delta first'
 subprocess.run(['git','commit','-m','Replace flat geode seam markers with whole painted tap states'],cwd=R,check=True,capture_output=True);rev=gs('rev-parse','HEAD');stage('SOURCE_COMMITTED_PUSH_PENDING',source_revision=rev);eol_cleanup('POSTCOMMIT_EOL_CLEANUP');assert not gs('status','--porcelain'),'Unexpected dirty file after commit'
 subprocess.run(['git','push','origin',BR],cwd=R,check=True,capture_output=True);stage('SOURCE_PUSHED_ANONYMOUS_VERIFICATION',source_revision=rev)
 mp=(P/'MANIFEST.json').relative_to(R).as_posix();mb=git('show',rev+':'+mp);code,b=fetch(mp,rev);assert code==200 and b==mb
 def verify(row):
  rr=row['revision']or rev;code,b=fetch(row['path'],rr);assert code==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return {**row,'revision':rr,'http_status':code,'verified':True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 wr(S/'SOURCE_REMOTE_VERIFICATION.json',{'schema':'reef.remote_delivery_verification/1','repository':'Ebonyks/mermaid-roshan-reef','revision':rev,'manifest':mp,'manifest_sha256':digest(mb),'manifest_bytes':len(mb),'required_files':len(rows),'required_bytes':manifest['required_bytes'],'files':verified,'access_mode':'Anonymous HTTPS GET, no Authorization/cookies; exact immutable bytes/SHA256 for manifest and every required file.','checked_at_utc':now(),'state':'ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED','limits':'Transport/provenance only; not formal/device/child/owner acceptance.'})
 runs=json.loads(subprocess.check_output(['gh','run','list','--repo','Ebonyks/mermaid-roshan-reef','--branch',BR,'--limit','8','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=R,text=True,encoding='utf-8'));wr(S/'SOURCE_CI_HANDLES.json',[x for x in runs if x['headSha']==rev]);final={'state':'SOURCE_DELIVERED_ANONYMOUSLY_VERIFIED_EXACT_CI_PENDING','source_revision':rev,'branch':BR,'manifest':mp,'required_files':len(rows),'required_bytes':manifest['required_bytes'],'receipt':str(S/'SOURCE_REMOTE_VERIFICATION.json'),'source_clean':True,'origin_dev_at_publication':dev,'Dev_integrated':False,'PR_created':False,'completed_at_utc':now()};wr(S/'SOURCE_PUBLICATION_FINAL.json',final);stage('TERMINAL_SOURCE_DELIVERY_SUCCESS',**final);print('R111_SOURCE_DELIVERED',rev,len(rows),flush=True)
except Exception as e:
 wr(S/'PUBLICATION_STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect exact handle/source/log; no healthy restart, no force push.'});stage('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
