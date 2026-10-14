from pathlib import Path
import json,hashlib,subprocess,collections
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r28_teacher_pointer_reuse';BASE='4c5ffcaf73b4b730b266d5bf415fd662bf6084f1'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
S=rd(P/'SOURCES.json');assert len(S['sources'])==10
for x in S['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256'];raw=(R/x['path']).read_bytes();assert sha(raw)==x['current_worktree_raw_sha256'] and (raw==b or raw.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'))
idx=rd(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==idx['current_bounded_file_count']==idx['current_unique_sha256_count']==idx['directly_viewed_count']==16 and idx['excluded_duplicate_file_count']==0
C=rd(P/'CAPTURE_CONTRACT.json');assert C['status']=='PASS_DIAGNOSTIC_ONLY' and C['fixture_hash']==sha((P/'capture_startup.gd').read_bytes());exec(compile(C['exact_check_python'],'R29_CAPTURE_CONTRACT_RECHECK','exec'),{})
assert len(rd(P/'SCRIPT_GATES.json'))==3 and all(x['exit_code']==0 for x in rd(P/'SCRIPT_GATES.json')) and rd(P/'LAUNCH.json')['returncode']==0
D=rd(P/'CATALOGUE_SOURCE_CENSUS.json');assert len(D['catalogue'])==D['registered_stage_count']==100 and len(D['source_slot_to_existing_named_design'])==D['registered_slots']==300 and D['continuous_registered_slots']==200 and D['idle_registered_slots']==100 and D['distinct_raw_motif_tokens']==29 and D['distinct_existing_named_design_ids_used']==26
slots=D['source_slot_to_existing_named_design'];assert len({x['slot_id'] for x in slots})==300 and len({x['existing_piece_id'] for x in slots})==26 and len({x['motif_token'] for x in slots})==29 and sum(D['existing_design_slot_counts'].values())==300 and D['renderer_design_with_zero_current_catalogue_slots'] not in D['existing_design_slot_counts'] and D['visible_screen_total'] is None and not D['all_game_reachability_complete']
for f in (P/'native').glob('*/capture_manifest.json'):assert rd(f)['catalogue']==D['catalogue']
for x in slots:
 spec=D['catalogue'][x['stage_id']];assert x['canvas_layer']==spec['canvas_layer'] and any(y['id']==x['slot_id'] and y['motif']==x['motif_token'] for y in spec['animations']+[spec['idle_event']])
route=rd(P/'ROUTE_CORRECTION.json');assert [x['id'] for x in route['effective_records']]==['intro.storybook','ui.start','ui.intro'] and route['effective_partial_entries']==78 and route['effective_entries_without_current_slice']==98 and route['effective_complete_entries']==0
for x in route['excerpts']:
 ls=(R/x['path']).read_text().splitlines();assert x['exact_lines']==[f'{i+1}: {ls[i]}' for i in range(x['start_line']-1,min(x['end_line'],len(ls)))]
review=rd(P/'REVIEW.json');assert len(review['ten_axes'])==10 and review['direct_native_views']==idx['directly_viewed_native_files'] and review['acceptance']['owner'] is None and not review['source_reuse_first']['generation_required']
selected=['FV-286EA25FDB27','FV-D4719703FA36','FV-2FA8B6B257A3'];assert review['piece_ids']==selected
U=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');oldU=rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert U['records'][:-3]==oldU['records'] and [x['id'] for x in U['records'][-3:]]==selected and len(U['records'])==len({x['id'] for x in U['records']})==54 and len({x['family'] for x in U['records']})==12
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/name);old=rd(O/name);assert d['revision']=='FV-AUDIT-20261014-R29' and d['startup_ambience_context']['piece_ids']==selected and d['startup_ambience_context']['accepted_removed']==d['startup_ambience_context']['new_design_ids']==d['startup_ambience_context']['new_art_drawings']==0
 for k in ['pieces','supplemental_piece_records','entries','named_status_counts','status_lanes','teacher_pointer_context','teacher_pointer_reuse','boxing_pointer_reuse','ballet_pointer_reuse','pointer_candidate','current_context_sample_lanes']:
  if k in old:assert d[k]==old[k],k
T=rd(P/'tally.json');old=rd(O/'tally.json');assert T['historical_totals'][:-1]==old['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
c=T['current_context'];assert c['exact_capture_count']==2748 and c['retained_native_captures']==c['retained_native_capture_count']==3031 and c['excluded_diagnostic_native_count']==283 and c['partial_overlapping_entries']==78 and c['entries_without_current_slice']==98 and c['complete_entries']==0
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30 and T['current_partial_context_counts']['existing_named_records']==54 and T['current_partial_context_counts']['existing_families']==12
assert T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
sc=rd(P/'scene_coverage.json');assert len(sc['entries'])==176 and sc['entries_without_current_slice']==sc['effective_entries_without_current_slice']==98 and sc['partial_entries']==len(sc['effective_current_partial_entry_ids'])==78 and sc['complete_entries']==0
assert set(sc['effective_current_partial_entry_ids'])=={x['id'] for x in rd(O/'scene_coverage.json')['entries'] if x['status']!='COVERAGE_GAP'}|{'intro.storybook'}
assert subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).strip()==''
print('R29_SOURCE_NATIVE_CANONICAL_PASS:10bindings,16natural nativeviews,3partialexisting designs;catalogue100/300/29/26sourceonly;effective78partial/98gaps;0artadoption/acceptance,unknown global totals.')
