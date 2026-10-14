from pathlib import Path
import json,hashlib,subprocess,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r41_companion_context';B='ef3b12fc456720bce2123876fe042ccd9e191505'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['cases'])==6 and len(idx['captures'])==100
assert sum(x['art_context_credit'] for x in idx['captures'])==56
assert len({x['sha256'] for x in idx['captures']})==100
for x in idx['captures']:
 b=(R/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'];assert list(Image.open(R/x['path']).size)==x['aspect']
for c in idx['cases']:
 d=rd(R/c['manifest']['path']);assert d['errors']==[] and d['normal_before']==d['normal_after'] and len(d['normal_before'])==8
 assert d['engine']['major']==4 and d['engine']['minor']==7 and d['engine']['patch']==2 and d['engine']['status']=='stable' and d['engine']['build']=='official'
 assert d['renderer']=='mobile' and d['quality']=='speedy' and d['actual_child_data'] is False
 assert d['synthetic_seed']['custom_fish'] and len(d['synthetic_seed']['custom_friends'])==3
 m={s['id']:s for s in d['states']};assert m['picker_default']['pick_id']==c['identity'] and m['care_saved_colors']['care_open']
 assert not m['confirmed_teardown']['picker_open'] and not m['reentry_cancel_teardown']['picker_open']
 assert m['reloaded_picker_saved_colors']['companion_colors']==d['adopted_colors']
 assert m['castle_card_saved_colors']['castle_card']['identity']==c['identity']
 log=(R/c['result']['path']).parent/'native.log';assert not re.search(r'(?m)^(ERROR:|SCRIPT ERROR|.*Parse Error)|[|]FAIL',log.read_text(encoding='utf-8',errors='replace'))
proof=rd(P/'NATIVE_FIT_PROOF.json');assert proof['current_expected_box_observations']==40 and all(x['expected']==x['actual'] and x['pass'] for x in proof['observations'])
ablation=rd(P/'PREVIEW_SIZE_PROOF.json');assert len(ablation['cases'])==8 and ablation['failures']==0
assert all(x['current_order_reproduces_intrinsic_clamp'] and x['corrected_order_respects_requested_box'] and not x['original_pixels_modified'] for x in ablation['cases'])
assert rd(P/'SIDECAR_GUARD.json')['before_count']==4039 and rd(P/'SIDECAR_GUARD.json')['all_equal']
for d in rd(P/'MEWSHA.json')['cases']:
 assert d['third_color_still_nondrawn'] and len(set(d['third_color_pixel_sha256']))==1 and d['default_preview_matches_R41_decoded_RGBA']
for name,frozen in [('per_piece.json','pieces'),('scene_coverage.json','entries')]:
 a=rd(P/name);o=rd(O/name);assert a[frozen]==o[frozen] and a['companion_preview_fit']['accepted_removed']==0
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 a=rd(P/name);o=rd(O/name)
 for k,v in o.items():
  if k not in ['revision','publication','change_record','current_ci_snapshot','current_context','historical_totals']:assert a[k]==v,(name,k)
t=rd(P/'tally.json');old=rd(O/'tally.json');assert t['historical_totals'][:-1]==old['historical_totals']
assert t['known_named_design_records_including_supplemental']==230 and t['known_family_count_including_supplemental']==31
assert t['all_game_individual_piece_total'] is None and t['regression_count'] is None and t['accepted_removed']==t['integrated']==t['runtime_verified']==0
c=t['current_context'];assert c['exact_capture_count']==3761 and c['retained_native_capture_count']==5299 and c['excluded_diagnostic_native_count']==1538 and 3761+1538==5299
assert c['entries_without_current_slice']==98 and c['partial_overlapping_entries']==78 and c['complete_entries']==0
assert rd(P.parent/'CURRENT.json')['current_tally']=='r42_companion_preview_fit/tally.json'
assert not subprocess.check_output(['git','diff','--name-only',B,'--','assets','scripts','scenes','shaders','addons','project.godot'],cwd=R).strip()
for x in rd(P/'CONTEXT_PREREQUISITE.json')['checks']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R);assert len(b)==x['bytes'] and sha(b)==x['sha256']
for x in rd(P/'REVIEW.json')['source_references']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R);assert sha(b)==x['sha256']
for f in P.rglob('*.json'):assert f.stat().st_size<4194304,f
print('R42_VALIDATE_PASS: actual native/private-save/fit/old-failure/Mewsha pixels/frozen history/canonical counters/current source unchanged; acceptance open')
