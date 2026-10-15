from pathlib import Path
import json,hashlib,subprocess,ast,collections
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r51_farmer_context';B='65adbc4ace23d5988b0c444c269f43142a7127e3';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def main():
 idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['captures'])==81 and idx['lanes']=={'EXCLUDED_DIAGNOSTIC':7,'CURRENT_SOURCE_CONTROL':30,'NONRUNTIME_REUSE_CANDIDATE':44}
 for x in idx['captures']:
  f=P/x['path'];assert sha(f.read_bytes())==x['sha256']and list(Image.open(f).size)==x['dimensions']
 for c in idx['cases']:
  n=P/'native'/c['case'];report=rd(n/'capture_manifest.json');result=rd(n/'RESULT.json');assert report['source_revision']==D and report['renderer']=='mobile'and report['time_scale']==1 and not report['errors']and result['exit_code']==0
  e=report['engine'];assert(e['major'],e['minor'],e['patch'],e['status'],e['build'])==(4,7,2,'stable','official')and e['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079';assert len(report['comparison_checks'])==20 and all(x['story_phase_progress_geometry_unchanged']for x in report['comparison_checks'])
  for name,key in [('capture_manifest.json','report_sha256'),('fixture_source.gd','fixture_sha256')]:assert sha((n/name).read_bytes())==c[key]
  assert sha(rd(P/'EXECUTED_CANDIDATE_SOURCE.json')['utf8_text'].encode())==c['candidate_sha256'];assert sha((n/'candidate_source.gd').read_bytes())==c['readable_candidate_sha256'];assert (n/'candidate_source.gd').read_bytes()==rd(P/'EXECUTED_CANDIDATE_SOURCE.json')['utf8_text'].encode().rstrip(b'\r\n')+b'\n'
  assert result['sidecars_exact']and not result['source_byte_changes']and result['normal_before']==result['normal_after']and result['fixture_unchanged']and result['candidate_unchanged']and not result['script_or_shader_errors']and sha((n/'engine.log').read_bytes())==result['log_sha256']
  states={x['id']:x for x in report['states']};assert states['first_world']['snapshot']['freeplay']==states['farmer_result_return']['snapshot']['freeplay'];assert states['farmer_result_return']['snapshot']['story']['chapter2_job_phase_masks'][0]==7
  for prefix in ['gather_ready','fill_ready','fill_partial_two','delivery_ready','delivery_half_released']:
   for mode in ['original','centered','preserve_lower','original_restore']:
    s=states[prefix+'_'+mode]['snapshot'];v=s['visual_trial'];assert v['mode']==mode and v['original_backdrop_visible']==(mode in ['original','original_restore'])and v['candidate_visible']==(mode not in ['original','original_restore'])
    if mode=='preserve_lower':assert len(v['candidate_mapping'])==4
 a=np.asarray(Image.open(P/'native/attempt1_panorama_1280/component_original.png'));b=np.asarray(Image.open(P/'native/attempt1_panorama_1280/component_preserve_lower.png'));assert np.array_equal(a[360:],b[360:])and np.any(a[:360]!=b[:360]);m=rd(P/'MAPPING_MEASUREMENTS.json');assert m['original_to_preserve_lower']['bottom_half_changed_pixels']==0 and m['original_to_preserve_lower']['bottom_half_pixel_count']==460800
 for x in rd(P/'SOURCE_REFERENCES.json')['files']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256']and x['http_status']==200
 review=rd(P/'REVIEW.json');assert len(review['actually_viewed_native_frames'])==12 and len(review['actually_viewed_new_source_images'])==2 and len(review['candidate_dispositions'])==2 and not review['full_context_review_complete']and review['accepted_removed']==0
 for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
  d=rd(P/name);old=rd(O/name);assert d['farmer_panorama_reuse']['runtime_source_revision']==D
  if name=='per_piece.json':assert d['pieces']==old['pieces']and d['supplemental_piece_records']==old['supplemental_piece_records']and len(d['pieces'])+len(d['supplemental_piece_records'])==240
  if name=='scene_coverage.json':assert d['entries']==old['entries']and d['effective_current_partial_entry_ids']==old['effective_current_partial_entry_ids']and(d['effective_partial_entries'],d['effective_entries_without_current_slice'],d['complete_entries'])==(83,93,0)
  if name=='tally.json':
   assert d['historical_totals'][:-1]==old['historical_totals']and d['historical_totals'][-1]['immutable_final_byte_proof_revision']==B;assert d['current_context_sample_lanes']==old['current_context_sample_lanes']and d['current_partial_context_counts']==old['current_partial_context_counts'];assert(d['current_context']['exact_capture_count'],d['current_context']['retained_native_capture_count'],d['current_context']['excluded_diagnostic_native_count'])==(4173,5931,1758);assert d['current_context_sample_lanes']['approved']==d['accepted_removed']==d['integrated']==d['runtime_verified']==0 and d['all_game_individual_piece_total']is None and d['regression_count']is None
 for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
 assert not git('diff','--name-only',B,'--','scripts','scenes','assets','assets_src','shaders','addons','project.godot').strip();assert rd(H/'CURRENT.json')['current_tally']==P.name+'/tally.json'
 for f in P.rglob('*'):
  if f.is_file():
   assert f.stat().st_size<4194304,(str(f),f.stat().st_size)
   if f.suffix=='.py':ast.parse(f.read_text(encoding='utf-8-sig'))
 assert not rd(P/'WORK_IN_PROGRESS.json')['mission_complete'];print('R52_INTEGRITY_PASS 81native/74bounded/7excluded=30controls+44candidates+7diagnostics;40unchangedstatechecks/460800exactlowerpixels;2aspects/59exactrefs;frozen/runtimeunchanged;0accepted/globalunknown',flush=True)
if __name__=='__main__':main()
