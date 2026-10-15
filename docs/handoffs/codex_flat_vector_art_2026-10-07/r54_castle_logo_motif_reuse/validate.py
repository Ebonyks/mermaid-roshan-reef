from pathlib import Path
import json,hashlib,subprocess,ast,collections
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r53_castle_logo_context';B='97ab587f5c34594a8ed13b765338aff781a2934a';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def main():
 idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['captures'])==372 and idx['lanes']=={'EXCLUDED_ORIGINAL_RESTORED_COMPARISON':254,'BOUNDED_NONRUNTIME_REUSE_CANDIDATE':118}
 for x in idx['captures']:
  f=P/x['path'];assert sha(f.read_bytes())==x['sha256'] and list(Image.open(f).size)==x['dimensions']
 for c in idx['cases']:
  n=P/'native'/c['case'];d=rd(n/'capture_manifest.json');q=rd(n/'RESULT.json');assert not d['errors'] and q['exit_code']==0 and not q['timed_out'] and not q['script_or_shader_errors'];assert d['source_revision']==D and d['renderer']=='mobile' and d['time_scale']==1 and d['boot_count']==2
  e=d['engine'];assert(e['major'],e['minor'],e['patch'],e['status'],e['build'])==(4,7,2,'stable','official') and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
  assert len(d['states'])==186 and len(d['checks'])==126 and all(x['pass'] for x in d['checks']) and len(d['comparison_checks'])==58
  for row in d['comparison_checks']:assert row['state_and_local_layout_unchanged'] and row['before_sha256']==row['candidate_sha256']==row['restored_sha256'] and len(row['signature']['controls'])==14
  for name,key in [('capture_manifest.json','report_sha256'),('fixture_source.gd','fixture_sha256')]:assert sha((n/name).read_bytes())==c[key]
  assert q['sidecars_exact'] and q['sidecar_before_count']==q['sidecar_after_count']==4041 and not q['source_byte_changes'] and q['normal_before']==q['normal_after'] and q['fixture_unchanged'] and sha((n/'engine.log').read_bytes())==q['log_sha256']
  states={x['id']:x['snapshot'] for x in d['states']};choices=[x for x in d['states'] if x['id'].startswith('choice_') and x['id'].endswith('_candidate')];assert len(choices)==48
  for x in choices:
   _,color,symbol,_=x['id'].split('_');s=x['snapshot'];v=s['visual_trial'];assert s['color']==s['preview']['color']==color and s['symbol']==s['preview']['symbol']==symbol and s['game']=='level2' and s['navigation_top']=='castle_logo_studio' and s['preview']['is_source_logo_preview'];assert v['mode']=='candidate' and len(v['selector_images'])==8
   for a in v['selector_images']:assert a['visible'] and a['mouse_filter']==2 and a['size']=='(100.0, 100.0)' and a['local_position']=='(29.0, 25.0)' and a['rendered_button_text']=='' and a['texture']['path']=='res://assets/flats/castle/logo_studio_v2/castle_banner_motif_'+a['id']+'.png'
   assert v['status_image']['visible'] and v['status_image']['mouse_filter']==2 and v['status_image']['size']=='(52.0, 52.0)' and v['status_image']['texture']['path']==s['preview']['motif']['path']
   for mode in ['original','restored']:
    other=states[x['id'].removesuffix('candidate')+mode]['visual_trial'];assert other['mode']=='original' and not other['status_image']['visible'] and all(not a['visible'] and a['rendered_button_text']==a['source_glyph'] for a in other['selector_images'])
  for id in ['craft_committed_display','playroom_committed_display','fresh_main_loaded_display']:
   s=states[id];assert s['color']==s['disk']['color']=='purple' and s['symbol']==s['disk']['symbol']=='dog' and s['disk']['unknown']=={'keep':[3,7],'token':'R54_PRIVATE_ONLY'}
  assert not states['library_unregistered_absence']['display']['exists']
  assert states['draft_after_background_candidate']['color']=='gold' and states['draft_after_background_candidate']['disk']['color']=='purple' and not states['draft_after_background_candidate']['save_pending'] and not states['draft_after_background_candidate']['save_dirty']
 for x in rd(P/'SOURCE_REFERENCES.json')['files']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256'] and x['http_status']==200
 review=rd(P/'REVIEW.json');assert len(review['actually_viewed_native_frames'])==15 and len(review['actually_viewed_source_images'])==8 and len(review['comparison_axes'])==10 and not review['full_context_review_complete'] and not review['production_adopted'] and review['accepted_removed']==0
 for x in review['actually_viewed_native_frames']:assert x in idx['captures']
 assert rd(P/'MODE_COMPARISONS.json')['total']==116 and rd(P/'REUSE_RESULT.json')['status']=='ADDRESSED_IN_ISOLATED_SOURCE_REUSE_CANDIDATE_ONLY'
 for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
  d=rd(P/name);old=rd(O/name);assert d['castle_logo_motif_reuse']['runtime_source_revision']==D
  if name=='per_piece.json':assert d['pieces']==old['pieces'] and d['supplemental_piece_records']==old['supplemental_piece_records'] and len(d['pieces'])+len(d['supplemental_piece_records'])==240
  if name=='scene_coverage.json':assert d['entries']==old['entries'] and d['effective_current_partial_entry_ids']==old['effective_current_partial_entry_ids'] and (d['effective_partial_entries'],d['effective_entries_without_current_slice'],d['complete_entries'])==(84,92,0)
  if name=='tally.json':
   assert d['historical_totals'][:-1]==old['historical_totals'] and d['historical_totals'][-1]['immutable_final_byte_proof_revision']==B and d['current_context_sample_lanes']==old['current_context_sample_lanes'] and d['current_partial_context_counts']==old['current_partial_context_counts'];assert(d['current_context']['exact_capture_count'],d['current_context']['retained_native_capture_count'],d['current_context']['excluded_diagnostic_native_count'])==(4431,6583,2152);assert d['accepted_removed']==d['integrated']==d['runtime_verified']==0 and d['all_game_individual_piece_total'] is None and d['regression_count'] is None
 assert (P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
 for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
 assert not git('diff','--name-only',B,'--','scripts','scenes','assets','assets_src','shaders','addons','project.godot').strip();assert rd(H/'CURRENT.json')['current_tally']==P.name+'/tally.json'
 for f in P.rglob('*'):
  if f.is_file():
   assert f.stat().st_size<4194304,(str(f),f.stat().st_size)
   if f.suffix=='.py':ast.parse(f.read_text(encoding='utf-8-sig'))
 assert not rd(P/'WORK_IN_PROGRESS.json')['mission_complete'];print('R54_INTEGRITY_PASS 372native=118bounded candidate+254excluded comparisons;252checks/116parities/48choices peraspect;94refs/15native8sourceviews;frozen/runtime unchanged;0accepted/globalunknown',flush=True)
if __name__=='__main__':main()
