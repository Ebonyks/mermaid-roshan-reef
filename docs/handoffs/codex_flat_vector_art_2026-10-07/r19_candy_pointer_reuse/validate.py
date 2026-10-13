"""Bind R19 CandyMaker nonruntime reuse diagnostics to exact source and stable units."""
from pathlib import Path
import json,subprocess,hashlib
P=Path(__file__).resolve().parent;R=P.parents[3];V=P.parent/'r18_candy_pointer_context';BASE='73caf71ad24f1e2471ee8bc4353a60bcfc497e37'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
for x in get('SOURCES.json')['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert x['revision']==BASE and len(b)==x['bytes'] and sha(b)==x['sha256']
 c=(R/x['path']).read_bytes();assert c.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n') if x['path'].endswith(('.gd','.tscn','.godot','.json')) else c==b
idx=get('CAPTURE_INDEX.json');assert idx['native_files']==62 and idx['unique_image_sha256']==62 and idx['excluded']==0
candidate='assets_src/flat_vector_pointer_20261013/pointer_1024.png';candidate_sha=sha((R/candidate).read_bytes());assert candidate_sha=='7e80a06704e21d780e66692c68d1226ea3b9a88544e927ba293b49ed1d3451ec'
prototype=(P/'candidate_candy_surface.gd').read_bytes();prototype_sha=sha(prototype);assert prototype==(R/'.godot/r19_candy_pointer_surface.gd').read_bytes()
s=prototype.decode();assert s.count('draw_texture_rect(')==1 and 'super._draw_demo_finger()' in s and 'if not _is_candymaker_pour():' in s and '_demo_finger_pose()' in s and 'draw_circle(' not in s and 'draw_arc(' not in s
assert (P/'capture_candy_pointer_reuse.gd').read_bytes()==(R/'.godot/r19_capture_candy_pointer_reuse.gd').read_bytes()
for x in idx['rows']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and x['bounded'] and not x['QA11']
for aspect in ['1280x720','1600x720']:
 d=get('native/'+aspect+'/capture_manifest.json');assert d['errors']==[] and len(d['states'])==31 and d['renderer']=='mobile' and d['quality']=='speedy' and d['source_revision']==BASE and d['normal_save_before']==d['normal_save_after']
 e=d['engine'];assert e['major']==4 and e['minor']==7 and e['patch']==2 and e['build']=='official' and e['status']=='stable' and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
 for x in d['states']:
  assert x['mode']=='pourt' and x['visual_context']=='pour_candymaker' and x['phase_index']==0
  c=x['candidate_contract'];assert c['candidate_loaded'] and c['source_sha256']==candidate_sha and c['script_sha256']==prototype_sha and c['tip_error']==0 and c['side']==(58 if c['pressing'] else 54) and c['whole_texture_draw_count']==1 and not c['old_hand_field_required']
  if x['id'].startswith(('normal_','missing_hand_','wrong_')):assert x['pour_level']==0 and x['widget_fill']==0
  if x['id'].startswith('missing_hand'):assert not x['pointer_present'] and c['candidate_draw_active']
  if x['id'].startswith('normal_'):assert x['pointer_present'] and c['candidate_draw_active']
  if x['id']=='ladle_held_08s':assert x['pour_hold'] and x['held'] and 0<x['pour_level']<1 and not c['candidate_draw_active']
  if x['id']=='ladle_released':assert not x['pour_hold'] and not x['held'] and not c['candidate_draw_active']
assert len(get('SCRIPT_GATES.json'))==4 and all(x['exit_code']==0 for x in get('SCRIPT_GATES.json')) and get('LAUNCH.json')['returncode']==0
old=json.loads((V/'per_piece.json').read_text());new=get('per_piece.json');assert [(x['id'],x['status']) for x in old['pieces']]==[(x['id'],x['status']) for x in new['pieces']]
a=json.loads((V/'tally.json').read_text());b=get('tally.json')
for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','current_distinct_screen_total','accepted_removed','integrated','runtime_verified','remaining_source_scopes_to_disposition']:assert a[k]==b[k],k
assert b['historical_totals'][:-1]==a['historical_totals'] and b['current_context_sample_lanes']['samples_awaiting_review']==1
assert b['current_context']['exact_capture_count']==a['current_context']['exact_capture_count']+62==2262 and b['current_context']['retained_native_capture_count']==2376 and b['current_context']['retained_native_captures']==2376
u=get('CURRENT_PARTIAL_CONTEXT_UNION.json');assert len(u['records'])==48 and len({x['family'] for x in u['records']})==9 and u['full_context_review_complete']==0
old_scene=json.loads((V/'scene_coverage.json').read_text());new_scene=get('scene_coverage.json');assert [(x['id'],x['status']) for x in old_scene['entries']]==[(x['id'],x['status']) for x in new_scene['entries']]
assert not subprocess.check_output(['git','diff',BASE,'--','scripts','scenes','assets','assets_src','project.godot','tools'],cwd=R,stderr=subprocess.PIPE)
review=get('REVIEW.json');assert len(review['viewed_native_files'])==8 and len(review['source_images_viewed'])==1 and len(review['ten_axis_comparison'])==10 and review['accepted_removed']==0 and review['candidate']['new_generations']==0
for x in idx['rows']:assert (P/x['path']).relative_to(R).as_posix() in (R/'ASSET_LICENSES.md').read_text(encoding='utf-8')
print('R19 PASS:62 exact native files/two Mobile aspects,22 source hashes,eight direct views/ten axes; one whole reused hand,zero tip error and unchanged passive/wrong/hold/release/save invariants;225/30stable,48partial/9families,one sample/two contexts,zero production adoption/acceptance')
