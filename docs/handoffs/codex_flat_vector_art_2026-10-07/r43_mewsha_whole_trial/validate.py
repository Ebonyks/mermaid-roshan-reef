from pathlib import Path
import json,hashlib,subprocess,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r42_companion_preview_fit';A=R/'assets_src/flat_vector_r43_mewsha_whole_20261015';B='1ca647a57943dc4b6a645f7cffb85a9be600f173'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['cases'])==7 and sum(x['current_fixture'] for x in idx['cases'])==6
assert len(idx['captures'])==132 and sum(x['art_context_credit'] for x in idx['captures'])==60
assert len({x['sha256'] for x in idx['captures']})==idx['summary']['unique_png_byte_hashes']==132
for x in idx['captures']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and list(Image.open(R/x['path']).size)==x['aspect']
for c in idx['cases']:
 d=rd(R/c['manifest']['path']);assert d['errors']==[] and d['normal_before']==d['normal_after'] and len(d['normal_before'])==8 and d['actual_child_data'] is False
 assert d['engine']['major']==4 and d['engine']['minor']==7 and d['engine']['patch']==2 and d['engine']['status']=='stable' and d['engine']['build']=='official'
 assert d['renderer']=='mobile' and d['quality']=='speedy' and len(d['synthetic_seed']['custom_friends'])==3 and d['synthetic_seed']['custom_fish']
 states={x['id']:x for x in d['states']};assert states['picker_default']['pick_id']==c['identity'] and states['care_saved_colors']['care_open']
 assert not states['confirmed_teardown']['picker_open'] and not states['reentry_cancel_teardown']['picker_open']
 assert states['reloaded_picker_saved_colors']['companion_colors']==d['adopted_colors'] and states['castle_card_saved_colors']['castle_card']['identity']==c['identity']
 log=(R/c['result']['path']).parent/'native.log';assert not re.search(r'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR|Shader compilation failed|[|]FAIL',log.read_text(encoding='utf-8',errors='replace'))
 if c['current_fixture']:
  for x in rd(R/c['launch']['path'])['source_bindings_before_launch']:assert sha((R/x['path']).read_bytes())==x['sha256']
  if c['identity']=='mewsha':
   assert states['castle_card_saved_colors']['castle_card']['child_count']==1
   for slot in range(3):
    for i in range(8):
     st=states['slot%d_color%d'%(slot,i)];nodes=[n for n in st['nodes'] if n.get('r43_whole_unit') and 'StuffiePreviewCard' in n['path']];assert len(nodes)==1 and nodes[0]['r43_palette_tokens']==st['pick_colors']
geometry=rd(P/'WHOLE_UNIT_GEOMETRY_PROOF.json');assert geometry['current_whole_image_observations']==124 and len(geometry['observations'])==124
assert all(x['uniform_whole_image'] and x['meaningful_alpha_inside_requested_box'] for x in geometry['observations'])
assert len(geometry['inherited_nonpaintable_fit_observations'])==40 and all(x['expected']==x['actual'] for x in geometry['inherited_nonpaintable_fit_observations'])
for case in rd(P/'PALETTE_PIXEL_PROOF.json')['cases']:
 w=case['aspect'][0];q=P/'native'/('native_current_%d_mewsha'%w)/'captures'
 for slot in case['slots']:
  hashes=[sha(Image.open(q/('slot%d_color%d.png'%(slot['slot'],i))).convert('RGBA').crop(tuple(case['ROI'])).tobytes()) for i in range(8)]
  assert hashes==slot['ROI_sha256'] and len(set(hashes))==8
 assert case['slots'][2]['red_vs_green_changed_pixel_count']==1613
for x in rd(O/'MEWSHA.json')['cases']:assert len(set(x['third_color_pixel_sha256']))==1
native=Image.open(A/'mewsha_native.png');roundtrip=Image.open(A/'native_roundtrip.png');assert native.mode==roundtrip.mode=='RGBA' and native.size==roundtrip.size==(1254,1254) and native.tobytes()==roundtrip.tobytes()
assert Image.open(A/'mewsha_1024.png').size==(1024,1024)
master=rd(A/'MASTER_PROOF.json');assert master['layers']==master['frames']==1 and master['native_roundtrip_decoded_RGBA_exact'] and not any(master[x] for x in ['crop','redraw','recolor','part_separation'])
for x in master['files']:assert sha((R/x['path']).read_bytes())==x['sha256']
gen=rd(A/'GENERATION_RESULT.json');assert gen['call_count']==gen['call_cap_total']==1 and gen['cap_exhausted'] and gen['sha256']==sha((A/'mewsha_native.png').read_bytes())
assert rd(P/'PLAN.json')['generation_job']['used_calls']==1 and rd(P/'PLAN.json')['generation_job']['attempt_cap_total']==1
assert rd(P/'SIDECAR_GUARD.json')['before_count']==4039 and rd(P/'SIDECAR_GUARD.json')['all_equal']
for name,frozen in [('per_piece.json','pieces'),('scene_coverage.json','entries')]:assert rd(P/name)[frozen]==rd(O/name)[frozen]
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 a=rd(P/name);o=rd(O/name)
 for k,v in o.items():
  if k not in ['revision','publication','change_record','current_ci_snapshot','current_context','historical_totals','current_context_sample_lanes']:assert a[k]==v,(name,k)
t=rd(P/'tally.json');assert t['historical_totals'][:-1]==rd(O/'tally.json')['historical_totals'];assert t['known_named_design_records_including_supplemental']==230 and t['known_family_count_including_supplemental']==31
assert t['all_game_individual_piece_total'] is None and t['regression_count'] is None and t['accepted_removed']==t['integrated']==t['runtime_verified']==0
c=t['current_context'];assert c['exact_capture_count']==3821 and c['retained_native_capture_count']==5431 and c['excluded_diagnostic_native_count']==1610 and 3821+1610==5431
assert c['entries_without_current_slice']==98 and c['partial_overlapping_entries']==78 and c['complete_entries']==0
assert t['current_context_sample_lanes']['unique_whole_drawing_samples']==t['current_context_sample_lanes']['samples_awaiting_review']==3
assert rd(P.parent/'CURRENT.json')['current_tally']=='r43_mewsha_whole_trial/tally.json'
assert not subprocess.check_output(['git','diff','--name-only',B,'--','assets','scripts','scenes','shaders','addons','project.godot'],cwd=R).strip()
for x in rd(P/'CONTEXT_PREREQUISITE.json')['checks']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R);assert len(b)==x['bytes'] and sha(b)==x['sha256']
for x in rd(P/'REVIEW.json')['source_references']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R) if x['revision'] else (R/x['path']).read_bytes();assert sha(b)==x['sha256']
for f in [*P.rglob('*.json'),*A.rglob('*.json')]:assert f.stat().st_size<4194304,f
print('R43_VALIDATE_PASS: actual3slot-pixels/save/onewhole-image/identityguards/native/ASEPRITE/sourcecap/frozenhistory/counters; artQC/globalacceptance open')
