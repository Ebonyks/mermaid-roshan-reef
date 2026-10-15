from pathlib import Path
import json,hashlib,subprocess,ast,collections
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r54_castle_logo_motif_reuse';B='d464dfd07cf53563a3fa3b729624bd12909c751d';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def main():
 idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['captures'])==184 and idx['lanes']=={'EXCLUDED_FIXTURE_OR_BOOT_DIAGNOSTIC':66,'BOUNDED_CURRENT_ORIGINAL_COMFY_CONTEXT':118}
 assert len(idx['cases'])==4
 for x in idx['captures']:
  f=P/x['path'];assert sha(f.read_bytes())==x['sha256'] and list(Image.open(f).size)==x['dimensions']
 for c in idx['cases']:
  n=P/'native'/c['case'];d=rd(n/'capture_manifest.json');q=rd(n/'RESULT.json');current=c['current']
  assert d['source_revision']==D and d['renderer']=='mobile' and d['time_scale']==1 and not d['actual_child_data'] and not d['normal_route_proved']
  e=d['engine'];assert(e['major'],e['minor'],e['patch'],e['status'],e['build'])==(4,7,2,'stable','official') and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
  assert not q['timed_out'] and not q['script_or_shader_errors'] and q['sidecars_exact'] and q['sidecar_before_count']==q['sidecar_after_count']==4041 and not q['source_byte_changes'] and q['normal_before']==q['normal_after'] and q['fixture_unchanged'] and sha((n/'engine.log').read_bytes())==q['log_sha256']
  for name,key in [('capture_manifest.json','report_sha256'),('fixture_source.gd','fixture_sha256')]:assert sha((n/name).read_bytes())==c[key]
  if not current:
   assert q['exit_code']==1 and d['errors']==c['errors']
   assert d['errors']==(['original hall door unavailable mermaid_pool']if c['case'].startswith('attempt1')else['main story counters unchanged','reloaded story counters unchanged'])
   continue
  assert q['exit_code']==0 and not d['errors'] and len(d['checks'])==44 and all(x['pass']for x in d['checks']) and len(d['states'])==61 and len(d['route_events'])==14 and d['boot_count']==3
  assert sum(x['label'].startswith('Comfy action preserves story counters')for x in d['checks'])==15
  route=d['route_events'][0];narrow=c['case'].endswith('_1280');assert route['button']=='HallDoor_mermaid_pool' and route['dust_before']=={} and route['dust_after']==({'runner_bunny':True}if narrow else{}) and (route['pearl_before'],route['pearl_after'])==((23,24)if narrow else(23,23))
  states={x['id']:x for x in d['states']};s=states['final_library_repeat']['snapshot'];assert s['game']=='level2' and s['quality']=='speedy' and s['comfy']==s['disk']['comfy'] and s['disk']['unknown']=={'keep':[3,7],'token':'R55_PRIVATE_ONLY'} and s['story_counters']==[0,0,24 if narrow else 23] and s['disk']['stickers']['super_seeker']
  quest=s['comfy']['day2_family_comfy_evening'];assert quest['completed'] and quest['movie']['scenes_watched']==3 and quest['dinner']['pot_stirred'] and all(quest['bedtime']['tucked_in'].values()) and quest['reward']=={'id':'comfy_evening_mystery_reward','introduced':False,'unlocked':True,'verified':False}
  assert states['fresh_main_two_finds']['snapshot']['comfy']['day2_castle_hide_and_seek']['found']=={'rumi':True,'baby_eagle':True,'daddy_mermaid':False}
  assert states['pool_passive']['snapshot']['comfy']==states['find_rumi_before']['snapshot']['comfy']
  for id in ['movie_1_before','movie_2_before','movie_3_before']:
   node=next(n for n in states[id]['selected_canvas_nodes']if n['path'].endswith('/ComfyFamilyMovieScreen'));assert node['texture']['path']=='res://assets/flats/castle/dream_house/movie_screen_frame.png'
  for id in ['dinner_stir_before','dinner_stir_pressed']:
   node=next(n for n in states[id]['selected_canvas_nodes']if n['path'].endswith('/ComfyDinnerSoupPot'));assert node['texture']['path']=='res://assets/flats/castle/rooms/room_kitchen_item_soup_pot.png'
 refs=rd(P/'SOURCE_REFERENCES.json')['files'];assert len(refs)==155
 for x in refs:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256'] and x['http_status']==200
 rev=rd(P/'REVIEW.json');assert len(rev['actually_viewed_native_frames'])==15 and len(rev['actually_viewed_source_images'])==9 and len(rev['comparison_axes'])==10 and len(rev['observations'])==5 and not rev['full_context_review_complete'] and rev['accepted_removed']==0
 for x in rev['actually_viewed_native_frames']:assert x in idx['captures']
 cons=rd(P/'CONSUMER_BINDINGS.json');assert len(cons['consumers'])==12 and len(set(x['id']for x in cons['consumers']))==12 and len(set(x['resolved_texture']['path']for x in cons['consumers']))==9
 for c in cons['consumers']:
  assert c['id']=='FVC-'+sha(('scripts/comfy_games.gd::'+c['node']).encode())[:12].upper() and c['resolved_texture']in refs and c['same_scene_reference_hashes'] and all(x in refs for x in c['same_scene_reference_hashes'])
  for e in c['evidence']:
   report=rd(P/'native'/e['case']/'capture_manifest.json');s=next(s for s in report['states']if s['id']==e['capture_id']);assert e['sha256']==s['sha256'] and e['node']in s['selected_canvas_nodes']
 for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
  d=rd(P/name);old=rd(O/name);assert d['comfy_room_context']['runtime_source_revision']==D
  if name=='per_piece.json':assert d['pieces']==old['pieces'] and d['supplemental_piece_records']==old['supplemental_piece_records'] and len(d['pieces'])+len(d['supplemental_piece_records'])==240
  if name=='scene_coverage.json':assert d['entries']==old['entries'] and set(d['effective_current_partial_entry_ids'])==set(old['effective_current_partial_entry_ids'])|{'game.comfy_games'} and(d['effective_partial_entries'],d['effective_entries_without_current_slice'],d['complete_entries'])==(85,91,0)
  if name=='tally.json':
   assert d['historical_totals'][:-1]==old['historical_totals'] and d['historical_totals'][-1]['immutable_final_byte_proof_revision']==B and d['current_context_sample_lanes']==old['current_context_sample_lanes'] and d['current_partial_context_counts']==old['current_partial_context_counts']
   assert(d['current_context']['exact_capture_count'],d['current_context']['retained_native_capture_count'],d['current_context']['excluded_diagnostic_native_count'])==(4549,6767,2218) and d['accepted_removed']==d['integrated']==d['runtime_verified']==0 and d['all_game_individual_piece_total']is None and d['regression_count']is None
 assert(P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
 for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
 assert not git('diff','--name-only',B,'--','scripts','scenes','assets','assets_src','shaders','addons','project.godot').strip() and rd(H/'CURRENT.json')['current_tally']==P.name+'/tally.json'
 for f in P.rglob('*'):
  if f.is_file():
   assert f.stat().st_size<4194304,(str(f),f.stat().st_size)
   if f.suffix=='.py':ast.parse(f.read_text(encoding='utf-8-sig'))
 assert not rd(P/'WORK_IN_PROGRESS.json')['mission_complete'];print('R55_INTEGRITY_PASS 184native=118bounded+66excluded;88current checks/155refs/12consumers9textures/15native9source views;frozen/runtime unchanged;0accepted/globalunknown',flush=True)
if __name__=='__main__':main()
