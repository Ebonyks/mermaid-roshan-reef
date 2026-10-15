"""Validate R58 provenance/count scopes; machine gates do not grant visual acceptance."""
from pathlib import Path
import json,hashlib,subprocess,re
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r57_catalogue_selector_crosswalk';B='5459a484f9f1a5d11c9b4c8b2f9279af87905a0a'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
s=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');par=rd(P/'SOURCE_PARITY.json');r=rd(P/'REVIEW.json');pre=rd(P/'CONTEXT_PREREQUISITE.json');assert pre['files']==376 and pre['bytes']==34911196 and pre['reference_manifest_sha256']==sha((P/'SOURCE_REFERENCES.json').read_bytes())
assert s['new_native_files']==110 and s['new_bounded_contexts']==71 and s['new_excluded_diagnostics']==39 and s['passing_checks']==59
assert s['retained_bounded']==4583+71 and s['retained_excluded']==2288+39 and s['retained_native_events']==6871+110
assert len(idx['states'])==110 and sum(x['bounded_context']for x in idx['states'])==71 and len(list(P.rglob('*.png')))==110
for row in idx['states']:assert sha((P/row['path']).read_bytes())==row['sha256'] and row['height']==720 and row['width']in[1280,1600]
assert par['runtime_files']==4420 and par['initialized_sidecars']==4041 and par['normal_suffixes']==8 and all(par[k]for k in ['all_runtime_files_unchanged','all_sidecars_exact','all_normal_hashes_exact'])
assert len(par['jobs'])==4
passing=[]
for row in par['jobs']:
 f=P/row['directory'];c=rd(f/'capture_manifest.json');g=rd(f/'RESULT.json');assert g['normal_before']==g['normal_after']and g['sidecars_exact']and not g['source_byte_changes']and not g['script_or_shader_errors'];assert g['log_sha256']==sha((f/'engine.log').read_bytes());assert rd(f/'LAUNCH.json')['fixture_sha256']==sha((f/'fixture_source.gd').read_bytes())
 assert c['engine']['string']=='4.7.2-stable (official)'and c['renderer']=='mobile'and c['display']!='headless'and c['time_scale']==1.0
 if row['failed_fixture']:assert len(c['states'])==34 and c['errors']==['private unknown key retained']and sum(not x['pass']for x in c['checks'])==1
 else:assert not c['errors']and all(x['pass']for x in c['checks'])and g['exit_code']==0;passing.append(c)
assert sum(len(c['checks'])for c in passing)==59
# Actual book route remains independent of game alias; record one-pixel widths without inferring unseen caught/art states.
assert all(x['snapshot']['game']=='level2'for x in idx['states']if x['snapshot'].get('book_exists'))
assert all(x['snapshot']['caught_count']==0 for x in idx['states'])
c=rd(P/'native/attempt2_critter_book_1280/capture_manifest.json');v=next(x for x in c['states']if x['id']=='fish_ready');labels=[x for x in v['selected_canvas_nodes']if x.get('class')=='Label'and('Critter Book'in x.get('text','')or'Swim close'in x.get('text',''))];assert len(labels)==2 and all('S: (1.0,'in x['global_rect']for x in labels)
c=rd(P/'native/attempt3_critter_passive_1280/capture_manifest.json');v=next(x for x in c['states']if x['id']=='book_after_10_real_seconds');assert v['snapshot']['message_timer']<=0 and not v['snapshot']['castle_caption']['visible']
assert len(r['native_direct_views'])==9 and len(r['source_direct_views'])==2 and r['human_reviews']==[] and r['approved']==r['accepted_removed']==0
for x in r['native_direct_views']:assert sha((P/x['path']).read_bytes())==x['sha256']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 before=rd(O/name);after=rd(P/name);allowed={'revision','phase','publication','change_record','current_ci_snapshot'}
 for k,v in before.items():
  if k not in allowed:assert after[k]==v,(name,k)
 assert after['critter_book_context']['new_alias_credits']==0 and after['critter_book_context']['accepted_removed']==0
assert (P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
assert rd(P/'scene_coverage.json')['effective_partial_entries']==85 and rd(P/'scene_coverage.json')['effective_entries_without_current_slice']==91
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert subprocess.check_output(['git','show',B+':'+(H/name).relative_to(R).as_posix()],cwd=R)==(H/name).read_bytes()
t=rd(P/'tally.json');assert t['accepted_removed']==t['replaced']==t['integrated']==t['runtime_verified']==0 and t['all_game_individual_piece_total']is None and t['current_distinct_screen_total']is None and t['regression_count']is None
for f in P.rglob('*.json'):assert f.stat().st_size<4*1024*1024;rd(f)
for f in [P/'capture_critter_book.gd',P/'capture_critter_passive.gd']:
 code=f.read_text(encoding='utf-8');assert not re.search(r'm\.(?:critter_collection|collection_category|msg_timer)\s*=(?!=)',code)
print('R58_VALIDATED 110native/71bounded/39excluded/59checks;9native2source views;85partial91without0complete/0art;unknown totals')

pix=rd(P/"FRAME_PIXEL_IDENTITY.json");assert pix["files"]==110 and len(pix["frames"])==110 and all(x["decoded_nonblank"] and sha((P/x["path"]).read_bytes())==x["sha256"]for x in pix["frames"])
rep=rd(P/"REPRODUCTION_INPUTS.json");assert rep["baseline"]["actual_staging_raw_exact"]

assert pix["unique_png_byte_sha256"]==len({x["sha256"]for x in pix["frames"]})==100
