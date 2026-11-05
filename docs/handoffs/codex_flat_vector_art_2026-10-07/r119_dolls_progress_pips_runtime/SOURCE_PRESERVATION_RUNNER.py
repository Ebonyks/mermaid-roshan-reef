from pathlib import Path
import json,hashlib,subprocess,datetime,os,sys,time,urllib.request,urllib.parse,concurrent.futures,shutil
U=Path.cwd();S=Path(__file__).parent;H='docs/handoffs/codex_flat_vector_art_2026-10-07';P=U/H/'r119_dolls_progress_pips_runtime';IP=U/'design/audit_impacts/flat-vector-dolls-progress-pips-20261031.json';BASE='218ae766f8e60afb3f6338b8fafce28ec9fab7f2';BR='codex/flat-vector-geologist-pan-runtime-20261017';AUTH='a0bb2cf4691631a534e210a5fb60fd227213322f';REPO='Ebonyks/mermaid-roshan-reef'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def wr(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def wt(p,x):p.write_text(x,encoding='utf-8',newline='\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest(p.read_bytes())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*a):return subprocess.check_output(['git',*a],cwd=U,stderr=subprocess.PIPE)
def gs(*a):return git(*a).decode('utf-8').strip()
def state(n,**kw):wr(S/'SOURCE_PARK_STATE.json',dict(state=n,at_utc=now(),**kw))
def gate(name,cmd):
 q=subprocess.run(cmd,cwd=U,capture_output=True,env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8'));b=q.stdout+q.stderr;(S/(name+'.log')).write_bytes(b);assert q.returncode==0,b.decode('utf-8',errors='replace')[-3000:];return dict(gate=name,exit_code=0,command=cmd,log_sha256=digest(b))
def fetch(rev,path):
 req=urllib.request.Request('https://raw.githubusercontent.com/'+REPO+'/'+rev+'/'+urllib.parse.quote(path,safe='/'),headers={'User-Agent':'MermaidReef-anonymous-preservation-verifier'})
 for i in range(5):
  try:
   with urllib.request.urlopen(req,timeout=90)as q:return q.status,q.read()
  except Exception:
   if i==4:raise
   time.sleep(2*(i+1))
try:
 assert not(S/'SOURCE_PARK_FINAL.json').exists() and gs('rev-parse','HEAD')==BASE and gs('branch','--show-current')==BR
 v=rd(S/'full_validation_chapter2_child_recovery/FINAL_RESULT.json');assert v['status']=='PASS_ALL_82_AND_CURRENT_STATIC'and v['probe_count']==82 and all(x['exit_code']==0 and not x['failure_lines']for x in v['results'])and v['normal_unchanged']and not v['runtime_changes']
 assert rd(S/'PUBLICATION_CH2DIAG_STOP.json')['error']=='Topic/Dev advanced: stop for exactsource reconciliation'
 state('PRESERVING_ALREADY_COMPLETED_CANDIDATE_UNDER_EXPLICIT_OWNER_DEMO_FREEZE')
 delta=gs('diff','--name-only',BASE+'..'+AUTH).splitlines();runtime_delta=[x for x in delta if x.startswith(('scripts/','scenes/','assets/','tools/','.github/'))or x=='project.godot'];assert not runtime_delta
 decisions=json.loads(git('show',AUTH+':audit/cycles/demo-readiness-20261031/owner_answers.json'));freeze=next(x for x in decisions if x['id']=='ODR-DEMO-FREEZE-20261031')
 disposition=dict(state='PARKED_SOURCE_CANDIDATE_DO_NOT_MERGE_DEV_DURING_DEMO_FREEZE',decision_id=freeze['id'],recorded_owner_decision=freeze,authority_revision=AUTH,authority_url='https://github.com/'+REPO+'/blob/'+AUTH+'/docs/handoffs/codex_demo_readiness_2026-10-31/README.md#3-freeze-rules',exact_scope_quote='Park, do not merge: the flat-vector art campaign after R118. Parked work loses nothing; it resumes after the demo.',source_task_baseline=BASE,incoming_dev_at_discovery=AUTH,incoming_changed_files=delta,incoming_runtime_engine_tool_or_workflow_changes=runtime_delta,Dev_integrated=False,new_partial_Dev_artifact_credits=0,existing_partial_Dev_artifacts=20,existing_Dev_art_source=BASE,preservation_only=True,no_new_art_after_freeze_discovery=True,all82_local_zero_exits=True,exact_source_CI='May run automatically after workbranch push; not integration or creative acceptance.',formal_QA11=None,device=None,child=None,owner=None,whole_role_closed=False,accepted_removed=0,mission_complete=False,at_utc=now())
 wr(P/'DEMO_FREEZE_DISPOSITION.json',disposition);shutil.copy2(S/'PUBLICATION_CH2DIAG_STOP.json',P/'ORIGINAL_PUBLICATION_FRESHNESS_STOP.json');shutil.copy2(Path(__file__),P/'SOURCE_PRESERVATION_RUNNER.py')
 text=(P/'README.md').read_text(encoding='utf-8');text='# PARKED after R118 for the owner-approved demo freeze\n\n'+text+'\n[Owner freeze disposition](DEMO_FREEZE_DISPOSITION.json): the owner-approved demo plan explicitly parks the flat-vector campaign afterR118. This preserves the already-produced R119 empty/filled artwork, runtime candidate, native review and passing82probes on its established work branch. It is not merged toDev and earns0newDev credits. No new art or runtime edits follow freeze discovery. ExactsourceCI may run automatically; its result grants no integration or creative acceptance. The mission remains unfinished and is parked until the owner resumes it after the demo.\n';text=text.replace('Exact source CI, normalDev integration and anonymously byte-verified immutable source/canonical delivery remain pending.','Source preservation is being published and anonymously verified; Dev integration is held by the explicit demo freeze. Exact source CI and formal/external acceptance remain separate.')
 wt(P/'README.md',text);status=rd(P/'STATUS.json');status.update(state=disposition['state'],parked=True,freeze_decision_id=freeze['id'],Dev_integrated=False,new_partial_Dev_artifact_credits=0,source_CI=None,preservation_only=True);wr(P/'STATUS.json',status)
 # Annotate current task facts without rewriting historical gates or owner records.
 master=U/'audit/MASTER_AUDIT_2026-08-09.md';lines=master.read_text(encoding='utf-8').splitlines();i=next(i for i,l in enumerate(lines)if l.startswith('| Full-game flat-vector audit |'));lines[i]=lines[i][:-1]+' R119 preserved on workbranch only; parked afterR118 under [owner demo freeze](https://github.com/'+REPO+'/blob/'+AUTH+'/docs/handoffs/codex_demo_readiness_2026-10-31/README.md#3-freeze-rules),0newDev credit. |';wt(master,'\n'.join(lines)+'\n')
 ledger=U/'design/05_DOC_LEDGER.md';text=ledger.read_text(encoding='utf-8');needle='| `'+P.relative_to(U).as_posix()+'/README.md`';lines=text.splitlines();i=next(i for i,l in enumerate(lines)if l.startswith(needle));lines[i]=lines[i][:-1]+' PARKED source preservation underODR-DEMO-FREEZE-20261031; noDev integration. |';wt(ledger,'\n'.join(lines)+'\n')
 active=U/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=active.read_text(encoding='utf-8');i=text.index('R119 boundedproduction2026-10-31:');j=text.index('\n',i);wt(active,text[:j]+' Completed local82zero exits/currentstatic/native342checks are preserved on the workbranch; owner demo freeze parks campaign afterR118,0newDev credit. Existing lifecycle/acceptance gaps remain open.'+text[j:])
 ch=U/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';wt(ch,ch.read_text(encoding='utf-8')+'\nCHG-125 preservation under owner demo freeze2026-10-31: localall82zeroexits/currentstatic/current2D/no source drift/normal11unchanged are retained for completedR119 candidate. ODR-DEMO-FREEZE-20261031 at immutable'+AUTH+' explicitly parks this campaign afterR118. Publish existing work and provenance on the owned source branch only;0newDev credit,no new generation or runtime changes after freeze discovery,formal/external/global remainOPEN.\n')
 oldbinding=rd(P/'DELIVERY_SOURCE_BINDING.json');pin=rd(S/'SOURCE_PIN.json');assert len(oldbinding['files'])==len(pin['runtime_hashes'])==5006
 # Verify unchanged indexed runtime in one Git-index read instead of repeating5006Git-show calls.
 index={}
 for entry in git('ls-files','--stage','-z').split(b'\0'):
  if not entry:continue
  meta,path=entry.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';index[path.decode()]=(mode,oid)
 checked=[]
 for i,row in enumerate(oldbinding['files']):
  path=row['path'];b=(U/path).read_bytes();assert digest(b)==row['current_filesystem_sha256'],path
  blob=b if digest(b)==row['staged_blob_sha256']else b.replace(b'\r\n',b'\n');assert digest(blob)==row['staged_blob_sha256'],path
  oid=hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest();assert index[path][1]==oid,path;checked.append(path+'\0'+oid+'\0'+row['staged_blob_sha256'])
  if i%500==0:state('VERIFYING_EXISTING_TESTED_RUNTIME_BINDING_NO_ENGINE_RESTART',checked=i+1,total=5006)
 assert all(x not in index and not(U/x).exists()for x in pin['runtime_deletions'])
 wr(P/'PRESERVATION_RUNTIME_REUSE.json',dict(state='ALL5006_TESTED_RUNTIME_FILES_EXACT_CURRENT_INDEX_BLOBS',files_checked=5006,source_pin_sha256=sha(S/'SOURCE_PIN.json'),original_delivery_source_binding_sha256=sha(P/'DELIVERY_SOURCE_BINDING.json'),sorted_runtime_index_and_blob_sha256=digest('\n'.join(sorted(checked)).encode()),runtime_or_pixels_changed=False,engine_native_or82probes_restarted=False,reason='Only freeze/preservation metadata changes. IncomingDev13files are documentation/ownerdecisions only; source remains the exact tested candidate, intentionally parked without merging.',at_utc=now()))
 previous=rd(P/'MANIFEST.json');own={x['path']for x in previous['files']if not x.get('revision')};own|={f.relative_to(U).as_posix()for f in P.rglob('*')if f.is_file()}|{IP.relative_to(U).as_posix(),(P/'MANIFEST.json').relative_to(U).as_posix()}
 d=rd(IP);d['scope']+=' Preservation-only update underODR-DEMO-FREEZE-20261031: park completedR119 afterR118 on workbranch,do not mergeDev,no newart/runtime changes; retain passed machine/native evidence.';d['files']=sorted(own-{IP.relative_to(U).as_posix()});d['acceptance_gaps']+=' Dev integration held by owner demo freeze; sourceCI/creative acceptance remain separate.';wr(IP,d)
 files=sorted(own-{(P/'MANIFEST.json').relative_to(U).as_posix()});subprocess.run(['git','add','-f','--',*files],cwd=U,check=True,capture_output=True);assert not gs('diff','--name-only')
 # Rebuild only actual current payload rows; unchanged same-scene references stay immutable.
 rows=[]
 for path in files:
  b=git('show',':'+path);rows.append(dict(revision=None,path=path,bytes=len(b),sha256=digest(b),role='Parked R119 completed candidate/provenance/native/machine/freeze preservation payload'))
 rows += [x for x in previous['files']if x.get('revision')]
 for path in ['docs/handoffs/codex_demo_readiness_2026-10-31/README.md','audit/cycles/demo-readiness-20261031/owner_answers.json']:
  b=git('show',AUTH+':'+path);rows.append(dict(revision=AUTH,path=path,bytes=len(b),sha256=digest(b),role='Exact owner-approved demo freeze authority; explicitly parks flat-vector campaign afterR118'))
 manifest=dict(previous);manifest.update(state=disposition['state'],files=rows,required_files=len(rows),required_bytes=sum(x['bytes']for x in rows),Dev_integrated=False,new_partial_Dev_artifact_credits=0,freeze_decision_id=freeze['id'],freeze_authority_revision=AUTH,preservation_only=True,sourceCI_required_before_future_integration=True);wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',(P/'MANIFEST.json').relative_to(U).as_posix()],cwd=U,check=True,capture_output=True)
 state('RUNNING_PRESERVATION_METADATA_PRECOMMIT_GATES_NO_ENGINE_RESTART');gates=[]
 for name,cmd in [('PARK_PARSER',[sys.executable,'-m','gdtoolkit.parser','scripts/games/dolls.gd','scripts/opera_career_world_2d.gd',str(P/'capture_progress.gd'),str(P/'geologist_rest_repair/capture_geologist_rest.gd')]),('PARK_INFERENCE',[sys.executable,'-B','tools/lint_inference.py','scripts/games/dolls.gd','scripts/opera_career_world_2d.gd']),('PARK_AUTHORITY',[sys.executable,'-B','tools/audit_document_authority.py']),('PARK_DEVELOPMENT',[sys.executable,'-B','tools/audit_development.py','--base','auto'])]:gates.append(gate(name,cmd))
 wr(S/'SOURCE_PARK_PRECOMMIT_GATES.json',gates);assert not gs('diff','--name-only');subprocess.run(['git','fetch','origin'],cwd=U,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE and gs('rev-parse','HEAD')==BASE
 subprocess.run(['git','commit','-m','Preserve PARKED R119 painted progress candidate under owner demo freeze'],cwd=U,check=True,capture_output=True);rev=gs('rev-parse','HEAD');assert not gs('status','--porcelain');state('PARKED_SOURCE_COMMITTED_PUSH_PENDING',source_revision=rev)
 subprocess.run(['git','push','origin',BR],cwd=U,check=True,capture_output=True);state('PARKED_SOURCE_PUSHED_ANONYMOUS_VERIFICATION',source_revision=rev)
 mp=(P/'MANIFEST.json').relative_to(U).as_posix();expected=git('show',rev+':'+mp);status,b=fetch(rev,mp);assert status==200 and b==expected
 def verify(row):
  rr=row['revision']or rev;status,b=fetch(rr,row['path']);assert status==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return dict(row,revision=rr,http_status=status,verified=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 receipt=dict(schema='reef.remote_delivery_verification/1',state='ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED_PARKED_SOURCE_ONLY',repository=REPO,revision=rev,manifest=mp,manifest_sha256=digest(expected),manifest_bytes=len(expected),required_files=len(rows),required_bytes=manifest['required_bytes'],files=verified,access_mode='Anonymous immutable HTTPS GET without Authorization/cookies; exactbytes/SHA256 manifest/everyrequiredfile.',checked_at_utc=now(),Dev_integrated=False,freeze_decision_id=freeze['id'],creative_acceptance=False);wr(S/'SOURCE_PARK_REMOTE_VERIFICATION.json',receipt)
 runs=json.loads(subprocess.check_output(['gh','run','list','--repo',REPO,'--branch',BR,'--limit','10','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=U,text=True,encoding='utf-8'));exact=[x for x in runs if x['headSha']==rev];wr(S/'SOURCE_PARK_CI_HANDLES.json',exact)
 final=dict(state='PARKED_R119_SOURCE_PRESERVED_ANONYMOUSLY_VERIFIED_NO_DEV',source_revision=rev,branch=BR,manifest=mp,required_files=len(rows),required_bytes=manifest['required_bytes'],source_CI=exact,Dev_integrated=False,new_Dev_credits=0,source_clean=True,freeze_decision_id=freeze['id'],authority_revision=AUTH,all82_local_pass=True,new_generation_calls=0,new_frame_events=0,accepted_removed=0,mission_complete=False,completed_at_utc=now());wr(S/'SOURCE_PARK_FINAL.json',final);state('TERMINAL_PARKED_SOURCE_PRESERVATION_SUCCESS',source_revision=rev);print('R119_PARKED_SOURCE_PRESERVED',rev,len(rows),flush=True)
except Exception as e:wr(S/'SOURCE_PARK_STOP.json',dict(state='PRESERVATION_STOP_INSPECT_EXACT_HANDLE_NO_RESTART',error=str(e),at_utc=now()));state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
