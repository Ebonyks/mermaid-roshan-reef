"""Validate count-unit preservation and verified source audit consistency; no art acceptance."""
from pathlib import Path
import json,subprocess,hashlib
P=Path(__file__).resolve().parent;R=P.parents[3];OLD='d26512b120500492be8e2694ac552a187f0091ca';PREV=P.parent/'r12_geode_layered_reveal'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def frozen(n):return json.loads(subprocess.check_output(['git','show',OLD+':'+(PREV/n).relative_to(R).as_posix()],cwd=R,stderr=subprocess.PIPE))
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=get(n);assert d['revision']=='FV-AUDIT-20261013-R13' and d['geode_source_closure']['native_captures_added']==0 and d['geode_source_closure']['accepted_removed']==0
pieces=get('per_piece.json');assert pieces['pieces']==frozen('per_piece.json')['pieces'] and pieces['supplemental_piece_records']==frozen('per_piece.json')['supplemental_piece_records']
coverage=get('scene_coverage.json');assert coverage['entries']==frozen('scene_coverage.json')['entries'];assert (coverage['partial_entries'],coverage['complete_entries'],coverage['entries_without_current_slice'])==(77,0,99)
t=get('tally.json');old=frozen('tally.json')
for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','source_function_scopes','source_image_count','replaced','integrated','runtime_verified','accepted_removed','remaining_source_scopes_to_disposition','regression_count','current_context','published_technical_source_trials','new_nonruntime_technical_derivatives']:
 assert t[k]==old[k],k
assert t['all_game_individual_piece_total'] is None and t['current_distinct_screen_total'] is None and t['accepted_removed']==0
assert t['historical_totals'][:-1]==old['historical_totals'];assert t['historical_totals'][-1]['immutable_commit']==OLD
assert t['known_named_design_records_including_supplemental']==225 and t['known_family_count_including_supplemental']==30
au=get('SOURCE_AUDIT.json');assert len(au['crystal_resource_consumers'])==3 and au['unused_binding']['draw_consumer_count']==0
assert len(au['unused_binding']['geode_texture_occurrences'])==2 and len(au['rejected_checkerboard_sheets'])==2
assert not au['scope']['runtime_caller_closure_complete'] and not au['whole_unit_disposition']['complete_approved_action_family_found']
review=get('REVIEW.json');assert len(review['all_ten_comparison_axes'])==10 and len(review['existing_native_images_reinspected'])==3 and len(review['source_images_inspected'])==3
assert all(review[k] is None for k in ['candidate','integration','runtime_verified_replacement','device','child','owner','QA11'])
for x in au['image_inventory']+au['source_files']+au['provenance']+review['existing_native_images_reinspected']+review['same_scene_reference_bindings']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
parity=get('ORIGIN_DEV_RECONCILIATION.json');assert not parity['production_diff_paths'] and parity['origin_dev']=='831d0bbb155b99d75ef0289cc5cc694e0ef00c1e'
changed=subprocess.check_output(['git','diff','--name-only',OLD,'--','scripts','scenes','assets','shaders','project.godot'],cwd=R,stderr=subprocess.PIPE).decode();assert not changed
print('R13_VALIDATION_OK; frozen counts/history preserved; declared source bindings exact; whole-game/runtime/acceptance still open')
