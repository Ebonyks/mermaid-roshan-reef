"""Validate only bounded R10 marker/source fit and immutable count/source evidence."""
from pathlib import Path
import json,hashlib,subprocess,math
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];OLD=P.parent/'r9_geode_reuse'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(b):return hashlib.sha256(b).hexdigest()
prior=read(OLD/'per_piece.json');now=read(P/'per_piece.json')
assert len(now['pieces'])==224 and len(now['supplemental_piece_records'])==1
assert now['known_named_design_records_including_supplemental']==225 and now['known_family_count_including_supplemental']==30
for a,b in zip(prior['pieces'],now['pieces']):
 assert {k:v for k,v in b.items() if k!='geode_marker_fit'}==a,a['id']
assert now['supplemental_piece_records']==prior['supplemental_piece_records']
t=read(P/'tally.json');old=read(OLD/'tally.json')
for k in ['named_status_counts','known_named_design_records_including_supplemental','known_family_count_including_supplemental','remaining_source_scopes_to_disposition','all_game_individual_piece_total','regression_count','replaced','integrated','runtime_verified','accepted_removed','new_nonruntime_technical_derivatives']:
 assert t[k]==old[k],k
assert t['current_context']['exact_capture_count']==old['current_context']['exact_capture_count']+44==1796
assert t['current_context']['retained_native_captures']==t['current_context']['retained_native_capture_count']==1898
c=read(P/'scene_coverage.json');assert len(c['entries'])==176 and c['partial_entries']==77 and c['complete_entries']==0 and c['entries_without_current_slice']==99
for a,b in zip(read(OLD/'scene_coverage.json')['entries'],c['entries']):assert {k:v for k,v in b.items() if k!='geode_marker_fit'}==a
proof=read(P/'SOURCE_PARITY.json');assert len(proof['captures'])==44 and not proof['raw_byte_changes'] and proof['normal_save_hashes_unchanged_both_aspects']
assert proof['unique_png_sha256_count']==len({x['sha256'] for x in proof['captures']})==35
for cap in proof['captures']:
 raw=(P/cap['path']).read_bytes();assert len(raw)==cap['bytes'] and digest(raw)==cap['sha256'];assert list(Image.open(P/cap['path']).size)==cap['dimensions']
fit=read(P/'FIT_MEASUREMENTS.json');assert fit['draw_box']==[575,165,350,350] and fit['whole_source_translation']==[-20,0]
assert fit['input_seam_points']==read(OLD/'FIT_MEASUREMENTS.json')['input_seam_points'] and fit['input_radius']==56 and fit['input_tap_travel_limit']==34 and fit['pull_required']==120
for row in fit['guide_rows']:
 offset=math.dist(row['original_hit_center'],row['visible_guide_center']);assert abs(offset-row['center_offset'])<1e-9
 assert abs(row['maximum_reach_from_original_center']-(offset+31+5/2))<1e-9 and row['maximum_reach_from_original_center']<=56
for aspect in ['1280x720','1600x720']:
 d=read(P/'native'/aspect/'capture_manifest.json');assert len(d['states'])==22 and not d['errors'] and d['renderer']=='mobile' and d['quality']=='speedy'
 assert d['engine']['major']==4 and d['engine']['minor']==7 and d['engine']['patch']==2 and d['engine']['status']=='stable' and d['engine']['build']=='official'
 assert d['normal_save_before']==d['normal_save_after'] and d['source_revision']=='0c2732204bec7f882db26d835e2ce32ee12c7471'
 assert [x['seams'].count(True) for x in d['states'][6:16]]==[0,1,1,2,2,3,3,4,4,5]
 for st in d['states'][6:16]:assert st['input']['actual_visible_guide_touch'] is True
 assert all(x['pull']==60 for x in d['states'][-4:]) and all(x['painted_closed_candidate_drawn'] for x in d['states'][:18]) and not any(x['painted_closed_candidate_drawn'] for x in d['states'][-4:])
 assert d['candidate_sha256']=='b639c2cbe36b460bb29db5f0e459329f8b6b8266d205412c95e539e9b7dc95ff'
 assert d['candidate_script_sha256']==digest((P/'candidate_geode_surface.gd').read_bytes())
for source in read(P/'SOURCES.json')['sources']:
 raw=subprocess.check_output(['git','show',source['immutable_revision']+':'+source['path']],cwd=R,stderr=subprocess.PIPE);assert len(raw)==source['bytes'] and digest(raw)==source['sha256'],source['path']
pre=read(P/'PREFLIGHT.json')
for source in pre['source_census']:
 raw=(R/source['path']).read_bytes();assert len(raw)==source['bytes'] and digest(raw)==source['sha256'],source['path']
assert not subprocess.check_output(['git','diff','--name-only',pre['baseline'],'--','scripts','scenes','assets','shaders','project.godot'],cwd=R,stderr=subprocess.PIPE).strip()
rev=read(P/'REVIEW.json');assert rev['actually_viewed_unique_native']==5 and len(rev['viewed_native'])==5 and len(rev['all_ten_comparison_axes'])==10
assert not rev['runtime_changes'] and rev['new_generation_calls']==0 and rev['accepted_removed']==0 and not rev['full_context_review_complete'] and all(x is None for x in rev['acceptance_lanes'].values())
assert len(read(P/'SCRIPT_GATES.json'))==4 and all(x['returncode']==0 for x in read(P/'SCRIPT_GATES.json'))
assert read(P/'LAUNCH.json')['returncode']==0
print('R10_FIT|ALL OK|44 diagnostic snapshots; guide halo max55.3 within original56;225 known/30 families;1796 bounded/1898 retained;zero acceptance;production/pixels unchanged')
