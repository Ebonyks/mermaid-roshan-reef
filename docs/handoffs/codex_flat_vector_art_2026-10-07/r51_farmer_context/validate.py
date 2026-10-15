from pathlib import Path
import json,hashlib,subprocess,re,ast
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;B='801b36a56923567dee37cf744e0fc80b605dd775';D='5120b6d59885dd057937aaf284e73681d8eac9f5';O=H/'r50_upstream_source_refresh'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def main():
 idx=rd(P/'CAPTURE_INDEX.json');assert(idx['new_retained_native'],idx['new_bounded'],idx['new_excluded'])==(120,96,24);assert len(idx['captures'])==120
 for x in idx['captures']:
  f=P/x['path'];assert sha(f.read_bytes())==x['sha256']and list(Image.open(f).size)==x['dimensions']
 for c in idx['cases']:
  p=P/'native'/c['case'];report=rd(p/'capture_manifest.json');result=rd(p/'RESULT.json');assert report['source_revision']==D and (report['engine']['major'],report['engine']['minor'],report['engine']['patch'],report['engine']['status'],report['engine']['build'])==(4,7,2,'stable','official')and report['renderer']=='mobile'and report['time_scale']==1
  assert sha((p/'capture_manifest.json').read_bytes())==c['report_sha256']and sha((p/'fixture_source.gd').read_bytes())==c['fixture_sha256'];assert result['sidecars_exact']and not result['source_byte_changes']and result['fixture_unchanged']and result['normal_before']==result['normal_after']and not result['script_or_shader_errors'];assert result['log_sha256']==sha((p/'engine.log').read_bytes())
  if c['case']=='attempt1_farmer_1280':assert result['exit_code']==1 and report['errors']==['original Farmer DiningRoom picture unavailable']and report['boot_count']==2
  else:
   assert result['exit_code']==0 and not report['errors']and report['boot_count']==1
   states={x['id']:x for x in report['states']};first=states['gather_4_released']['snapshot'];assert first['story']['chapter2_party_piece_mask']==0 and first['private_disk_story']['chapter2_party_piece_mask']==64
   assert states['fill_first_ready']['snapshot']['story']['chapter2_job_phase_masks'][0]==1;assert states['delivery_ready']['snapshot']['story']['chapter2_job_phase_masks'][0]==3;assert states['farmer_result_return']['snapshot']['story']['chapter2_job_phase_masks'][0]==7
   assert states['delivery_passive']['snapshot']['world']['phase_progress']==0 and states['delivery_passive']['snapshot']['surface']['long_push_journey']==0
   assert states['delivery_partial_released']['snapshot']['surface']['long_push_journey']>0;assert states['delivery_endpoint_released']['snapshot']['surface']['long_push_journey']>=0.98
   assert states['first_world']['snapshot']['freeplay']==states['farmer_result_return']['snapshot']['freeplay'];assert states['fill_off_target_pressed']['snapshot']['world']['phase_progress']==states['fill_passive']['snapshot']['world']['phase_progress']==0
 assert sha((P/'native/attempt1_farmer_1280/private_checkpoint_saved.json').read_bytes())=='90b2b171a282d67516122193caa5dc5f561b8dfd03d1b4535b39e15e510399fd'
 for x in rd(P/'SOURCE_REFERENCES.json')['files']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256']
 rev=rd(P/'REVIEW.json');assert rev['actually_viewed_count']==len(rev['actually_viewed_native_frames'])==12 and len(rev['actually_viewed_source_images'])==5 and len(rev['point_by_point_observations'])==6
 for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
  d=rd(P/name);o=rd(O/name);assert d['farmer_context']['source_revision']==D
  if name=='per_piece.json':assert d['pieces']==o['pieces']and d['supplemental_piece_records']==o['supplemental_piece_records']and len(d['pieces'])+len(d['supplemental_piece_records'])==240
  if name=='scene_coverage.json':assert d['entries']==o['entries']and d['effective_current_partial_entry_ids']==o['effective_current_partial_entry_ids']and(d['effective_partial_entries'],d['effective_entries_without_current_slice'],d['complete_entries'])==(83,93,0)
  if name=='tally.json':
   assert d['historical_totals'][:-1]==o['historical_totals']and d['historical_totals'][-1]['immutable_final_byte_proof_revision']==B
   assert(d['current_context']['exact_capture_count'],d['current_context']['retained_native_capture_count'],d['current_context']['excluded_diagnostic_native_count'])==(4099,5850,1751)
   assert d['current_context_sample_lanes']==o['current_context_sample_lanes']and d['current_partial_context_counts']==o['current_partial_context_counts'];assert d['accepted_removed']==d['integrated']==d['runtime_verified']==0 and d['all_game_individual_piece_total']is None and d['regression_count']is None
 for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
 assert not git('diff','--name-only',B,'--','scripts','scenes','assets','assets_src','shaders','addons','project.godot').strip()
 assert rd(H/'CURRENT.json')['current_tally']==P.name+'/tally.json';assert rd(P/'SAVE_REGRESSION.json')['status']=='REPRODUCED_UNREPAIRED_AT_DECLARED_SOURCE'
 for f in P.rglob('*'):
  if f.is_file():
   assert f.stat().st_size<4194304,(str(f),f.stat().st_size)
   if f.suffix=='.py':ast.parse(f.read_text(encoding='utf-8-sig'))
 assert not rd(P/'WORK_IN_PROGRESS.json')['mission_complete'];print('R51_INTEGRITY_PASS 120native/96bounded/24excluded;2continuouspass+1coldreloadFAIL retained;44exactrefs;240roles32families/0accepted/globalunknown;frozen/runtimeunchanged',flush=True)
if __name__=='__main__':main()
