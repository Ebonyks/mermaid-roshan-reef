from pathlib import Path
import json,hashlib,subprocess,importlib.util,re
from PIL import Image
from evidence_rules import validate_trial,validate_lane,SOURCE,CANDIDATE
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r81_touch_flash_ownership';B='2acd2c969faeb3fb61d3ff5bcf1540aadba6735b';D='dd799b2d43871b29d1d6e0503646308a194dad1e';sp=importlib.util.spec_from_file_location('b82validate',P/'bounded_json.py');A=importlib.util.module_from_spec(sp);sp.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
s=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');bind=rd(P/'SOURCE_BINDINGS.json');ref=bind['retained_current_owner_graph'];assert ref['revision']==B and sha(git('show',B+':'+ref['path']))==ref['sha256']and not ref['new_AST_scan_claimed']
for x in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 raw=git('show',x['revision']+':'+x['path']);assert sha(raw)==x['sha256']and len(raw)==x['bytes'],x['path']
assert len(idx['captures'])==39 and len(idx['cases'])==2 and sum(x['bounded_original_source']for x in idx['captures'])==19 and sum(x['nonruntime_candidate']for x in idx['captures'])==16
checks=0;source_trials=0;candidate_trials=0
for case in idx['cases']:
 folder=P/case['path'];d=rd(folder/'capture_manifest.json');res=rd(folder/'RESULT.json');launch=rd(folder/'LAUNCH.json');assert res['exit_code']==0 and not res['timed_out']and not res['script_or_shader_errors']and not res['source_byte_changes']and res['sidecars_exact']and res['sidecar_after_count']==4088 and res['normal_before']==res['normal_after']and len(res['normal_before'])==11 and res['fixture_dependency_unchanged']
 assert d['observer_status']=='PASS'and all(x['pass']for x in d['checks'])and not d['errors']and d['production_changes']==[]and d['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and d['renderer']=='mobile'and d['time_scale']==1.0
 assert sha((folder/'capture_entry.gd').read_bytes())==launch['fixture_sha256']==sha((P/'capture_entry.gd').read_bytes())and sha((folder/'engine.log').read_bytes())==res['log_sha256']and 'LOCAL_NONRUNTIME_PAINTED_RING'in launch['scope'];checks+=len(d['checks'])
 for f in d['states']:
  raw=(folder/f['path']).read_bytes();im=Image.open(folder/f['path']);assert sha(raw)==f['sha256']and list(im.size)==f['dimensions']==d['aspect'];snap=f['snapshot'];validate_lane(snap['mode'],f['classification'])
  if f['classification']!='EXCLUDED_BOOTSTRAP_CONTROL':assert snap['quality']=='speedy'and snap['world']['game']=='level2'and snap['world']['phase']=='promenade'and snap['touch']['owner_script']=='res://scripts/touch_ui.gd'
 for t in d['flash_trials']:
  validate_trial(t);source_trials+=t['mode']==SOURCE;candidate_trials+=t['mode']==CANDIDATE;ent=[x for x in d['flash_lifecycle']if x['event']=='child_entered_tree'and x['panel']['instance_id']==t['instance_id']];ex=[x for x in d['flash_lifecycle']if x['event']=='tree_exiting'and x['instance_id']==t['instance_id']];assert len(ent)==len(ex)==1 and ex[0]['ticks_msec']>ent[0]['ticks_msec']
assert checks==84 and source_trials==candidate_trials==4
assert rd(P/'FIXTURE_SYNTAX_GATES.json')['status']=='PASS_BEFORE_NATIVE'and all(x['exit_code']==0 for x in rd(P/'FIXTURE_SYNTAX_GATES.json')['checks'])and rd(P/'FIXTURE_SYNTAX_GATES.json')['fixture_files'][0]['sha256']==sha((P/'capture_entry.gd').read_bytes())
code=(P/'capture_entry.gd').read_text();assert 'Engine.time_scale ='not in code and not re.search(r'\bm\.(game|g|quality|position)\s*=(?!=)',code)and'create_tween('not in code
assert s['known_roles']==263 and s['known_families']==35 and s['existing_partial_roles']==76 and s['existing_partial_families']==15 and s['supplemental_partial_roles']==39 and s['new_roles']==s['new_families']==s['new_alias_credits']==0
assert(s['retained_bounded'],s['retained_excluded'],s['retained_native_events'])==(6489,3552,10041)and(s['catalogue_partial'],s['catalogue_without_current_slice'],s['catalogue_complete'])==(92,84,0)
assert s['new_reuse_samples']==s['current_role_samples_awaiting_review']==1 and s['samples_awaiting_review_global']is None and not s['reuse_ready']and s['drawing_required']is None and s['production_flat_flash_still_present']
for k in ['generation_calls','new_runtime_assets','approved','integrated','runtime_verified_replacements','accepted_removed','new_drawing_samples']:assert s[k]==0,k
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert s[k]is None,k
assert not s['mission_complete']and not s['allcaller_closure']and len(rd(P/'REVIEW.json')['axes'])==10 and not rd(P/'CANDIDATE_SAMPLE.json')['approved']and rd(P/'CANDIDATE_SAMPLE.json')['source_center_alpha']==0
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/name);new=rd(P/name);assert all(new[k]==v for k,v in old.items()if k not in {'revision','phase','current_effective_summary','publication'}),name;assert new['touch_flash_reuse']==s and new['inherited_r81_reference_base']['revision']==B
for name in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:
 old=rd(O/name);new=rd(P/name);assert all(new[k]==v for k,v in old.items()),name
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
licenses=(R/'ASSET_LICENSES.md').read_text(encoding='utf-8');old_license=git('show',B+':ASSET_LICENSES.md').decode();assert licenses.startswith(old_license)and licenses.count('## R82 TouchUI feedback audit derivatives')==1
for x in idx['captures']:assert licenses.count('`'+x['path']+'`')==1 and x['sha256']in licenses
assert len(rd(P/'CAPTURE_PROVENANCE.json')['files'])==39 and rd(P/'REPRODUCTION_CHECK.json')['all_byte_identical']and rd(P/'REPRODUCTION_CHECK.json')['derived_file_count']==7 and rd(P/'ANALYSIS_TESTS.json')['tests']==14
allowed={'ASSET_LICENSES.md','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md','design/audit_impacts/flat-vector-touch-flash-reuse-20261016.json',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix()};changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();assert all(x in allowed or x.startswith(P.relative_to(R).as_posix()+'/')for x in changed)
assert rd(H/'CURRENT.json')['current_tally']==P.name+'/tally.json'and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval']is False
print('R82_VALIDATION_PASS 2cases84checks39raw19source20excluded;4source4candidate;wholeRing/originalPanel/fade/free;1sample;263/35;76partial;39licenses;0production/acceptance;globalunknown')
