"""Validate R60 exact saved-state context scopes; never art/route acceptance."""
from pathlib import Path
import json,hashlib,subprocess,re
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r59_critter_book_reuse';B='2e2464a742885d0d0803870ffea9dfdd51b49889'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
s=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');par=rd(P/'SOURCE_PARITY.json');rv=rd(P/'REVIEW.json');pre=rd(P/'CONTEXT_PREREQUISITE.json');assert pre['files']==444 and pre['bytes']==56092387 and pre['source_reference_sha256']==sha((P/'SOURCE_REFERENCES.json').read_bytes())
assert (s['new_native_files'],s['new_bounded_contexts'],s['new_excluded_diagnostics'],s['passing_checks'])==(148,140,8,140)
assert s['retained_bounded']==4782+140 and s['retained_excluded']==2539+8 and s['retained_native_events']==7321+148
assert len(idx['states'])==148 and sum(x['bounded_context']for x in idx['states'])==140 and len(list(P.rglob('*.png')))==148
for x in idx['states']:assert sha((P/x['path']).read_bytes())==x['sha256']and x['height']==720 and x['width']in[1280,1600]
assert par['runtime_files']==4420 and par['initialized_sidecars']==4041 and par['normal_suffixes']==8 and all(par[k]for k in ['all_runtime_files_unchanged','all_sidecars_exact','all_normal_hashes_exact','all_fixtures_unchanged'])and len(par['jobs'])==4
observations=[]
for row in par['jobs']:
 f=P/row['directory'];c=rd(f/'capture_manifest.json');g=rd(f/'RESULT.json');la=rd(f/'LAUNCH.json');assert g['exit_code']==0 and g['normal_before']==g['normal_after']and g['sidecars_exact']and not g['source_byte_changes']and not g['script_or_shader_errors'];assert g['log_sha256']==sha((f/'engine.log').read_bytes())
 assert la['fixture_sha256']==sha((f/'fixture_source.gd').read_bytes())==sha((P/'capture_critter_saved.gd').read_bytes())
 assert c['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and c['engine']['string']=='4.7.2-stable (official)'and c['renderer']=='mobile'and c['display']!='headless'and c['time_scale']==1.0
 assert len(c['states'])==37 and not c['errors']and len(c['checks'])==35 and all(x['pass']for x in c['checks'])
 expected=6 if c['saved_mode']=='partial' else 18;assert c['expected_caught']==expected and c['seed']['critters']['r60_future_species']is False
 for st in c['states']:
  snap=st['snapshot'];assert snap['game']=='level2'and snap['phase']=='hall'and snap['quality']=='speedy'and snap['caught_count']==expected and snap['collection']==c['seed']['critters']
  if snap['book_exists']:
   assert len(st['card_bindings'])==6
   for card in st['card_bindings']:
    assert card['caught']==bool(c['seed']['critters'].get(card['id'],False))and len(card['labels'])==3 and card['style_class']=='StyleBoxFlat'
    labels={x['role']:x for x in card['labels']};assert set(labels)=={'category_or_unknown_status','species_name','habitat'}
    assert labels['species_name']['text']==(card['name']if card['caught']else'Mystery Friend')
    assert labels['category_or_unknown_status']['text']==({'fish':'🐟','insect':'🦋','bird':'🐦'}[card['category']]if card['caught']else'?')
   observations.extend(st['card_bindings'])
 assert any(st['id']=='same_category_repeat_settled'for st in c['states'])
assert len(observations)==480 and len({x['id']for x in observations})==18 and len({(x['id'],x['caught'])for x in observations})==30
cards=rd(P/'SAVED_CARD_BINDINGS.json');assert cards['book_state_observations']==len(cards['observations'])==80 and cards['card_observations']==480 and cards['label_observations']==1440
q=rd(P/'COMPONENT_QUERIES.json');g=rd(P/'COMPONENT_RESULT.json');assert q['failures']==0 and len(q['queries'])==16 and all(x['pass']for x in q['queries'])and q['native_frames']==0;assert g['exit_code']==0 and g['sidecars_exact']and not g['runtime_files_changed']and g['normal_before']==g['normal_after']and g['fixture_unchanged'];assert g['fixture_sha256']==sha((P/'query_collection.gd').read_bytes())
cs=rd(P/'COLLECTION_SOURCE_CENSUS.json');assert cs['counts']=={'files':312,'calls':35,'symbols':16,'functions':26};assert cs['analyzer_sha256']==sha((P/'audit_collection_source.py').read_bytes())
for x in cs['files']:assert x['parse']=='PASS'and sha(subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R))==x['sha256']
for x in cs['functions']:assert sha(x['source_excerpt'].encode())==x['sha256']
assert rv['human_reviews']==[]and rv['approved']==rv['accepted_removed']==0 and len(rv['native_direct_views'])==14 and len(rv['source_direct_views'])==5
for x in rv['native_direct_views']:assert sha((P/x['path']).read_bytes())==x['sha256']
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 before=rd(O/n);after=rd(P/n);allowed={'revision','phase','publication','change_record','current_ci_snapshot'}
 for k,v in before.items():
  if k not in allowed:assert after[k]==v,(n,k)
 assert after['critter_saved_context']['new_alias_credits']==after['critter_saved_context']['accepted_removed']==0
assert (P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
assert rd(P/'scene_coverage.json')['effective_partial_entries']==85 and rd(P/'scene_coverage.json')['effective_entries_without_current_slice']==91
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert subprocess.check_output(['git','show',B+':'+(H/n).relative_to(R).as_posix()],cwd=R)==(H/n).read_bytes()
t=rd(P/'tally.json');assert t['accepted_removed']==t['replaced']==t['integrated']==t['runtime_verified']==0 and t['all_game_individual_piece_total']is None and t['current_distinct_screen_total']is None and t['regression_count']is None
before=json.loads(subprocess.check_output(['git','show',B+':'+(H/'CURRENT.json').relative_to(R).as_posix()],cwd=R));after=rd(H/'CURRENT.json');allowed={'revision','current_entry','current_per_piece','current_scene_coverage','current_tally','current_backlog','current_manifest','current_ci_evidence'}
for k,v in before.items():
 if k not in allowed:assert after[k]==v,k
assert after['schema']==before['schema']and after['revision']=='FV-AUDIT-20261015-R60'and after['current_tally']=='r60_critter_saved_context/tally.json'
for f in P.rglob('*.json'):assert f.stat().st_size<4*1024*1024;rd(f)
code=(P/'capture_critter_saved.gd').read_text(encoding='utf-8');assert not re.search(r'm\.(?:critter_collection|collection_category|msg_timer)\s*=(?!=)',code)
pix=rd(P/'FRAME_PIXEL_IDENTITY.json');assert pix['files']==len(pix['frames'])==148 and all(x['decoded_nonblank']and sha((P/x['path']).read_bytes())==x['sha256']for x in pix['frames']);assert pix['unique_png_byte_sha256']==len({x['sha256']for x in pix['frames']})
assert rd(P/'REPRODUCTION_INPUTS.json')['baseline']['actual_staging_raw_exact']and not rd(P/'REUSE_INVENTORY.json')['new_use_approved']and not rd(P/'REUSE_INVENTORY.json')['failed_reuse_gap_proved']
print('R60_VALIDATED148native140bounded8excluded140checks;80book480cards1440labels16purequeries312source;CURRENT history/frozen exact;0art/alias/globalunknown')
