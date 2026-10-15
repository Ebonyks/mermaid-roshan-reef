"""Validate R59 evidence scopes and source/input invariants; no creative acceptance."""
from pathlib import Path
import json,hashlib,subprocess,re
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r58_critter_book_context';B='431c165647f4dcca4aec0e4ccada517534ead513'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
s=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');par=rd(P/'SOURCE_PARITY.json');rv=rd(P/'REVIEW.json');pre=rd(P/'CONTEXT_PREREQUISITE.json');assert pre['files']==407 and pre['bytes']==43018367 and pre['source_reference_sha256']==sha((P/'SOURCE_REFERENCES.json').read_bytes())
assert (s['new_native_files'],s['new_bounded_contexts'],s['new_excluded_diagnostics'],s['passing_checks'])==(340,128,212,104)
assert s['retained_bounded']==4654+128 and s['retained_excluded']==2327+212 and s['retained_native_events']==6981+340
assert len(idx['states'])==340 and sum(x['bounded_context']for x in idx['states'])==128 and len(list(P.rglob('*.png')))==340
for x in idx['states']:assert sha((P/x['path']).read_bytes())==x['sha256']and x['height']==720 and x['width']in[1280,1600]
assert par['runtime_files']==4420 and par['initialized_sidecars']==4041 and par['normal_suffixes']==8 and all(par[k]for k in ['all_runtime_files_unchanged','all_sidecars_exact','all_normal_hashes_exact','all_fixtures_unchanged'])
assert len(par['jobs'])==10;final=[]
for row in par['jobs']:
 f=P/row['directory'];c=rd(f/'capture_manifest.json');g=rd(f/'RESULT.json');la=rd(f/'LAUNCH.json');assert g['exit_code']==0 and g['normal_before']==g['normal_after']and g['sidecars_exact']and not g['source_byte_changes']and not g['script_or_shader_errors'];assert g['log_sha256']==sha((f/'engine.log').read_bytes())
 assert la['fixture_sha256']==sha((f/'fixture_source.gd').read_bytes())and la['base_fixture_sha256']==sha((P/('base_capture_critter.gd'if row['final_matrix']else'historical_base_capture_critter.gd')).read_bytes())
 assert c['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and c['engine']['string']=='4.7.2-stable (official)'and c['renderer']=='mobile'and c['display']!='headless'and c['time_scale']==1.0
 assert len(c['states'])==34 and not c['errors']and len(c['checks'])==26 and all(x['pass']for x in c['checks'])
 assert all(x['snapshot']['game']=='level2'and x['snapshot']['quality']=='speedy'and x['snapshot']['caught_count']==0 for x in c['states'])
 if row['final_matrix']:
  final.append(c);assert la['fixture_sha256']==sha((P/'capture_reuse.gd').read_bytes())and la['base_fixture_sha256']==sha((P/'base_capture_critter.gd').read_bytes())
  for x in c['states']:
   a=x['snapshot']['candidate']
   if x['snapshot']['book_exists']:
    assert a['book_layer']==28 and len(a['button_invariants'])==3
    assert all(all(b[k]for k in ['callbacks_unchanged','declared_trial_rect_matches','size_unchanged','mouse_filter_unchanged'])and not b['rect_unchanged']for b in a['button_invariants'])
    orn=[n for n in a['nodes']if n.get('ornament_binding')];assert len(orn)==5 and all(n['visible']==(a['mode']=='layout')for n in orn)
    for n in a['nodes']:
     assert n['id']==n['source_id']
     for pic in n['pictures']:assert pic['mouse_filter']==2 and pic['show_behind_parent']
     if n['class']=='Label':
      vals=list(map(float,re.findall(r'-?\d+\.\d+',n['rect'])));assert vals[2]>=n['text_width']and vals[1]+vals[3]<=720
assert len(final)==4 and sum(len(c['checks'])for c in final)==104
iv=rd(P/'NODE_AND_INPUT_INVARIANTS.json');assert iv['book_state_observations']==len(iv['observations'])==68 and iv['button_observations']==204
recipe=rd(P/'SOURCE_RECIPE_REPLAY.json');rguard=rd(P/'RECIPE_RESULT.json');assert recipe['failures']==0 and len(recipe['rows'])==2 and all(x['decoded_rgba8_exact']and x['actual_rgba8_sha256']==x['expected_rgba8_sha256']for x in recipe['rows']);assert rguard['exit_code']==0 and rguard['sidecars_exact']and not rguard['runtime_files_changed']and rguard['normal_before']==rguard['normal_after']
assert rv['human_reviews']==[] and rv['approved']==rv['accepted_removed']==0 and len(rv['native_direct_views'])>=17
for x in rv['native_direct_views']:assert sha((P/x['path']).read_bytes())==x['sha256']
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 before=rd(O/n);after=rd(P/n);allowed={'revision','phase','publication','change_record','current_ci_snapshot'}
 for k,v in before.items():
  if k not in allowed:assert after[k]==v,(n,k)
 assert after['critter_book_reuse']['new_alias_credits']==after['critter_book_reuse']['accepted_removed']==0
assert (P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
assert rd(P/'scene_coverage.json')['effective_partial_entries']==85 and rd(P/'scene_coverage.json')['effective_entries_without_current_slice']==91
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert subprocess.check_output(['git','show',B+':'+(H/n).relative_to(R).as_posix()],cwd=R)==(H/n).read_bytes()
t=rd(P/'tally.json');assert t['accepted_removed']==t['replaced']==t['integrated']==t['runtime_verified']==0 and t['all_game_individual_piece_total']is None and t['current_distinct_screen_total']is None and t['regression_count']is None
for f in P.rglob('*.json'):assert f.stat().st_size<4*1024*1024;rd(f)
code=(P/'capture_reuse.gd').read_text(encoding='utf-8');assert not re.search(r'm\.(?:critter_collection|collection_category|msg_timer)\s*=(?!=)',code)
pix=rd(P/'FRAME_PIXEL_IDENTITY.json');assert pix['files']==len(pix['frames'])==340 and all(x['decoded_nonblank']and sha((P/x['path']).read_bytes())==x['sha256']for x in pix['frames']);assert pix['unique_png_byte_sha256']==len({x['sha256']for x in pix['frames']})
assert rd(P/'REPRODUCTION_INPUTS.json')['baseline']['actual_staging_raw_exact']
assert rd(P/'REUSE_MAPPING.json')['new_generation_calls']==0 and not rd(P/'REUSE_MAPPING.json')['new_use_approved']
print('R59_VALIDATED 340native128bounded212excluded104checks;68book204buttons;recipe exact;0art/adoption/alias/global unknown')
