from pathlib import Path
import json,hashlib,subprocess,math
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r27_teacher_pointer_context';BASE='36b97a183c75ca897d7fd52fe9d54d4f44edda2a'
def rd(f):return json.loads(f.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
rows=rd(P/'SOURCES.json')['sources'];assert len(rows)==40
for x in rows:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R,stderr=subprocess.PIPE);assert len(b)==x['bytes'] and sha(b)==x['sha256'];c=(R/x['path']).read_bytes();assert sha(c)==x['current_worktree_raw_sha256'] or c.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
idx=rd(P/'CAPTURE_INDEX.json');assert idx['native_file_count']==84 and idx['current_bounded_file_count']==idx['current_unique_sha256_count']==24 and idx['excluded_duplicate_file_count']==60 and idx['directly_viewed_count']==20 and idx['directly_viewed_unique_count']==18
contract=rd(P/'CAPTURE_CONTRACT.json');assert contract['status']=='PASS_DIAGNOSTIC_ONLY' and contract['credited_unique_frame_count']==24 and contract['retained_event_frame_count']==84;exec(compile(contract['exact_check_python'],'R28_CAPTURE_CONTRACT_RECHECK','exec'),{})
fs=list((P/'native').rglob('capture_manifest.json'));assert len(fs)==8
for f in fs:
 d=rd(f);old=rd(O/'native'/f.relative_to(P/'native'));e=d['engine'];assert [e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash']]==[4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079']
 assert [x['id'] for x in d['states']]==[x['id'] for x in old['states']]
 for x,y in zip(d['states'],old['states']):
  for key in ['mode','lesson','counted','joined','can_answer','solved','wrong_attempts','phase_progress','completion_accepted','held','touch_owner','help_visible','assisted','snapshot']:assert x[key]==y[key],(f,x['id'],key)
  assert not x['solved'] and x['phase_progress']==0 and x['actor_visible'] and len(x['backdrop_tiles'])==8
  z=x['pointer_trial'];assert z['trial_enabled'] and z['source_sha256']=='7e80a06704e21d780e66692c68d1226ea3b9a88544e927ba293b49ed1d3451ec' and z['prototype_sha256']==sha((P/'candidate_teacher_surface.gd').read_bytes());c=z['last_callback']
  if x['lesson']['kind']=='add' and x['join_t']>0:assert c['route']=='hidden_until_counter_actionable' and c['declared_whole_texture_commands']==0
  elif x['original_guide_formula']['target_role']=='NONE':assert c['route']=='hidden_no_eligible_guide' and c['declared_whole_texture_commands']==0
  else:
   assert c['route']=='whole_painted_source' and c['eligible_target'] and c['tip_error']<0.001 and c['declared_whole_texture_commands']==1 and abs(c['rotation_radians']-math.pi)<0.00001
   assert c['side']==(72 if c['target_role']=='CORRECT_ANSWER_CARD' else 80);dy={'JOIN_BUTTON':28,'NEXT_UNTOUCHED_COUNTER':20,'CORRECT_ANSWER_CARD':55}[c['target_role']];assert abs(c['target'][0]-c['center'][0])<.001 and abs(c['target'][1]-c['center'][1]-dy)<.001
assert rd(P/'LAUNCH.json')['returncode']==0 and len(rd(P/'SCRIPT_GATES.json'))==6 and all(x['exit_code']==0 for x in rd(P/'SCRIPT_GATES.json'))
pr=rd(P/'CONTEXT_PREREQUISITE.json');assert pr['file_count']==51 and pr['status']=='ALL_SELECTED_CONTEXT_FILES_ANONYMOUSLY_VERIFIED_BEFORE_PROTOTYPE_EDIT'
review=rd(P/'REVIEW.json');assert len(review['ten_axes'])==10 and len(review['direct_source_images_viewed'])==2 and review['direct_native_views']==idx['directly_viewed_native_files'] and review['acceptance']['owner'] is None
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/name);old=rd(O/name);assert d['revision']=='FV-AUDIT-20261014-R28'
 for key in ['pieces','supplemental_piece_records','entries','named_status_counts','status_lanes','teacher_pointer_context','boxing_pointer_reuse','ballet_pointer_reuse','pointer_candidate']:
  if key in old:assert d[key]==old[key],key
 a=d['teacher_pointer_reuse'];assert a['piece_id']=='FV-E1049E4945A3' and a['new_design_ids']==a['new_art_drawings']==a['new_generation_calls']==a['accepted_removed']==0
T=rd(P/'tally.json');old=rd(O/'tally.json');C=T['current_context'];assert C['exact_capture_count']==old['current_context']['exact_capture_count']+24==2732 and C['retained_native_captures']==C['retained_native_capture_count']==3015 and C['excluded_diagnostic_native_count']==283 and C['complete_entries']==0 and C['partial_overlapping_entries']==77
assert T['all_game_individual_piece_total'] is None and T['current_distinct_screen_total'] is None and T['regression_count'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0 and T['known_named_design_records_including_supplemental']==225 and T['known_family_count_including_supplemental']==30
assert T['historical_totals'][:-1]==old['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
U=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert U['records']==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records'] and len(U['records'])==51 and len({x['family'] for x in U['records']})==11
lanes=T['current_context_sample_lanes'];assert lanes['samples_awaiting_review']==lanes['unique_whole_drawing_samples']==1 and lanes['per_piece_context_review_requests']==lanes['family_count']==len(lanes['individual_existing_piece_ids'])==4 and lanes['approved']==lanes['integrated']==lanes['accepted_removed']==0
assert subprocess.check_output(['git','diff','--name-only',BASE,'--','assets','assets_src','scripts','scenes','shaders','project.godot'],cwd=R,text=True,stderr=subprocess.PIPE).strip()==''
print('R28_SOURCE_NATIVE_CANONICAL_PASS:40sourcebindings,51before-edit publiccontext files;84retained/24uniquecredit/60duplicateexcluded;20views/18unique;1hand/4piececontexts,0artadoption/acceptance,unknown totals.')
