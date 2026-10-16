from pathlib import Path
import json,subprocess,hashlib,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;B='d3d5124c2373d17bb835ae85f63044b6fd2dfbdc';D='dd799b2d43871b29d1d6e0503646308a194dad1e';O=H/'r77_intro_entry_ownership'
spec=importlib.util.spec_from_file_location('bounded78',P/'bounded_json.py');A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
g=rd(P/'SOURCE_PAYLOAD_GRAPH.json');s=rd(P/'SUMMARY.json');disp=rd(P/'CALLER_DISPOSITIONS.json');sem=rd(P/'SEMANTIC_PROOF.json')
assert g['source_revision']==D and len(g['files'])==313 and len(g['resources'])==5 and all(x['parse']=='PASS'for x in g['files'])
assert g['scanner_sha256']==sha((P/'scan_game_payload.py').read_bytes())
for row in g['files']+g['resources']:
 b=git('show',D+':'+row['path']);assert sha(b)==row['sha256']and len(b)==row['bytes'],row['path']
assert len(g['named_calls'])==47 and len([x for x in g['named_calls']if not x['probe_or_test_filename']])==7 and len(g['literal_reflective_calls'])==1
assert len(disp['entry_producers'])==4 and len(disp['slide_named_callers'])==3 and len(set(x['id']for x in disp['entry_producers']))==4
assert sorted(x['initializer_game_string']for x in disp['entry_producers'])==['dustboss','dustboss','fairyshoot','race']
assert all(not x['normal_route_runtime_verified']and not x['all_alias_mutations_closed']and x['art_or_screen_credit']==0 for x in disp['entry_producers'])
assert len(disp['field_references_non_test'])==5 and not disp['field_literal_property_access']
assert disp['fade_callback']['function_evidence']['text'].count('cb.call()')==2 and not disp['fade_callback']['production_fade_executed_here']
assert not disp['picture_selector']['actual_child_route_verified']and not disp['picture_selector']['global_old_slide_unreachable']and not disp['allcaller_closure']
assert sem['status']=='PASS'and len(sem['checks'])==13 and all(x['pass']for x in sem['checks'])and len(sem['normal_save_names'])==11 and sem['normal_save_hashes_before']==sem['normal_save_hashes_after']and not sem['main_instantiated']and not sem['production_methods_executed']and sem['native_frames']==0
assert sem['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and sem['engine']['string']=='4.7.2-stable (official)'
launch=rd(P/'SEMANTIC_LAUNCH.json');assert launch['fixture_sha256']==sha((P/'payload_semantics.gd').read_bytes())and len(launch['checks'])==4 and all(x['exit_code']==0 and 'ERROR:'not in x['output']for x in launch['checks'])
guard=rd(P/'SEMANTIC_SOURCE_GUARD.json');assert guard['source_revision']==D and guard['runtime_raw_file_count']==4425 and guard['all_before_after_equal']and guard['worktree_clean']and guard['normal11_guard']
assert rd(P/'REPRODUCTION_CHECK.json')['byte_identical']is True and rd(P/'SOURCE_TESTS.json')['tests']==15 and rd(P/'SOURCE_TESTS.json')['exit_code']==0
prior=rd(O/'SUMMARY.json')
for k in ['retained_bounded','retained_excluded','retained_native_events','known_roles','known_families','existing_partial_roles','existing_partial_families','supplemental_partial_roles','catalogue_partial','catalogue_without_current_slice','catalogue_complete']:
 assert s[k]==prior[k],k
assert s['known_roles']==262 and s['known_families']==35 and s['retained_bounded']==6342 and s['retained_excluded']==3498 and s['retained_native_events']==9840 and s['catalogue_partial']==92 and s['catalogue_without_current_slice']==84 and s['catalogue_complete']==0
for k in ['new_native_frames','new_bounded_contexts','new_excluded_diagnostics','new_roles','new_families','new_alias_credits','approved','integrated','runtime_verified_replacements','accepted_removed','generation_calls','new_drawing_samples','new_runtime_assets']:assert s[k]==0,k
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert s[k]is None,k
assert not s['allcaller_closure']and not s['global_unreachability_proved']and not s['mission_complete']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/name);new=rd(P/name);allowed={'revision','phase','inherited_r77_reference_base','game_payload_closure','current_effective_summary','publication'}
 assert all(new[k]==v for k,v in old.items()if k not in allowed),name
 assert set(new)-set(old)<=allowed and new['game_payload_closure']==s and new['inherited_r77_reference_base']['revision']==B
for name in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:
 old=rd(O/name);new=rd(P/name);assert {k:v for k,v in new.items()if k!='r78_scope'}==old,name
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix()),name
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()
allowed_doc={'audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/audit_impacts/flat-vector-game-payload-20261016.json',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()}
assert all(x in allowed_doc or x.startswith(P.relative_to(R).as_posix()+'/')for x in changed),changed
assert rd(H/'CURRENT.json')['current_tally']=='r78_game_payload_closure/tally.json'and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval']is False
assert not git('diff','--name-only',B,'--','scripts','scenes','assets','shaders','project.godot').strip()
print('R78_VALIDATION_PASS 313exactAST;4namedproducers/3slidecallers;15adversarial/13languagechecks;4425rawsource/11saveguard;262/35and9840historyunchanged;0newart/runtime/native/acceptance;globalunknown')