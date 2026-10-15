from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r46_melody_context';B='dca7e7ce8d712b2b16ab004b7fcd070d3133b8b7'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
ci=rd(P/'CAPTURE_INDEX.json');assert len(ci['files'])==108 and sum(x['art_context_credit'] for x in ci['files'])==78 and ci['excluded_native']==30
for x in ci['files']:
 f=R/x['path'];assert f.stat().st_size==x['bytes'] and sha(f.read_bytes())==x['sha256'] and list(Image.open(f).size)==x['aspect']
for r in ci['reports']:
 f=R/r['path'];assert sha(f.read_bytes())==r['sha256'];d=rd(f);e=rd(f.parent/'RESULT.json');launch=rd(f.parent/'LAUNCH.json');assert d['normal_before']==d['normal_after'] and e['normal_before']==e['normal_after'] and e['sidecars_exact'] and e['sidecars_before_count']==e['sidecars_after_count']==4039 and e['fixture_unchanged'];assert sha((f.parent/'engine.log').read_bytes())==e['log_sha256']
 source=P/'prior_attempts/capture_day_one_rooms_attempt1.gd' if f.parent.name.startswith('attempt1') else P/'capture_day_one_rooms.gd';assert sha(source.read_bytes())==launch['fixture_sha256']
 if f.parent.name.startswith('attempt1'):
  assert len(d['states'])==12 and e['exit_code']==1 and d['errors']==['unavailable actual control StuffieCard_eagle'];continue
 assert e['exit_code']==0 and d['errors']==[]
 states={x['id']:x for x in d['states']};ready=states['room_ready']['snapshot'];passive=states['room_passive']['snapshot'];last=states['reload_reentry']['snapshot'];before=d['before_reload']
 assert ready['director']==passive['director'] and ready['stuffie_wins']==passive['stuffie_wins']
 assert last['director']==before['director'] and last['companion']==before['companion'] and last['stuffie_wins']==before['stuffie_wins']
 assert last['room']==('playroom' if d['mode']=='rescue' else 'craft_room') and last['companion']=='eagle'
 if d['mode']=='rescue':
  assert before['stuffie_wins']['rescued_eagle'] and not ready['stuffie_wins'].get('rescued_eagle',False)
  assert any(e['type']=='OFFER_READINESS_OBSERVATION' and e['automatic_offer_present'] for e in d['events'])
  assert not any(e['type']=='SOURCE_TOY_NOOK_RECOVERY_OBSERVATION' for e in d['events'])
 else:
  assert before['director']['day_one_art_customization_completed'] and 'art' in before['director']['day_one_completed_rooms']
  assert len(before['director']['day_one_art_collected_materials'])==4 and len(before['director']['day_one_art_cleaned_grime'])==3
  assert ready['director']['day_one_art_collected_materials']=={} and ready['director']['day_one_art_cleaned_grime']=={}
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 a=rd(O/name);b=rd(P/name)
 for key in ['pieces','entries']:
  if key in a:assert a[key]==b[key]
 if name=='per_piece.json':assert b['supplemental_piece_records'][:6]==a['supplemental_piece_records'] and len(b['supplemental_piece_records'])==11 and len({x['id'] for x in b['pieces']+b['supplemental_piece_records']})==235
 if name=='tally.json':
  assert b['historical_totals'][:-1]==a['historical_totals'] and b['known_named_design_records_including_supplemental']==235 and b['known_family_count_including_supplemental']==31
  assert b['accepted_removed']==b['integrated']==b['runtime_verified']==0 and b['all_game_individual_piece_total'] is None and b['current_distinct_screen_total'] is None and b['regression_count'] is None
  c=b['current_context'];assert c['exact_capture_count']==3947 and c['retained_native_capture_count']==5670 and c['excluded_diagnostic_native_count']==1723 and 3947+1723==5670
 if name=='scene_coverage.json':assert len(set(b['effective_current_partial_entry_ids']))==82 and b['effective_entries_without_current_slice']==94 and 82+94==176
u=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert len(u['records'])==len({x['id'] for x in u['records']})==73 and len({x['family'] for x in u['records']})==15
for x in rd(P/'SOURCE_REFERENCES.json')['files']+rd(P/'REUSE_INVENTORY.json')['sources']+rd(P/'CONTEXT_PREREQUISITE.json')['checks']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R);assert sha(b)==x['sha256'] and len(b)==x['bytes']
for x in rd(P/'REVIEW.json')['actually_viewed_native_frames']:assert sha((P/x['path']).read_bytes())==x['sha256']
for role in rd(P/'NEW_ROLE_RECORDS.json')['records']:
 assert role['id']=='FVR-'+sha(role['stable_id_input'].encode())[:12].upper()
 source=role['source'];raw=subprocess.check_output(['git','show',B+':'+source['path']],cwd=R);text=raw.decode('utf-8');start=text.index('func '+source['function']+'(');end=text.find('\nfunc ',start+1);end=len(text) if end<0 else end
 assert sha(raw)==source['file_sha256'] and sha(text[start:end].encode())==source['body_sha256']
assert not subprocess.check_output(['git','diff','--name-only',B,'--','scripts','assets','scenes','shaders','addons','project.godot'],cwd=R).strip()
print('R47_INTEGRITY_PASS 4currentcases 108retained78bounded30excluded 235roles31families 73existingpartial15families 82partial94without0complete 0accepted globalunknown')
