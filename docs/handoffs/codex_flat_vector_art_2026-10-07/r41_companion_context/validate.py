"""R41 original-source consumer evidence. Machine/source checks do not accept artwork."""
from pathlib import Path
import json,hashlib,subprocess,math,re
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r40_craft_whole_fish_trial';B='de44f9bb67ae7cb41a33d6eba25d56d9ed074f21'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def check(x):
 b=git('show',x['revision']+':'+x['path']) if x.get('revision') else (R/x['path']).read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes'],x['path']
def eq(a,b):
 if isinstance(a,list) and isinstance(b,list):return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 if isinstance(a,(float,int)) and isinstance(b,(float,int)) and not isinstance(a,bool) and not isinstance(b,bool):return math.isfinite(a) and math.isfinite(b) and abs(a-b)<=1e-6
 return type(a)==type(b) and a==b
assert eq([.9200000167],[.92]) and not eq([.92],[.922]) and not eq([1],[0]) and not eq(['cat'],['bird']) and not eq([0]*6,[0]*8) and not eq([float('nan')],[0]) and not eq([True],[1])
c=rd(P/'CAPTURE_INDEX.json');s=c['summary'];assert len(c['cases'])==11 and len(c['captures'])==167 and sum(x['current_fixture'] for x in c['cases'])==6;assert sum(x['art_context_credit'] for x in c['captures'])==56 and s['excluded_native']==111;assert (s['current_bounded'],s['current_retained'],s['current_excluded'])==(3705,5199,1494)
for x in c['files']:check(x)
for x in c['captures']:assert list(Image.open(R/x['path']).size)==x['aspect'];assert not x['art_context_credit'] or x['current_fixture']
known={sha(f.read_bytes()) for f in P.rglob('*.gd')};seen=set();normal=None
for case in c['cases']:
 check(case['manifest']);check(case['launch']);check(case['result']);d=rd(R/case['manifest']['path']);launch=rd(R/case['launch']['path']);assert launch['fixture_sha256'] in known;assert case['native_exit_code']==0 and d['errors']==[] and d['source_revision']==B and d['normal_before']==d['normal_after'] and len(d['normal_before'])==8 and not d['actual_child_data'];assert d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079' and d['engine']['major']==4 and d['engine']['minor']==7 and d['engine']['patch']==2 and d['renderer']=='mobile' and d['quality']=='speedy'
 if normal is None:normal=d['normal_before']
 assert normal==d['normal_before']
 private=rd((R/case['manifest']['path']).parent/'private_profile/reef_save.json');assert private['companion']==d['identity'] and private['companion_colors']==d['adopted_colors'] and private['care_points']==8
 for key in ['custom_fish','custom_friends']:assert eq(private[key],d['synthetic_seed'][key]),(case['attempt'],key)
 if not case['current_fixture']:continue
 seen.add((d['identity'],d['aspect'][0]));states={x['id']:x for x in d['states']}
 if d['identity']=='mewsha':
  for slot in range(3):
   colors=[]
   for i in range(8):
    st=states[f'slot{slot}_color{i}'];assert st['pick_slot']==slot and st['input']['palette_index']==i;colors.append(st['pick_colors'][slot])
   assert len(set(colors))==8
 else:
  assert case['attempt'].startswith('native_swap_')
  for name in ['picker_default','nonpaintable_identity_guard']:
   assert not any('/StuffiePart_' in n['path'] or '/StuffieSwatch_' in n['path'] for n in states[name]['nodes'])
 for name in ['castle_card_default_colors','castle_card_saved_colors']:
  card=states[name]['castle_card'];assert card['visible'] and card['identity']==d['identity'];assert card['child_count']==(3 if d['identity']=='mewsha' else 1)
 assert states['reloaded_picker_saved_colors']['pick_colors']==d['adopted_colors']
assert seen=={(identity,width) for identity in ['mewsha','eagle','lamma'] for width in [1280,1600]}
proof=rd(P/'PREVIEW_SIZE_PROOF.json');assert len(proof['cases'])==8 and proof['failures']==0 and all(x['current_order_reproduces_intrinsic_clamp'] and x['corrected_order_respects_requested_box'] and x['original_pixels_modified'] is False for x in proof['cases'])
for x in rd(P/'THIRD_COLOR_PIXEL_PROOF.json')['comparisons']:
 row=next(r for r in c['captures'] if r['attempt']==f"native_current_{x['width']}_mewsha" and r['state']==x['state']);assert row['sha256']==x['native_sha256'];im=np.array(Image.open(R/row['path']).convert('RGBA'));left,top,right,bottom=x['ROI_xyxy'];assert sha(im[top:bottom,left:right].tobytes())==x['ROI_decoded_RGBA_sha256'] and x['changed_ROI_pixels_vs_color0']==0
review=rd(P/'REVIEW.json');assert len(review['direct_native_views'])==14 and len(review['prior_direct_native_views'])==10 and len(review['direct_source_view_paths'])==6 and len(review['ten_axes'])==10
for x in review['direct_native_views']+review['prior_direct_native_views']+review['source_references']:check(x)
for x in rd(P/'CONTEXT_PREREQUISITE.json')['checks']:check(x)
g=rd(P/'SIDECAR_GUARD.json');assert g['before']==g['after'] and len(g['before'])==4039
for p,digest in g['after'].items():assert sha((R/p).read_bytes())==digest,p
assert not git('diff','--name-only',B,'--','assets','scripts','scenes','shaders','addons','project.godot').strip()
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/name);new=rd(P/name);assert new['revision']=='FV-AUDIT-20261014-R41' and new['companion_context']['accepted_removed']==new['companion_context']['new_generation_calls']==0
 for k in ['pieces','entries','observations']:
  if k in old:assert new[k]==old[k],(name,k)
 if name=='per_piece.json':
  assert new['supplemental_piece_records'][:len(old['supplemental_piece_records'])]==old['supplemental_piece_records'];roles=new['pieces']+new['supplemental_piece_records'];assert len(roles)==230 and len({x['id'] for x in roles})==230 and len({x['family'] for x in roles})==31
  for x in new['supplemental_piece_records'][-3:]:assert x['id']=='FVR-'+sha(('companion::'+x['source']['identity']+'_whole_assembly').encode())[:12].upper()
t=rd(P/'tally.json');assert t['historical_totals'][:-1]==rd(O/'tally.json')['historical_totals'];assert t['current_context']['exact_capture_count']==3705 and t['current_context']['retained_native_capture_count']==5199 and t['current_context']['excluded_diagnostic_native_count']==1494;assert t['known_named_design_records_including_supplemental']==230 and t['known_family_count_including_supplemental']==31;assert t['all_game_individual_piece_total'] is None and t['accepted_removed']==t['integrated']==t['runtime_verified']==0;assert t['current_context']['entries_without_current_slice']==98 and t['current_context_sample_lanes']['unique_whole_drawing_samples']==2
assert rd(P.parent/'CURRENT.json')['revision']=='FV-AUDIT-20261014-R41'
for p in P.rglob('*.json'):assert p.stat().st_size<4*1024*1024,p
print('R41_SOURCE_NATIVE_CANONICAL_PASS 167retained/56credits/111excluded;6supportedcurrent;14current10priorviews;8bad/fixedorderpairs;16thirdROIinvariant;4039sidecars;230roles31families;accepted0/globalunknown')
