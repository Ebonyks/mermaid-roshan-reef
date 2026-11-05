from delivery_common import *
import shutil
P=U/REL
IP=U/'design/audit_impacts/flat-vector-melody-curtains-20261101.json'
W=S/'full_validation_audit_contract_recovery'
try:
    assert not(S/'SOURCE_FINAL.json').exists()
    assert gs(U,'rev-parse','HEAD')==SOURCE_BASE and gs(U,'branch','--show-current')==SOURCE_BRANCH
    failure=rd(S/'SOURCE_AUDIT_RECOVERY_STOP.json')
    assert failure['error']=="'assets/melody/curtain_left_painted.png.import'"
    assert rd(W/'FINAL_RESULT.json')['status']=='PASS_ALL82_CURRENT_STATIC_ANALYZER_2D'
    assert '### CHG-126' in (U/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md').read_text(encoding='utf-8')
    assert not(P/'DELIVERY_SOURCE_BINDING.json').exists()
    pin=rd(S/'SOURCE_PIN_AUDIT_RECOVERY.json')
    imports=['assets/melody/curtain_left_painted.png.import','assets/melody/curtain_right_painted.png.import']
    assert all(sha(U/p)==pin['runtime_hashes'][p] for p in imports)
    shutil.copy2(S/'SOURCE_AUDIT_RECOVERY_STOP.json',P/'SOURCE_PUBLICATION_IMPORT_STAGING_FAILURE.json')
    shutil.copy2(Path(__file__),P/'SOURCE_PUBLICATION_IMPORT_STAGE_RECOVERY_RUNNER.py')
    wr(P/'SOURCE_PUBLICATION_IMPORT_STAGE_RECOVERY.json',dict(state='EXACT_TESTED_IMPORT_SIDECARS_EXPLICITLY_STAGED',
        reason='New .png.import files were excluded by Git ignore from the initial untracked-file census. Missing index entries stopped publication before commit.',
        files=[dict(path=p,sha256=sha(U/p))for p in imports],runtime_or_pixel_changes=False,
        engine_or_native_restarts=False,original_failure_preserved=True,at_utc=now()))
    run(U,'git','add','-f','--',*imports)
    state('SOURCE','RESUMING_AT_ACTUAL_TESTED_INDEX_BINDING_WITH_EXPLICIT_IMPORTS')
    idx=index(U); pin=rd(S/'SOURCE_PIN_AUDIT_RECOVERY.json'); bindings=[]
    for n,(path,expected) in enumerate(sorted(pin['runtime_hashes'].items())):
        raw=(U/path).read_bytes(); assert digest(raw)==expected,path
        mode,oid=idx[path]; blob=raw
        def object_id(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        normalization='raw bytes exact'
        if object_id(blob)!=oid:
            blob=raw.replace(b'\r\n',b'\n'); normalization='CRLF-to-LF text only'
        assert object_id(blob)==oid,path
        bindings.append(dict(path=path,current_filesystem_sha256=expected,staged_blob_sha256=digest(blob),git_blob=oid,mode=mode,normalization=normalization))
        if n%750==0:state('SOURCE','BINDING_TESTED_RUNTIME_TO_ACTUAL_INDEX',checked=n+1,total=len(pin['runtime_hashes']))
    assert all(p not in idx and not(U/p).exists() for p in pin['runtime_deletions'])
    wr(P/'DELIVERY_SOURCE_BINDING.json',dict(state='ALL_FROZEN_RUNTIME_FILES_MATCH_ACTUAL_STAGED_BLOBS',
        source_baseline=SOURCE_BASE, source_pin_sha256=sha(S/'SOURCE_PIN_AUDIT_RECOVERY.json'),files=bindings,count=len(bindings),
        runtime_or_pixels_changed_after_validation=False, all82_restarted=False, Dev_integrated=False))
    # A bounded delivery: new material and the six existing stage/actor resources, never the historical archive.
    snapshot=rd(P/'candidate/1280x720/RESULT.json')['captures'][0]['stage_snapshot']
    ref_paths=[p.removeprefix('res://') for p in snapshot['tile_paths']+[snapshot['daddy_path'],snapshot['roshan_path']]]
    assert len(ref_paths)==6
    reference_paths=sorted(ref_paths+[p+'.import' for p in ref_paths])
    wt(P/'MANIFEST.json','{}\n')
    own=changed(U) | {f.relative_to(U).as_posix() for root in [P,U/ART] for f in root.rglob('*') if f.is_file()}; scope_files(own)
    impact=rd(IP); impact['files']=sorted(own-{IP.relative_to(U).as_posix()})
    impact['change_record']='audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md#chg-126--r120-painted-melody-curtain-candidate'
    impact['validation'][2]=dict(command='Current complete static prefix, exact Godot analyzer, 2D regression guard and all82 trusted probes',result='PASS',evidence=REL+'/LOCAL_82_RESULT.json; STATIC_RESULT.json; CHANGED_PROBE_ANALYZER.log; GAME2D.log; DELIVERY_SOURCE_BINDING.json')
    impact['validation'].append(dict(command='Exact-source CI / formalQA11 / device / child / owner',result='PENDING',evidence=REL+'/VALIDATION_STATUS.json; sourceCI tracked separately; Dev explicitly held'))
    wr(IP,impact)
    run(U,'git','add','-f','--',*sorted(own))
    rows=payload_rows(U,own-{REL+'/MANIFEST.json'})
    for path,b in blobs(U,reference_paths).items(): rows.append(dict(revision=SOURCE_BASE,path=path,bytes=len(b),sha256=digest(b),role='Unchanged actual Melody stage/actor source and import setting; bounded same-scene reference'))
    manifest=dict(schema='reef.runtime_trial_delivery/1',revision=REVISION,source_baseline=SOURCE_BASE,
        state='PAINTED_CURTAIN_SOURCE_CANDIDATE_DEV_FROZEN',files=rows,required_files=len(rows),required_bytes=sum(r['bytes'] for r in rows),
        owner_scope='Resume art candidates; keep Dev frozen',runtime_binding=REL+'/DELIVERY_SOURCE_BINDING.json',
        new_bounded_source_artifacts=1,existing_named_roles=2,new_roles=0,new_families=0,
        generation_calls=2,animation_calls=0,new_frame_events=dict(bounded=12,excluded=6,retained=18),
        Dev_integrated=False,formal_QA11=None,device=None,child=None,owner=None,accepted_removed=0,mission_complete=False)
    wr(P/'MANIFEST.json',manifest);run(U,'git','add','--',REL+'/MANIFEST.json')
    state('SOURCE','FINAL_METADATA_GATES_NO_ENGINE_RESTART')
    gates=document_gates(U,'SOURCE_FINAL')
    gates += [gate(U,'SOURCE_PARSER',[sys.executable,'-m','gdtoolkit.parser','scripts/games/melody.gd','scripts/probe_melody.gd','scripts/probe_audit.gd',str(P/'capture_curtains.gd')]),
        gate(U,'SOURCE_INFERENCE',[sys.executable,'-B','tools/lint_inference.py','scripts/games/melody.gd','scripts/probe_melody.gd','scripts/probe_audit.gd'])]
    wr(S/'SOURCE_PRECOMMIT_GATES.json',gates)
    assert not gs(U,'diff','--name-only')
    run(U,'git','fetch','origin')
    assert gs(U,'rev-parse','HEAD')==SOURCE_BASE and gs(U,'branch','--show-current')==SOURCE_BRANCH
    assert not gs(U,'ls-remote','--heads','origin','refs/heads/'+SOURCE_BRANCH),'Topic already published: inspect exact handle'
    run(U,'git','commit','-m','Replace Melody curtain polygons with painted storybook source candidates; Dev frozen')
    rev=gs(U,'rev-parse','HEAD');state('SOURCE','COMMITTED_PUSH_PENDING',source_revision=rev)
    assert not gs(U,'status','--porcelain')
    run(U,'git','push','-u','origin',SOURCE_BRANCH)
    state('SOURCE','PUSHED_VERIFYING_ANONYMOUS_IMMUTABLE_MANIFEST',source_revision=rev)
    receipt=verify_manifest(U,rev,REL+'/MANIFEST.json',manifest);wr(S/'SOURCE_REMOTE_VERIFICATION.json',receipt)
    q= subprocess.run(['gh','run','list','--repo',REPO,'--branch',SOURCE_BRANCH,'--limit','10','--json','databaseId,headSha,status,conclusion,url,workflowName'],cwd=U,capture_output=True,text=True,encoding='utf-8',check=True)
    runs=[x for x in json.loads(q.stdout) if x['headSha']==rev];wr(S/'SOURCE_CI_HANDLES.json',runs)
    out=dict(state='R120_SOURCE_PUBLISHED_EVERY_REQUIRED_FILE_ANONYMOUSLY_VERIFIED',source_revision=rev,
        source_branch=SOURCE_BRANCH,manifest=REL+'/MANIFEST.json',required_files=len(rows),required_bytes=manifest['required_bytes'],
        source_clean=True,all82_local_pass=True,source_CI=runs,Dev_integrated=False,new_Dev_credits=0,
        accepted_removed=0,mission_complete=False,completed_at_utc=now())
    wr(S/'SOURCE_FINAL.json',out);state('SOURCE','TERMINAL_SOURCE_PUBLICATION_SUCCESS',source_revision=rev)
    print('R120_SOURCE_DELIVERED',rev,len(rows),flush=True)
except Exception as exc:
    wr(S/'SOURCE_IMPORT_STAGE_RECOVERY_STOP.json',dict(state='STOPPED_INSPECT_EXACT_HANDLE_NO_AUTOMATIC_RETRY',error=str(exc),at_utc=now()))
    state('SOURCE','STOPPED_NO_AUTOMATIC_RETRY',error=str(exc));raise
