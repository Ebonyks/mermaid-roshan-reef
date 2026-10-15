from pathlib import Path
import json,hashlib,subprocess,base64
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r45_dispatch_semantics_audit';B='7cdb9bf63bd8f3846b34b17cce74b065747aae92'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
ci=rd(P/'CAPTURE_INDEX.json');assert len(ci['files'])==58 and sum(x['art_context_credit'] for x in ci['files'])==48 and ci['excluded_native']==10
for x in ci['files']:
 f=R/x['path'];assert f.stat().st_size==x['bytes'] and sha(f.read_bytes())==x['sha256'] and list(Image.open(f).size)==x['aspect']
for x in ci['manifests']:
 f=R/x['path'];assert sha(f.read_bytes())==x['sha256'];d=rd(f);assert d['errors']==[] and d['normal_before']==d['normal_after'] and d['normal_route_proved']==False
 states={x['id']:x for x in d['states']}
 for n in range(7):
  assert states[f'note_{n}_pressed']['snapshot']['input_down']==True
  if n<6:assert states[f'note_{n}_released']['progress']==n+1
 assert states['note_6_released']['game']=='' and states['note_6_released']['presentation']['medal_present']==True
 assert states['reentry']['game']=='melody' and states['reentry']['progress']==0 and states['voluntary_exit']['game']==''
 e=rd(f.parent/'RESULT.json');assert e['exit_code']==0 and e['sidecars_exact'] and e['sidecars_before_count']==4039 and e['sidecars_after_count']==4039 and e['normal_before']==e['normal_after'] and e['fixture_unchanged']
 assert sha((f.parent/'engine.log').read_bytes())==e['log_sha256']
 executed=rd(P/'EXECUTED_FIXTURE.json');raw=base64.b64decode(executed['source_base64']);assert sha(raw)==executed['executed_sha256']==rd(f.parent/'LAUNCH.json')['fixture_sha256'];assert raw==(P/'capture_melody_context.gd').read_bytes()+b'\n';assert sha((P/'capture_melody_context.gd').read_bytes())==executed['publishable_sha256']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 a=rd(O/name);b=rd(P/name)
 for key in ['pieces','entries','supplemental_piece_records']:
  if key in a:assert a[key]==b[key],(name,key)
 if name=='tally.json':
  assert b['historical_totals'][:-1]==a['historical_totals']
  assert b['known_named_design_records_including_supplemental']==230 and b['known_family_count_including_supplemental']==31
  assert b['accepted_removed']==b['integrated']==b['runtime_verified']==0 and b['all_game_individual_piece_total'] is None and b['current_distinct_screen_total'] is None and b['regression_count'] is None
  c=b['current_context'];assert c['exact_capture_count']==3869 and c['retained_native_capture_count']==5562 and c['excluded_diagnostic_native_count']==1693 and 3869+1693==5562
 if name=='scene_coverage.json':assert len(set(b['effective_current_partial_entry_ids']))==80 and b['effective_entries_without_current_slice']==96 and 80+96==176
bind=rd(P/'SOURCE_BINDING.json');assert len(bind['piece_ids'])==11 and len(bind['visible_partial_ids'])==10 and bind['new_piece_ids']==[]
review=rd(P/'REVIEW.json');assert len(review['role_reviews'])==11 and len(review['actually_viewed_native_frames'])==8
for x in review['actually_viewed_native_frames']:assert sha((P/x['path']).read_bytes())==x['sha256']
for x in rd(P/'REUSE_INVENTORY.json')['sources']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R);assert sha(b)==x['sha256'] and len(b)==x['bytes'] and (R/x['path']).read_bytes()==b
for x in rd(P/'CONTEXT_PREREQUISITE.json')['checks']:
 b=subprocess.check_output(['git','show',x['revision']+':'+x['path']],cwd=R);assert sha(b)==x['sha256'] and len(b)==x['bytes']
assert not subprocess.check_output(['git','diff','--name-only',B,'--','scripts','assets','scenes','shaders','addons','project.godot'],cwd=R).strip()
print('R46_INTEGRITY_PASS 58native48bounded10excluded 11frozenMelodyIDs10visible 230roles31families 80partial96without0complete 0accepted globalunknown')
