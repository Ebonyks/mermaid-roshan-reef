"""Validate exact R65 native evidence and additive history without granting art acceptance."""
from pathlib import Path
import json,hashlib,subprocess,io,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r64_wardrobe_material_reuse';B='6647c56cb0c05f0130557f022abf5d421b4cc871';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
index=rd(P/'CAPTURE_INDEX.json');summary=rd(P/'SUMMARY.json');frames={(x['case'],x['id']):x for x in index['frames']};assert len(frames)==304 and len(index['cases'])==6
counts={'native':0,'bounded':0,'excluded':0};candidate_checks=control_checks=0;profiles=set();candidate_states=control_states=0;launch_times=[];epochs=[];retired=[]
for case in index['cases']:
 folder=P/'native'/case['case'];m=rd(folder/'capture_manifest.json');launch=rd(folder/'LAUNCH.json');result=rd(folder/'RESULT.json');candidate=m['refined_enabled'];adjunct=launch['early_close_adjunct'];launch_times.append(launch['started_at_utc']);cache_by_epoch={}
 assert case['manifest_sha256']==sha((folder/'capture_manifest.json').read_bytes())and result['log_sha256']==sha((folder/'engine.log').read_bytes())
 assert m['source_revision']==D and m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'and m['renderer']=='mobile'and m['display']=='Windows'and m['time_scale']==1 and m['quality_requested']=='speedy'and not m['actual_child_data']and not m['normal_route_proved']
 assert candidate==launch['refined_candidate']and m['fairy_unlocked_profile']==launch['fairy_unlocked_profile']==m['seed']['fairyskin']and m['seed']['skin']=='classic'
 assert result['exit_code']==0 and not result['timed_out']and not result['source_byte_changes']and not launch['source_before_byte_changes']and not result['script_or_shader_errors']and result['fixture_dependencies_unchanged']and result['sidecars_exact']and result['sidecar_before_count']==result['sidecar_after_count']==4041
 assert result['normal_before']==result['normal_after']==m['normal_before']==m['normal_after']and len(result['normal_before'])==8 and all(x['pass']for x in m['checks'])and not m['errors']
 for name,digest in launch['fixture_dependencies'].items():assert sha((folder/name).read_bytes())==digest==sha((P/name).read_bytes())
 if candidate:
  candidate_checks+=len(m['checks'])
  if not adjunct:profiles.add((m['fairy_unlocked_profile'],m['aspect'][0]));assert len(m['checks'])==50 and len(m['states'])==56
  else:assert len(m['checks'])==25 and len(m['states'])==24
 else:control_checks+=len(m['checks']);assert len(m['checks'])==50 and len(m['states'])==56
 for st in m['states']:
  x=frames[(case['case'],st['id'])];raw=(P/x['path']).read_bytes();assert sha(raw)==x['sha256']==st['sha256'];im=Image.open(io.BytesIO(raw));im.load();assert list(im.size)==m['aspect']==x['dimensions']and sha(im.tobytes())==x['pixel_sha256']
  counts['native']+=1;excluded=not candidate or st['id']in ['main_hall_checkpoint','fresh_main_checkpoint'];counts['excluded'if excluded else'bounded']+=1;assert x['classification'].startswith('EXCLUDED')==excluded
  snap=st['snapshot'];assert snap['quality']=='speedy'and snap['time_scale']==1 and snap['r65_refined_enabled']==candidate
  assert snap['r64_owner_script']==('res://export/flat_vector_r65/wardrobe_cached_fit_candidate.gd'if candidate else'res://export/flat_vector_r65/wardrobe_previous_candidate.gd')
  mat=snap['r64_materials'];fit=snap['r65_fit']
  if fit['active']:
   candidate_states+=int(candidate);control_states+=int(not candidate);assert len(mat['panels'])==2 and len(fit['buttons'])==5 and not mat['ornaments']and mat['heading']['size']=='(430.0, 64.0)'and mat['heading']['line_count']==1
   for bt in fit['buttons']:
    assert len(bt['styles'])==6 and bt['pressed_connections']>=1 and all(z['class']==('StyleBoxEmpty'if candidate else'StyleBoxTexture')for z in bt['styles'].values())
    if bt['name'].startswith('WardrobeLook_'):assert bt['size']=='(480.0, 110.0)'and bt['portrait']['size']=='(96.0, 94.0)'and bt['portrait']['position']=='(10.0, 8.0)'
    if candidate:
     cache=snap['r65_cache'];assert cache['style_creations']==5 and len(set(cache['resource_ids'].values()))==5;key=cache['resource_ids']['empty'];cache_by_epoch.setdefault(key,cache['resource_ids']);assert cache_by_epoch[key]==cache['resource_ids']
     frame=bt['frame'];assert frame['behind_parent']and frame['mouse_filter']==2 and frame['position']=='(0.0, -7.0)'and frame['style']['class']=='StyleBoxTexture'and all(z['resource_id']==key for z in bt['styles'].values())and frame['style']['resource_id']==cache['resource_ids'][frame['mode']]
 if not adjunct:
  snapshots={x['id']:x['snapshot']for x in m['states']};assert snapshots['fairy_choice_early']['skin']==('fairy'if m['fairy_unlocked_profile']else'classic')and snapshots['fairy_choice_settled']['feedback']['burst_count']==0
  assert snapshots['reload_caption_settled']['skin']==snapshots['reload_caption_settled']['disk']['skin']=='huluu'and snapshots['fashion_child_entry_only']['fashion_child']and snapshots['final_royal_bedroom_classic']['skin']==snapshots['final_royal_bedroom_classic']['disk']['skin']=='classic'
 if candidate:epochs.extend(cache_by_epoch.values());retired.extend(m['r65_retired_owners'])
assert counts=={'native':304,'bounded':239,'excluded':65}and(candidate_checks,control_checks,candidate_states,control_states)==(225,50,139,32)and profiles=={(False,1280),(False,1600),(True,1280),(True,1600)}
assert len(epochs)==len(retired)==9 and all(not x['owner_valid_after_3frames']for x in retired)
marks=rd(P/'LIFECYCLE.json')['early_close_marks'];assert len(marks)==2 and all(len(x['owned_frame_ids'])==5 and not x['surviving_frame_ids_after_12frames']and x['source_tween_valid_before']and not x['source_tween_valid_after']and not x['old_burst_valid_after']and x['source_closed']and not x['wardrobe_block_after']for x in marks)
assert not rd(P/'MATERIAL_STATE_IDENTITY.json')['mode_gaps']
assert summary['retained_bounded']==5559+239==5798 and summary['retained_excluded']==2828+65==2893 and summary['retained_native_events']==8387+304==8691
assert(P/'base_capture.gd').read_bytes()==git('show',B+':'+(O/'base_capture.gd').relative_to(R).as_posix())and(P/'wardrobe_previous_candidate.gd').read_bytes()==git('show',B+':'+(O/'wardrobe_material_candidate.gd').relative_to(R).as_posix())
assert rd(P/'FIXTURE_LINEAGE.json')['current_source_refresh_preserved_except_declared_style_helper']and rd(P/'REUSE_PROVENANCE.json')['candidate_script_sha256']==sha((P/'wardrobe_cached_fit_candidate.gd').read_bytes())
art=git('show',D+':assets/fashion/skin_engine_v2/ui/wardrobe_card.png');assert Image.open(io.BytesIO(art)).getchannel('A').getbbox()==(9,8,232,232)
refs=rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files'];assert len(refs)==63
for x in refs:
 raw=git('show',x['revision']+':'+x['path']);assert len(raw)==x['bytes']and sha(raw)==x['sha256']and x['http_status']==200
assert max(x['checked_at_utc']for x in rd(P/'SOURCE_REFERENCES.json')['files'])<min(launch_times)
for n in ['CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert(P/n).read_bytes()==git('show',B+':'+(O/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n)
 for k,v in old.items():
  if k not in ['revision','phase','publication','change_record','current_ci_snapshot']:assert d[k]==v,(n,k)
 cur=d['wardrobe_cached_fit'];assert cur['known_roles']==240 and cur['families']==32 and cur['catalogue_partial']==cur['catalogue_without_current_slice']==88 and cur['catalogue_complete']==cur['accepted_removed']==cur['new_alias_credits']==0 and not cur['mission_complete']
review=rd(P/'REVIEW.json');assert len(review['direct_passing_views'])==12 and review['human_review']is None and not review['creative_acceptance']
for role in review['per_piece_comparisons']:assert set(role['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'}and role['owner']is None and not role['accepted_removed']
assert rd(H/'CURRENT.json')['current_tally']=='r65_wardrobe_cached_fit/tally.json'
changes=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();assert not any(x.startswith(('assets/','scripts/','scenes/','shaders/','.codex/','.claude/','.github/'))or x in ['project.godot','AGENTS.md','SECURITY.md','ASSET_LICENSES.md']for x in changes)
assert summary['generation_calls']==summary['new_drawing_samples']==summary['approved']==summary['integrated']==summary['runtime_verified_replacements']==summary['accepted_removed']==0 and summary['all_game_artwork_total']is None and not summary['mission_complete']
print('R65_VALIDATION_PASS:304PNG/pixelhashes;225candidate50R64controlchecks;139candidate32controlstates;9cacheepochs/ownerretirements/10earlycloseframes;239bounded65excluded;63refs/frozen/history/unions/acceptance preserved')
