"""Verify R20 contact/source/diagnostic evidence without granting art acceptance."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];V=P.parent/'r19_candy_pointer_reuse';BASE='f2b91f6ecfee41adc9c1300a67bdd9cafbe08b17'
def get(n):return json.loads((P/n).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
for x in get('SOURCES.json')['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert x['revision']==BASE and len(b)==x['bytes'] and sha(b)==x['sha256']
 c=(R/x['path']).read_bytes();assert c.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n') if x['path'].endswith(('.gd','.tscn','.godot','.json')) else c==b
assert len(get('SOURCES.json')['sources'])==35 and get('REUSE_NAME_CENSUS.json')['candidate_paths']==276
lookup=get('FILL_CONTACT_ROWS.json');image=Image.open(R/lookup['source_path']).convert('RGBA');assert sha((R/lookup['source_path']).read_bytes())==lookup['source_sha256'] and list(image.size)==lookup['dimensions']
count=0
for y,runs in enumerate(lookup['rows']):
 for a,b in runs:
  for x in range(a,b+1):assert image.getpixel((x,y))[3]>=128;count+=1
assert count==lookup['main_component_pixels']==149243 and (P/'FILL_CONTACT_ROWS.json').read_bytes()==(R/'.godot/r20_fill_contact_rows.json').read_bytes()
prototype=(P/'candidate_stream_surface.gd').read_bytes();assert prototype==(R/'.godot/r20_candy_stream_surface.gd').read_bytes();s=prototype.decode();assert 'func _pour_tick(' not in s and 'func _pour_landing_point(' not in s and s.count('draw_polyline(')==3 and s.index('\t_draw_candymaker_pour_stream()\n\t_draw_progress_overlay(')>0
for n,copy in [('capture_stream_contact.gd','r20_capture_stream_contact.gd'),('capture_stream_partial_release.gd','r20_capture_stream_partial_release.gd')]:assert (P/n).read_bytes()==(R/'.godot'/copy).read_bytes()
idx=get('CAPTURE_INDEX.json');assert idx['native_files']==68 and idx['unique_image_sha256']==54 and idx['excluded']==0 and len(idx['rows'])==68
for x in idx['rows']:
 b=(P/x['path']).read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes'] and x['bounded'] and not x['QA11'];assert (P/x['path']).relative_to(R).as_posix() in (R/'ASSET_LICENSES.md').read_text(encoding='utf-8')
for ref in idx['manifests']:
 d=get(ref['path']);assert sha((P/ref['path']).read_bytes())==ref['sha256'] and d['errors']==[] and d['normal_save_before']==d['normal_save_after'] and d['source_revision']==BASE and d['renderer']=='mobile' and d['quality']=='speedy'
 e=d['engine'];assert e['major']==4 and e['minor']==7 and e['patch']==2 and e['status']=='stable' and e['build']=='official' and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
 states={x['id']:x for x in d['states']};assert len(states)==(10 if ref['path'].startswith('partial_release/') else 12)
 for x in d['states']:
  assert x['mode']=='pourt' and x['visual_context']=='pour_candymaker' and x['phase_index']==0 and x['stream_contract']['prototype_sha256']==sha(prototype) and x['stream_contract']['lookup_sha256']==sha((P/'FILL_CONTACT_ROWS.json').read_bytes())
  if x['id'] in ['ready','passive_03s','wrong_pressed','wrong_released']:assert x['pour_level']==0 and x['widget_fill']==0
  c=x['stream_contract']
  if c.get('valid'):
   px,py=c['source_pixel'];assert image.getpixel((px,py))[3]>=128 and py>=c['reveal_first_source_y'] and c['source_alpha']>=0.5
 low=states['held_08s'];assert 0<low['pour_level']<1 and low['pour_hold'] and low['stream_contract']['stream_active'] and low['stream_contract']['valid'] and not low['stream_contract']['original_endpoint_in_revealed_alpha']
 assert not states['held_02s']['stream_contract']['valid'],'Near-zero onset limit must remain explicit'
 assert not states['released']['pour_hold'] and not states['released']['held'] and not states['released']['stream_contract']['stream_active']
 if ref['path'].startswith('partial_release/'):
  assert 0<states['dragged_12px']['pour_level']<1 and states['dragged_12px']['pour_hold'] and states['dragged_12px']['held'] and states['dragged_12px']['stream_contract']['stream_active']
  assert 0<states['released']['pour_level']<1
 else:assert states['held_40s']['pour_level']==1 and not states['held_40s']['stream_contract']['stream_active'],'Incidental terminal scope retained,not partial-release evidence'
for n in ['SCRIPT_GATES.json','PARTIAL_RELEASE_SCRIPT_GATES.json']:assert all(x['exit_code']==0 for x in get(n))
for n in ['LAUNCH.json','PARTIAL_RELEASE_LAUNCH.json']:assert get(n)['returncode']==0
for n in ['native_capture.log','partial_release_native.log']:assert 'ERROR:' not in (P/n).read_text(encoding='utf-8',errors='replace')
a=json.loads((V/'per_piece.json').read_text());b=get('per_piece.json');assert [(x['id'],x['status']) for x in a['pieces']]==[(x['id'],x['status']) for x in b['pieces']]
a=json.loads((V/'tally.json').read_text());b=get('tally.json')
for k in ['named_piece_records','named_family_count','named_status_counts','all_game_individual_piece_total','current_distinct_screen_total','accepted_removed','integrated','runtime_verified','remaining_source_scopes_to_disposition','current_context_sample_lanes']:assert a[k]==b[k],k
assert b['historical_totals'][:-1]==a['historical_totals'] and b['current_context']['exact_capture_count']==a['current_context']['exact_capture_count']+68==2330 and b['current_context']['retained_native_capture_count']==2444 and b['current_context']['retained_native_captures']==2444
u=get('CURRENT_PARTIAL_CONTEXT_UNION.json');assert len(u['records'])==48 and len({x['family'] for x in u['records']})==9 and u['full_context_review_complete']==0
assert not subprocess.check_output(['git','diff',BASE,'--','scripts','scenes','assets','assets_src','project.godot','tools'],cwd=R,stderr=subprocess.PIPE)
r=get('REVIEW.json');assert len(r['viewed_native_files'])==14 and len(r['source_images_viewed'])==6 and len(r['ten_axis_comparison'])==10 and r['new_drawing_samples']==r['new_generation_calls']==r['accepted_removed']==0
print('R20 PASS:68 exact native event files/54 unique hashes,35 source hashes,14 direct views/six source views/ten axes; low-fill contact and actual partial release,near-zero/flat material/terminal limits explicit;149243pixel read-only functional lookup;225/30stable,48partial/9families,one old sample/zero adoption,global totals unknown')
