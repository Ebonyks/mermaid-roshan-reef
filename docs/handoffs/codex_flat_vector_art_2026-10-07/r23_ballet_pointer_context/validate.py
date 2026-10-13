"""Verify exact Ballet context/source/frozen inventory;no acceptance inference."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r22_candy_stream_onset';BASE='45cb1b26b9bcf16ac1bd5142cc5c38085b631dee'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
sources=read(P/'SOURCES.json')['sources'];assert len(sources)==51
for x in sources:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
 cur=(R/x['path']).read_bytes();assert cur==b or (x['path'].endswith(('.gd','.godot','.json','.tscn')) and cur.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')),x['path']
idx=read(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==idx['unique_sha256_count']==54 and idx['directly_viewed_count']==18 and len(set(idx['directly_viewed_native_files']))==18
for x in idx['files']:
 f=P/x['path'];b=f.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and list(Image.open(f).size)==x['dimensions']
assert len({x['sha256'] for x in idx['files']})==54
manifests=list((P/'native').rglob('capture_manifest.json'));assert len(manifests)==6
modes=['ballet_pose','ballet_ribbon','ballet_twirl']
for f in manifests:
 d=read(f);assert d['source_revision']==BASE and d['errors']==[] and d['teardown_verified'] and len(d['states'])==9
 e=d['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 assert d['renderer']=='mobile' and d['quality']=='speedy' and d['aspect'] in [[1280,720],[1600,720]] and d['normal_save_before']==d['normal_save_after'] and len(d['normal_save_before'])==8
 states={x['id']:x for x in d['states']}
 for s in d['states']:
  assert s['mode']==modes[d['phase']] and s['phase_index']==d['phase'] and s['task_open'] and s['atlas_path']=='res://assets/opera/worlds/actors/animation/roshan_ballerina_sheet_a.png'
  assert s['presentation']['fade_alpha']<=0.02 and not s['presentation']['medal_present']
  b=(f.parent/s['image']['file']).read_bytes();assert len(b)==s['image']['bytes'] and sha(b)==s['image']['sha256']
 for key in ['opened_demo_04s','demo_press_12s']:assert states[key]['demo_active'] and states[key]['guide_expected_visible']
 assert not states['demo_finished_passive']['demo_active'] and not states['demo_finished_passive']['guide_expected_visible']
 for key in ['opened_demo_04s','demo_press_12s','demo_finished_passive','wrong_pressed','wrong_released']:assert states[key]['pose_round']==0 and states[key]['ribbon_progress']==states[key]['twirl_progress']==0.0
 assert not states['correct_released']['held'] and not states['post_input_passive_03s']['held']
 if d['phase']==0:assert states['correct_moved']['pose_round']==1 and states['correct_moved']['guide_expected_visible']
 else:
  key='ribbon_progress' if d['phase']==1 else 'twirl_progress';assert 0<states['correct_moved'][key]<1 and not states['correct_moved']['guide_expected_visible'] and states['correct_released']['guide_expected_visible']
assert read(P/'LAUNCH.json')['returncode']==0 and all(x['exit_code']==0 for x in read(P/'SCRIPT_GATES.json'))
assert b'ERROR:' not in (P/'native_capture.log').read_bytes() and b'SCRIPT ERROR' not in (P/'native_capture.log').read_bytes()
C=read(P/'CALLER_CLOSURE.json');assert C['current_phase_count']==3 and C['current_modes']==modes and C['independent_of_shared_pointer'] and len(C['source_call_sites'])==1
review=read(P/'REVIEW.json');assert len(review['ten_axes'])==10 and review['direct_native_views']==idx['directly_viewed_native_files'] and len(review['direct_source_images_viewed'])==4 and review['acceptance']['owner'] is None
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=read(P/name);prior=read(O/name);assert d['revision']=='FV-AUDIT-20261013-R23'
 for key in ['pieces','supplemental_piece_records','entries','named_status_counts','status_lanes','candy_stream_onset','candy_stream_material','pointer_candidate']:
  if key in prior:assert d[key]==prior[key],key
 x=d['ballet_pointer_context'];assert x['piece_id']=='FV-D2EA0464919A' and x['new_design_ids']==x['new_art_drawings']==x['new_generation_calls']==x['accepted_removed']==0
T=read(P/'tally.json');assert T['accepted_removed']==T['integrated']==T['runtime_verified']==0 and T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None
assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30
C=T['current_context'];assert C['exact_capture_count']==2510 and C['retained_native_capture_count']==C['retained_native_captures']==2624 and C['excluded_diagnostic_native_count']==114 and C['partial_overlapping_entries']==77 and C['complete_entries']==0 and C['entries_without_current_slice']==99
assert T['historical_totals'][:-1]==read(O/'tally.json')['historical_totals'] and T['historical_totals'][-1]['immutable_receipt_revision']==BASE
U=read(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');old=read(O/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert U['current_existing_named_records_with_partial_context']==49 and U['current_existing_families_with_partial_context']==10
assert len(U['records'])==49 and {x['id'] for x in U['records']}=={x['id'] for x in old['records']}|{'FV-D2EA0464919A'} and len({x['family'] for x in U['records']})==10
assert isinstance(T['current_partial_context_union'],str) and T['current_partial_context_counts']['existing_named_records']==49
assert subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).strip()==''
print('R23_SOURCE_NATIVE_CANONICAL_PASS:51exact source references,54native/54unique/18views,three current Ballet modes;49existing partial/10families;0newart/acceptance,unknown totals preserved.')
