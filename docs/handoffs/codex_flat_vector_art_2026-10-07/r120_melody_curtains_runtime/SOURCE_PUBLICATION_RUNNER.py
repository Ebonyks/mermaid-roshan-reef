from delivery_common import *
import shutil

P = U/REL
IP = U/'design/audit_impacts/flat-vector-melody-curtains-20261101.json'
W = S/'full_validation_audit_contract_recovery'
try:
    assert not (S/'SOURCE_FINAL.json').exists(), 'Resume recorded publication, never duplicate it'
    v = rd(W/'FINAL_RESULT.json')
    assert v['status'] == 'PASS_ALL82_CURRENT_STATIC_ANALYZER_2D' and v['probe_count'] == v['passed_count'] == 82
    assert all(x['exit_code'] == 0 and not x['timed_out'] and not x['failure_lines'] for x in v['results'])
    assert v['normal_unchanged'] and not v['runtime_changes']
    assert rd(W/'STATIC_RESULT.json')['state'] == 'PASS'
    assert gs(U,'rev-parse','HEAD') == SOURCE_BASE and gs(U,'branch','--show-current') == SOURCE_BRANCH
    assert rd(P/'OWNER_RESUME.json')['quote'] == 'Resume art candidates; keep Dev frozen'
    state('SOURCE', 'ASSEMBLING_VERIFIED_SOURCE_CANDIDATE_NO_DEV')
    copies = {
        S/'SOURCE_PIN.json': 'ORIGINAL_VALIDATION_PIN.json',
        S/'full_validation/analyzer/engine.log': 'ORIGINAL_MELODY_ANALYZER.log',
        W/'REFRESHED_STATIC_GATES.json': 'REFRESHED_TEST_CORRECTION_GATES.json',
        W/'RECOVERY_BASIS.json': 'FULL_VALIDATION_RECOVERY_BASIS.json',
        S/'SOURCE_PIN_AUDIT_RECOVERY.json': 'SOURCE_PIN.json',
        S/'SOURCE_CAPTURE_FIXTURE_EXACT.gd.txt': 'SOURCE_CAPTURE_FIXTURE_EXACT.gd.txt',
        S/'SOURCE_FIXTURE_RECONSTRUCTION.json': 'SOURCE_FIXTURE_RECONSTRUCTION.json',
        W/'FINAL_RESULT.json': 'LOCAL_82_RESULT.json', W/'LAUNCH.json': 'FULL_VALIDATION_LAUNCH.json',
        W/'STATIC_RESULT.json': 'STATIC_RESULT.json', W/'STATIC_PREFIX.log': 'STATIC_PREFIX.log',
        W/'GAME2D.log': 'GAME2D.log', W/'analyzer/engine.log': 'CHANGED_PROBE_ANALYZER.log',
        Path(__file__): 'SOURCE_PUBLICATION_RUNNER.py', S/'delivery_common.py': 'delivery_common.py'}
    for src,dst in copies.items(): shutil.copy2(src,P/dst)
    shutil.copy2(W/'LAUNCH.json',P/'RECOVERY_LAUNCH_RAW.json')
    launch=rd(P/'FULL_VALIDATION_LAUNCH.json');launch['original_attempt_native_reuse_declaration']=launch['native_reused'];launch['native_reused']=dict(checks=96,frames=6,all_rendering_inputs_unchanged=True,only_updated_tests=['scripts/probe_melody.gd','scripts/probe_audit.gd']);launch['clarification']='Raw inherited launch retained in RECOVERY_LAUNCH_RAW.json; exact current scope is the two-test delta in FULL_VALIDATION_RECOVERY_BASIS.json.';wr(P/'FULL_VALIDATION_LAUNCH.json',launch)
    log_index = []; joined = bytearray()
    for row in v['results']:
        raw = Path(row['log']).read_bytes(); assert digest(raw) == row['log_sha256']
        joined.extend(('\nR120 ORIGINAL TRUSTED PROBE SCRIPT NAME: '+row['probe']+'\n').encode())
        offset = len(joined); joined.extend(raw)
        log_index.append(dict(probe=row['probe'], offset=offset, bytes=len(raw), sha256=digest(raw), exit_code=0,
            command=row['command'], elapsed_seconds=row['elapsed_seconds']))
    assert len(joined) < 90*1024*1024
    (P/'TRUSTED_PROBES.log').write_bytes(joined)
    wr(P/'TRUSTED_LOG_INDEX.json',dict(container='TRUSTED_PROBES.log',container_sha256=digest(joined),
        count=82, logs=log_index, note='Raw stdout/stderr bytes retained at exact offsets; 80 other probe scripts unchanged; Melody and full-game curtain art assertions updated as declared. One original failed full-game assertion is retained separately.'))
    status = dict(state='PASS_ALL82_CURRENT_STATIC_ANALYZER_2D', local_probe_count=82, all_exit_zero=True,
        exact_engine='4.7.2.stable.official.ed1daf0bf', native_source_checks=69, native_candidate_checks=96,
        effective_native_checks=165, excluded_fixture_checks=54, native_frames=dict(bounded=12,excluded=6,retained=18),
        normal_unchanged=True, source_drift=[], source_CI='PENDING_AUTOMATIC_EXACT_SOURCE_RUN',
        Dev_integrated=False, formal_QA11=None, device=None, child=None, owner=None,
        natural_route_complete=False, accepted_removed=0, whole_role_closed=False, mission_complete=False)
    status.update(test_art_contract_recovery=True,retained_original_passes=3,original_failed_attempts=1,executed_probe_attempts_total=83,unique_passing_probe_scripts=82)
    wr(P/'VALIDATION_STATUS.json', status)
    text=(P/'README.md').read_text(encoding='utf-8')
    text=text.replace('The current full static/trusted suite is pending, recorded separately in VALIDATION_STATUS.json.',
        'The current full static prefix, real Godot analyzer, 2D regression guard and all 82 trusted probes pass with zero exits; [machine result](LOCAL_82_RESULT.json), [raw logs](TRUSTED_PROBES.log), [log index](TRUSTED_LOG_INDEX.json), and [separate evidence lanes](VALIDATION_STATUS.json). Exact-source CI is recorded after publication and remains separate from Dev integration.')
    text+='\nThe original full-game audit rejected retired-polygon presence assertions. Its failure remains in ORIGINAL_FULL_VALIDATION_FAILURE.json and ORIGINAL_FULL_GAME_AUDIT_FAILURE.log. Only those two art terms were replaced with a strict painted-resource predicate;122 other audit methods and all other entry instructions remain exact. The recovery retains three healthy probe results and the successful complete static/2D/native evidence, then runs the corrected full-game probe and remaining78 original scripts. No gameplay or pixels changed. See FULL_GAME_ART_CONTRACT_CORRECTION.json and FULL_VALIDATION_RECOVERY_BASIS.json.\n'
    wt(P/'README.md',text)
    ledger=U/'design/05_DOC_LEDGER.md'
    text=ledger.read_text(encoding='utf-8').replace('actual three-aspect native comparison and pending complete machine/external acceptance; owner keeps Dev frozen.',
        'actual three-aspect native comparison and current local82/static/analyzer/2D pass; formal/external acceptance remains open and owner keeps Dev frozen.')
    wt(ledger,text)
    change=U/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md'
    text=change.read_text(encoding='utf-8');assert 'CHG-126' not in text
    text=text.replace('### R120 painted Melody curtain candidate','### CHG-126 — R120 painted Melody curtain candidate')
    text+='\nCHG-126 implementation binding: baseline `'+SOURCE_BASE+'`; actual staged runtime blobs are pinned by `'+REL+'/DELIVERY_SOURCE_BINDING.json` and the containing delivery commit. Exact published source commit is recorded in the canonical R120 SOURCE_FINAL/PAYLOAD_PIN. Paths: `scripts/games/melody.gd`, `scripts/probe_melody.gd`, `scripts/probe_audit.gd`, both `assets/melody/curtain_*_painted.png` plus imports, `'+ART+'/`, and the R120 evidence/impact documents. Benefit: painted cloth replaces flat curtain polygons without changing play. Plausible negative effects: edge clipping, filtering/overdraw, resource growth or an art-contract regression. Dependencies: unchanged six stage/actor images, exact4.7.2 Mobile/Speedy and original memory/coverage ceilings. Evidence: current local82/static/analyzer/2D,165 effective native executed checks and12 inspected effective stills; formal/device/child/owner open. Rollback class: bounded mixed code/assets/art-test contract. Plan read-only from a clean dedicated `codex/rollback-chg-126` branch; inspect the complete coupled diff and stop on conflicts, preserve protected/native/history sources, then earn focused/import/full gates. No one-line partial rollback or Dev action is authorized here.\n'
    wt(change,text)
    # Bind the complete frozen runtime to actual staged Git blobs in one index read.
    initial=changed(U) | {f.relative_to(U).as_posix() for root in [P,U/ART] for f in root.rglob('*') if f.is_file()}; scope_files(initial)
    assert all(p in rd(IP)['files'] or p.startswith(REL+'/') or p==IP.relative_to(U).as_posix() for p in initial), sorted(initial-set(rd(IP)['files']))
    run(U,'git','add','-f','--',*sorted(initial))
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
    wr(S/'SOURCE_AUDIT_RECOVERY_STOP.json',dict(state='STOPPED_INSPECT_EXACT_HANDLE_NO_AUTOMATIC_RETRY',error=str(exc),at_utc=now()))
    state('SOURCE','STOPPED_NO_AUTOMATIC_RETRY',error=str(exc));raise
