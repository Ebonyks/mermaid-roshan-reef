from pathlib import Path
import json,hashlib,subprocess,re,importlib.util
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;B='ce4a454f65fc5b61f915ce41176af866fdf633ab';D='dd799b2d43871b29d1d6e0503646308a194dad1e';O=H/'r78_game_payload_closure'
sp=importlib.util.spec_from_file_location('bounded79',P/'bounded_json.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
g=rd(P/'SOURCE_OWNER_GRAPH.json');s=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');roles=rd(P/'NEW_ROLE_RECORDS.json')['pieces'];assert len(g['files'])==313 and g['scanner_sha256']==sha((P/'scan_promenade_owner.py').read_bytes())
assert g['summary']['named_target_calls']==98 and g['summary']['non_test_named_target_calls']==27 and g['summary']['non_test_wall_array_references']==8
for row in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 b=git('show',row['revision']+':'+row['path']);assert len(b)==row['bytes']and sha(b)==row['sha256'],row['path']
assert len(idx['captures'])==78 and len(idx['cases'])==4 and sum(x['bounded']for x in idx['captures'])==70
checks=0
for case in idx['cases']:
 folder=P/case['path'];d=rd(folder/'capture_manifest.json');res=rd(folder/'RESULT.json');launch=rd(folder/'LAUNCH.json');script=(folder/'capture_entry.gd').read_bytes();assert sha(script)==launch['fixture_sha256']and res['fixture_dependency_unchanged']
 assert res['exit_code']==0 and not res['timed_out']and not res['script_or_shader_errors']and not res['source_byte_changes']and res['sidecars_exact']and res['sidecar_after_count']==4088 and res['normal_before']==res['normal_after']
 assert d['observer_status']=='PASS'and d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and d['renderer']=='mobile'and d['time_scale']==1.0 and not d['errors']and d['normal_before']==d['normal_after']and len(d['normal_before'])==11
 checks+=len(d['checks']);assert all(x['pass']for x in d['checks']);seen=set()
 for frame in d['states']:
  f=folder/frame['path'];raw=f.read_bytes();assert sha(raw)==frame['sha256'];im=Image.open(f);assert list(im.size)==frame['dimensions']and im.size[0]in [1280,1600]and im.height==720 and frame['id']not in seen;seen.add(frame['id'])
  if frame['classification'].startswith('BOUNDED_'):
   w=frame['snapshot']['world'];assert frame['snapshot']['quality']=='speedy'and w['game']=='level2'and w['phase']=='promenade'and w['wall_pics_count']==0 and not w['legacy_lagoon_constructed']and w['promenade_constructed']
 if 'attempt2_'in folder.name:
  for kind in ['slide','swing','seesaw']:assert all(kind+'_action_'+str(i)in seen for i in range(4))and kind+'_completed'in seen and kind+'_focused'in seen
assert checks==100 and s['healthy_observer_checks']==100
for name in ['FIXTURE_SYNTAX_GATES.json','FIXTURE_SYNTAX_GATES_ATTEMPT1.json']:assert rd(P/name)['status']=='PASS_BEFORE_NATIVE'and all(x['exit_code']==0 for x in rd(P/name)['checks'])
assert rd(P/'FIXTURE_SYNTAX_GATES.json')['fixture_files'][0]['sha256']==sha((P/'capture_entry.gd').read_bytes())
code=(P/'capture_entry.gd').read_text(encoding='utf-8');assert not re.search(r'\bm\.(game|g|quality|intro_active|first_session|day_one_active|save_data|position)\s*=(?!=)',code)and'Engine.time_scale ='not in code and'ProjectSettings.save('not in code
assert len(roles)==1 and roles[0]['id']=='FVR-5344465CE503'and roles[0]['family']=='sky_lagoon_affordances'and roles[0]['reviewed_active_instances']==['slide','swing','seesaw']and roles[0]['visible_artwork_not_functional_geometry']
assert not roles[0]['reuse_ready']and roles[0]['drawing_required']is None and all(x is None for x in roles[0]['acceptance_evidence'].values())

measure=rd(P/'CUE_MEASUREMENTS.json')['measurements'];assert len(measure)==8
for x in measure:
 expected={'slide':118.0,'swing':110.0,'seesaw':110.0}[x['consumer']];assert x['native_hit_radius_px']==expected and x['source_hit_disk_contains_glow_center']==(x['consumer']=='seesaw')and not x['direct_glow_center_gesture_executed']
assert len(rd(P/'REVIEW.json')['axes'])==10 and not rd(P/'REVIEW.json')['mission_complete']and not rd(P/'OWNER_DISPOSITIONS.json')['legacy_picture_race_paths_globally_unreachable']
assert s['known_roles']==263 and s['known_families']==35 and s['new_roles']==1 and s['new_families']==0 and s['supplemental_partial_roles']==39 and s['existing_partial_roles']==75 and s['existing_partial_families']==15
assert s['retained_bounded']==6412 and s['retained_excluded']==3506 and s['retained_native_events']==9918 and s['new_native_frames']==78 and s['new_bounded_contexts']==70 and s['new_excluded_diagnostics']==8
assert s['catalogue_partial']==92 and s['catalogue_without_current_slice']==84 and s['catalogue_complete']==0
for k in ['approved','integrated','runtime_verified_replacements','accepted_removed','generation_calls','new_drawing_samples','new_runtime_assets','new_alias_credits']:assert s[k]==0,k
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert s[k]is None,k
assert not s['allcaller_closure']and not s['global_unreachability_proved']and not s['mission_complete']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/name);new=rd(P/name);allowed={'revision','phase','inherited_r78_reference_base','promenade_playground_ownership','current_effective_summary','publication','playground_piece_records','r79_route_qualification','r79_point_by_point_items'};assert all(new[k]==v for k,v in old.items()if k not in allowed),name
 assert new['promenade_playground_ownership']==s and new['inherited_r78_reference_base']['revision']==B
u=rd(P/'CURRENT_KNOWN_ROLE_UNION.json');assert len(u['records'])==263 and len({x['id']for x in u['records']})==263 and u['known_roles']==263 and u['known_families']==35 and u['records'][:-1]==rd(O/'CURRENT_KNOWN_ROLE_UNION.json')['records']
assert rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')['supplemental_partial_records']==39
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix()),name
assert rd(P/'REPRODUCTION_CHECK.json')['all_byte_identical']and rd(P/'SOURCE_TESTS.json')['tests']==10 and rd(P/'SOURCE_TESTS.json')['exit_code']==0
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();allowed_doc={'audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/audit_impacts/flat-vector-promenade-slide-20261016.json',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()};assert all(x in allowed_doc or x.startswith(P.relative_to(R).as_posix()+'/')for x in changed)
assert rd(H/'CURRENT.json')['current_tally']=='r79_promenade_slide_ownership/tally.json'and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval']is False
print('R79_VALIDATION_PASS 313exactAST/8wallrefs;4nativecases100checks;78raw70bounded8excluded;onecue3consumers;263/35;6412bounded9918history;0art/runtime/acceptance;globalunknown')