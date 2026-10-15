"""Validate R66 evidence identity; preserve current native legacy-policy failures."""
from pathlib import Path
import json,hashlib,subprocess,io,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r65_wardrobe_cached_fit';B='0ff29db519e81bb98c69669fffe79de1d68db065';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
idx=rd(P/'CAPTURE_INDEX.json');summary=rd(P/'SUMMARY.json');frames={(x['case'],x['id']):x for x in idx['frames']};assert len(frames)==126 and len(idx['cases'])==9
counts={'native':0,'bounded':0,'excluded':0};passed=dependency=legacy_checks=legacy_failures=0;launch_times=[];profiles=set();bindings=0
for c in idx['cases']:
 folder=P/'native'/c['case'];m=rd(folder/'capture_manifest.json');la=rd(folder/'LAUNCH.json');result=rd(folder/'RESULT.json');mode=m['mode'];launch_times.append(la['started_at_utc']);failed=result['exit_code']!=0
 assert m['source_revision']==D and m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and m['renderer']=='mobile'and m['display']=='Windows'and m['time_scale']==1 and not m['actual_child_data']and not m['authored_world_bootstrap']and not m['source_route_forced']and not m['production_changes']
 assert c['manifest_sha256']==sha((folder/'capture_manifest.json').read_bytes())and result['log_sha256']==sha((folder/'engine.log').read_bytes())and mode==la['mode']
 assert not result['timed_out']and not result['source_byte_changes']and not la['source_before_byte_changes']and not result['script_or_shader_errors']and result['sidecars_exact']and result['sidecar_before_count']==result['sidecar_after_count']==4041 and result['fixture_dependencies_unchanged']
 assert result['normal_before']==result['normal_after']==m['normal_before']==m['normal_after']and len(result['normal_before'])==11
 for name,digest in la['fixture_dependencies'].items():assert sha((folder/name).read_bytes())==digest==sha((P/name).read_bytes())
 for b in m['bindings']:assert b['before_ready']and b['private_path']==m['private_profile']and b['scene_file_path']=='res://scenes/main.tscn';bindings+=1
 failing=[x['label']for x in m['checks']if not x['pass']]
 if failed:assert mode=='legacy'and result['exit_code']==1 and failing==m['errors']==['legacy Continue remains outside DayOne and no opening movie']and len(m['checks'])==12;legacy_checks+=len(m['checks']);legacy_failures+=len(failing)
 else:
  assert not failing and not m['errors']
  if mode=='dependency':dependency+=len(m['checks']);assert len(m['bindings'])==2
  else:passed+=len(m['checks']);profiles.add((mode,m['aspect'][0]))
 for st in m['states']:
  row=frames[(c['case'],st['id'])];raw=(P/row['path']).read_bytes();im=Image.open(io.BytesIO(raw));im.load();assert sha(raw)==st['sha256']==row['sha256']and list(im.size)==m['aspect']==row['dimensions']and sha(im.tobytes())==row['pixel_sha256']and any(lo<hi for lo,hi in im.convert('RGB').getextrema())
  snap=st['snapshot'];assert snap['private_path']==m['private_profile']and snap['time_scale']==1 and snap['scene_file_path']=='res://scenes/main.tscn'
  excluded=failed or mode=='dependency'or snap['quality']!='speedy';counts['native']+=1;counts['excluded'if excluded else'bounded']+=1;assert row['classification'].startswith('EXCLUDED')==excluded
  for bt in snap['controls']:
   assert len(bt['styles'])==6 and all(x['class']=='StyleBoxFlat'for x in bt['styles'].values())
   if bt['name']!='StartMenuConfirmNewGameButton':assert bt['pressed_connections']>=1
   else:assert bt['button_down_connections']>=1
 if mode=='legacy':
  assert'day_one_active'not in m['seed'];byid={s['id']:s['snapshot']for s in m['states']};assert byid['original_menu_settled']['disk']['day_one_active']and byid['continue_route_onset']['movie']['active']and byid['continue_route_onset']['movie']['id']=='d1_opening'and byid['continue_world_settled']['day_one']['day_one_active']
 if mode=='newgame':
  assert len(m['bindings'])==2;last=m['final_snapshot_before_retire'];assert last['day_one']['day_one_active']and not last['reset_marker']and last['archive']['unknown']==m['seed']['flat_vector_private_unknown']and int(last['archive']['save_generation'])>=int(m['seed']['save_generation'])
  hold=next(s for s in m['states']if s['id']=='full_hold_live_fill');bar=next(n for n in hold['selected_canvas_nodes']if n['path'].endswith('StartMenuNewGameHoldFill'));size=re.search(r'S: \(([-\d.]+), ([-\d.]+)\)',bar['global_rect']);assert size and 0<float(size[1])<240 and float(size[2])==8 and hold['snapshot']['main_id']==m['bindings'][0]['main_id']
assert counts=={'native':126,'bounded':70,'excluded':56}and(passed,dependency,legacy_checks,legacy_failures,bindings)==(60,3,24,2,12)and profiles=={(m,w)for m in ['missing','dayone','newgame']for w in [1280,1600]}
assert summary['retained_bounded']==5798+70==5868 and summary['retained_excluded']==2893+56==2949 and summary['retained_native_events']==8691+126==8817
assert(P/'base_capture.gd').read_bytes()==git('show',B+':'+(O/'base_capture.gd').relative_to(R).as_posix())
fixture=(P/'capture_entry.gd').read_text(encoding='utf-8-sig');assert'main._save_state = SaveState.new(main, profile)'in fixture and'reload_current_scene()'in fixture and not re.search(r'(?:m\.(?:game|skin_id|day_one_active|quality)|m\.g\[[^\n]+\]|Engine\.time_scale)\s*=(?!=)',fixture) and not any(x in fixture for x in ['m._enter_','m._launch_','m._apply_quality'])
project=git('show',D+':project.godot').decode();scene=git('show',D+':scenes/main.tscn').decode();uid=re.search(r'uid="([^"]+)"',scene)[1];assert ('run/main_scene="'+uid+'"')in project or 'run/main_scene="res://scenes/main.tscn"'in project
for row in rd(P/'CURRENT_SOURCE_METHODS.json')['methods']:
 raw=git('show',D+':'+row['path']);body=''.join(raw.decode().splitlines(keepends=True)[row['start_line']-1:row['end_line']]);assert sha(raw)==row['file_sha256']and sha(body.encode())==row['body_sha256']and body==row['body']
refs=rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files'];assert len(refs)==68
for row in refs:
 raw=git('show',row['revision']+':'+row['path']);assert len(raw)==row['bytes']and sha(raw)==row['sha256']and row['http_status']==200
assert max(x['checked_at_utc']for x in rd(P/'SOURCE_REFERENCES.json')['files'])<min(launch_times)
new=rd(P/'NEW_NAMED_PIECE.json');assert new['id']=='FVR-'+sha(new['stable_id_input'].encode())[:12].upper()=='FVR-42846B2A5A82'and new['family']=='sky_lagoon_affordances'and new['visible_artwork_not_functional_geometry']and new['drawing_required']is None and new['integration_sha']is None
mask=rd(P/'MASK_SOURCE_IDENTITY.json');assert mask['alpha_positive_rgb_values']==[[255,255,255]]and mask['dimensions']==[199,228]and not mask['source_edits']
for obs in mask['observations']:
 n=obs['node'];assert n['class']=='Sprite2D'and n['texture']['path']=='res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png'
known=rd(P/'CURRENT_KNOWN_ROLE_UNION.json');assert len(known['records'])==len({x['id']for x in known['records']})==241 and len({x['family']for x in known['records']})==33
oldunion=rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json');union=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert union['records'][:74]==oldunion['records']and len(union['records'])==75 and len({r['family']for r in union['records']})==15 and union['new_R66_partial_existing_ids']==['FV-50B38661B1E4']and union['supplemental_partial_records']==17
oldcat=rd(O/'CURRENT_CATALOGUE_CONTEXT_UNION.json');cat=rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json');assert set(cat['current_partial_ids'])==set(oldcat['current_partial_ids'])|{'standalone.main'}and cat['current_partial_count']==89 and cat['without_current_slice_count']==87 and cat['complete_count']==0 and cat['all_entries_still_incomplete']==176
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n)
 for k,v in old.items():
  if k not in ['revision','phase','publication','change_record','current_ci_snapshot']:assert d[k]==v,(n,k)
 block=d['display_entry_context'];assert block['known_roles']==241 and block['families']==33 and block['catalogue_partial']==89 and block['catalogue_without_current_slice']==87 and block['catalogue_complete']==block['accepted_removed']==0 and block['native_policy_status']=='FAIL_LEGACY_SOURCE_CONTRACT_UNFIXED'
review=rd(P/'REVIEW.json');assert len(review['direct_native_views'])==14 and not review['all126manually_viewed']and review['human_review']is None and not review['creative_acceptance']
for role in review['per_piece_comparisons']:assert set(role['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'}and role['owner']is None and not role['accepted_removed']
assert rd(H/'CURRENT.json')['current_tally']=='r66_display_entry_context/tally.json'
changes=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();assert not any(x.startswith(('assets/','scripts/','scenes/','shaders/','.codex/','.claude/','.github/'))or x in ['project.godot','AGENTS.md','SECURITY.md','ASSET_LICENSES.md']for x in changes)
assert summary['generation_calls']==summary['new_drawing_samples']==summary['approved']==summary['integrated']==summary['runtime_verified_replacements']==summary['accepted_removed']==0 and summary['all_game_artwork_total']is None and summary['regression_total']is None and not summary['mission_complete']
print('R66_EVIDENCE_IDENTITY_PASS:126rawPNGs;70bounded56excluded;6cases60checks/preflight3pass;legacy24checks2FAIL preserved;68refs/241roles33families/89partial87without0complete/frozen5/history;NO_PRODUCT_OR_ART_ACCEPTANCE')
