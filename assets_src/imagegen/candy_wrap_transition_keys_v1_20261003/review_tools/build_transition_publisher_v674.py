from pathlib import Path
import re
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');R=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp')
source=(B/'assets_src/local_motion/candy_twist_release_components_v1_20261003/review_tools/publish_component_review_v651.py').read_text()
replacements={
'assets_src/local_motion/candy_twist_release_components_v1_20261003':'assets_src/imagegen/candy_wrap_transition_keys_v1_20261003',
'design/audit_impacts/job-candy-twist-release-components-20261003.json':'design/audit_impacts/job-candy-wrap-transition-keys-20261003.json',
"BASE='b6501351a854cc0133b17a74d557ce1c4d14b5af'":"BASE='296b2adc8cf4e9b3adbc27a5b5d281471893f6bf'",
"MAP='audit/job_review_v2_20261001/CANDY_TWIST_RELEASE_COMPONENT_FILES_V27.json';PRIOR='audit/job_review_v2_20261001/CANDY_TWIST_RELEASE_ENDPOINT_FILES_V26.json';SHARDS='audit/job_review_v2_20261001/v27_unchanged_dependency_shards'":"MAP='audit/job_review_v2_20261001/CANDY_TRANSITION_KEY_FILES_V28.json';PRIOR='audit/job_review_v2_20261001/CANDY_TWIST_RELEASE_COMPONENT_FILES_V27.json';SHARDS='audit/job_review_v2_20261001/v28_unchanged_dependency_shards'",
'tmp/component_publish_v651':'tmp/transition_publish_v674','tmp/component_remote_v651':'tmp/transition_remote_v674','tmp/component_sealed_v651.json':'tmp/transition_sealed_v674.json',
'.v651_next':'.v674_next','previous_AC_remote_verified':'previous_AD_remote_verified',
'PENDING_EXACT_REJECTED_COMPONENT_REVIEW_STAGED_SEAL':'PENDING_EXACT_TRANSITION_SOURCE_REVIEW_STAGED_SEAL',
'EXACT_SHARDED_COMPONENT_REVIEW_BYTES_SEALED':'EXACT_SHARDED_TRANSITION_REVIEW_BYTES_SEALED',
'PUBLICATION_BOUNDARY_V651.json':'PUBLICATION_BOUNDARY_V674.json',
'Source-only review structural/document/2D no-regression/register gates':'Source-only structural/document/2D no-regression/register gates',
'PREPARED_EXACT_TWIST_RELEASE_COMPONENT_PUBLICATION_SCOPE':'PREPARED_EXACT_TRANSITION_PUBLICATION_SCOPE',
}
for a,b in replacements.items():assert a in source,a;source=source.replace(a,b)
checks='''def checks():
    assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()==BRANCH
    for label in ['authority','development','document_tests','game2d','register_parts']:assert read(C/'gates_v1'/(label+'.receipt.json'))['status']=='PASS',label
    sys.path.insert(0,str(L/'review_tools'));from register_parts_v51 import load_register
    reg=load_register(L);assert reg['display_revision']=='V55' and len(reg['items'])==2160 and reg['counts']['inclusive_current_source_priorities']==1063 and reg['counts']['unique_source_file_priorities']==686 and reg['counts']['unreviewed_current_source']==294 and reg['counts']['unique_source_files']==1308
    stamp=read(L/'CURRENT_BOUNDARY_REFRESH.json');assert stamp['registry_items']==stamp['registered_source_matches']==2160 and stamp['assembled_registry_parts_verified'] and stamp['registry_root_sha256']==sha((L/'ALL_ITEMS.json').read_bytes()) and stamp['registry_parts']==reg['item_shards'] and stamp['candy_capture_boundary_match']
    previous=read(C/'previous_v54/ALL_ITEMS.json');current=read(L/'ALL_ITEMS.json');assert len(previous['items'])==2064 and current['items'][:2064]==previous['items'] and len(current['items'])==2072 and current['item_shards']==previous['item_shards'] and (L/'ALL_ITEMS.json').stat().st_size<4194304
    review=read(C/'REVIEW_SUMMARY.json');assert review['native_sources']==8 and review['individual_source_component_opinions']==88 and review['static_neighbor_opinions']==6 and review['total_individual_opinions']==94 and review['best_midturn_source_score']==4.2 and review['selected_midturn_key'] is None and review['early_release_source_score']==4.5 and review['current_game_wrap_score']==2.8 and review['complete_wrapping_score'] is None and not review['runtime_integration'] and not review['new_motion_dispatched'] and review['owner_acceptance'] is None
    for stage,scores in [('midturn',[4.0,4.1,4.0,4.2]),('release',[4.1,4.3,4.2,4.5])]:
        for i,score in enumerate(scores,1):
            M=C/(stage+'_attempt'+str(i).zfill(2));r=read(M/'DIRECT_REVIEW.json');receipt=read(M/'GENERATION_RECEIPT.json');request=read(M/'GENERATION_REQUEST.json')
            assert r['source_score']==score and len(r['opinions'])==11 and r['direct_complete_native_review'] and r['owner_acceptance'] is None and not r['runtime_integration'] and r['mounted_score'] is None and r['sequence_score'] is None and r['action_score'] is None
            assert sha((M/'native.png').read_bytes())==r['native_sha256']==receipt['native_sha256'] and r['native_path']==receipt['native_path'] and r['dimensions']==receipt['native_dimensions']==[1672,941]
            assert sha((M/'PROMPT.txt').read_bytes())==receipt['prompt_sha256']==request['prompt_sha256'] and receipt['method']=='BUILTIN_IMAGEGEN_COMPLETE_FLATTENED_SOURCE' and receipt['references']==request['references']
            for ref in receipt['references']:assert sha((B/ref['path']).read_bytes())==ref['sha256'],ref['path']
    relation=read(C/'NEIGHBOR_SOURCE_REVIEW.json');assert len(relation['opinions'])==6 and all(x['temporal_score'] is None and x['current_game_score'] is None for x in relation['opinions']) and relation['complete_wrapping_score'] is None
    proof=read(C/'TRANSITION_BROWSER_OBSERVATIONS_V670.json');assert 'V55: 2,160' in proof['library']['summary'] and proof['report']['componentRows']==88 and proof['report']['neighborRows']==6 and proof['report']['articles']==8 and proof['report']['stages']==7 and not proof['library']['overflow'] and 'Mounted: unassigned' in proof['item']['item'] and 'Complete action: unassigned' in proof['item']['item']
    preservation=read(C/'DISPLAY_COPY_EDIT.json')
    for path,h in preservation['protected_members'].items():assert sha((B/path).read_bytes())==h,path
    snapshot=read(C/'gates_v1/CANDIDATE_TRANSITION_SOURCE_V672.json')
    for row in snapshot['members']:
        if row['path']=='.gitattributes':continue # Added literal map/shard attributes separately sealed.
        assert [(B/row['path']).stat().st_size,sha((B/row['path']).read_bytes())]==[row['bytes'],row['sha256']],row['path']
    prior=read(C/'previous_AD_remote_verified/RESULT.json');assert prior['status']=='PASS_ALL_ANONYMOUS_REMOTE_BYTES' and prior['files_including_manifest']==24850 and prior['revision']==BASE
    journal=read(C/'previous_AD_remote_verified/JOURNAL_SHARDS.json');assert journal['rows']==24850
    for row in journal['shards']:assert [(B/row['path']).stat().st_size,sha((B/row['path']).read_bytes())]==[row['bytes'],row['sha256']]
    boundary=read(P/'PRODUCTION_BOUNDARY.json');assert len(boundary['members'])==783 and all(sha((B/x['path']).read_bytes())==x['sha256'] for x in boundary['members'])
'''
start=source.index('def checks():');end=source.index('\ndef run(',start);source=source[:start]+checks+source[end:]
source=source.replace('all24611','all24850').replace('24611','24850')
old_qualification=re.search(r"qualification='V54 known2152.*?acceptance.'\)",source).group(0)
qualification='V55:2160 known entries/1308 primary sources/1063 inclusive source-cell-region priorities/686 unique priority sources/294 pending primary opinions. Eight complete native ImageGen transition drafts/88 individual component and6 static-neighbor opinions. Seven intended-stage rejections retained;early-releaseA4 source4.5 provisional with coherent thumbs/cuffs,purple clearance and thin flat paper necks. Midturn best4.2 remains rejected,no selected midpoint or newmotion. Prior localtwist2.2/release1.7,current actualWRAP2.8/all783 production literals unchanged. Current turquoise widget/whisk work atlas do not bind gold family. Prior2064 root dictionaries/literal88-item part and4MiB ceiling preserved. Actual report/library/disclosure/individual-source browser proof,52 document tests/9 integrity tests and all24850 preceding AD anonymous rows retained. No runtime/protected-original/3D/security/gate/workflow/finding lifecycle/integration/release or full causal wrapping/broad jobs/day/Opera training/ordinary routes/device/child/owner/comprehensive report acceptance.'
source=source.replace(old_qualification,"qualification="+repr(qualification)+')')
start=source.index("message=OUT/'COMMIT_MESSAGE.txt';");end=source.index("\nrun('commit'",start)
message='Audit gold-wrapper midpoint and early-release source corrections\n\nPreserve all eight complete native ImageGen drafts and94 individual source/neighbor opinions. Early-releaseA4 source4.5 provisional with continuous thumb/cuff ownership,clear paper separation and thin flat neck folds. Midturn best4.2 remains rejected;no selected midpoint or newmotion.\n\nKeep actual story-job/Opera training WRAP2.8 and all783 production literals unchanged. Current turquoise widget/current whisk work row remain distinct from proposed gold family. Preserve V55 known2160 entries,all prior2064 dictionaries/literal88-item part,current-first library and all24850 prior AD anonymous remote rows. Source-bound browser proofs,52 document tests and9 register-integrity tests retained.\n\nNo runtime/cinematic binding,finding closure,integration or release. Full causal action,broad jobs/day/training,ordinary routes,device,child,owner and comprehensive report acceptance remain open.\n'
source=source[:start]+"message=OUT/'COMMIT_MESSAGE.txt';message.write_text("+repr(message)+",encoding='utf-8',newline='\\n')"+source[end:]
source=source.replace('Review-only. New exact remote/hosted status remains separate from source/action/device/child/owner/all-job/integration/release acceptance.','Source review-only. New exact remote/hosted status stays separate from motion/current-game/device/child/owner/comprehensive acceptance.')
source=source.replace('Only review sources/QA/local reference outputs/illustrated reports change.','Only review ImageGen source drafts/QA/illustrated reports change.')
out=R/'publish_transition_review_v674.py';out.write_text(source,encoding='utf-8',newline='\n');compile(source,str(out),'exec')
assert "V54" not in source and 'previous_AC' not in source and '24611' not in source and 'v651' not in source
print('FRESH_V28_TRANSITION_PUBLISHER_CREATED',len(source),'bytes')
