from pathlib import Path
import json,hashlib,subprocess,sys,importlib.util,collections,os
from PIL import Image
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parent;O=P.parent/'r68_gate_missing_art';H=P.parent;B='fe7ad2cb55205dd21035cc59beca0d2d918b3920';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
s=importlib.util.spec_from_file_location('bounded69validator',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
sum_=rd(P/'SUMMARY.json');oldsum=rd(O/'SUMMARY.json');assert sum_['source_revision']==D and sum_['bounded_observer_cases']==4 and sum_['bounded_observer_checks']==55 and sum_['new_native_frames']==62 and sum_['new_bounded_contexts']==40 and sum_['new_excluded_diagnostics']==22
assert sum_['retained_bounded']==oldsum['retained_bounded']+40==5960 and sum_['retained_excluded']==oldsum['retained_excluded']+22==2991 and sum_['retained_native_events']==oldsum['retained_native_events']+62==8951
assert sum_['source_art_status']=='FAIL_OPAQUE_FALLBACK_OCCLUDES_LOADED_ART'and sum_['source_return_status']=='FAIL_SOURCE_RETURN_CONTRACT'and sum_['source_return_failures']==2
for k in ['generation_calls','new_drawing_samples','new_runtime_assets','approved','integrated','runtime_verified_replacements','accepted_removed']:assert sum_[k]==0
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert sum_[k]is None
assert not sum_['mission_complete']
frames=rd(P/'PIXEL_EVIDENCE.json')['raw_frames'];assert len(frames)==62 and len({v['path']for v in frames})==62
for row in frames:
 f=R/row['path'];raw=f.read_bytes();im=Image.open(f).convert('RGBA');assert sha(raw)==row['sha256']and len(raw)==row['bytes']and list(im.size)==row['size']and sha(im.tobytes())==row['decoded_rgba_sha256'];assert im.convert('RGB').getextrema()!=((0,0),(0,0),(0,0))
for row in rd(P/'PIXEL_EVIDENCE.json')['opaque_field_measurements']:
 im=Image.open(R/row['path']).convert('RGB');rgb,count=collections.Counter(im.get_flattened_data()).most_common(1)[0];assert list(rgb)==row['dominant_rgb']and count==row['dominant_pixel_count'] and row['fraction']>.96 and row['loaded_tiles']==8 and row['walkway_loaded']and row['house_loaded'];assert max(abs(a-b)for a,b in zip(rgb,[51,31,92]))<=1
checks=0;routes=[]
for row in sum_['cases']:
 a=P/'native'/row['case'];m=rd(a/'capture_manifest.json');res=rd(a/'RESULT.json');assert sha((a/'capture_manifest.json').read_bytes())==row['manifest_sha256'];assert m['normal_before']==m['normal_after']==res['normal_after']==res['normal_before'];assert res['sidecar_before_count']==res['sidecar_after_count']==4041 and res['sidecars_exact'] and res['fixture_dependencies_unchanged']and not res['source_byte_changes'];assert m['source_revision']==D and m['actual_child_data']is False and m['production_changes']==[];assert m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079' and m['renderer']=='mobile' and m['display']=='Windows'
 if row['case'].startswith('attempt3'):
  assert m['observer_status']=='PASS'and not m['errors']and all(v['pass']for v in m['checks']) and res['exit_code']==0 and not res['script_or_shader_errors'];checks+=len(m['checks']);assert all(v['before_ready']for v in m['bindings']);assert all((a/n).read_bytes()==(P/n).read_bytes()for n in ['base_capture.gd','capture_entry.gd','capture_fairy.gd'])
  assert m['seed']['quality']=='speedy'and m['seed']['day_one_active']is False and m['seed']['custom_fish']==m['seed']['custom_friends']==[] and m['seed']['companion']==''
  if m['mode']=='dormant':assert m['source_route_status']=='DORMANT_NEGATIVE_ONLY'and not m['source_route_failures']
  else:
   assert m['source_route_status']=='FAIL_SOURCE_RETURN_CONTRACT'and len(m['source_route_failures'])==1;post=next(v['snapshot']for v in m['states']if v['id']=='05_back_source_failure');pre=next(v['snapshot']for v in m['states']if v['id']=='05_butterfly_world_passive');assert pre['game']=='galaxy'and pre['galaxy']['script']=='res://scripts/galaxy.gd'and pre['galaxy']['mode']=='planet';assert pre['navigation_bindings'][0]['id']=='pearl_castle';assert post['game']=='level2'and post['phase']=='promenade'and post['hall']['layer_id']==0 and post['galaxy_return_flags']['galaxy_instance_alive']and post['galaxy_return_flags']['fairy_conservatory']and post['galaxy_return_flags']['return_set'];assert post['navigation_bindings']==[];routes.append(post)
  if m['mode']=='revealed':assert len(m['bindings'])==2 and m['final_snapshot']['profile_reloaded']and m['final_snapshot']['moonflower']['visual_state']=='open'
 else:assert res['exit_code']==1 and m['errors']
assert checks==55 and len(routes)==2
sources=rd(P/'SOURCE_BINDINGS.json')['functions']
for row in sources:
 raw=git('show',D+':'+row['path']);ls=raw.decode('utf-8').splitlines(keepends=True);body=''.join(ls[row['start_line']-1:row['end_line']]).encode('utf-8');assert sha(raw)==row['file_sha256']and sha(body)==row['body_sha256']and body.decode()==row['body']
raw=git('show',D+':scripts/arena/fairy_conservatory_handoff_2d.gd').decode('utf-8');assert '_backdrop.z_index'not in raw and 'tile.z_index = -20'in raw and '_walkway.z_index = -5'in raw and '_house.z_index = -4'in raw
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 o=rd(O/name);x=rd(P/name)
 for k in o:
  if k not in ['revision','phase','publication']:assert x[k]==o[k],(name,k)
 assert x['fairy_route_context']['known_roles']==243 and x['fairy_route_context']['catalogue_partial']==92 and x['fairy_route_context']['accepted_removed']==0
roles=rd(P/'PIECE_RECORDS.json')['records'];assert len(roles)==2
for row in roles:assert row['id']=='FVR-'+sha(row['stable_id_input'].encode())[:12].upper()and not row['full_context_review_complete']and row['drawing_required']is None
k=rd(P/'CURRENT_KNOWN_ROLE_UNION.json');ko=rd(O/'CURRENT_KNOWN_ROLE_UNION.json');assert k['records'][:len(ko['records'])]==ko['records']and len(k['records'])==len({v['id']for v in k['records']})==k['known_roles']==243 and len({v['family']for v in k['records']})==k['known_families']==34
u=rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json');prior=rd(O/'CURRENT_CATALOGUE_CONTEXT_UNION.json');assert set(u['current_partial_ids'])==set(prior['current_partial_ids'])|{'game.fairy_conservatory','game.galaxy','galaxy.butterfly_garden'}and len(u['current_partial_ids'])==u['current_partial_count']==92 and u['without_current_slice_count']==84 and u['complete_count']==0 and u['entry_count']==176
part=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert part['records']==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records']and part['current_existing_named_records_with_partial_context']==75 and part['current_existing_families_with_partial_context']==15 and part['supplemental_partial_records']==19
rv=rd(P/'REVIEW.json');assert len(rv['axes'])==10 and len(rv['direct_views'])==12 and sum(v['classification']=='BOUNDED_PARTIAL_CURRENT_CONTEXT'for v in rv['direct_views'])==9
for row in rv['direct_views']:assert sha((P/row['path']).read_bytes())==row['sha256']
for row in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:b=git('show',row['revision']+':'+row['path']);assert sha(b)==row['sha256']and len(b)==row['bytes']
cur=rd(H/'CURRENT.json');assert cur['current_tally']=='r69_fairy_route_context/tally.json'and not cur['mission_complete']
allowed={str((P).relative_to(R)).replace('\\','/')+'/', 'design/audit_impacts/flat-vector-fairy-route-20261015.json','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md','docs/handoffs/codex_flat_vector_art_2026-10-07/README.md','docs/handoffs/codex_flat_vector_art_2026-10-07/CURRENT.json'}
for path in set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()):assert path in allowed or path.startswith(P.relative_to(R).as_posix()+'/'),path
base=json.loads((H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json').read_text(encoding='utf-8'));W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef')
assert len(base['runtime_raw_hashes'])==4420 and all(sha((W/k).read_bytes())==v for k,v in base['runtime_raw_hashes'].items())
side={}
for root,dirs,files in os.walk(W):
 dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
 for name in files:
  f=Path(root)/name
  if f.suffix in {'.uid','.import'}:side[f.relative_to(W).as_posix()]=sha(f.read_bytes())
assert side==base['sidecars'] and len(side)==4041
normal=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
for suffix,digest in base['normal_save_hashes'].items():
 f=Path(str(normal)+suffix);assert (sha(f.read_bytes()) if f.is_file() else 'absent')==digest
print('R69_EVIDENCE_PASS; source art/return remain FAIL;62 frames40 bounded22 excluded;55 observer checks;243 roles34families;92partial84without0complete;0acceptedremoved')
