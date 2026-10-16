from pathlib import Path
import json,hashlib,subprocess,importlib.util,collections,io,math,re,os
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r70_skyway_art_reuse';B='872b45515e27df6b833ea4b697755186563ed904';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
sp=importlib.util.spec_from_file_location('bounded71v',P/'bounded_json.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
x=rd(P/'SUMMARY.json');old=rd(O/'SUMMARY.json');assert x['native_cases']==8 and x['final_cases']==4 and x['final_checks']==178 and x['new_native_frames']==163 and x['new_bounded_contexts']==86 and x['new_excluded_diagnostics']==77
assert x['retained_bounded']==old['retained_bounded']+86==6082 and x['retained_excluded']==old['retained_excluded']+77==3121 and x['retained_native_events']==old['retained_native_events']+163==9203
for k in ['generation_calls','new_drawing_samples','new_runtime_assets','approved','integrated','runtime_verified_replacements','accepted_removed','new_roles','new_families','new_alias_credits']:assert x[k]==0
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert x[k]is None
assert not x['mission_complete']and x['known_roles']==243 and x['families']==34 and x['catalogue_partial']==92 and x['catalogue_without_current_slice']==84 and x['catalogue_complete']==0
frames=rd(P/'PIXEL_EVIDENCE.json')['raw_frames'];assert len(frames)==len({f['path']for f in frames})==163
for row in frames:
 raw=(R/row['path']).read_bytes();im=Image.open(io.BytesIO(raw)).convert('RGBA');assert sha(raw)==row['sha256']and len(raw)==row['bytes']and list(im.size)==row['size']and sha(im.tobytes())==row['decoded_rgba_sha256'];assert im.convert('RGB').getextrema()!=((0,0),(0,0),(0,0))
 if row['classification'].startswith('BOUNDED_'):assert im.size in [(1280,720),(1600,720)]
finals={'attempt3_source_1280','attempt3_source_1600','attempt4_registered_1280','attempt4_registered_1600'};checks=0;total_cycles=0;source_misses=0;registered_taps=0
for case in x['cases']:
 d=P/'native'/case['case'];m=rd(d/'capture_manifest.json');res=rd(d/'RESULT.json');h=rd(d/'hint_cycles.json');launch=rd(d/'LAUNCH.json');assert sha((d/'capture_manifest.json').read_bytes())==case['manifest_sha256'];assert res['normal_before']==res['normal_after']==m['normal_before']==m['normal_after']and res['sidecars_exact']and res['sidecar_before_count']==res['sidecar_after_count']==4041 and not res['source_byte_changes']and res['fixture_dependencies_unchanged']and not res['script_or_shader_errors'];assert sha((d/'engine.log').read_bytes())==res['log_sha256']
 assert m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and m['renderer']=='mobile'and m['display']=='Windows'and m['source_revision']==D and not m['actual_child_data']and m['production_changes']==[]
 assert m['seed']['quality']=='speedy'and m['seed']['custom_fish']==m['seed']['custom_friends']==[]and not m['seed']['day_one_active']and m['seed']['companion']==''and all(v['before_ready']for v in m['bindings'])
 for name,digest in launch['fixture_dependencies'].items():assert sha((d/name).read_bytes())==digest
 if case['case']not in finals:continue
 checks+=len(m['checks']);assert m['observer_status']=='PASS'and not m['errors']and res['exit_code']==0 and all(v['pass']for v in m['checks']);assert m['source_route_status']=='FAIL_SOURCE_RETURN_CONTRACT'and len(m['source_route_failures'])==1
 for k in ['candidate_comparisons','pointer_comparisons']:
  for row in m['final_snapshot'][k]:assert row['before']==row['after']
 for name in launch['fixture_dependencies']:
  if name!='pointer_registration.gd':assert (d/name).read_bytes()==(P/name).read_bytes()
 if case['hint_variant']=='registered':assert (d/'pointer_registration.gd').read_bytes()==(P/'pointer_registration.gd').read_bytes()
 else:assert (d/'pointer_registration.gd').read_bytes()==(P/'pointer_registration_center_rejected.gd').read_bytes()
 before=next(s['snapshot']['hall']for s in m['states']if s['id']=='03_hall_camera_settled');after=next(s['snapshot']['hall']for s in m['states']if s['id']=='05_direct_back_hall');assert before['layer_id']==after['layer_id']and abs(before['view_left_art']-after['view_left_art'])<.0011
 assert len(h['cycles'])==4 and len(h['inputs'])==4
 for c in h['cycles']:
  total_cycles+=1;rows=c['samples'];span=rows[-1]['phase']-rows[0]['phase'];assert span*4>=math.tau and abs(span-c['phase_span_seconds'])<1e-8;outside=0
  for q in rows:
   px,py=q['native_tip'];tx,ty,tw,th=q['target_rect'];inside=tx<=px<tx+tw and ty<=py<ty+th;assert inside==q['inside'];outside+=not inside
   base_y=(600,500,375,194)[q['index']]-(88 if q['state']=='butterfly_house' else 82);assert abs(q['pointer_position'][1]-(base_y+math.sin(q['phase']*4)*7))<.001
   expected_offset=[0,0]if case['hint_variant']=='source'else[55.6666666667,492.3333333333];assert all(abs(a-b)<.0001 for a,b in zip(q['pointer_offset'],expected_offset))
  assert outside==c['outside_count']and len(rows)-outside==c['inside_count']
  if case['hint_variant']=='registered':assert outside==0
  elif c['index']<3:assert outside>0
 for item in h['inputs']:
  q=item['before'];point=q['native_tip'];assert any(e['type']=='floor_touch'and e['pressed']and all(abs(float(a)-b)<.001 for a,b in zip(re.findall(r'-?\d+(?:\.\d+)?',e['point']),point))for e in m['events'])
  if item['role']=='original_rendered_fingertip':assert not q['inside'];source_misses+=1
  if item['role']=='registered_rendered_fingertip':assert q['inside'];registered_taps+=1
assert checks==178 and total_cycles==16 and source_misses==registered_taps==6
raw=git('show',D+':assets/castle/training/ghost_hand.png');im=Image.open(io.BytesIO(raw)).convert('RGBA');mask=im.getchannel('A').point(lambda x:255 if x>=64 else 0);b=mask.getbbox();xs=[i for i in range(im.width)if im.getpixel((i,b[3]-1))[3]>=64];g=rd(P/'GEOMETRY.json');assert list(b)==g['alpha_bounds']and [(min(xs)+max(xs))/2,b[3]-1]==g['tip']==[217,447]and sha(raw)==g['source_sha256']
code=(P/'pointer_registration.gd').read_text(encoding='utf-8');assert 'pointer.offset = registered_offset'in code and not re.search(r'\btexture\s*=(?!=)',code)
for text in ['probe_tap','Engine.time_scale','m.game','_finish','_teardown','set_script','pointer.scale =','pointer.position =']:assert text not in code
clear=rd(P/'HERO_CLEARANCE.json')['rows'];assert len(clear)==24
for row in clear:
 if row['case'].startswith('attempt4'):assert row['nearest_alpha64_overlap_hand_source_pixel_count_max']==0
 if row['case'].startswith('attempt3_registered')and row['index']<3:assert row['nearest_alpha64_overlap_hand_source_pixel_count_max']>0
for row in rd(P/'SOURCE_BINDINGS.json')['functions']:
 raw=git('show',D+':'+row['path']);body=''.join(raw.decode('utf-8').splitlines(keepends=True)[row['start_line']-1:row['end_line']]).encode();assert sha(raw)==row['file_sha256']and sha(body)==row['body_sha256']and body.decode()==row['body']
for row in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:raw=git('show',row['revision']+':'+row['path']);assert sha(raw)==row['sha256']and len(raw)==row['bytes']
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 olddoc=rd(O/n);new=rd(P/n)
 for k in olddoc:
  if k not in ['revision','phase','publication']:assert olddoc[k]==new[k],(n,k)
 assert new['skyway_pointer']['accepted_removed']==0
for n in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert (P/n).read_bytes()==(O/n).read_bytes()
review=rd(P/'REVIEW.json');assert len(review['direct_views'])==8 and len(review['ten_axes'])==10 and not review['approved']and not review['full_context_review_complete']
for row in review['direct_views']:assert sha((P/row['path']).read_bytes())==row['sha256']
req=rd(P/'NEW_ART_REVIEW_REQUEST.json');assert req['generation_calls']==0 and req['maximum_total_takes']==2 and len(req['inputs'])==2 and req['status']=='DEFERRED_PENDING_APPROVED_GESTURE_REUSE_TRIAL_AND_EXPORT_AUTHORIZATION'and sha((P/'PROMPT.txt').read_bytes())==req['prompt_sha256']
for row in req['inputs']:raw=git('show',row['revision']+':'+row['path']);assert sha(raw)==row['sha256']and len(raw)==row['bytes']
blocked=rd(P/'GENERATION_BLOCKED.json');assert blocked['generation_calls']==0 and not blocked['generated_outputs']and not blocked['workaround_or_cli_attempted']
assert rd(H/'CURRENT.json')['current_tally']=='r71_skyway_pointer/tally.json'
allowed={'design/audit_impacts/flat-vector-skyway-pointer-20261015.json','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()}
for path in set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()):assert path in allowed or path.startswith(P.relative_to(R).as_posix()+'/'),path
base=rd(H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json');W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');assert len(base['runtime_raw_hashes'])==4420 and all(sha((W/k).read_bytes())==v for k,v in base['runtime_raw_hashes'].items());side={}
for root,dirs,files in os.walk(W):
 dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
 for name in files:
  f=Path(root)/name
  if f.suffix in {'.uid','.import'}:side[f.relative_to(W).as_posix()]=sha(f.read_bytes())
assert side==base['sidecars']and len(side)==4041
normal=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
for suffix,digest in base['normal_save_hashes'].items():
 f=Path(str(normal)+suffix);assert (sha(f.read_bytes())if f.is_file()else'absent')==digest
print('R71_EVIDENCE_PASS;4finalcases178checks;163native86bounded77excluded;6source misses/6candidate tip advances;0art generation/removal;export approval and all acceptance open')
