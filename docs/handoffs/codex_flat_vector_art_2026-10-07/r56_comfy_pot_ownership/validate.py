from pathlib import Path
import json,hashlib,subprocess,ast,math
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r55_comfy_room_context';B='49704228df9ca9cbff4b559a80a6c9d465665da0';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def main():
 idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['captures'])==104 and len(idx['cases'])==7 and idx['lanes']=={'EXCLUDED_BOOT_COMPARISON_OR_REJECTED_CONTACT_FIT':70,'BOUNDED_CURRENT_OWNERSHIP_OR_REFINED_FIT':34}
 for x in idx['captures']:
  f=P/x['path'];assert sha(f.read_bytes())==x['sha256'] and list(Image.open(f).size)==x['dimensions']
 for c in idx['cases']:
  n=P/'native'/c['case'];q=rd(n/'RESULT.json');assert sha((n/'fixture_source.gd').read_bytes())==c['fixture_sha256'] and not q['timed_out'] and q['sidecars_exact'] and q['sidecar_before_count']==q['sidecar_after_count']==4041 and not q['source_byte_changes'] and q['normal_before']==q['normal_after'] and q['fixture_unchanged'] and sha((n/'engine.log').read_bytes())==q['log_sha256']
  if not c['native']:
   assert c['case']=='attempt2_pot_ownership_1280'and q['exit_code']==1 and q['script_or_shader_errors'] and not(n/'capture_manifest.json').exists();continue
  d=rd(n/'capture_manifest.json');assert q['exit_code']==0 and not q['script_or_shader_errors'] and not d['errors'] and d['source_revision']==D and d['renderer']=='mobile' and d['time_scale']==1 and d['boot_count']==2 and not d['actual_child_data'] and not d['normal_route_proved'] and len(d['route_events'])==6
  assert sha((n/'capture_manifest.json').read_bytes())==c['report_sha256'] and len(d['states'])==c['native'] and len(d['checks'])==c['checks'] and all(x['pass']for x in d['checks'])
  e=d['engine'];assert(e['major'],e['minor'],e['patch'],e['status'],e['build'],e['hash'])==(4,7,2,'stable','official','ed1daf0bf001b61586d9930840f2f1394092c079')
  states={s['id']:s for s in d['states']};a=states['pot_original_owners']['snapshot'];z=states['repeat_completed_underlay']['snapshot'];assert not a['comfy']['day2_family_comfy_evening']['dinner']['completed'] and z['comfy']['day2_family_comfy_evening']['dinner']['completed'] and z['comfy']==z['disk']['comfy'] and z['disk']['unknown']=={'keep':[3,7],'token':'R56_PRIVATE_ONLY'}
  stage=states['completed_underlay_owners']['visible_stage_nodes'];oven=next(x for x in stage if x['path'].endswith('/Animated_oven'));assert oven['texture']['path']=='res://assets/flats/castle/interactions_v2/kitchen_oven_sheet.png' and oven['frame']==0 and oven['hframes']==4 and oven['vframes']==2 and oven['metadata_as_strings']['source_ownership_verified']=='false'
  tiles=[x for x in stage if x['path'].split('/')[-1].startswith('RoomTile_kitchen_')];assert len(tiles)==12 and all(x['texture']['path'].startswith('res://assets/flats/castle/interactions_v4/background_tiles/')for x in tiles)
  assert all(not x['path'].endswith('/ComfyDinnerSoupPot')for x in stage)
  if c['case'].startswith('attempt1'):assert c['checks']==12 and c['native']==14
  else:
   assert c['checks']==16 and c['native']==19 and len(d['mode_comparisons'])==1
   comp=d['mode_comparisons'][0];assert comp['unchanged'] and comp['restored_visual'] and comp['before']==comp['candidate']==comp['restored'] and comp['before']['pressed_callbacks']==['_stir_dinner']
   fits=[s for s in d['states']if s['role']=='NONRUNTIME_SCOPED_REJECT_POT_FIT'];assert len(fits)==5
   for s in fits:
    q=s['snapshot']['pot_trial'];assert q['mode']=='candidate' and q['source_region']=='[P: (0.0, 0.0), S: (443.0, 443.0)]' and math.isfinite(q['anchor_error_pixels'])
    button=next(x for x in s['selected_canvas_nodes']if x['path'].endswith('/ComfyDinnerSoupPot'));assert button['texture']['class']=='AtlasTexture' and button['texture']['region']==q['source_region'] and button['mouse_filter']==0
    if c['case'].startswith('attempt4'):assert 'alpha_bbox_bottom_center'in q and 'declared_oven_support_point'in q
 for x in rd(P/'SOURCE_REFERENCES.json')['files']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256'] and x['http_status']==200
 assert len(rd(P/'SOURCE_REFERENCES.json')['files'])==204
 rev=rd(P/'REVIEW.json');assert len(rev['actually_viewed_native_frames'])==12 and len(rev['actually_viewed_source_images'])==5 and len(rev['comparison_axes'])==10 and not rev['full_context_review_complete'] and rev['accepted_removed']==0
 for x in rev['actually_viewed_native_frames']:assert x in idx['captures']
 result=rd(P/'OWNERSHIP_AND_REUSE_RESULT.json')['result'];assert result['status']=='ISOLATED_NEW_PURPOSE_RETAINED_SOURCE_FIT_ONLY' and result['generation_calls']==result['new_drawing_samples']==result['approved']==result['integrated']==result['accepted_removed']==0 and not result['production_adopted'] and result['source']['sha256']=='504928531b4214b0762804dc5b08e8a920c37609f6bb7a04a01f95d1cdb45d23'
 assert rd(P/'SOURCE_ALPHA_BOUNDS.json')['native_size']==[1774,887] and 1774*887*4==6294152
 for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
  d=rd(P/name);old=rd(O/name);assert d['comfy_pot_ownership_reuse']['runtime_source_revision']==D
  if name=='per_piece.json':assert d['pieces']==old['pieces'] and d['supplemental_piece_records']==old['supplemental_piece_records'] and len(d['pieces'])+len(d['supplemental_piece_records'])==240
  if name=='scene_coverage.json':assert d['entries']==old['entries'] and d['effective_current_partial_entry_ids']==old['effective_current_partial_entry_ids'] and(d['effective_partial_entries'],d['effective_entries_without_current_slice'],d['complete_entries'])==(85,91,0)
  if name=='tally.json':assert d['historical_totals'][:-1]==old['historical_totals'] and d['historical_totals'][-1]['immutable_final_byte_proof_revision']==B and d['current_context_sample_lanes']==old['current_context_sample_lanes'] and d['current_partial_context_counts']==old['current_partial_context_counts'] and(d['current_context']['exact_capture_count'],d['current_context']['retained_native_capture_count'],d['current_context']['excluded_diagnostic_native_count'])==(4583,6871,2288) and d['accepted_removed']==d['integrated']==d['runtime_verified']==0 and d['all_game_individual_piece_total']is None and d['regression_count']is None
 assert(P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
 for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
 assert not git('diff','--name-only',B,'--','scripts','scenes','assets','assets_src','shaders','addons','project.godot').strip() and rd(H/'CURRENT.json')['current_tally']==P.name+'/tally.json'
 for f in P.rglob('*'):
  if f.is_file():
   assert f.stat().st_size<4194304,(str(f),f.stat().st_size)
   if f.suffix=='.py':ast.parse(f.read_text(encoding='utf-8-sig'))
 assert not rd(P/'WORK_IN_PROGRESS.json')['mission_complete'];print('R56_INTEGRITY_PASS 104native=34bounded+70excluded;24ownership32refined32contact-rejected checks;204refs/12native5source views;frozen/runtime unchanged;oldreject intact;0accepted/globalunknown',flush=True)
if __name__=='__main__':main()
