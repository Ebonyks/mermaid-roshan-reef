from pathlib import Path
import subprocess,hashlib,importlib.util,re,math,json
from PIL import Image
from evidence_rules import validate_lane,validate_card
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r79_promenade_slide_ownership';B='fab29b2b25db8bfc732cda623190f32c5edd9d41';D='dd799b2d43871b29d1d6e0503646308a194dad1e'
sp=importlib.util.spec_from_file_location('bounded80validate',P/'bounded_json.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
s=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');clar=rd(P/'SCOPE_CLARIFICATION.json');actual=rd(P/'INPUT_OUTCOMES.json');geom=rd(P/'CANDIDATE_GEOMETRY.json');sample=rd(P/'CANDIDATE_SAMPLE.json')
for row in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 b=git('show',row['revision']+':'+row['path']);assert len(b)==row['bytes']and sha(b)==row['sha256'],row['path']
assert len(idx['captures'])==61 and len(idx['cases'])==2 and sum(x['bounded_original_source']for x in idx['captures'])==39 and sum(x['nonruntime_candidate']for x in idx['captures'])==18
checks=0;allframes=[];alltrials=[]
for case in idx['cases']:
 folder=P/case['path'];d=rd(folder/'capture_manifest.json');res=rd(folder/'RESULT.json');launch=rd(folder/'LAUNCH.json');script=(folder/'capture_entry.gd').read_bytes();raw_log=(folder/'engine.log').read_bytes();assert sha(script)==launch['fixture_sha256']==clar['before_fixture_sha256']and res['fixture_dependency_unchanged']and sha(raw_log)==res['log_sha256']
 assert res['exit_code']==0 and not res['timed_out']and not res['script_or_shader_errors']and not res['source_byte_changes']and res['sidecars_exact']and res['sidecar_before_count']==4088 and res['sidecar_after_count']==4088 and res['normal_before']==res['normal_after']and len(res['normal_before'])==11
 assert d['observer_status']=='PASS'and d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and d['renderer']=='mobile'and d['time_scale']==1.0 and not d['errors']and d['normal_before']==d['normal_after']and len(d['normal_before'])==11 and d['production_changes']==[]
 assert d['scope']==clar['inherited_caption']and script.decode().count(clar['inherited_caption'])==1 and script.decode().replace(clar['inherited_caption'],clar['corrected_caption'],1)==(P/'capture_entry.gd').read_text(encoding='utf-8')
 c=next(x for x in clar['cases']if x['case']==folder.name);assert c['raw_manifest_sha256']==sha((folder/'capture_manifest.json').read_bytes())and c['executed_fixture_sha256']==sha(script)
 checks+=len(d['checks']);assert len(d['checks'])==42 and all(x['pass']for x in d['checks']);seen=set()
 for f in d['states']:
  path=folder/f['path'];raw=path.read_bytes();assert sha(raw)==f['sha256'];im=Image.open(path);assert list(im.size)==f['dimensions']==d['aspect']and im.width in [1280,1600]and im.height==720 and f['id']not in seen;seen.add(f['id']);snap=f['snapshot'];validate_lane(snap['mode'],f['classification']);allframes.append(f)
  if f['classification']!='EXCLUDED_BOOTSTRAP_CONTROL':
   w=snap['world'];assert snap['quality']=='speedy'and w['game']=='level2'and w['phase']=='promenade'and w['wall_pics_count']==0 and not w['legacy_lagoon_constructed']and w['promenade_constructed']
  if snap['mode']=='LOCAL_NONRUNTIME_STAR_REUSE':
   assert f['classification']=='EXCLUDED_NONRUNTIME_PAINTED_CUE_PROTOTYPE'and len(snap['candidate'])==3
   for row in snap['candidate']:validate_card(row)
  else:assert snap['candidate']==[]
 assert len(d['cue_trials'])==9;alltrials.extend(d['cue_trials']);assert {x['mode']for x in d['cue_trials']}=={'ORIGINAL_SOURCE','LOCAL_NONRUNTIME_STAR_REUSE'}
 for toy in ['slide','swing','seesaw']:
  source=[x for x in d['cue_trials']if x['mode']=='ORIGINAL_SOURCE'and x['consumer']==toy];candidate=[x for x in d['cue_trials']if x['mode']=='LOCAL_NONRUNTIME_STAR_REUSE'and x['consumer']==toy];assert len(source)==2 and {x['part']for x in source}=={'center','tip'}and len(candidate)==1 and candidate[0]['source_controller_unchanged']
  for t in source:
   expected=t['part']=='tip'or toy=='seesaw';assert t['actual_input']and(t['after']['play']['kind']==toy)==expected
   if not expected:assert t['after']['focus']==''and t['after']['walk_goal']!='<null>'
  assert candidate[0]['actual_input']and candidate[0]['after']['play']['kind']==toy
assert checks==84 and len(alltrials)==18 and actual['source_trials']==12 and actual['source_activations']==8 and actual['source_glow_center_defocus_walk']==4 and actual['source_arrow_tip_activations']==6 and actual['source_seesaw_center_activations']==2 and actual['prototype_center_activations']==6 and not actual['actual_child_behavior_verified']
assert len(geom['measurements'])==54 and geom['source_sha256']==sample['source']['sha256']=='3cc5d5cbc5d6e0df0540cdc00ef557b0c7ed6e566331035c4e75d5d971ef3b98'
for row in geom['measurements']:
 validate_card(row);computed=max(math.dist(p,row['equipment_hit_center'])for p in row['native_corners']);assert abs(computed-row['farthest_card_corner_distance'])<.001
assert geom['minimum_card_to_hit_boundary_margin_px']>17 and not geom['production_fallbacks_retired']and not geom['runtime_verified_replacement']
assert sample['sample_id']=='FV-CAND-R80-STAR-01'and sample['role_id']=='FVR-5344465CE503'and sample['state']=='NONRUNTIME_REUSE_SAMPLE_AWAITING_NEW_USE_REVIEW'and not sample['approved']and not sample['integrated']and not sample['runtime_verified_replacement']
for name,key in [('FIXTURE_SYNTAX_GATES_EXECUTED.json','before_fixture_sha256'),('FIXTURE_SYNTAX_GATES.json','after_fixture_sha256')]:
 g=rd(P/name);assert g['status']=='PASS_BEFORE_NATIVE'and all(x['exit_code']==0 for x in g['checks'])and g['fixture_files'][0]['sha256']==clar[key]
assert sha((P/'capture_entry.gd').read_bytes())==clar['after_fixture_sha256']and clar['new_native_executions']==0 and clar['raw_launcher_caption_qualification']
code=(P/'capture_entry.gd').read_text();assert not re.search(r'\bm\.(game|g|quality|intro_active|first_session|day_one_active|save_data|position)\s*=(?!=)',code)and'Engine.time_scale ='not in code and'ProjectSettings.save('not in code
assert len(rd(P/'REVIEW.json')['axes'])==10 and not rd(P/'REVIEW.json')['mission_complete']and rd(P/'REVIEW.json')['current_role_samples_awaiting_review']==1
assert s['known_roles']==263 and s['known_families']==35 and s['new_roles']==0 and s['new_families']==0 and s['supplemental_partial_roles']==39 and s['existing_partial_roles']==75 and s['existing_partial_families']==15
assert s['retained_bounded']==6451 and s['retained_excluded']==3528 and s['retained_native_events']==9979 and s['new_native_frames']==61 and s['new_bounded_contexts']==39 and s['new_excluded_diagnostics']==22
assert s['catalogue_partial']==92 and s['catalogue_without_current_slice']==84 and s['catalogue_complete']==0 and s['new_reuse_samples']==1 and s['current_role_samples_awaiting_review']==1 and s['samples_awaiting_review_global']is None
for k in ['approved','integrated','runtime_verified_replacements','accepted_removed','generation_calls','new_drawing_samples','new_runtime_assets','new_alias_credits']:assert s[k]==0,k
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert s[k]is None,k
assert not s['allcaller_closure']and not s['global_unreachability_proved']and not s['mission_complete']and not s['reuse_ready']and s['drawing_required']is None and s['production_cue_still_flat']
allowed={'revision','phase','current_effective_summary','publication'}
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/name);new=rd(P/name);assert all(new[k]==v for k,v in old.items()if k not in allowed),name
 assert new['playground_cue_reuse']==s and new['inherited_r79_reference_base']['revision']==B
for name in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:
 old=rd(O/name);new=rd(P/name);assert all(new[k]==v for k,v in old.items()),name
assert len(rd(P/'CURRENT_KNOWN_ROLE_UNION.json')['records'])==263 and rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')['supplemental_partial_records']==39
u=rd(P/'UNRESOLVED_VISIBLE_SCOPES.json');assert u['new_observation_scope_count']==1 and u['all_game_unresolved_scope_total']is None and u['new_observation_scopes'][0]['new_piece_count']==0
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix()),name
assert rd(P/'REPRODUCTION_CHECK.json')['all_byte_identical']and rd(P/'REPRODUCTION_CHECK.json')['derived_file_count']==7 and rd(P/'ANALYSIS_TESTS.json')['tests']==8 and rd(P/'ANALYSIS_TESTS.json')['exit_code']==0
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();allowed_doc={'audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/audit_impacts/flat-vector-playground-cue-reuse-20261016.json',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()};assert all(x in allowed_doc or x.startswith(P.relative_to(R).as_posix()+'/')for x in changed)
cur=rd(H/'CURRENT.json');assert cur['current_tally']==P.name+'/tally.json'and cur['current_known_role_union']==P.name+'/CURRENT_KNOWN_ROLE_UNION.json'and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval']is False
print('R80_VALIDATION_PASS 2cases84checks;61raw39source22excluded;12source+6candidateinputs;54containedcards;1reuseSample;263/35;frozen/history/source preserved;0production/acceptance;globalunknown')
