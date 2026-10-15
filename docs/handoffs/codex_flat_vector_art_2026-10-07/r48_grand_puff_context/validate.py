from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageStat
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r47_day_one_room_context';B='677ee7b734c9c58dc2464c99f021715d347835db'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
ci=rd(P/'CAPTURE_INDEX.json');assert len(ci['files'])==60 and len({x['path'] for x in ci['files']})==60 and sum(x['art_context_credit'] for x in ci['files'])==56 and ci['excluded_native']==4
for row in ci['files']:
 f=R/row['path'];assert sha(f.read_bytes())==row['sha256'] and f.stat().st_size==row['bytes'];im=Image.open(f);assert list(im.size)==row['aspect'] and sum(ImageStat.Stat(im.convert('RGB').resize((64,36))).var)>1.0
for row in ci['reports']:
 f=R/row['path'];d=rd(f);e=rd(f.parent/'RESULT.json');launch=rd(f.parent/'LAUNCH.json');assert sha(f.read_bytes())==row['sha256'] and sha((P/'capture_grand_puff.gd').read_bytes())==launch['fixture_sha256'] and e['fixture_unchanged']
 assert e['exit_code']==0 and d['errors']==[] and d['renderer']=='mobile' and d['quality']=='speedy' and d['engine']['major']==4 and d['engine']['minor']==7 and d['engine']['patch']==2 and d['engine']['status']=='stable' and d['engine']['build']=='official'
 assert d['normal_before']==d['normal_after']==e['normal_before']==e['normal_after'] and e['sidecars_exact'] and e['sidecars_before_count']==e['sidecars_after_count']==4039
 assert sha((f.parent/'engine.log').read_bytes())==e['log_sha256']
 states={x['id']:x for x in d['states']};assert len(states)==len(d['states'])==30 and states['hall_checkpoint']['snapshot']['game']=='level2' and states['boss_entry']['snapshot']['boss_values']['db_hits']==0
 end=d['ending'];assert end['game']=='level2' and end['room']=='main_hall' and end['pearl_count']==28 and end['director']['day_one_giant_dust_bunny_boss_defeated'] and not end['director']['day_one_active']
 final=states['r3_s1_friends']['snapshot']['boss_values'];assert final['db_hits']==3 and final['db_damage_taken']==0 and final['db_avoids']==5
 assert {'landing_circle','swept_lane'}<={x['snapshot'].get('geometry',{}).get('kind') for x in d['states']}
 hit=[x for x in d['events'] if x['type']=='SOURCE_HIT_AREA_OBSERVATION'];assert len(hit)==3 and all(x['hit'] for x in hit)
 assert len([x for x in d['events'] if x['type']=='InputEventMouseButton'])==30
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 a=rd(O/name);b=rd(P/name)
 for key in ['pieces','entries']:
  if key in a:assert a[key]==b[key]
 if name=='per_piece.json':assert b['supplemental_piece_records'][:11]==a['supplemental_piece_records'] and len(b['supplemental_piece_records'])==16 and len({x['id'] for x in b['pieces']+b['supplemental_piece_records']})==240 and len({x['family'] for x in b['pieces']+b['supplemental_piece_records']})==32
 if name=='tally.json':
  assert b['historical_totals'][:-1]==a['historical_totals'] and b['known_named_design_records_including_supplemental']==240 and b['known_family_count_including_supplemental']==32
  assert b['accepted_removed']==b['integrated']==b['runtime_verified']==0 and b['all_game_individual_piece_total'] is None and b['current_distinct_screen_total'] is None and b['regression_count'] is None
  c=b['current_context'];assert c['exact_capture_count']==4003 and c['retained_native_capture_count']==5730 and c['excluded_diagnostic_native_count']==1727 and 4003+1727==5730
 if name=='scene_coverage.json':assert len(set(b['effective_current_partial_entry_ids']))==83 and b['effective_entries_without_current_slice']==93 and set(b['effective_current_partial_entry_ids'])-set(a['effective_current_partial_entry_ids'])=={'game.grand_puff'}
u=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert u['records']==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records'] and len(u['records'])==73 and u['supplemental_partial_records']==16
for row in rd(P/'SOURCE_REFERENCES.json')['files']+rd(P/'REUSE_INVENTORY.json')['sources']+rd(P/'CONTEXT_PREREQUISITE.json')['checks']:
 b=subprocess.check_output(['git','show',row['revision']+':'+row['path']],cwd=R,stderr=subprocess.PIPE);assert sha(b)==row['sha256'] and len(b)==row['bytes']
for row in rd(P/'REVIEW.json')['actually_viewed_native_frames']:assert sha((P/row['path']).read_bytes())==row['sha256']
for row in rd(P/'NEW_ROLE_RECORDS.json')['records']:
 assert row['id']=='FVR-'+sha(row['stable_id_input'].encode())[:12].upper()
 src=row['source'];b=subprocess.check_output(['git','show',B+':'+src['path']],cwd=R,stderr=subprocess.PIPE);text=b.decode();a=text.index('func '+src['function']+'(');z=text.find('\nfunc ',a+1);z=len(text) if z<0 else z;assert sha(b)==src['file_sha256'] and sha(text[a:z].encode())==src['body_sha256']
assert not subprocess.check_output(['git','diff','--name-only',B,'--','scripts','assets','scenes','shaders','addons','project.godot'],cwd=R).strip()
print('R48_INTEGRITY_PASS 2sourceassistedportalruns60native56bounded4excluded 240roles32families 83partial93without0complete 0accepted globalunknown')
