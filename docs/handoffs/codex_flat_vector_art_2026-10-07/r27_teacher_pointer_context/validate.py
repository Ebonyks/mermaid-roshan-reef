"""Validate source-bound Teacher diagnostics; no creative or authoritative runtime acceptance."""
from pathlib import Path
import json,hashlib,subprocess,math
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r26_boxing_pointer_reuse';BASE='b5c061dfd5bc36b405bd38aa0ac141eba277a012'
def read(f):return json.loads(f.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
sources=read(P/'SOURCES.json')['sources'];assert len(sources)==36
for x in sources:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256']
 c=(R/x['path']).read_bytes();assert sha(c)==x['current_worktree_raw_sha256'] or c.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
idx=read(P/'CAPTURE_INDEX.json');current=[x for x in idx['files'] if x['scope']=='CURRENT_BOUNDED_CONTEXT'];assert idx['current_bounded_file_count']==len(current)==84 and idx['directly_viewed_count']==20
for x in idx['files']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and list(Image.open(P/x['path']).size)==x['dimensions']
assert len({x['sha256'] for x in current})==idx['current_unique_sha256_count']
assert set(idx['directly_viewed_native_files'])<=set(x['path'] for x in current)
assert '.duplicate(true)' in (P/'capture_teacher_context.gd').read_text() and 'surface.finished' not in (P/'capture_teacher_context.gd').read_text()
fs=list((P/'native').rglob('capture_manifest.json'));assert len(fs)==8
kinds=['pattern','count','add','match'];state_counts=[7,13,15,7]
for f in fs:
 d=read(f);e=d['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 phase=d['phase'];assert d['source_revision']==BASE and d['renderer']=='mobile' and d['quality']=='speedy' and d['errors']==[] and d['teardown_verified'] and len(d['states'])==state_counts[phase]
 assert d['normal_save_before']==d['normal_save_after'] and len(d['normal_save_before'])==8
 states={x['id']:x for x in d['states']}
 for x in d['states']:
  assert x['mode']=='teacher_'+kinds[phase] and x['lesson']['kind']==kinds[phase] and x['lesson']['tier']==x['lesson']['sequence']==0 and x['phase_index']==phase and x['task_open'] and not x['solved'] and not x['completion_accepted'] and x['phase_progress']==0.0
  assert len(x['backdrop_tiles'])==8 and all('room_library_background' in p for p in x['backdrop_tiles']) and x['actor_atlas']=='res://assets/opera/worlds/actors/animation/roshan_teacher_sheet_a.png' and x['actor_visible']
  assert x['presentation']['fade_alpha']<=0.02 and not x['presentation']['medal_present']
  b=(f.parent/x['image']['file']).read_bytes();assert len(b)==x['image']['bytes'] and sha(b)==x['image']['sha256'] and x['image']['dimensions']==d['aspect']
  if x['id'].endswith('released') or x['id'] in ['final_partial','join_moving','join_settled']:assert not x['held'] and x['touch_owner']==-1
 opened=states['opened_04s'];passive=states['passive_96s'];assert not any(opened['counted']) and not any(passive['counted']) and passive['help_visible'] and passive['assisted'] and not opened['assisted']
 if phase in [0,3]:
  assert not opened['guide_formula']['expected_visible'] and passive['guide_formula']['target_role']=='CORRECT_ANSWER_CARD' and states['wrong_choice_released']['wrong_attempts']==1
 elif phase==1:
  assert opened['counted']==[False] and opened['guide_formula']['target_role']=='NEXT_UNTOUCHED_COUNTER' and states['wrong_choice_released']['wrong_attempts']==0
  assert states['counter0_released']['counted']==states['counter0_repeat_released']['counted']==[True] and states['counter0_released']['can_answer'] and states['counter0_released']['guide_formula']['target_role']=='CORRECT_ANSWER_CARD' and not states['counter0_released']['demo_active']
  assert states['count_answer_wrong_released']['wrong_attempts']==1 and states['count_answer_wrong_released']['counted']==[True]
 else:
  assert not opened['joined'] and opened['guide_formula']['target_role']=='JOIN_BUTTON' and states['wrong_choice_released']['wrong_attempts']==0
  assert states['join_released']['joined'] and 0<states['join_moving']['join_t']<0.4 and states['join_settled']['join_t']==0
  assert states['counter0_released']['counted']==states['counter0_repeat_released']['counted']==[True,False] and not states['final_partial']['can_answer'] and states['final_partial']['guide_formula']['at']==[799,290]
assert read(P/'LAUNCH.json')['returncode']==0 and len(read(P/'SCRIPT_GATES.json'))==3 and all(x['exit_code']==0 for x in read(P/'SCRIPT_GATES.json'))
assert b'ERROR:' not in (P/'native_capture.log').read_bytes() and b'SCRIPT ERROR' not in (P/'native_capture.log').read_bytes()
assert b"'finished'" in (P/'initial_invalid_field/native_capture.log').read_bytes() and read(P/'initial_invalid_field/LAUNCH.json')['returncode']!=0
review=read(P/'REVIEW.json');assert len(review['ten_axes'])==10 and review['direct_native_views']==idx['directly_viewed_native_files'] and len(review['direct_source_images_viewed'])==10 and review['acceptance']['owner'] is None
caller=read(P/'CALLER_CLOSURE.json');assert caller['current_phase_count']==4 and caller['current_modes']==['teacher_'+k for k in kinds] and not caller['full_caller_coverage_complete']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=read(P/name);old=read(O/name);assert d['revision']=='FV-AUDIT-20261014-R27'
 for key in ['pieces','supplemental_piece_records','entries','named_status_counts','status_lanes','current_context_sample_lanes','boxing_pointer_reuse','boxing_pointer_context','ballet_pointer_reuse','candy_stream_material','pointer_candidate']:
  if key in old:assert d[key]==old[key],key
 x=d['teacher_pointer_context'];assert x['piece_id']=='FV-E1049E4945A3' and x['new_design_ids']==x['new_art_drawings']==x['new_generation_calls']==x['accepted_removed']==0 and x['current_phase_contexts']==4
T=read(P/'tally.json');assert T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30
assert T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0
C=T['current_context'];old=read(O/'tally.json')['current_context'];assert C['exact_capture_count']==old['exact_capture_count']+84 and C['retained_native_capture_count']==C['retained_native_captures']==old['retained_native_captures']+idx['native_file_count'] and C['excluded_diagnostic_native_count']==old['excluded_diagnostic_native_count']+idx['excluded_invalid_file_count'] and C['partial_overlapping_entries']==77 and C['complete_entries']==0 and C['entries_without_current_slice']==99
assert C['exact_capture_count']+C['excluded_diagnostic_native_count']==C['retained_native_captures']
assert T['historical_totals'][:-1]==read(O/'tally.json')['historical_totals'] and T['historical_totals'][-1]['immutable_receipt_revision']==BASE
U=read(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');old=read(O/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert U['current_existing_named_records_with_partial_context']==51 and U['current_existing_families_with_partial_context']==11
assert len(U['records'])==51 and len({x['family'] for x in U['records']})==11 and {x['id'] for x in U['records']}=={x['id'] for x in old['records']}|{'FV-E1049E4945A3'} and not U['full_context_review_complete']
assert isinstance(T['current_partial_context_union'],str) and T['current_partial_context_counts']['existing_named_records']==51
assert subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).strip()==''
print('R27_SOURCE_NATIVE_CANONICAL_PASS:36exact sources;84corrected native/20direct views,initial invalid run excluded;51existing partial/11families,0newart/adoption/acceptance;unknown totals,higher tiers/sequences and complete routes open.')
