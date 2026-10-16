from pathlib import Path
import json,hashlib,subprocess,importlib.util,io,math,os,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r71_skyway_pointer';B='63b842887eb14d6b51bedb0b676afbe17b6453a7';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
sp=importlib.util.spec_from_file_location('b72validate',P/'bounded_json.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
x=rd(P/'SUMMARY.json');old=rd(O/'SUMMARY.json');assert x['native_cases']==7 and x['healthy_native_checks']==322 and x['bounded_control_cases']==2 and x['bounded_control_checks']==92 and x['distinct_reuse_crop_trials']==2 and x['new_native_frames']==142 and x['new_bounded_contexts']==40 and x['new_excluded_diagnostics']==102
assert x['retained_bounded']==old['retained_bounded']+40==6122 and x['retained_excluded']==old['retained_excluded']+102==3223 and x['retained_native_events']==old['retained_native_events']+142==9345
assert x['known_roles']==243 and x['families']==34 and x['catalogue_partial']==92 and x['catalogue_without_current_slice']==84 and x['catalogue_complete']==0 and x['rejected_reuse_candidates']==2 and not x['mission_complete']
for k in ['new_roles','new_families','new_alias_credits','generation_calls','new_drawing_samples','new_runtime_assets','approved','integrated','runtime_verified_replacements','accepted_removed','new_reuse_candidates_awaiting_review']:assert x[k]==0
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert x[k]is None
frames=rd(P/'PIXEL_EVIDENCE.json')['raw_frames'];assert len(frames)==len({v['path']for v in frames})==142
for row in frames:
 raw=(R/row['path']).read_bytes();im=Image.open(io.BytesIO(raw)).convert('RGBA');assert sha(raw)==row['sha256']and len(raw)==row['bytes']and list(im.size)==row['size']and sha(im.tobytes())==row['decoded_rgba_sha256'];assert im.convert('RGB').getextrema()!=((0,0),(0,0),(0,0))
 if row['classification'].startswith('BOUNDED_'):assert im.size in [(1280,720),(1600,720)]
checks=0;cycles=0;inputs=0;wrong_prebinding=0;corrected_prebinding=0
for case in x['cases']:
 d=P/'native'/case['case'];m=rd(d/'capture_manifest.json');res=rd(d/'RESULT.json');h=rd(d/'hint_cycles.json');launch=rd(d/'LAUNCH.json');assert sha((d/'capture_manifest.json').read_bytes())==case['manifest_sha256']and sha((d/'hint_cycles.json').read_bytes())==case['hint_sha256'];assert res['exit_code']==0 and not res['timed_out']and res['normal_before']==res['normal_after']==m['normal_before']==m['normal_after'];assert res['sidecars_exact']and res['sidecar_before_count']==res['sidecar_after_count']==4041 and not res['source_byte_changes']and res['fixture_dependencies_unchanged']and not res['script_or_shader_errors']and sha((d/'engine.log').read_bytes())==res['log_sha256']
 assert m['observer_status']=='PASS'and not m['errors']and all(v['pass']for v in m['checks'])and m['source_route_status']=='FAIL_SOURCE_RETURN_CONTRACT'and len(m['source_route_failures'])==1;checks+=len(m['checks'])
 assert m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and m['renderer']=='mobile'and m['display']=='Windows'and m['source_revision']==D and not m['actual_child_data']and m['production_changes']==[]
 assert m['seed']['quality']=='speedy'and m['seed']['custom_fish']==m['seed']['custom_friends']==[]and m['seed']['companion']==''and not m['seed']['day_one_active']and all(v['before_ready']for v in m['bindings'])
 for name,digest in launch['fixture_dependencies'].items():
  assert sha((d/name).read_bytes())==digest
  alternatives=[(P/name).read_bytes()]
  if name=='capture_pointer.gd':alternatives.extend((P/v).read_bytes() for v in ['capture_pointer_prebinding_v1.gd','capture_pointer_actual_binding_v2.gd'])
  if name=='pointer_registration.gd':alternatives.extend((P/v).read_bytes() for v in ['pointer_registration_forearm_rejected.gd','pointer_registration_imported_v2.gd'])
  assert (d/name).read_bytes()in alternatives,(case['case'],name)
 for key in ['candidate_comparisons','pointer_comparisons']:
  for row in m['final_snapshot'][key]:assert row['before']==row['after']
 for row in m['final_snapshot']['pointer_comparisons']:
  delta=row['declared_pointer_draw_delta'];before=delta['before'];after=delta['after'];assert before['id']==after['id']and before['position']==after['position']and before['z_index']==after['z_index']and before['visible']==after['visible'];assert before['texture_path']=='res://assets/castle/training/ghost_hand.png'
  if case['hand_variant'] in ['painted','lossless']:assert after['texture_path']==('' if case['hand_variant']=='lossless' else 'res://assets/characters/roshan_25d/roshan_gesture_b.png')and after['region_enabled']and after['region_rect']==[527,819,40 if case['case']=='attempt1_painted_1280'else 28,35]
  else:assert after['texture_path']==before['texture_path']and not after['region_enabled']and after['scale']==before['scale']
 before=next(v['snapshot']['hall']for v in m['states']if v['id']=='03_hall_camera_settled');after=next(v['snapshot']['hall']for v in m['states']if v['id']=='05_direct_back_hall');assert before['layer_id']==after['layer_id']and abs(before['view_left_art']-after['view_left_art'])<.0011
 if case['hand_variant']=='lossless':
  a=m['final_snapshot']['pointer_registration'];assert a['source_rgba_sha256']==a['texture_rgba_sha256']=='204f563328550f43268f7b98483f95bc27422b89cea98049a64c1afb1dbdefae' and a['original_png_sha256']=='59daf2a2efdbabba1a28bedfed5312805b4351627f0882704b11c4b6ca488ead' and not a['direct_png_export_ready'];assert 'will not work on export' in (d/'engine.log').read_text(encoding='utf-8')
 assert len(m['states'])==20 and len(h['cycles'])==4 and len(h['inputs'])==4
 for c in h['cycles']:
  cycles+=1;rows=c['samples'];assert (rows[-1]['phase']-rows[0]['phase'])*4>=math.tau and c['outside_count']==0 and c['inside_count']==len(rows)
  snap=next(v['snapshot']for v in m['states']if v.get('snapshot',{}).get('tip_state',{}).get('index')==c['index']and v['id'].startswith('07_'));wm=snap['candidate_visual_nodes'];wp=wm['world_position'];ws=wm['world_scale'];assert ws==[1,1]
  for q in rows:
   tip=[1,6.5]if case['hand_variant'] in ['painted','lossless']else[217,447];rx,ry,_,_=q['pointer_draw_rect'];lx=(rx+tip[0])*q['pointer_scale'][0];ly=(ry+tip[1])*q['pointer_scale'][1];a=q['pointer_rotation'];px=q['pointer_position'][0]+math.cos(a)*lx-math.sin(a)*ly;py=q['pointer_position'][1]+math.sin(a)*lx+math.cos(a)*ly;expected=[wp[0]+ws[0]*px,wp[1]+ws[1]*py];assert all(abs(a-b)<.002 for a,b in zip(expected,q['native_tip']))
   tx,ty,tw,th=q['target_rect'];nx,ny=q['native_tip'];assert q['inside']and tx<=nx<tx+tw and ty<=ny<ty+th
   base_y=(600,500,375,194)[q['index']]-(88 if q['state']=='butterfly_house'else 82);assert abs(q['pointer_position'][1]-(base_y+math.sin(q['phase']*4)*7))<.001
   if case['hand_variant'] in ['painted','lossless']:assert q['texture']['path']==('' if case['hand_variant']=='lossless' else 'res://assets/characters/roshan_25d/roshan_gesture_b.png')and q['pointer_region_enabled']and abs(a+math.pi/2)<1e-6
   else:assert q['texture']['path']=='res://assets/castle/training/ghost_hand.png'and not q['pointer_region_enabled']and abs(a)<1e-8
 for item in h['inputs']:
  inputs+=1;q=item['before'];assert q['inside'];point=q['native_tip'];assert any(e['type']=='floor_touch'and e['pressed']and all(abs(float(a)-b)<.001 for a,b in zip(re.findall(r'-?\d+(?:\.\d+)?',e['point']),point))for e in m['events'])
 for st in m['states']:
  if st['id']not in ['04_skyway_entry','04_reuse_visible','06_reentry_skyway_entry','06_reentry_reuse_visible']:continue
  q=st['snapshot']['tip_state'];assert q['texture']['path']=='res://assets/castle/training/ghost_hand.png'
  if case['hand_variant']=='painted'and case['case']!='attempt3_painted_1280':assert q['tip_region']==[1,6.5];wrong_prebinding+=1
  else:assert q['tip_region']==[217,447];corrected_prebinding+=1
assert checks==322 and cycles==28 and inputs==28 and wrong_prebinding==12 and corrected_prebinding==16
inspection=rd(P/'SOURCE_INSPECTION.json');assert inspection['exit_code']==0 and sha((P/'inspect_source.gd').read_bytes())==inspection['script_sha256']and sha((P/'source_inspection.png').read_bytes())==inspection['png_sha256']and not inspection['source_pixels_modified']
decode=rd(P/'decode_comparison.json');assert decode['exit_code']==0 and decode['no_source_pixels_modified'] and sha((P/'decode_comparison.png').read_bytes())==decode['png_sha256'] and sha((P/'compare_decode.gd').read_bytes())==decode['script_sha256'];assert decode['opaque_region_rgb_sample_count']==852 and 12<decode['opaque_region_rgb_mae_8bit']<13
imp=rd(P/'IMPORT_DECODE_FINDING.json');assert imp['normalized_lf_bytes_exact'] and not imp['current_initialized_bytes_exact'] and imp['settings']['compress/mode']==2
inv=rd(P/'REUSE_INVENTORY.json');assert inv['native_header']['width']==inv['native_header']['height']==1024 and inv['native_header']['frames']==1 and inv['native_header']['rgba_depth']==32
for row in inv['exact_sources']+rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 raw=git('show',row['revision']+':'+row['path']);assert sha(raw)==row['sha256']and len(raw)==row['bytes']
for row in rd(P/'SOURCE_BINDINGS.json')['functions']:
 raw=git('show',D+':'+row['path']);body=''.join(raw.decode('utf-8').splitlines(keepends=True)[row['start_line']-1:row['end_line']]).encode();assert sha(raw)==row['file_sha256']and sha(body)==row['body_sha256']and body.decode()==row['body']
caller=rd(P/'POINTER_CALLER_RECONCILIATION.json');assert caller['listed_paths']==382 and caller['scanned_text_paths']==316 and len(caller['literal_rows'])==20 and len({r['path']for r in caller['literal_rows']})==19 and sum('ghost_hand.png'in r['text']for r in caller['literal_rows'])==18
for row in caller['literal_rows']:
 raw=git('show',D+':'+row['path']);ls=raw.decode('utf-8').splitlines(keepends=True);a,b=row['body_lines'];assert sha(raw)==row['file_sha256']and ls[row['line']-1].rstrip()==row['text']and sha(''.join(ls[a-1:b]).encode())==row['body_sha256']
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 olddoc=rd(O/n);new=rd(P/n)
 for k in olddoc:
  if k not in ['revision','phase','publication']:assert olddoc[k]==new[k],(n,k)
 assert new['skyway_hand_reuse']['accepted_removed']==0 and new['skyway_hand_reuse']['rejected_reuse_candidates']==2
for n in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert (P/n).read_bytes()==(O/n).read_bytes()
rv=rd(P/'REVIEW.json');assert len(rv['direct_native_views'])==14 and len(rv['ten_axes'])==10 and not rv['new_reuse_approved']and rv['new_reuse_rejected']==2 and not rv['full_context_review_complete']and not rv['production_adoption']
for row in rv['direct_native_views']+[rv['source_inspection_view'],rv['source_decode_view']]:assert sha((P/row['path']).read_bytes())==row['sha256']
req=rd(P/'NEW_ART_REVIEW_REQUEST.json');assert req['status']=='AWAITING_EXPLICIT_OWNER_IMAGEGEN_EXPORT_AUTHORIZATION'and not req['owner_approval']and not req['generation_ready']and req['generation_calls']==0 and req['intended_takes']==1 and req['maximum_total_takes']==2 and len(req['inputs'])==2 and sha((P/'PROMPT.txt').read_bytes())==req['prompt_sha256']
for row in req['inputs']:
 raw=(R/row['path']).read_bytes()if row['revision']is None else git('show',row['revision']+':'+row['path']);assert sha(raw)==row['sha256']and len(raw)==row['bytes']
assert rd(P/'GENERATION_BLOCKED.json')['generation_calls']==0 and not rd(P/'GENERATION_BLOCKED.json')['workaround_or_cli_attempted']and not rd(P/'GENERATION_BLOCKED.json')['generated_outputs']
code=(P/'pointer_registration.gd').read_text(encoding='utf-8');assert 'pointer.region_enabled = true'in code and 'pointer.texture = texture'in code and 'pointer.offset ='in code
for forbidden in ['probe_tap','Engine.time_scale','m.game','_finish(','_teardown(','set_script','pointer.position =']:assert forbidden not in code
assert rd(H/'CURRENT.json')['current_tally']=='r72_skyway_hand_reuse/tally.json'
allowed={'design/audit_impacts/flat-vector-skyway-hand-reuse-20261015.json','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()}
for path in set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()):assert path in allowed or path.startswith(P.relative_to(R).as_posix()+'/'),path
base=rd(H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json');W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');assert len(base['runtime_raw_hashes'])==4420 and all(sha((W/p).read_bytes())==v for p,v in base['runtime_raw_hashes'].items());side={}
for root,dirs,files in os.walk(W):
 dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
 for name in files:
  f=Path(root)/name
  if f.suffix in {'.uid','.import'}:side[f.relative_to(W).as_posix()]=sha(f.read_bytes())
assert side==base['sidecars']and len(side)==4041
normal=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json'
for suffix,digest in base['normal_save_hashes'].items():
 f=Path(str(normal)+suffix);assert (sha(f.read_bytes())if f.is_file()else'absent')==digest
print('R72_EVIDENCE_PASS;7cases322checks28cycles;142raw40bounded102excluded;2reuse crops REJECTED;source gardenBack FAIL;0generation/production/removal;owner export authorization required')
