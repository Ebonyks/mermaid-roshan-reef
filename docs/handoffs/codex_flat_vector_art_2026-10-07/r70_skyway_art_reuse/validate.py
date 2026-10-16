from pathlib import Path
import json,hashlib,subprocess,collections,importlib.util,os,re
from PIL import Image
R=Path(__file__).resolve().parents[4];P=Path(__file__).resolve().parent;H=P.parent;O=H/'r69_fairy_route_context';B='dccb444efd0277bbcea62af1384a78b535d5b569';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
s=importlib.util.spec_from_file_location('bounded70validator',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
x=rd(P/'SUMMARY.json');old=rd(O/'SUMMARY.json');assert x['native_cases']==5 and x['final_cover_cases']==2 and x['final_cover_checks']==52 and x['new_native_frames']==89 and x['new_bounded_contexts']==36 and x['new_excluded_diagnostics']==53
for key in ['new_roles','new_families','new_alias_credits','generation_calls','new_drawing_samples','new_runtime_assets','approved','integrated','runtime_verified_replacements','accepted_removed']:assert x[key]==0
assert x['source_reuse_candidate_awaiting_review']==1 and not x['mission_complete']
for key in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert x[key]is None
assert x['retained_bounded']==old['retained_bounded']+36==5996 and x['retained_excluded']==old['retained_excluded']+53==3044 and x['retained_native_events']==old['retained_native_events']+89==9040
assert x['known_roles']==243 and x['families']==34 and x['catalogue_partial']==92 and x['catalogue_without_current_slice']==84 and x['catalogue_complete']==0
frames=rd(P/'PIXEL_EVIDENCE.json')['raw_frames'];assert len(frames)==len({v['path']for v in frames})==89
for row in frames:
 f=R/row['path'];raw=f.read_bytes();im=Image.open(f).convert('RGBA');assert sha(raw)==row['sha256']and len(raw)==row['bytes']and list(im.size)==row['size']and sha(im.tobytes())==row['decoded_rgba_sha256'];assert im.convert('RGB').getextrema()!=((0,0),(0,0),(0,0))
for row in rd(P/'PIXEL_EVIDENCE.json')['fallback_color_measurements']:
 im=Image.open(R/row['path']).convert('RGBA');count=collections.Counter(im.get_flattened_data())[(51,31,92,255)];assert count==row['exact_fallback_pixels']and abs(count/(im.width*im.height)-row['fraction'])<1e-12
 if row['backdrop_z']==0:assert row['fraction']>.96 and row['class']=='SOURCE_OCCLUDED_BASELINE'
 elif row['case'].startswith('attempt3_cover'):assert row['fraction']<.001 and row['backdrop_z']==-30
 elif row['aspect'][0]==1600:assert .18<row['fraction']<.21
checks=0;compares=0;finals=0
for case in x['cases']:
 a=P/'native'/case['case'];m=rd(a/'capture_manifest.json');res=rd(a/'RESULT.json');assert sha((a/'capture_manifest.json').read_bytes())==case['manifest_sha256'];assert res['normal_before']==res['normal_after']==m['normal_before']==m['normal_after'];assert res['sidecars_exact']and res['sidecar_before_count']==res['sidecar_after_count']==4041 and not res['source_byte_changes']and res['fixture_dependencies_unchanged']and not res['script_or_shader_errors'];assert m['source_revision']==D and not m['actual_child_data']and m['production_changes']==[];assert m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and m['renderer']=='mobile'and m['display']=='Windows';assert len(m['states'])==(17 if case['raw_exit_code']==1 else 18)
 assert all(v['before_ready']for v in m['bindings'])and m['seed']['quality']=='speedy'and m['seed']['day_one_active']is False and m['seed']['custom_fish']==m['seed']['custom_friends']==[] and m['seed']['companion']==''
 for c in m['final_snapshot']['candidate_comparisons']:
  assert c['equal']and c['before']==c['after']and c['before']['source_script']=='res://scripts/arena/fairy_conservatory_handoff_2d.gd'
 assert m['source_route_status']=='FAIL_SOURCE_RETURN_CONTRACT'and len(m['source_route_failures'])==1
 post=next(v['snapshot']for v in m['states']if v['id']=='07_back_source_failure');assert post['game']=='level2'and post['phase']=='promenade'and post['galaxy_return_flags']['galaxy_instance_alive']and post['galaxy_return_flags']['fairy_conservatory']
 if case['raw_exit_code']==0:
  assert res['exit_code']==0 and m['observer_status']=='PASS'and not m['errors']and all(v['pass']for v in m['checks']);assert all((a/n).read_bytes()==(P/n).read_bytes()for n in ['base_capture.gd','capture_entry.gd','capture_fairy.gd','capture_skyway.gd','skyway_reuse.gd'])
  before=next(v['snapshot']for v in m['states']if v['id']=='03_hall_camera_settled')['hall'];after=next(v['snapshot']for v in m['states']if v['id']=='05_direct_back_hall')['hall'];assert before['layer_id']==after['layer_id']and before['controller_id']==after['controller_id']and abs(before['view_left_art']-after['view_left_art'])<.0011
 else:assert case['case']=='attempt1_z_only_1280'and m['errors']==['original direct Skyway Back resumes same cached hall']
 if case['case'].startswith('attempt3_cover'):
  finals+=1;checks+=len(m['checks']);compares+=len(m['final_snapshot']['candidate_comparisons'])
assert finals==2 and checks==52 and compares==4
cov=rd(P/'BACKGROUND_COVERAGE.json');assert not cov['full_native_background_quality_accepted']and not cov['source_pixels_modified']
for row in cov['observations']:
 assert row['tile_seams_geometrically_abut']and not row['source_native_coverage_policy_accepted'];l,t,r,b=row['native_bounds'];w,h=row['native_viewport'];assert l<=.001 and t<=.001 and r>=w-.001 and b>=h-.001
 if w==1600:assert 1637<row['effective_visible_source_extent'][1]<1639
for row in rd(P/'LIFECYCLE.json')['private_synthetic_profiles']:assert row['source_unknown_key_preserved']and not row['child_drawings_seeded_or_copied']and row['quality']=='speedy'
for row in rd(P/'SOURCE_BINDINGS.json')['functions']:
 raw=git('show',D+':'+row['path']);ls=raw.decode('utf-8').splitlines(keepends=True);body=''.join(ls[row['start_line']-1:row['end_line']]).encode();assert sha(raw)==row['file_sha256']and sha(body)==row['body_sha256']and body.decode()==row['body']
for row in rd(P/'SOURCE_LINEAGE.json')['observer_derived_files']:assert sha(git('show',row['source_revision']+':'+row['source_path']))==row['source_sha256']and sha((P/row['path']).read_bytes())==row['candidate_sha256']
assert rd(P/'SOURCE_LINEAGE.json')['candidate_sha256']==sha((P/'skyway_reuse.gd').read_bytes());code=(P/'skyway_reuse.gd').read_text(encoding='utf-8');assert 'backdrop.z_index = -30'in code and 'tile.scale = Vector2.ONE * scale_value'in code and 'tile.position = center +'in code
assert not re.search(r'\btexture\s*=(?!=)',code)
for forbidden in ['probe_tap','_teardown','_start_galaxy','m.game','Engine.time_scale','set_script']:assert forbidden not in code
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 before=rd(O/n);after=rd(P/n)
 for k in before:
  if k not in ['revision','phase','publication']:assert before[k]==after[k],(n,k)
 assert after['skyway_art_reuse']['accepted_removed']==0 and after['skyway_art_reuse']['known_roles']==243
for n in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert (P/n).read_bytes()==(O/n).read_bytes()
rv=rd(P/'REVIEW.json');assert len(rv['ten_axes'])==10 and len(rv['direct_views'])==10 and sum(v['classification']=='BOUNDED_COVER_CANDIDATE'for v in rv['direct_views'])==6 and not rv['approved']and not rv['production_adoption']and not rv['full_context_review_complete']
for row in rv['direct_views']:assert sha((P/row['path']).read_bytes())==row['sha256']
for row in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:raw=git('show',row['revision']+':'+row['path']);assert sha(raw)==row['sha256']and len(raw)==row['bytes']
cur=rd(H/'CURRENT.json');assert cur['current_tally']=='r70_skyway_art_reuse/tally.json'and not cur['mission_complete']
allowed={'design/audit_impacts/flat-vector-skyway-art-reuse-20261015.json','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md','docs/handoffs/codex_flat_vector_art_2026-10-07/README.md','docs/handoffs/codex_flat_vector_art_2026-10-07/CURRENT.json'}
for path in set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()):assert path in allowed or path.startswith(P.relative_to(R).as_posix()+'/'),path
base=json.loads((H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json').read_text(encoding='utf-8'));W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');assert len(base['runtime_raw_hashes'])==4420 and all(sha((W/k).read_bytes())==v for k,v in base['runtime_raw_hashes'].items());side={}
for root,dirs,files in os.walk(W):
 dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
 for name in files:
  f=Path(root)/name
  if f.suffix in {'.uid','.import'}:side[f.relative_to(W).as_posix()]=sha(f.read_bytes())
assert side==base['sidecars']and len(side)==4041
normal=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
for suffix,digest in base['normal_save_hashes'].items():
 f=Path(str(normal)+suffix);assert (sha(f.read_bytes())if f.is_file()else'absent')==digest
print('R70_EVIDENCE_PASS;2covercases52checks/4exactsignatures;89native36bounded53excluded;source art/Back FAIL and acceptance open;0acceptedremoved')
