from pathlib import Path
import json,hashlib,subprocess,re
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r29_startup_ambience_context';BASE='fdf41220b8cfe16f129741e364b2ea75f4e5e7f1'
def rd(f):return json.loads(f.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
S=rd(P/'SOURCES.json');assert len(S['sources'])==12
for x in S['sources']:
 b=(R/x['path']).read_bytes() if x['revision'] is None else subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256']
 if x['revision'] is not None and x['path'] not in ['scripts/living_world.gd','scripts/probe_living_world.gd']:
  raw=(R/x['path']).read_bytes();assert raw==b or raw.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
pr=rd(P/'CONTEXT_PREREQUISITE.json');assert pr['status']=='ALL_SELECTED_CONTEXT_FILES_ANONYMOUSLY_VERIFIED_BEFORE_PRODUCTION_EDIT' and pr['file_count']==len(pr['checks'])==57
for x in pr['checks']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert sha(b)==x['sha256'] and len(b)==x['bytes']
B=rd(P/'BASELINE_NEGATIVE.json');assert B['status']=='EXPECTED_BASELINE_FAILURE_VERIFIED' and B['exit_code']==1 and len(B['actual_failure_rows'])==4 and len(B['expected_failure_rows'])==3
F=rd(P/'FOCUSED_GATES.json');assert F['status']=='PASS' and len(F['commands'])==5 and all(x['exit_code']==0 for x in F['commands'])
assert F['production_director_sha256']==sha((R/'scripts/living_world.gd').read_bytes()) and F['regression_probe_sha256']==sha((R/'scripts/probe_living_world.gd').read_bytes())
assert rd(P/'IMPORT.json')['status']=='PASS' and rd(P/'STATIC_GATES.json')['status']=='PASS' and rd(P/'LAUNCH.json')['returncode']==0 and len(rd(P/'CAPTURE_SCRIPT_GATES.json'))==3 and all(x['exit_code']==0 for x in rd(P/'CAPTURE_SCRIPT_GATES.json'))
V=rd(P/'FULL_VALIDATION.json');assert V['status']=='PASS_ALL_82_TRUSTED_NATIVE' and V['trusted_required']==V['trusted_passed']==len(V['rows'])==82 and V['normal_save_hashes_unchanged'] and V['tracked_sidecars_preserved']==1998
ci=(R/'scripts/ci.sh').read_text();roster=re.search(r'for p in (probe_reef_districts .*?); do',ci).group(1).split();assert [x['probe'] for x in V['rows']]==roster
for x in V['rows']:
 b=(P/x['evidence']).read_bytes();assert sha(b)==x['raw_output_sha256'] and len(b)==x['raw_output_bytes'] and x['exit_code']==0 and x['result']=='PASS' and not re.search(V['failure_regex'],b.decode(errors='replace')) and not re.search(V['resource_error_regex'],b.decode(errors='replace'))
C=rd(P/'CAPTURE_CONTRACT.json');assert C['status']=='PASS_DIAGNOSTIC_ONLY' and C['fixture_hash']==sha((P/'capture_startup_retirement.gd').read_bytes());exec(compile(C['exact_check_python'],'R30_CAPTURE_CONTRACT_RECHECK','exec'),{})
idx=rd(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==idx['current_bounded_file_count']==idx['current_unique_sha256_count']==78 and idx['retained_native_added']==202 and idx['excluded_failed_run_native']==124 and idx['directly_viewed_count']==idx['directly_viewed_unique_count']==18
for x in idx['excluded_failed_diagnostics']:assert sha((P/x['path']).read_bytes())==x['sha256'] and not x['credit']
assert len(list((P/'initial_missing_options/native').rglob('*.png')))==46 and len(list((P/'initial_false_key_comparison/native').rglob('*.png')))==78
view=rd(P/'REVIEW.json');assert len(view['ten_axes'])==10 and view['direct_native_views']==idx['directly_viewed_native_files'] and view['startup_role_retirement_count']==3 and view['global_accepted_removed']==0 and view['acceptance']['owner'] is None
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/name);old=rd(O/name);assert d['revision']=='FV-AUDIT-20261014-R30' and d['startup_ambience_retirement']['startup_role_retirements']==3 and d['startup_ambience_retirement']['accepted_removed']==0
 for key in ['pieces','supplemental_piece_records','entries','status_lanes','named_status_counts','startup_ambience_context','current_context_sample_lanes','current_partial_context_counts','teacher_pointer_reuse']:
  if key in old:assert d[key]==old[key],key
T=rd(P/'tally.json');old=rd(O/'tally.json');c=T['current_context'];assert c['exact_capture_count']==2826 and c['retained_native_captures']==c['retained_native_capture_count']==3233 and c['excluded_diagnostic_native_count']==407 and c['partial_overlapping_entries']==78 and c['entries_without_current_slice']==98 and c['complete_entries']==0
assert T['historical_totals'][:-1]==old['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30 and T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
assert rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')
changed=subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).splitlines();assert changed==['scripts/living_world.gd','scripts/probe_living_world.gd'],changed
old=subprocess.check_output(['git','show',BASE+':scripts/living_world.gd'],cwd=R,stderr=subprocess.PIPE).decode();new=(R/'scripts/living_world.gd').read_text();addition='\t# The painted launch menu owns its presentation. Its intro_active input\n\t# guard does not make the retained intro ornaments part of the menu art.\n\tif m.start_menu_active:\n\t\treturn true\n';assert new.replace(addition,'',1)==old and new.count(addition)==1
print('R30_SOURCE_NATIVE_CANONICAL_PASS:57before-editcontext/12sourcebindings;baselinefail/fixed4menuchecks/full82zeroexit;78current/18views/124excluded,2826bounded/3233retained.3boundedretiredstartuproles,0globalacceptance,unknownallgame totals.')
