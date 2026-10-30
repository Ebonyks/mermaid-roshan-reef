from pathlib import Path
import json,subprocess,datetime,time,hashlib,urllib.request,urllib.parse,concurrent.futures
S=Path(__file__).parent;R=Path.cwd();OLDDEV='ca58aacd96bf10b2c5413659b1ee0f1b1a45f63b';W=S/'dev_integration'
def wr(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def gs(*a):return git(*a).decode('utf-8').strip()
def gh(*a):
 last=None
 for attempt in range(6):
  try:
   q=subprocess.run(['gh',*a],cwd=R,text=True,encoding='utf-8',capture_output=True,timeout=45)
   if q.returncode==0:return json.loads(q.stdout)
   last=q.stderr[-1000:]
  except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:last=str(e)
  wr(W/'OBSERVATION_RETRY.json',{'state':'TRANSIENT_READ_RETRY_SAME_JOB_NOT_RESTARTED','attempt':attempt+1,'error':last,'at_utc':now()})
  if attempt<5:time.sleep(15)
 raise RuntimeError('CI observation unavailable after bounded samejob read retries: '+str(last))
def stage(n,**kw):wr(W/'STATE.json',{'state':n,'updated_at_utc':now(),**kw})
def digest(b):return hashlib.sha256(b).hexdigest()
assert W.is_dir() and not(W/'LAUNCH.json').exists() and not(W/'FINAL_RESULT.json').exists(),'Resume only stopped pre-discovery observer'
assert (S/'catalog_path_recovery/dev_integration_STOP.json').exists()
try:
 stage('WAITING_FOR_EXISTING_R114_SOURCE_PUBLICATION',terminal=str(S/'SOURCE_PUBLICATION_FINAL.json'),do_not_restart=True);waiting=time.monotonic()
 while not(S/'SOURCE_PUBLICATION_FINAL.json').exists():
  if(S/'PUBLICATION_STOP.json').exists():raise RuntimeError('Existing source publisher stopped; retain it, do not restart or integrate unpublished work')
  if time.monotonic()-waiting>7200:raise RuntimeError('Existing source publication not terminal after120min; inspect exact handle, no restart')
  time.sleep(10)
 published=json.loads((S/'SOURCE_PUBLICATION_FINAL.json').read_text(encoding='utf-8-sig'));assert published['state']=='SOURCE_DELIVERED_ANONYMOUSLY_VERIFIED_EXACT_CI_PENDING'and published['source_clean'];REV=published['source_revision'];BR=published['branch'];waiting=time.monotonic()
 while True:
  runs=gh('run','list','--repo','Ebonyks/mermaid-roshan-reef','--branch',BR,'--limit','12','--json','databaseId,headSha,status,conclusion,url,workflowName');matches=[x for x in runs if x['headSha']==REV and x['workflowName']=='Probe suite (graphics fork)'];wr(W/'SOURCE_CI_DISCOVERY.json',{'source_revision':REV,'checked_at_utc':now(),'matching_runs':matches})
  if matches:RUN=matches[0]['databaseId'];break
  stage('WAITING_FOR_REAL_EXACT_SOURCE_CI_HANDLE',source_revision=REV,no_new_workflow_dispatched=True)
  if time.monotonic()-waiting>7200:raise RuntimeError('ExactsourceCI handle still undiscovered after120min; inspect, no duplicate run')
  time.sleep(20)
except Exception as e:
 wr(W/'STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect sourcepublication/CI discovery; never restart healthy jobs or integrate without exact sourcegreen.'});raise

wr(W/'LAUNCH.json',{'source_revision':REV,'source_branch':BR,'prior_dev':OLDDEV,'source_CI_run':RUN,'started_at_utc':now(),'method':'Wait for existing exact-head source workflow, no rerun. Fresh-fetch, require clean owned topic and tested source; fast-forward Dev only with optimistic old-ref guard. Do not touch local Dev/master or another checkout. Verify resulting immutable runtime bytes anonymously; no release promotion.'})
try:
 started=time.monotonic();seen=None
 while True:
  d=gh('run','view',str(RUN),'--repo','Ebonyks/mermaid-roshan-reef','--json','status,conclusion,headSha,headBranch,event,url,jobs,createdAt,updatedAt');assert d['headSha']==REV and d['headBranch']==BR
  wr(W/'SOURCE_CI_LATEST.json',d)
  current=(d['status'],d['conclusion'])
  if current!=seen:stage('WAITING_FOR_EXISTING_SOURCE_CI',run=RUN,status=d['status'],conclusion=d['conclusion']);seen=current
  if d['status']=='completed':break
  if time.monotonic()-started>7200:raise RuntimeError('Existing source CI still nonterminal after120minutes; no restart')
  time.sleep(45)
 assert d['conclusion']=='success','Source CI is not green: '+d['conclusion']
 assert all(x['conclusion']=='success'for x in d['jobs']),d['jobs']
 trusted=[s for j in d['jobs']for s in j['steps']if s['name']=='Run trusted probes'];assert len(trusted)==1 and trusted[0]['conclusion']=='success'
 wr(W/'SOURCE_CI_GREEN.json',d);stage('SOURCE_CI_GREEN_FRESH_RECONCILIATION')
 assert gs('branch','--show-current')==BR and gs('rev-parse','HEAD')==REV and gs('status','--porcelain')==''
 subprocess.run(['git','fetch','origin'],cwd=R,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==REV;dev=gs('rev-parse','origin/dev');assert dev in [OLDDEV,REV],'Dev advanced outside tested source; reconcile before integration: '+dev
 if dev==OLDDEV:
  subprocess.run(['git','merge-base','--is-ancestor',dev,REV],cwd=R,check=True,capture_output=True)
  stage('PUSHING_FAST_FORWARD_DEV',old_dev=dev,new_dev=REV)
  # Ordinary non-force fast-forward only. A race causes rejection rather than overwriting another editor.
  q=subprocess.run(['git','push','origin',REV+':refs/heads/dev'],cwd=R,capture_output=True);(W/'DEV_PUSH.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
 else:stage('EXACT_SOURCE_ALREADY_ON_DEV_NO_PUSH',dev=dev)
 subprocess.run(['git','fetch','origin','dev'],cwd=R,check=True,capture_output=True);remote=gs('ls-remote','origin','refs/heads/dev').split()[0];assert remote==REV,'Dev moved after integration; inspect ancestry and do not overwrite'
 assert gs('status','--porcelain')==''
 deleted=json.loads((R/'docs/handoffs/codex_flat_vector_art_2026-10-07/r114_geologist_goal_runtime/SOURCE_PIN.json').read_text(encoding='utf-8'))['runtime_deletions']
 for p in deleted:
  q=subprocess.run(['git','cat-file','-e',REV+':'+p],cwd=R,capture_output=True);assert q.returncode!=0,'RetiredSVG path still in runtime source: '+p
 paths=['scripts/opera_career_world_2d.gd','scripts/opera_hotspot_catalog.gd','assets/opera/worlds/props/goal_geologist.tres']+[p for x in json.loads((R/'assets_src/flat_vector_geologist_goal_20261030/DERIVATION.json').read_text(encoding='utf-8'))['exports']for p in[x['path'],x['path']+'.import']];rows=[]
 def verify(p):
  expected=git('show',REV+':'+p);url='https://raw.githubusercontent.com/Ebonyks/mermaid-roshan-reef/'+REV+'/'+urllib.parse.quote(p,safe='/');req=urllib.request.Request(url,headers={'User-Agent':'MermaidReef-anonymous-integration-verifier'})
  with urllib.request.urlopen(req,timeout=90)as response:status=response.status;b=response.read()
  assert status==200 and b==expected,p
  return {'path':p,'revision':REV,'bytes':len(b),'sha256':digest(b),'http_status':status,'anonymous_exact':True}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(verify,paths))
 runs=gh('run','list','--repo','Ebonyks/mermaid-roshan-reef','--branch','dev','--limit','12','--json','databaseId,headSha,status,conclusion,url,workflowName');exact=[x for x in runs if x['headSha']==REV];wr(W/'DEV_WORKFLOW_HANDLES.json',exact)
 result={'state':'PAINTED_GEOLOGIST_GOAL_EXACT_GREEN_SOURCE_FAST_FORWARD_INTEGRATED_DEV','source_revision':REV,'integrated_dev_revision':REV,'prior_dev':OLDDEV,'source_branch':BR,'source_CI_run':RUN,'source_CI_url':d['url'],'source_CI_conclusion':'success','trusted_step':'success','Dev_head_verified_by_anonymous_runtime_bytes_and_git_remote':True,'runtime_files':rows,'retired_runtime_paths_absent_at_integrated_revision':deleted,'access_mode':'Anonymous immutable HTTPS GET without Authorization/cookies, exact bytes/SHA256 for five changed/reused runtime files; Git remote exactDev ref checked separately. The actual full source delivery was previously independently verified.','source_clean':True,'local_dev_master_untouched':True,'PR_created':False,'Dev_workflows':exact,'exact_new_Dev_APK_verified':False,'new_generation_calls':0,'new_native_frame_events':0,'new_implementation_artifact_credits':0,'partial_dev_artifact_credit':1,'whole_role_closed':False,'formal_QA11':None,'device':None,'child':None,'owner':None,'accepted_removed':0,'mission_complete':False,'completed_at_utc':now()};wr(W/'FINAL_RESULT.json',result);stage('TERMINAL_DEV_INTEGRATION_SUCCESS',revision=REV);print('GEOLOGIST_GOAL_DEV_INTEGRATED',REV,flush=True)
except Exception as e:
 wr(W/'STOP.json',{'state':'STOPPED_NO_AUTOMATIC_RETRY','error':str(e),'at_utc':now(),'next':'Inspect sourceCI, current refs and operation state. Never force-push or restart a healthy job.'});stage('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
