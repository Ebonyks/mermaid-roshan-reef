from pathlib import Path
import json,hashlib,subprocess,importlib.util,io,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r76_stuffie_care_context';B='7fd93aa0d2036c06c9a65aea6c79a990cc9ae01b';D='dd799b2d43871b29d1d6e0503646308a194dad1e'
s=importlib.util.spec_from_file_location('a77validate',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
su=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');role=rd(P/'NEW_ROLE_RECORDS.json')['records'][0];review=rd(P/'REVIEW.json');graph=rd(P/'SOURCE_ENTRY_GRAPH.json')
assert (idx['raw_frames'],idx['bounded_source_contexts'],idx['excluded_diagnostics'],idx['failed_attempt_frames'],idx['prelaunch_frames'])==(54,32,22,18,0)
assert (su['retained_bounded'],su['retained_excluded'],su['retained_native_events'])==(6342,3498,9840)and(su['known_roles'],su['known_families'],su['new_roles'],su['new_families'])==(262,35,1,0)and su['healthy_observer_checks']==50
for x in idx['files']:
 raw=(R/x['path']).read_bytes();im=Image.open(io.BytesIO(raw));assert len(raw)==x['bytes']and sha(raw)==x['sha256']and list(im.size)==x['dimensions']and sha(im.convert('RGBA').tobytes())==x['decoded_rgba_sha256']
for c in sorted((P/'native').iterdir()):
 m=rd(c/'capture_manifest.json');res=rd(c/'RESULT.json');launch=rd(c/'LAUNCH.json');healthy=c.name.startswith('attempt3')
 assert len(m['states'])==18 and len(m['checks'])==25 and all(x['pass']for x in m['checks'])and not m['errors']and m['observer_status']=='PASS'
 assert res['exit_code']==0 and not res['timed_out']and res['normal_before']==res['normal_after']and m['normal_before']==m['normal_after']and len(m['normal_before'])==11
 assert res['sidecars_exact']and res['sidecar_after_count']==4088 and not res['source_byte_changes']and res['fixture_dependency_unchanged']
 assert sha((c/'capture_entry.gd').read_bytes())==launch['fixture_sha256']and m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and m['engine']['build']=='official'and m['renderer']=='mobile'and m['display']!='headless'and m['source_revision']==D and m['time_scale']==1 and not m['actual_child_data']and not m['production_changes']
 assert m['private_path']!=m['normal_path']and Path(m['private_path']).parent.name.startswith('mermaid-roshan-r77-')
 states={s['id']:s['snapshot']for s in m['states']}
 for name,st in states.items():
  assert not st['intro_layer_present']and not st['intro_overlay_constructed']and st['current_user_path']==m['private_path']and st['save_dependency_path']=='user://reef_save.json'
  assert st['quality']==('sparkly'if name in ['fresh_menu_default','fresh_options_default']else'speedy')
 for name in ['menu_speedy','keep_ready','reentry_start_menu']:assert states[name]['intro_active']and states[name]['living_stage']=='intro.storybook'and states[name]['start_menu_active']
 assert states['keep_ready']['private_hashes']==states['keep_tip_canceled_reset']['private_hashes']==states['short_release_no_reset']['private_hashes']
 assert states['new_main_dayone_entry']['main_id']!=states['keep_ready']['main_id']and not states['new_main_dayone_entry']['root_reset_marker']and states['new_main_dayone_entry']['private_hashes']['.before_new_game']!='absent'
 for name in ['new_main_dayone_entry','opening_or_fallback','opening_or_fallback_later']:assert states[name]['clip']['active']and states[name]['clip']['id']=='d1_opening'and states[name]['clip']['playing']
 assert not states['after_opening']['clip']['active']and not states['after_opening']['tree_paused']and states['continued_dayone']['day_one_active']
 assert all(p['inside']and p['centered']and p['texture_path']=='res://assets/castle/training/ghost_hand.png'for p in m['pointer_samples'])and len(m['pointer_samples'])==32
 if healthy:assert not res['script_or_shader_errors']and len(m['cache_directory_structure_only'])>=100
 else:assert res['script_or_shader_errors']and (c/'engine.log').read_bytes().count(b'ERROR:')==39
p=rd(P/'prelaunch/attempt2_entry_source_1280/PRELAUNCH_FAILURE.json');assert not p['engine_launched']and p['frames']==0
for x in rd(P/'POINTER_MEASUREMENTS.json')['cases']:assert x['sample_count']==32 and x['all_inside']and x['span_ms']>=840 and x['hand_y_max']-x['hand_y_min']>13.5 and x['maximum_projection_error_px']<0.001 and 30000<x['new_main_to_after_opening_ms']<38000 and not x['QA11_live_semantic_contact_accepted']
assert role['id']=='FVR-67E362D1DE53'=='FVR-'+sha(role['stable_id_input'].encode())[:12].upper()and role['family']=='shared_ui'and role['texture']['sha256']=='e484d14899d8137448128314536132dbd16f970cb1f0fabea006e9d51b5435b9'
assert len(review['reviewed_native_images'])==6 and len(review['hand_reviewed_images'])==4 and all(x in idx['files']for x in review['reviewed_native_images'])and set(review['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'}
assert not review['full_context_review_complete']and review['DL_QA_11']=='NOT_ESTABLISHED'and not role['approved']and not role['integrated']and not role['runtime_verified_replacement']and role['accepted_removed']==0
assert len(graph['files'])==313 and graph['summary']['named_target_calls']==130 and graph['summary']['non_test_candidate_target_calls']==12 and not graph['summary']['global_unreachability_proved']and not graph['summary']['raw_dispatch_semantics_recomputed']
ready=[x for x in graph['named_calls']if x['path']=='scripts/main.gd'and x['function']=='_ready'and x['method']=='_build_intro'];assert len(ready)==1 and any(x['kind']=='if_branch'and 'DisplayServer'in x['condition_AST']and 'headless'in x['condition_AST']for x in ready[0]['guards'])
for x in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 raw=git('show',x['revision']+':'+x['path']);assert sha(raw)==x['sha256']and len(raw)==x['bytes']
for x in graph['files']:assert x['parse']=='PASS'and sha(git('show',D+':'+x['path']))==x['sha256']
for x in rd(P/'SOURCE_BINDINGS.json')['functions']:
 raw=git('show',D+':'+x['path']);text=raw.decode();defs=list(re.finditer(r'^func (\w+)\(',text,re.M));i=next(i for i,d in enumerate(defs)if d.group(1)==x['function']);body=text[defs[i].start():defs[i+1].start()if i+1<len(defs)else len(text)];assert sha(raw)==x['file_sha256']and sha(body.encode())==x['body_sha256']
assert all(x['exact_equal']for x in rd(P/'PRIOR_R66_SCOPE.json')['source_comparisons'])and rd(P/'PRIOR_R66_SCOPE.json')['legacy_continue_policy_mismatch']=='OPEN_NOT_REPAIRED_OR_RETESTED_BY_R77_FRESH_DAYONE_PROFILES'
repro=rd(P/'REPRODUCTION_CHECK.json');assert repro['scanner_sha256']==sha((P/'scan_intro_entry.py').read_bytes())and repro['deriver_sha256']==sha((P/'derive_evidence.py').read_bytes())and len(repro['outputs'])==5
for x in repro['outputs']:assert x['logical_exact']and sha((P/x['path']).read_bytes())==x['sha256']
assert rd(P/'SOURCE_TESTS.json')['exit_code']==0 and rd(P/'SOURCE_TESTS.json')['test_count']==10
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n);assert d['intro_entry_ownership']==su
 for k,v in old.items():
  if k in ['revision','phase','publication','current_effective_summary']:continue
  if n=='per_piece.json'and k in ['pieces','supplemental_piece_records']:
   assert len(d[k])==len(v)+(1 if k=='supplemental_piece_records'else 0)
   for new,prior in zip(d[k],v):assert all(new[a]==b for a,b in prior.items())
   if k=='supplemental_piece_records':assert d[k][-1]==role
  else:assert d[k]==v,(n,k)
u=rd(P/'CURRENT_KNOWN_ROLE_UNION.json');assert u['records'][:-1]==rd(O/'CURRENT_KNOWN_ROLE_UNION.json')['records']and u['records'][-1]['id']==role['id']and len(u['records'])==262 and len({x['family']for x in u['records']})==35
u=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert u['records']==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records']and u['supplemental_partial_records']==38
u=rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json');assert all(u[k]==v for k,v in rd(O/'CURRENT_CATALOGUE_CONTEXT_UNION.json').items())and(u['current_partial_count'],u['without_current_slice_count'],u['complete_count'])==(92,84,0)
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();prefix=P.relative_to(R).as_posix()+'/';allowed={'design/audit_impacts/flat-vector-intro-entry-20261016.json','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix()};assert all(x.startswith(prefix)or x in allowed for x in changed)
g=rd(P/'SOURCE_GUARDS.json');assert g['runtime_count']==4425 and g['sidecar_count']==4088 and not g['runtime_changes']and g['sidecars_exact']and g['source_worktree_clean']
for n in ['FIXTURE_SYNTAX_GATES.json','FIXTURE_SYNTAX_GATES_ATTEMPT1.json','USERDIR_PREFLIGHT.json']:assert all(x['exit_code']==0 for x in rd(P/n)['checks'])
code=(P/'capture_entry.gd').read_text(encoding='utf-8');assert not re.search(r'\bm\.(game|g|quality|intro_active|first_session|day_one_active|save_data)\s*=(?!=)',code)and'ProjectSettings.save('not in code
assert rd(H/'CURRENT.json')['current_tally']=='r77_intro_entry_ownership/tally.json'and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval']is False
assert all(su[k]==0 for k in ['approved','integrated','runtime_verified_replacements','accepted_removed','new_drawing_samples','generation_calls','new_runtime_assets','new_alias_credits'])and all(su[k]is None for k in ['all_game_artwork_total','distinct_screen_total','regression_total'])and not su['mission_complete']
print('R77_VALIDATION_PASS 54raw32bounded22excluded;50healthy+10ASTtests;313sourceguard;sourcehand64samples+realcancel;262/35;0art/runtime/acceptance/globalunknown',flush=True)
