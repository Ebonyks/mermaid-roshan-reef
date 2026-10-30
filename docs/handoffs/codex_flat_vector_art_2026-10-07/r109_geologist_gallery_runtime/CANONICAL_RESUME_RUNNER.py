from pathlib import Path
import json,hashlib,subprocess,datetime,shutil,os,sys,time,urllib.request,urllib.parse,concurrent.futures
R=Path.cwd();S=Path(__file__).parent;V=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef');H=R/'docs/handoffs/codex_flat_vector_art_2026-10-07';P=H/'r109_geologist_gallery_runtime';IP=R/'design/audit_impacts/flat-vector-r109-gallery-runtime-20261029.json';BASE='970c4c36e5e8f0bd30a52f5f40bb0ad5f525dbbe';BR='codex/flat-vector-r6-20261012';REVISION='FV-AUDIT-20261029-R109-DEV'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def wt(p,t):p.write_text(t,encoding='utf-8',newline='\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def gs(*a):return git(*a).decode('utf-8').strip()
def state(n,**x):wr(S/'CANONICAL_STATE.json',{'state':n,'at_utc':now(),**x})
def gates(label):
 out=[]
 for name,cmd in [('authority',[sys.executable,'-B','tools/audit_document_authority.py']),('development',[sys.executable,'-B','tools/audit_development.py','--base','auto'])]:
  q=subprocess.run(cmd,cwd=R,capture_output=True,env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8'));b=q.stdout+q.stderr;(S/(label+'_'+name+'.log')).write_bytes(b);out.append({'gate':name,'exit_code':q.returncode,'command':cmd,'log_sha256':digest(b)});assert q.returncode==0,b.decode('utf-8',errors='replace')[-2500:]
 return out

def fetch(rev,p):
 req=urllib.request.Request('https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+rev+'/'+urllib.parse.quote(p,safe='/'),headers={'User-Agent':'MermaidReef-anonymous-delivery-verifier'})
 for attempt in range(5):
  try:
   with urllib.request.urlopen(req,timeout=90)as response:return response.status,response.read()
  except Exception:
   if attempt==4:raise
   time.sleep(2*(attempt+1))
try:
 prepared=rd(S/'CANONICAL_PREPARED.json');assert prepared['baseline']==BASE and prepared['counts_applied_once']=={'source':12,'partialDev':11,'bounded':6761,'excluded':4145,'retained':10906,'accepted_removed':0}
 assert gs('rev-parse','HEAD')==BASE and gs('branch','--show-current')==BR
 pub=rd(S/'SOURCE_PUBLICATION_FINAL.json');dev=rd(S/'dev_integration/FINAL_RESULT.json');SRC=pub['source_revision'];assert dev['source_CI_conclusion']=='success'and dev['integrated_dev_revision']==SRC
 rel=P.relative_to(R).as_posix();frozen=prepared['frozen_root5'];assert all(sha(H/n)==h for n,h in frozen.items())
 record=rd(P/'PRODUCTION.json');impact=rd(IP);files=impact['files'];assert record['source_revision']==SRC and record['new_frame_events']=={'bounded':16,'excluded':8,'retained':24}
 state('RESUMING_PREPARED_CANONICAL_AFTER_FINDING_REFERENCE_REPAIR_NO_COUNTER_REPEAT',source_revision=SRC)
 state('CANONICAL_PREPARED_BUILDING_MANIFEST_NO_ENGINE_RERUN',source_revision=SRC)
 code,raw=fetch(SRC,rel+'/MANIFEST.json');assert code==200;srcman=json.loads(raw);selected=[];runtime={'scripts/opera_geology_surface.gd'}|{x['path']for x in rd(P/'DERIVATION.json')['exports']}|{x['path']+'.import'for x in rd(P/'DERIVATION.json')['exports']}
 for row in srcman['files']:
  p=row['path']
  if p in runtime or p.startswith('assets_src/imagegen/geologist_crystal_gallery_20261029/')or(p.startswith(rel+'/candidate/')and p.endswith('.png'))or p.startswith(rel+'/excluded_preexisting_119/')or(p.startswith('docs/handoffs/codex_flat_vector_art_2026-10-07/r106_geologist_workbench_runtime/candidate/')and p.endswith('.png'))or row.get('revision')==record['source_baseline']:selected.append({**row,'revision':row.get('revision')or SRC})
 assert runtime<={x['path']for x in selected};assert len([x for x in selected if x['path'].startswith(rel+'/candidate/')and x['path'].endswith('.png')])==16;assert len([x for x in selected if x['path'].startswith(rel+'/excluded_preexisting_119/')and x['path'].endswith('.png')])==8
 existing=[p for p in files if(R/p).is_file()and not p.endswith(('/MANIFEST.json','/REMOTE_VERIFICATION.json','/PAYLOAD_PIN.json'))]+[IP.relative_to(R).as_posix()];subprocess.run(['git','add','--',*existing],cwd=R,check=True,capture_output=True);gate_rows=gates('CANONICAL');wr(P/'CANONICAL_GATES.json',{'state':'PASS','gates':gate_rows,'engine_rerun':False});impact['validation'][-1]['result']='PASS';impact['validation'][-1]['evidence']=rel+'/CANONICAL_GATES.json; publication/receipt verification separately recorded, not inferred.';wr(IP,impact);subprocess.run(['git','add','--',*existing],cwd=R,check=True,capture_output=True)
 rows=[]
 for p in existing:
  b=git('show',':'+p);rows.append({'revision':None,'path':p,'bytes':len(b),'sha256':digest(b),'role':'Verified current canonical production/Dev/evidence/count delta'})
 rows+=selected;manifest={'schema':'reef.runtime_trial_delivery/1','revision':REVISION,'baseline':BASE,'files':rows,'required_files':len(rows),'required_bytes':sum(x['bytes']for x in rows),'actual_runtime_source':SRC,'scope':'Currentcanonical whole-gallery production/Dev delta and complete new source/master/painted export,16reviewed candidateframes,8excluded119failureframes and6immutable sourceframes plus appearance refs. Fullsource independently delivered; no recursive historical archive.','new_generation_calls':1,'new_bounded_source_artifacts':1,'new_frame_events':{'bounded':16,'excluded':8,'retained':24},'accepted_removed':0,'mission_complete':False};wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',rel+'/MANIFEST.json'],cwd=R,check=True,capture_output=True);gates('PAYLOAD_FINAL');assert all(sha(H/n)==h for n,h in frozen.items());assert not gs('diff','--name-only');subprocess.run(['git','fetch','origin'],cwd=R,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE
 subprocess.run(['git','commit','-m','Publish painted crystal gallery and exact green Dev integration'],cwd=R,check=True,capture_output=True);payload=gs('rev-parse','HEAD');subprocess.run(['git','push','origin',BR],cwd=R,check=True,capture_output=True);state('CANONICAL_PAYLOAD_PUSHED_ANONYMOUS_VERIFICATION',payload=payload)
 mp=rel+'/MANIFEST.json';mb=git('show',payload+':'+mp);code,b=fetch(payload,mp);assert code==200 and b==mb
 def verify(row):
  rev=row['revision']or payload;code,b=fetch(rev,row['path']);assert code==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return {**row,'revision':rev,'verified':True,'http_status':code}
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 receipt={'schema':'reef.remote_delivery_verification/1','revision':payload,'repository':'Ebonyks/mermaid-roshan-reef','manifest':mp,'manifest_sha256':digest(mb),'manifest_bytes':len(mb),'required_files':len(rows),'required_bytes':manifest['required_bytes'],'files':verified,'access_mode':'Anonymous immutable HTTPS GET, no Authorization/cookies, exact bytes/SHA256 for manifest/every required file.','checked_at_utc':now(),'state':'ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED','limits':'Transport/provenance only.119gap/formalQA11/device/child/owner/natural/training/global acceptance remain open.'};wr(P/'REMOTE_VERIFICATION.json',receipt);wr(P/'PAYLOAD_PIN.json',{'payload_revision':payload,'source_revision':SRC,'manifest':mp,'manifest_sha256':digest(mb),'frozen_root5_unchanged':True,'new_native_frames':24,'new_bounded_frame_events':16,'new_excluded_frame_events':8,'new_bounded_source_artifacts':1,'new_partial_Dev_artifacts':1,'accepted_removed':0});subprocess.run(['git','add','--',rel+'/REMOTE_VERIFICATION.json',rel+'/PAYLOAD_PIN.json'],cwd=R,check=True,capture_output=True);gates('RECEIPT');subprocess.run(['git','commit','-m','Record anonymous immutable R109 gallery delivery verification'],cwd=R,check=True,capture_output=True);rev=gs('rev-parse','HEAD');subprocess.run(['git','push','origin',BR],cwd=R,check=True,capture_output=True)
 own=[]
 for n in['README.md','MANIFEST.json','REMOTE_VERIFICATION.json','PAYLOAD_PIN.json']:
  p=rel+'/'+n;expected=git('show',rev+':'+p);code,b=fetch(rev,p);assert code==200 and b==expected;own.append({'path':p,'revision':rev,'sha256':digest(b),'bytes':len(b),'verified':True})
 assert not gs('status','--porcelain')and all(sha(H/n)==h for n,h in frozen.items());final={'state':'CANONICAL_R109_DEV_PRODUCTION_DELIVERED_ANONYMOUSLY_VERIFIED','payload_revision':payload,'receipt_revision':rev,'source_revision':SRC,'required_files':len(rows),'required_bytes':manifest['required_bytes'],'all_required_anonymous_exact':True,'final_own_metadata':own,'frozen_root5_unchanged':True,'worktree_clean':True,'counts_applied_once':rd(S/'CANONICAL_PREPARED.json')['counts_applied_once'],'Dev_integrated':True,'source_CI_run':dev['source_CI_run'],'completed_at_utc':now()};wr(S/'CANONICAL_FINAL_PROOF.json',final);state('TERMINAL_SUCCESS',**final);print('CANONICAL_R109_DEV_DELIVERED',rev,payload,len(rows),flush=True)
except Exception as e:
 wr(S/'CANONICAL_RESUME_STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect exact source/Dev/canonical operation and preparedstate. Never repeat counter preparation once applied or restart healthy engine/CI.'});state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
