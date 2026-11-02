from delivery_common import *
import shutil

P=R/REL; UP=U/REL; C=R/H/'r96_geologist_mineral_candidate'
IP=R/'design/audit_impacts/flat-vector-r120-melody-curtains-20261101.json'
IDS=['FV-4ED0A2885065','FV-FD33A7BF6E0A']
try:
    assert not(S/'CANONICAL_FINAL.json').exists(), 'Resume recorded publication, never duplicate it'
    source=rd(S/'SOURCE_FINAL.json'); remote=rd(S/'SOURCE_REMOTE_VERIFICATION.json'); SRC=source['source_revision']
    assert source['source_clean'] and not source['Dev_integrated'] and remote['revision']==SRC and all(x['verified'] for x in remote['files'])
    assert gs(R,'rev-parse','HEAD')==CANON_BASE and gs(R,'branch','--show-current')==CANON_BRANCH and not gs(R,'status','--porcelain')
    run(R,'git','fetch','origin'); assert gs(R,'rev-parse','origin/'+CANON_BRANCH)==CANON_BASE
    assert not P.exists(), 'Canonical packet exists: inspect exact prepared state'
    frozen={n:sha(R/H/n) for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']}
    state('CANONICAL','PREPARING_VERIFIED_R120_SOURCE_CANDIDATE_ZERO_DEV_CREDIT');P.mkdir();wt(P/'.gdignore','')
    for n in ['OWNER_RESUME.json','PLAN.json','FRAME_REVIEW.json','FRAME_INDEX.json','ACTOR_LAYOUT_PRESERVATION.json',
              'FUNCTION_PRESERVATION.json','PROBE_ART_CONTRACT_CHANGE.json','VALIDATION_STATUS.json',
              'SOURCE_NATIVE_RESULT.json','CANDIDATE_NATIVE_RESULT.json','LOCAL_82_RESULT.json','STATIC_RESULT.json','R119_EXACT_CI_SUCCESS.json',
              'FULL_GAME_ART_CONTRACT_CORRECTION.json','FULL_VALIDATION_RECOVERY_BASIS.json','ORIGINAL_FULL_VALIDATION_FAILURE.json']:
        shutil.copy2(UP/n,P/n)
    for n in ['SOURCE_REMOTE_VERIFICATION.json','SOURCE_FINAL.json','SOURCE_PRECOMMIT_GATES.json','SOURCE_CI_HANDLES.json']:
        shutil.copy2(S/n,P/n)
    shutil.copy2(Path(__file__),P/'CANONICAL_PUBLICATION_RUNNER.py');shutil.copy2(S/'delivery_common.py',P/'delivery_common.py')
    record=dict(stable_ids=IDS,state='SOURCE_BOUND_PAINTED_RUNTIME_CANDIDATE_DEV_FROZEN',source_revision=SRC,
        source_branch=SOURCE_BRANCH,source_manifest=REL+'/MANIFEST.json',source_required_files=remote['required_files'],
        source_all_required_anonymous_exact=True,source_CI_snapshot=source['source_CI'],
        owner_scope=rd(P/'OWNER_RESUME.json'),new_bounded_source_artifacts=1,existing_named_roles=2,new_roles=0,new_families=0,
        new_runtime_PNG=2,native_generated_samples=2,generation_calls=2,rejected_native_takes=0,technical_exports=4,
        backend='Built-in image_gen; no model selector or model/version returned',model_version='NOT_EXPOSED',animation_calls=0,
        local82='PASS_ALL82_CURRENT_STATIC_ANALYZER_2D',native_executed_checks=dict(source=69,candidate=96,effective=165,excluded_fixture=54),
        check_count_unit='Executed checks, not unique requirements',new_native_frame_events=dict(bounded=12,excluded=6,retained=18),
        acceptance_scope='Qualified local role-only comparison across three configured Mobile/Speedy aspects; natural-route completeness and formalQA11 remain open',
        invisible_geometry='Two noninteractive Control clips delimit the original stage; supply no painted pixels or artwork-removal credit',
        original_controller_other_methods_LF_exact=67,original_probe_other_methods_LF_exact=81,full_game_audit_other_methods_LF_exact=122,
        full_game_audit_recovery='Only two retired-polygon presence terms replaced with exact painted-resource predicate. Original failure retained; three healthy probe results/current static/2D/native evidence reused.79 original script executions complete82 unique passing probes;83 total attempts including one original failed assertion.',
        original_texture_ceilings_unchanged=dict(decoded_bytes=24117248,declared_upload_bytes=12582912),
        Dev_integrated=False,new_partial_Dev_artifacts=0,formal_QA11=None,device=None,child=None,owner=None,
        whole_role_closed=False,accepted_removed=0,mission_complete=False)
    wr(P/'PRODUCTION.json',record)
    for name in ['per_piece','scene_coverage','tally','SUMMARY']:
        f=C/(name+'.json');x=rd(f);assert x['revision']=='FV-AUDIT-20261031-R119-PARKED'
        x['revision']=REVISION;x['r120_parent_receipt_revision']=CANON_BASE;x['r120_melody_curtains_runtime']=record
        x['r119_exact_source_CI_new_observation']=dict(revision='634c8e4a06aae91e30e71e5a5e314c59c29570ce',
            run_id=41255731431,conclusion='success',evidence=REL+'/R119_EXACT_CI_SUCCESS.json',
            unchanged_historical_snapshots=True,Dev_credit=0)
        x['mission_complete']=False
        if name=='per_piece':
            for piece in x['pieces']:
                if piece['id'] not in IDS:continue
                assert piece['status']=='IDENTIFIED'
                piece['r120_prior_status']=piece['status'];piece['r120_prior_dependencies']=piece['dependencies'][:]
                piece['dependencies']=[z for z in piece['dependencies'] if z!='Inspected suitable reuse or recorded exact missing gap']
                piece['dependencies']+=['Owner2026-10-17: reuse optional; no failed-reuse prerequisite.',
                    'Owner direct resume permits art candidates; Dev remains frozen.',
                    'Natural current route, remaining states, formal QA11, device, child and owner evidence remain open.']
                piece.update(status='SOURCE_CANDIDATE',candidate_source_revision=SRC,integration_sha=None,
                    evidence_level='SOURCE_BOUND_CONFIGURED_NATIVE_WORKBRANCH_ONLY',r120_melody_curtains_runtime=record)
                piece['screen_coverage']['r120_scope']='Configured Daddy/Melody entry and deliberate note at1280x720/1600x720/1280x800. Original opening/actors/input preserved; no Dev or complete-route/whole-role acceptance.'
                piece['acceptance_evidence'].update(workbranch_mobile_runtime='https://github.com/'+REPO+'/blob/'+SRC+'/'+REL+'/candidate/1280x720/01_stage_entry.png',
                    workbranch_wide_runtime='https://github.com/'+REPO+'/blob/'+SRC+'/'+REL+'/candidate/1600x720/01_stage_entry.png',
                    workbranch_machine='https://github.com/'+REPO+'/blob/'+SRC+'/'+REL+'/LOCAL_82_RESULT.json')
                piece['review_log'].append(dict(revision=SRC,evidence=REL+'/FRAME_REVIEW.json',
                    scope='Qualified local ten-axis static role comparison, all12 effective stills viewed; formal/external acceptance remains open.'))
        elif name=='scene_coverage':
            for entry in x['entries']:
                if entry['id'] in ['minigame.melody','game.melody']:
                    entry['r120_melody_curtains_runtime']=record
                    entry['r120_workbranch_captures']=['https://github.com/'+REPO+'/blob/'+SRC+'/'+REL+'/candidate/'+aspect+'/'+n+'.png'
                        for aspect in ['1280x720','1600x720','1280x800'] for n in ['01_stage_entry','02_one_deliberate_note']]
                    entry['r120_scope_limit']='Source-only configured stage coverage; existing natural-route/remaining-state gaps remain open.'
            x['current_effective_summary']='SUMMARY.json; R120 adds12 bounded/6 excluded/18 retained native events and one coupled source artifact; zero new Dev or acceptance credit.'
        elif name=='tally':
            assert x['bounded_implementation_artifacts_published_current_summary']==22 and x['partial_dev_artifacts_current_summary']==20
            x.update(bounded_implementation_artifacts_published_current_summary=23,partial_dev_artifacts_current_summary=20,
                retained_native_events_current_summary=11138,r120_retained_bounded_current_summary=6955,
                r120_retained_excluded_current_summary=4183,r120_new_frame_events=dict(bounded=12,excluded=6,retained=18),
                generation_calls_this_revision=2,generated_candidate_samples_this_revision=2,rejected_native_takes_this_revision=0,
                existing_runtime_candidates_committed_this_revision=1,new_runtime_PNG_this_revision=2,technical_exports_this_revision=4,
                new_partial_Dev_artifacts_this_revision=0,current_effective_summary='SUMMARY.json;23 published source/20 partialDev artifacts.6955 bounded4183 excluded11138 retained native PNG events; accepted removals0. Art candidates resumed, Dev frozen; formal/external/global gaps remain open.')
        else:
            assert x['existing_sample_work_branch_implemented']==22 and x['dev_integrated']==20 and x['retained_bounded']==6943 and x['retained_excluded']==4177
            x.update(existing_sample_work_branch_implemented=23,dev_integrated=20,retained_bounded=6955,retained_excluded=4183,
                retained_native_events=11138,new_native_frames=18,new_bounded_contexts=12,new_excluded_diagnostics=6,
                new_roles=0,new_families=0,new_alias_credits=0,new_partial_role_credit=0,new_runtime_implementations=1,
                new_partial_Dev_artifacts=0,existing_runtime_candidates_committed_this_revision=1,new_samples=2,new_generation_calls=2,
                generated_candidate_samples_this_revision=2,rejected_native_takes_this_revision=0,technical_exports_this_revision=4,
                new_runtime_PNG_this_revision=2,candidate_neighbor_context_frames_here=6,direct_candidate_frame_views_here=6,
                source_context_frames_here=6,source_current_frames_here=6,source_views_here=6,
                direct_native_frame_views_here=12,existing_context_frames_reinspected_here=0,
                chosen_next_consumer='Continue documented low-quality art candidates on workbranches; Dev held by owner.',
                known_implementation_count_scope='23 published bounded source artifacts,20 partialDev artifacts. R120 two existing curtain roles form one implementation artifact. Lower263 roles/35 families and unknown game-wide denominators retained.',
                new_frame_unit='Recorded native PNG events only:6 source+6 candidate bounded,6 excluded title-occluded fixture,18 retained. Direct-view fields here count the12 effective stills only. Counts do not establish accepted artwork removal.',
                production_hold='Art candidates resumed by direct owner answer; Dev integration remains frozen. Automation remains paused.')
        wr(f,x)
    current=R/H/'CURRENT.json';x=rd(current);assert x['revision']=='FV-AUDIT-20261031-R119-PARKED'
    x['r120_prior_production_hold']=x['production_hold'];x.update(revision=REVISION,current_entry=REL.removeprefix(H+'/')+'/README.md',
        current_manifest=REL.removeprefix(H+'/')+'/MANIFEST.json',production_phase='ITEM_BY_ITEM_ART_CANDIDATES_RESUMED_DEV_FROZEN',
        production_hold=dict(state='DEV_INTEGRATION_FROZEN_ART_CANDIDATE_PRODUCTION_RESUMED',owner_reply='Resume art candidates; keep Dev frozen',evidence=REL.removeprefix(H+'/')+'/OWNER_RESUME.json',Dev_integration_authorized=False,automation_unchanged=True),
        r120_melody_curtains_runtime=record);wr(current,x)
    wt(P/'README.md',f'''# R120 painted Melody theatre curtains

The owner resumed **art candidates and kept Dev frozen**. Two painted curtain assets replace the pink and lavender polygon curtains on their own work branch. The stage opening, actors, note interaction, saves and original texture-memory limits remain unchanged. This is one bounded implementation for two existing named art roles.

![Painted curtains in the actual Melody stage](https://raw.githubusercontent.com/{REPO}/{SRC}/{REL}/candidate/1280x720/01_stage_entry.png)

[Source packet and before/after images](https://github.com/{REPO}/blob/{SRC}/{REL}/README.md) · [Immutable source tree](https://github.com/{REPO}/tree/{SRC}) · [Source manifest](https://github.com/{REPO}/blob/{SRC}/{REL}/MANIFEST.json) · [Anonymous source verification](SOURCE_REMOTE_VERIFICATION.json).

All 82 current trusted probes, the complete static prefix, real Godot analyzer and 2D regression guard pass with exact Godot 4.7.2. Native Mobile/Speedy checks cover 1280×720, 1600×720 and 1280×800: 69 source and 96 candidate executed checks. All 12 effective before/after stills were inspected. Six initial title-occluded captures and 54 fixture checks remain excluded. [Local result](LOCAL_82_RESULT.json), [ten-axis qualified role comparison](FRAME_REVIEW.json), [production/evidence lanes](PRODUCTION.json), [owner scope](OWNER_RESUME.json).

Two built-in ImageGen calls produced preserved native RGBA originals, editable Aseprite masters and two whole 384×768 runtime images. Four technical exports include the two earlier 512×1024 intermediates. No model version was exposed. Animation calls: 0. The two invisible stage clips supply no artwork pixels. Other flat stage props and natural current-route coverage remain open.

The canonical registry now records 23 published source artifacts and 20 partial Dev artifacts: 6,955 bounded, 4,183 excluded and 11,138 retained native PNG events. Accepted removals and whole-role closures remain 0. Unknown game-wide denominators, formal QA11, physical device/performance, child and owner acceptance remain open. **No Dev integration or release occurred.**

R119’s already-running exact-source CI completed successfully at 634c8e4a06aae91e30e71e5a5e314c59c29570ce; [new observation](R119_EXACT_CI_SUCCESS.json). Historical pending snapshots are preserved, and no old engine suite was restarted. R120’s automatic exact-source CI is tracked separately in [SOURCE_CI_HANDLES.json](SOURCE_CI_HANDLES.json).

The original full-game check required the retired curtain polygons. Its [failure](ORIGINAL_FULL_VALIDATION_FAILURE.json) is preserved; [bounded art-contract correction](FULL_GAME_ART_CONTRACT_CORRECTION.json) and [healthy-evidence reuse](FULL_VALIDATION_RECOVERY_BASIS.json) keep every other gameplay assertion and122 audit methods unchanged. No healthy engine suite, native frame or generation was repeated.

[Delivery manifest](MANIFEST.json) · [Anonymous immutable verification receipt](REMOTE_VERIFICATION.json) · [Payload revision](PAYLOAD_PIN.json).
''')
    master=R/'audit/MASTER_AUDIT_2026-08-09.md';lines=master.read_text(encoding='utf-8').splitlines();i=next(i for i,l in enumerate(lines) if l.startswith('| Full-game flat-vector audit |'))
    lines[i]='| Full-game flat-vector audit | [R120 painted Melody curtains](../'+REL+'/README.md) | [Impact](../'+IP.relative_to(R).as_posix()+'); owner resumed candidates, Dev frozen.23 source/20 partialDev artifacts;0 accepted removals, formal/external/global gaps open. |';wt(master,'\n'.join(lines)+'\n')
    ledger=R/'design/05_DOC_LEDGER.md';wt(ledger,ledger.read_text(encoding='utf-8')+'\n| `'+REL+'/README.md` | 🟣 | `PROPOSED / CANDIDATE` source-only painted Melody curtains, two existing roles/one artifact; art resumed, Dev frozen.23 source/20 partialDev; formal/external/global open. |\n')
    active=R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md';text=active.read_text(encoding='utf-8');i=text.index('## MA-VIS-006');j=text.index('\n## ',i+3)
    wt(active,text[:j]+'\nR120 source production2026-11-01: [painted Melody curtains](../../'+REL+'/README.md), source'+SRC+', current local82/static/analyzer/2D and165 effective native executed checks.12 bounded6 excluded18 retained frames;23 source20 partialDev artifacts. Owner resumed candidates, Dev remains frozen. MA-VIS-006 lifecycle/formal/device/child/owner/global gaps remain OPEN; accepted removals0.\n'+text[j:])
    ch=R/'audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md';wt(ch,ch.read_text(encoding='utf-8')+'\n### R120 painted Melody curtains — source-only production\n\n[Candidate](../'+REL+'/README.md), source`'+SRC+'`, replaces two existing curtain roles with whole painted assets. Original controller/input/save/actor layout and coverage/memory ceilings retained. Local82/static/analyzer/2D/native165 checks pass;12 bounded6 excluded18 retained new native events. Owner resumed art candidates and kept Dev frozen:23 source20 partialDev artifacts,0 newDev credit, accepted removals0. Source impact owns bounded candidate rollback; no canonical engine or generation rerun. Formal/external/natural-route/global gaps remain open.\n')
    text=ch.read_text(encoding='utf-8');assert 'CHG-126' not in text
    text=text.replace('### R120 painted Melody curtains — source-only production','### CHG-126 — R120 painted Melody curtains — source-only production')
    text+='\nCHG-126 exact source: `'+SRC+'`, baseline `'+SOURCE_BASE+'`. Runtime paths: `scripts/games/melody.gd`, `scripts/probe_melody.gd`, `scripts/probe_audit.gd`, two `assets/melody/curtain_*_painted.png` resources/imports. Canonical paths: R120 packet, CURRENT.json, r96 current per-piece/coverage/tally/SUMMARY, authority navigation and impact. Plausible negative effects: clipping/filtering/overdraw/resource or art-contract regression. Dependencies and source evidence are pinned in the actual source manifest and DELIVERY_SOURCE_BINDING; canonical changes add no runtime dependency. Rollback class: bounded mixed code/assets/art-contract plus separately reversible registry metadata. Plan read-only from a clean `codex/rollback-chg-126` branch, inspect the exact coupled diff, stop on conflicts and earn focused/import/full gates before any rollback publication. Preserve native sources and historical evidence; never partial-revert the resource contract or change Dev during the freeze.\n'
    wt(ch,text)
    wt(P/'CANONICAL_GATES.json','{}\n');wt(P/'MANIFEST.json','{}\n')
    wr(P/'REMOTE_VERIFICATION.json',dict(state='PENDING_PAYLOAD_PUBLICATION_NO_REMOTE_VERIFICATION_CLAIM'))
    wr(P/'PAYLOAD_PIN.json',dict(state='PENDING_PAYLOAD_COMMIT_NO_REVISION_CLAIM'))
    files=changed(R)|{REL+'/'+n for n in ['CANONICAL_GATES.json','MANIFEST.json','REMOTE_VERIFICATION.json','PAYLOAD_PIN.json']}
    wr(IP,dict(id='flat-vector-r120-melody-curtains-20261101',baseline=CANON_BASE,
        scope='Record verified painted Melody curtain source candidate, owner candidate-only resume/Dev hold, bounded same-scene evidence and canonical counts. No runtime edits on canonical branch.',
        rules=['DL-AUTH-05','DL-AUTH-06','DL-AUTH-07','DL-VIS-01','DL-ASSET-03','DL-QA-03','DL-QA-11','DL-QA-14'],findings=['MA-VIS-006'],files=sorted(files),
        validation=[dict(command='Source exact4.7.2/static/analyzer/2D/all82/currentnative/everyrequiredfile anonymous immutable',result='PASS',evidence=REL+'/LOCAL_82_RESULT.json; SOURCE_REMOTE_VERIFICATION.json; FRAME_REVIEW.json'),
                    dict(command='Canonical document authority/development and immutable manifest verification',result='PENDING',evidence=REL+'/CANONICAL_GATES.json; REMOTE_VERIFICATION.json')],
        acceptance_gaps='Dev explicitly frozen. Exact-source CI and formalQA11/device/child/owner/natural-route/global evidence separate; accepted removals0.'))
    prepared=dict(source_revision=SRC,canonical_baseline=CANON_BASE,frozen_root5=frozen,
        counts_applied_once=dict(source=23,partialDev=20,bounded=6955,excluded=4183,retained=11138,accepted_removed=0),files=sorted(files))
    wr(S/'CANONICAL_PREPARED.json',prepared)
    existing=sorted((files|{IP.relative_to(R).as_posix()})-{REL+'/MANIFEST.json',REL+'/REMOTE_VERIFICATION.json',REL+'/PAYLOAD_PIN.json'})
    run(R,'git','add','-f','--',*existing);g=document_gates(R,'CANONICAL_PREPARE')
    wr(P/'CANONICAL_GATES.json',dict(state='PASS',gates=g,no_engine_restarted=True));run(R,'git','add','--',REL+'/CANONICAL_GATES.json')
    rows=payload_rows(R,existing)
    # Only the current R120 delivery is a dependency; no prior archive is recursively required.
    sm=rd(UP/'MANIFEST.json');rows += [dict(row,revision=row.get('revision') or SRC) for row in sm['files']]
    mb=git(U,'show',SRC+':'+REL+'/MANIFEST.json');rows.append(dict(revision=SRC,path=REL+'/MANIFEST.json',bytes=len(mb),sha256=digest(mb),role='Actual bounded R120 source-delivery manifest'))
    manifest=dict(schema='reef.runtime_trial_delivery/1',revision=REVISION,baseline=CANON_BASE,actual_runtime_source=SRC,
        state='PAINTED_CURTAIN_SOURCE_CANDIDATE_DEV_FROZEN',files=rows,required_files=len(rows),required_bytes=sum(x['bytes'] for x in rows),
        Dev_integrated=False,new_partial_Dev_artifacts=0,new_bounded_source_artifacts=1,new_frame_events=dict(bounded=12,excluded=6,retained=18),accepted_removed=0,mission_complete=False)
    wr(P/'MANIFEST.json',manifest);run(R,'git','add','--',REL+'/MANIFEST.json');document_gates(R,'CANONICAL_FINAL')
    assert not gs(R,'diff','--name-only') and all(sha(R/H/n)==v for n,v in frozen.items())
    run(R,'git','fetch','origin');assert gs(R,'rev-parse','origin/'+CANON_BRANCH)==CANON_BASE
    run(R,'git','commit','-m','Record R120 painted Melody source candidate and owner Dev hold; zero Dev credit')
    payload=gs(R,'rev-parse','HEAD');state('CANONICAL','PAYLOAD_COMMITTED_PUSH_PENDING',payload_revision=payload)
    run(R,'git','push','origin',CANON_BRANCH);state('CANONICAL','PAYLOAD_PUSHED_ANONYMOUS_VERIFICATION',payload_revision=payload)
    receipt=verify_manifest(R,payload,REL+'/MANIFEST.json',manifest);wr(P/'REMOTE_VERIFICATION.json',receipt)
    wr(P/'PAYLOAD_PIN.json',dict(payload_revision=payload,source_revision=SRC,manifest=REL+'/MANIFEST.json',manifest_sha256=receipt['manifest_sha256'],frozen_root5_unchanged=True,counts_applied_once=prepared['counts_applied_once'],Dev_integrated=False,accepted_removed=0))
    run(R,'git','add','--',REL+'/REMOTE_VERIFICATION.json',REL+'/PAYLOAD_PIN.json');document_gates(R,'CANONICAL_RECEIPT')
    run(R,'git','commit','-m','Record anonymous immutable R120 source and canonical delivery verification')
    final=gs(R,'rev-parse','HEAD');run(R,'git','push','origin',CANON_BRANCH)
    verified=[]
    for n in ['README.md','MANIFEST.json','REMOTE_VERIFICATION.json','PAYLOAD_PIN.json']:
        p=REL+'/'+n;expected=git(R,'show',final+':'+p);status,b=fetch(final,p);assert status==200 and b==expected
        verified.append(dict(path=p,revision=final,sha256=digest(b),bytes=len(b),verified=True))
    assert not gs(R,'status','--porcelain') and all(sha(R/H/n)==v for n,v in frozen.items())
    out=dict(state='R120_SOURCE_AND_CANONICAL_DELIVERY_ANONYMOUSLY_VERIFIED_DEV_FROZEN',source_revision=SRC,payload_revision=payload,
        receipt_revision=final,manifest=REL+'/MANIFEST.json',required_files=len(rows),required_bytes=manifest['required_bytes'],
        final_metadata=verified,counts_applied_once=prepared['counts_applied_once'],frozen_root5_unchanged=True,worktree_clean=True,
        Dev_integrated=False,accepted_removed=0,mission_complete=False,completed_at_utc=now())
    wr(S/'CANONICAL_FINAL.json',out);state('CANONICAL','TERMINAL_CANONICAL_PUBLICATION_SUCCESS',source_revision=SRC,receipt_revision=final)
    print('R120_CANONICAL_DELIVERED',final,payload,len(rows),flush=True)
except Exception as exc:
    wr(S/'CANONICAL_AUDIT_RECOVERY_STOP.json',dict(state='STOPPED_INSPECT_EXACT_HANDLE_NO_AUTOMATIC_RETRY',error=str(exc),at_utc=now()))
    state('CANONICAL','STOPPED_NO_AUTOMATIC_RETRY',error=str(exc));raise
