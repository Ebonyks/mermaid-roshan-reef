from pathlib import Path
exec((Path(__file__).parent/'preserve_source_for_demo_freeze.py').read_text(encoding='utf-8').split('\ntry:\n',1)[0])
try:
 assert not(S/'SOURCE_PARK_FINAL.json').exists() and gs('rev-parse','HEAD')==BASE and gs('branch','--show-current')==BR
 failure=rd(S/'SOURCE_PARK_RECOVERY_STOP.json');assert 'no changed audit-impact record covers' in failure['error'] and 'MANIFEST.json' in failure['error']
 shutil.copy2(S/'SOURCE_PARK_RECOVERY_STOP.json',P/'PRESERVATION_COVERAGE_FAILURE.json');shutil.copy2(S/'PARK_DEVELOPMENT_NAVIGATION_RECOVERY.log',P/'PRESERVATION_COVERAGE_FAILURE.log');shutil.copy2(Path(__file__),P/'SOURCE_PRESERVATION_COVERAGE_RECOVERY.py')
 state('RESUMING_FAILED_MANIFEST_IMPACT_COVERAGE_ONLY_NO_ENGINE_NO_DEV')
 binding=rd(P/'DELIVERY_SOURCE_BINDING.json');assert len(binding['files'])==5006
 for row in binding['files']:assert sha(U/row['path'])==row['current_filesystem_sha256'],row['path']
 wr(P/'PRESERVATION_COVERAGE_RECOVERY.json',dict(state='INCLUDE_ACTUAL_MANIFEST_IN_FULL_CHANGED_FILE_COVERAGE',original_failure='PRESERVATION_COVERAGE_FAILURE.json',original_log='PRESERVATION_COVERAGE_FAILURE.log',repair='Restore MANIFEST.json in impact files coverage. No runtime, artwork, metadata gate, or acceptance requirement changed.',all5006_runtime_files_unchanged=True,all82_native_not_restarted=True,Dev_integrated=False,at_utc=now()))
 manifest=rd(P/'MANIFEST.json');new=[(P/n).relative_to(U).as_posix()for n in['PRESERVATION_COVERAGE_FAILURE.json','PRESERVATION_COVERAGE_FAILURE.log','SOURCE_PRESERVATION_COVERAGE_RECOVERY.py','PRESERVATION_COVERAGE_RECOVERY.json']];mp=(P/'MANIFEST.json').relative_to(U).as_posix();ip=IP.relative_to(U).as_posix();own={r['path']for r in manifest['files']if not r.get('revision')}|set(new)|{mp,ip};impact=rd(IP);impact['files']=sorted(own-{ip});wr(IP,impact)
 subprocess.run(['git','add','-f','--',ip,*new],cwd=U,check=True,capture_output=True)
 current={r['path']:r for r in manifest['files']if not r.get('revision')}
 for path in[ip,*new]:
  b=git('show',':'+path);current[path]=dict(revision=None,path=path,bytes=len(b),sha256=digest(b),role='Parked R119 complete preservation/failed metadata gate recovery')
 rows=[current[p]for p in sorted(current)]+[r for r in manifest['files']if r.get('revision')];manifest.update(files=rows,required_files=len(rows),required_bytes=sum(x['bytes']for x in rows));wr(P/'MANIFEST.json',manifest);subprocess.run(['git','add','--',mp],cwd=U,check=True,capture_output=True)
 gates=[]
 for name in ['PARK_PARSER','PARK_INFERENCE']:
  log=S/(name+'.log');assert log.exists()and log.stat().st_size==0;gates.append(dict(gate=name,exit_code=0,log_sha256=sha(log),reused_original_successful_gate=True))
 gates += [gate('PARK_AUTHORITY_COVERAGE_RECOVERY',[sys.executable,'-B','tools/audit_document_authority.py']),gate('PARK_DEVELOPMENT_COVERAGE_RECOVERY',[sys.executable,'-B','tools/audit_development.py','--base','auto'])]
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
except Exception as e:wr(S/'SOURCE_PARK_COVERAGE_STOP.json',dict(state='PRESERVATION_COVERAGE_STOP_INSPECT_EXACT_BOUNDARY',error=str(e),at_utc=now()));state('STOPPED_NO_AUTOMATIC_RETRY',error=str(e));raise
