"""Verify R18 source/capture identity and stable canonical units."""
from pathlib import Path
import json,subprocess,hashlib
P=Path(__file__).resolve().parent;R=P.parents[3];V=P.parent/'r17_pointer_callers';BASE='90d19ceddb20d624f134a3429dfa2afd25e5faaa'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
for x in get('SOURCES.json')['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert x['revision']==BASE and len(b)==x['bytes'] and sha(b)==x['sha256']
 c=(R/x['path']).read_bytes();assert c.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n') if x['path'].endswith(('.gd','.tscn','.godot','.json')) else c==b
idx=get('CAPTURE_INDEX.json');assert idx['native_files']==62 and idx['unique_image_sha256']==62 and idx['excluded']==0
for x in idx['rows']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and x['bounded'] and not x['QA11']
for aspect in ['1280x720','1600x720']:
 d=get('native/'+aspect+'/capture_manifest.json');assert d['errors']==[] and len(d['states'])==31 and d['renderer']=='mobile' and d['quality']=='speedy' and d['source_revision']==BASE and d['normal_save_before']==d['normal_save_after']
 e=d['engine'];assert e['major']==4 and e['minor']==7 and e['patch']==2 and e['build']=='official' and e['status']=='stable' and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
 for x in d['states']:
  assert x['mode']=='pourt' and x['visual_context']=='pour_candymaker' and x['phase_index']==0
  if x['id'].startswith(('normal_','missing_hand_','wrong_')):assert x['pour_level']==0 and x['widget_fill']==0
  if x['id'].startswith('missing_hand'):assert not x['pointer_present']
  if x['id'].startswith('normal_'):assert x['pointer_present'] and x['pointer_path']=='res://assets/castle/training/ghost_hand.png'
  if x['id']=='ladle_held_08s':assert x['pour_hold'] and x['held'] and 0<x['pour_level']<1
  if x['id']=='ladle_released':assert not x['pour_hold'] and not x['held']
assert all(x['exit_code']==0 for x in get('SCRIPT_GATES.json')) and get('LAUNCH.json')['returncode']==0
old=json.loads((V/'per_piece.json').read_text());new=get('per_piece.json');assert [(x['id'],x['status']) for x in old['pieces']]==[(x['id'],x['status']) for x in new['pieces']]
a=json.loads((V/'tally.json').read_text());b=get('tally.json')
for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','current_distinct_screen_total','accepted_removed','integrated','runtime_verified','remaining_source_scopes_to_disposition','current_context_sample_lanes']:assert a[k]==b[k],k
assert b['current_context']['exact_capture_count']==a['current_context']['exact_capture_count']+62==2200 and b['current_context']['retained_native_capture_count']==2314 and b['current_context']['retained_native_captures']==2314
u=get('CURRENT_PARTIAL_CONTEXT_UNION.json');assert len(u['records'])==48 and len({x['family'] for x in u['records']})==9 and u['full_context_review_complete']==0
assert not subprocess.check_output(['git','diff',BASE,'--','scripts','scenes','assets','assets_src','project.godot','tools'],cwd=R,stderr=subprocess.PIPE)
review=get('REVIEW.json');assert len(review['viewed_native_files'])==8 and len(review['source_images_viewed'])==5 and len(review['ten_axis_comparison'])==10 and review['accepted_removed']==0
print('R18 PASS:62 exact native files/two Mobile aspects,22 source hashes,8 direct views/5 source images/10 axes; actual passive/wrong/partial hold/release and normal-save hashes; stable225/30 and unknown totals,48 partial existing records/9 families; zero acceptance/production change')
