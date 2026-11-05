from pathlib import Path
exec((Path(__file__).parent/'preserve_source_for_demo_freeze.py').read_text(encoding='utf-8').split('\ntry:\n',1)[0])
try:
 assert not (S/'SOURCE_PARK_FINAL.json').exists() and gs('rev-parse','HEAD')==BASE and gs('branch','--show-current')==BR
 failure=rd(S/'SOURCE_PARK_STOP.json');assert 'DOC080' in failure['error'] and 'README.md#3-freeze-rules' in failure['error']
 shutil.copy2(S/'SOURCE_PARK_STOP.json',P/'PRESERVATION_NAVIGATION_FAILURE.json');shutil.copy2(S/'PARK_AUTHORITY.log',P/'PRESERVATION_NAVIGATION_FAILURE.log');shutil.copy2(Path(__file__),P/'SOURCE_PRESERVATION_METADATA_RECOVERY.py')
 master=U/'audit/MASTER_AUDIT_2026-08-09.md';text=master.read_text(encoding='utf-8');url='https://github.com/'+REPO+'/blob/'+AUTH+'/docs/handoffs/codex_demo_readiness_2026-10-31/README.md#3-freeze-rules';needle='[owner demo freeze]('+url+')';assert text.count(needle)==1
 text=text.replace(needle,'[owner demo freeze disposition](../'+P.relative_to(U).as_posix()+'/DEMO_FREEZE_DISPOSITION.json)').replace('fresh fullgates pending.','local currentstatic/all82passed; exactsourceCI and formal/external acceptance remain separate.')
 wt(master,text)
 state('RESUMING_ONLY_FAILED_PRESERVATION_METADATA_BOUNDARY_NO_ENGINE_OR_DEV')
 old=rd(P/'DELIVERY_SOURCE_BINDING.json');idx={}
 for entry in git('ls-files','--stage','-z').split(b'\0'):
  if not entry:continue
  meta,path=entry.split(b'\t',1);mode,oid,stage=meta.decode().split();assert stage=='0';idx[path.decode()]=oid
 for row in old['files']:
  b=(U/row['path']).read_bytes();assert digest(b)==row['current_filesystem_sha256'],row['path'];blob=b if digest(b)==row['staged_blob_sha256']else b.replace(b'\r\n',b'\n');assert digest(blob)==row['staged_blob_sha256'];assert hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()==idx[row['path']]
 assert len(old['files'])==5006
 wr(P/'PRESERVATION_METADATA_RECOVERY.json',dict(state='RESUME_FAILED_NAVIGATION_ONLY_5006_RUNTIME_BINDINGS_UNCHANGED',original_failure='PRESERVATION_NAVIGATION_FAILURE.json',original_log='PRESERVATION_NAVIGATION_FAILURE.log',repair='Master navigation links to local disposition, which retains exact immutable owner freeze authority and quote. No checker changes.',healthy_parser_and_inference_reused=True,all82_and_native_not_restarted=True,runtime_files_checked=5006,runtime_or_pixels_changed=False,Dev_integrated=False,at_utc=now()))
 previous=rd(P/'MANIFEST.json');own={x['path']for x in previous['files']if not x.get('revision')};own|={f.relative_to(U).as_posix()for f in P.rglob('*')if f.is_file()}|{IP.relative_to(U).as_posix()}
 d=rd(IP);d['files']=sorted(own-{IP.relative_to(U).as_posix(),(P/'MANIFEST.json').relative_to(U).as_posix()});wr(IP,d)
 files=sorted(own-{(P/'MANIFEST.json').relative_to(U).as_posix()});subprocess.run(['git','add','-f','--',*files],cwd=U,check=True,capture_output=True)
 rows=[]
 for path in files:
  b=git('show',':'+path);rows.append(dict(revision=None,path=path,bytes=len(b),sha256=digest(b),role='Parked R119 completed candidate/provenance/native/machine/freeze preservation payload'))
 rows += [x for x in previous['files']if x.get('revision')]
 manifest=dict(previous);manifest.update(files=rows,required_files=len(rows),required_bytes=sum(x['bytes']for x in rows));wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',(P/'MANIFEST.json').relative_to(U).as_posix()],cwd=U,check=True,capture_output=True)
 gates=[]
 for name in ['PARK_PARSER','PARK_INFERENCE']:
  log=S/(name+'.log');assert log.exists() and log.stat().st_size==0;gates.append(dict(gate=name,exit_code=0,log_sha256=sha(log),reused_original_successful_gate=True))
 gates += [gate('PARK_AUTHORITY_NAVIGATION_RECOVERY',[sys.executable,'-B','tools/audit_document_authority.py']),gate('PARK_DEVELOPMENT_NAVIGATION_RECOVERY',[sys.executable,'-B','tools/audit_development.py','--base','auto'])]
 wr(S/'SOURCE_PARK_PRECOMMIT_GATES.json',gates);assert not gs('diff','--name-only');subprocess.run(['git','fetch','origin'],cwd=U,check=True,capture_output=True);assert gs('rev-parse','origin/'+BR)==BASE and gs('rev-parse','HEAD')==BASE
 subprocess.run(['git','commit','-m','Preserve PARKED R119 painted progress candidate under owner demo freeze'],cwd=U,check=True,capture_output=True);rev=gs('rev-parse','HEAD');assert not gs('status','--porcelain');state('PARKED_SOURCE_COMMITTED_PUSH_PENDING',source_revision=rev)
 subprocess.run(['git','push','origin',BR],cwd=U,check=True,capture_output=True);state('PARKED_SOURCE_PUSHED_ANONYMOUS_VERIFICATION',source_revision=rev)
 mp=(P/'MANIFEST.json').relative_to(U).as_posix();expected=git('show',rev+':'+mp);status,b=fetch(rev,mp);assert status==200 and b==expected
 def verify(row):
  rr=row['revision']or rev;status,b=fetch(rr,row['path']);assert status==200 and len(b)==row['bytes']and digest(b)==row['sha256'],row['path'];return dict(row,revision=rr,http_status=status,verified=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:verified=list(pool.map(verify,rows))
 receipt=dict(schema='reef.remote_delivery_verification/1',state='ALL_REQUIRED_FILES_ANONYMOUSLY_BYTE_VERIFIED_PARKED_SOURCE_ONLY',repository=REPO,revision=rev,manifest=mp,manifest_sha256=digest(expected),manifest_bytes=len(expected),required_files=len(rows),required_bytes=manifest['required_bytes'],files=verified,access_mode='Anonymous immutable HTTPS GET without Authorization/cookies; exactbytes/SHA256 manifest/everyrequiredfile.',checked_at_utc=now(),Dev_integrated=False,freeze_decision_id='ODR-DEMO-FREEZE-20261031',creative_acceptance=False);wr(S/'SOURCE_PARK_REMOTE_VERIFICATION.json',receipt)
 runs=json.loads(subprocess.check_output(['gh','run','list','--repo',REPO,'--branch',BR,'--limit','10','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=U,text=True,encoding='utf-8'));exact=[x for x in runs if x['headSha']==rev];wr(S/'SOURCE_PARK_CI_HANDLES.json',exact)
 final=dict(state='PARKED_R119_SOURCE_PRESERVED_ANONYMOUSLY_VERIFIED_NO_DEV',source_revision=rev,branch=BR,manifest=mp,required_files=len(rows),required_bytes=manifest['required_bytes'],source_CI=exact,Dev_integrated=False,new_Dev_credits=0,source_clean=True,freeze_decision_id='ODR-DEMO-FREEZE-20261031',authority_revision=AUTH,all82_local_pass=True,new_generation_calls=0,new_frame_events=0,accepted_removed=0,mission_complete=False,completed_at_utc=now());wr(S/'SOURCE_PARK_FINAL.json',final);state('TERMINAL_PARKED_SOURCE_PRESERVATION_SUCCESS',source_revision=rev);print('R119_PARKED_SOURCE_PRESERVED',rev,len(rows),flush=True)
except Exception as e:wr(S/'SOURCE_PARK_RECOVERY_STOP.json',dict(state='PRESERVATION_RECOVERY_STOP_INSPECT_EXACT_BOUNDARY',error=str(e),at_utc=now()));state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
