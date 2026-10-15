"""R57 semantic evidence invariants; never substitutes source for visual acceptance."""
from pathlib import Path
import json,hashlib,subprocess,os
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r56_comfy_pot_ownership';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
s=rd(P/'SOURCE_GAME_CENSUS.json');c=rd(P/'CATALOGUE_CROSSWALK.json');n=rd(P/'component/COMPONENT.json');g=rd(P/'component/RESULT.json');sums=rd(P/'SOURCE_AND_COMPONENT_SUMMARY.json');refs=rd(P/'SOURCE_REFERENCES.json')['files'];refmap={(x['revision'],x['path']):x for x in refs}
assert len(s['files'])==312 and len(s['rows'])==99 and len({r['id']for r in s['rows']})==99
assert s['bound_literal_main_field_write_rows']==29 and len(s['bound_literal_main_values'])==14 and not s['full_game_value_domain_closed']
assert s['analyzer_sha256']==sha((P/'audit_game_values.py').read_bytes())
for f in s['files']:
 assert f['revision']==D and f['sha256']==refmap[(D,f['path'])]['sha256'] and f['bytes']==refmap[(D,f['path'])]['bytes']
assert len(c['rows'])==176 and [r['id']for r in c['rows']]==[r['id']for r in rd(O/'scene_coverage.json')['entries']]
assert c['class_counts']=={'AMBIENT_CATALOGUE_ID':100,'UI_ALIAS_OWNER_STATE_OPEN':12,'GAME_ALIAS_CALLER_BINDING_OPEN':60,'STANDALONE_SOURCE_SCENE':4}
assert c['suffix_nonempty']==11 and c['suffix_empty']==49 and c['new_context_credits']==c['new_closed_routes']==0
assert all(not r['new_rendered_context_credit']and not r['normal_route_closed']for r in c['rows'])
for r in c['rows']:
 if r['kind']=='STANDALONE_SOURCE_SCENE':assert len(r['scenes'])==1,r['id']
assert len(n['catalogue'])==100 and len(n['queries'])==144 and n['failed']==0
assert n['engine']['string']=='4.7.2-stable (official)'and n['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
assert n['display']=='headless'and n['configured_renderer']=='mobile'
assert sum('pass'in r for r in n['queries'])==84 and len(n['checks'])==3
assert all(r.get('pass',True)for r in n['queries']+n['checks'])
assert g['exit_code']==0 and not g['engine_errors']and g['runtime_file_count']==4420 and not g['changed_runtime_files']and g['sidecar_count']==4041 and g['sidecars_exact']and g['fixture_unchanged']and g['normal_before']==g['normal_after']
assert g['log_sha256']==sha((P/'component/engine.log').read_bytes())
assert rd(P/'component/LAUNCH.json')['fixture_sha256']==sha((P/'selector_component.gd').read_bytes())
# Entire inherited records remain exact; only additive overlay and current publication routing differ.
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 before=rd(O/name);after=rd(P/name);allowed={'revision','phase','publication','change_record','current_ci_snapshot'}
 for k,v in before.items():
  if k not in allowed:assert after[k]==v,(name,k)
 assert after['catalogue_selector_crosswalk']['accepted_removed']==0 and not after['catalogue_selector_crosswalk']['normal_route_or_art_acceptance']
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:
 b=subprocess.check_output(['git','show','1e0589b3a99c0d4c0911d3e56304fa7a27a7f664:'+str((H/name).relative_to(R)).replace('\\','/')],cwd=R);assert b==(H/name).read_bytes()
assert (P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
t=rd(P/'tally.json');assert t['accepted_removed']==t['integrated']==t['runtime_verified']==t['replaced']==0 and t['all_game_individual_piece_total']is None and t['current_distinct_screen_total']is None and t['regression_count']is None
assert not list(P.rglob('*.png'))and sums['new_rendered_frames']==0 and sums['total_assertions']==87 and sums['retained']['bounded_native']==4583
for f in P.rglob('*.json'):
 assert f.stat().st_size<4*1024*1024,f.name;rd(f)
print('R57_VALIDATED 312scripts/99source candidates/14literal values/176preservedIDs/144component queries87assertions/0visual-route-art credit')

i=rd(P/"COMPONENT_INPUTS.json");assert i["aliases"]["sha256"]==sha((P/"COMPONENT_ALIASES.json").read_bytes()) and i["baseline"]["sha256"]==sha((H/"r51_farmer_context/RUNTIME_BYTE_BASELINE.json").read_bytes())
assert rd(P/"COMPONENT_ALIASES.json")==[q["id"].removeprefix("alias_suffix_")for q in n["queries"]if q["id"].startswith("alias_suffix_")]
