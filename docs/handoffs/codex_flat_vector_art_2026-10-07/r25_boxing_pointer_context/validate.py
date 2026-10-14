"""Verify exact current Boxing first-phase context and preserved invalid initial snapshots;no acceptance inference."""
from pathlib import Path
import json,hashlib,subprocess,math
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r24_ballet_pointer_reuse';BASE='ef975b9e92903ee61c585f9230c26f1dcb06641c'
def read(f):return json.loads(f.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
sources=read(P/'SOURCES.json')['sources'];assert len(sources)==57
for x in sources:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256'],x['path']
 c=(R/x['path']).read_bytes();assert c==b or (x['path'].endswith(('.gd','.json','.godot','.tscn','.md')) and c.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')),x['path']
idx=read(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==60 and idx['current_bounded_file_count']==idx['excluded_alias_file_count']==30 and idx['directly_viewed_count']==12 and idx['total_direct_native_views']==24
for x in idx['files']:
 f=P/x['path'];b=f.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and list(Image.open(f).size)==x['dimensions']
assert len({x['sha256'] for x in idx['files']})==idx['unique_sha256_count']
current=[x for x in idx['files'] if x['scope']=='CURRENT_BOUNDED_CONTEXT'];assert len({x['sha256'] for x in current})==idx['current_unique_sha256_count']==30
assert set(idx['directly_viewed_native_files'])<=set(x['path'] for x in current)
assert '.duplicate(true)' in (P/'capture_boxing_context.gd').read_text() and '.duplicate(true)' not in (P/'initial_aliased_state/capture_boxing_context.gd').read_text().split('"guide_done":')[1].split(',"touch_owners"')[0]
fs=list((P/'native').rglob('capture_manifest.json'));assert len(fs)==2
for f in fs:
 d=read(f);e=d['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 assert d['source_revision']==BASE and d['renderer']=='mobile' and d['quality']=='speedy' and d['phase']==0 and d['errors']==[] and d['teardown_verified'] and len(d['states'])==15
 assert d['normal_save_before']==d['normal_save_after'] and len(d['normal_save_before'])==8
 states={x['id']:x for x in d['states']}
 for x in d['states']:
  assert x['mode']=='boxing_guide' and x['phase_index']==0 and x['task_open'] and not x['finished'] and not x['completion_accepted']
  assert x['presentation']['fade_alpha']<=0.02 and not x['presentation']['medal_present']
  b=(f.parent/x['image']['file']).read_bytes();assert len(b)==x['image']['bytes'] and sha(b)==x['image']['sha256']
  guide=x['guide_formula'];assert guide['hand'] in [0,1] and 0<=guide['travel']<=1
  for axis in range(2):assert abs(guide['at'][axis]-(guide['start'][axis]+(guide['target'][axis]-guide['start'][axis])*guide['travel']))<0.001
  accepted=x['id'] in ['correct_target','correct_released','post_release_04s'];assert x['guide_done']==([True,False] if accepted else [False,False]) and x['round_index']==x['landed_count']==(1 if accepted else 0) and x['phase_progress']==(1.0 if accepted else 0.0)
 for key in ['opened_demo_04s','demo_left_12s','demo_left_22s','demo_right_28s','demo_right_38s','passive_assist_56s']:assert states[key]['demo_active'] and states[key]['guide_expected_visible']
 assert states['demo_left_12s']['guide_formula']['hand']==states['demo_left_22s']['guide_formula']['hand']==0
 assert states['demo_right_28s']['guide_formula']['hand']==states['demo_right_38s']['guide_formula']['hand']==1
 assert states['passive_assist_56s']['assist_level']>=1 and states['passive_assist_56s']['demo_t']<2
 for key in ['wrong_pressed','wrong_moved','correct_pressed','correct_mid','correct_target','correct_released','post_release_04s']:assert not states[key]['demo_active']
 assert states['wrong_released']['demo_active'] and states['wrong_returned_025s']['demo_active']
 for key in ['wrong_released','correct_released','post_release_04s']:assert not states[key]['held'] and states[key]['touch_owners']=={}
 old=read(P/'initial_aliased_state/native'/f.parent.relative_to(P/'native')/'capture_manifest.json');assert old['states'][0]['guide_done']==[True,False] and old['states'][0]['round_index']==0
assert read(P/'LAUNCH.json')['returncode']==0 and all(x['exit_code']==0 for x in read(P/'SCRIPT_GATES.json'))
assert b'ERROR:' not in (P/'native_capture.log').read_bytes() and b'SCRIPT ERROR' not in (P/'native_capture.log').read_bytes()
review=read(P/'REVIEW.json');assert len(review['ten_axes'])==10 and review['direct_native_views']==idx['directly_viewed_native_files'] and len(review['direct_source_images_viewed'])==13 and review['acceptance']['owner'] is None
caller=read(P/'CALLER_CLOSURE.json');assert caller['current_phase_count']==5 and caller['current_modes']==['boxing_guide','boxing_jab','boxing_guard','boxing_imp','boxing_belt'] and len(caller['source_call_sites'])==1 and not caller['full_caller_coverage_complete']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=read(P/name);old=read(O/name);assert d['revision']=='FV-AUDIT-20261014-R25'
 for key in ['pieces','supplemental_piece_records','entries','named_status_counts','status_lanes','current_context_sample_lanes','ballet_pointer_reuse','ballet_pointer_context','candy_stream_material','pointer_candidate']:
  if key in old:assert d[key]==old[key],key
 x=d['boxing_pointer_context'];assert x['piece_id']=='FV-DAA9072B905A' and x['new_design_ids']==x['new_art_drawings']==x['new_generation_calls']==x['accepted_removed']==0 and x['current_phase_contexts']==1
T=read(P/'tally.json');assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30
assert T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
C=T['current_context'];assert C['exact_capture_count']==2594 and C['retained_native_capture_count']==C['retained_native_captures']==2738 and C['excluded_diagnostic_native_count']==144 and C['partial_overlapping_entries']==77 and C['complete_entries']==0 and C['entries_without_current_slice']==99
assert T['historical_totals'][:-1]==read(O/'tally.json')['historical_totals'] and T['historical_totals'][-1]['immutable_receipt_revision']==BASE
U=read(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');old=read(O/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert U['current_existing_named_records_with_partial_context']==50 and U['current_existing_families_with_partial_context']==11
assert len(U['records'])==50 and len({x['family'] for x in U['records']})==11 and {x['id'] for x in U['records']}=={x['id'] for x in old['records']}|{'FV-DAA9072B905A'} and not U['full_context_review_complete']
assert isinstance(T['current_partial_context_union'],str) and T['current_partial_context_counts']['existing_named_records']==50
assert subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).strip()==''
print('R25_SOURCE_NATIVE_CANONICAL_PASS:57exact source bindings;30corrected native/30unique/12current views,30initial excluded;50existing partial/11families,0newart/adoption/acceptance;unknown totals and4modes remain open.')
