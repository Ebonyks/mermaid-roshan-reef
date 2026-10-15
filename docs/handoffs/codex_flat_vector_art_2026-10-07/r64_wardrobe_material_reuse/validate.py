"""Validate R64 candidate/control/failure evidence without promoting art or frozen historical status."""
from pathlib import Path
import json,hashlib,subprocess,io,re,datetime
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r63_wardrobe_context';B='d7703fef32f32c4e2727f43eaecef5ff73d8cdce';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
index=rd(P/'CAPTURE_INDEX.json');summary=rd(P/'SUMMARY.json');frames={(x['case'],x['id']):x for x in index['frames']};assert len(frames)==402 and len(index['cases'])==8
counts={'native':0,'bounded':0,'excluded':0};candidate_checks=control_checks=0;profiles=set();candidate_states=control_states=0;launch_times=[]
for case in index['cases']:
 folder=P/'native'/case['case'];m=rd(folder/'capture_manifest.json');launch=rd(folder/'LAUNCH.json');result=rd(folder/'RESULT.json');candidate=m['candidate_enabled'];failed=result['exit_code']!=0;adjunct=launch['early_close_adjunct'];launch_times.append(launch['started_at_utc'])
 assert case['manifest_sha256']==sha((folder/'capture_manifest.json').read_bytes()) and result['log_sha256']==sha((folder/'engine.log').read_bytes())
 assert m['source_revision']==D and m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079' and m['renderer']=='mobile' and m['display']=='Windows' and m['time_scale']==1 and m['quality_requested']=='speedy' and not m['actual_child_data'] and not m['normal_route_proved']
 assert candidate==launch['candidate'] and m['fairy_unlocked_profile']==launch['fairy_unlocked_profile']==m['seed']['fairyskin'] and m['seed']['skin']=='classic'
 assert not result['timed_out'] and not result['source_byte_changes'] and not launch['source_before_byte_changes'] and not result['script_or_shader_errors'] and result['fixture_dependencies_unchanged'] and result['sidecars_exact'] and result['sidecar_before_count']==result['sidecar_after_count']==4041
 assert result['normal_before']==result['normal_after']==m['normal_before']==m['normal_after'] and len(result['normal_before'])==8
 for name,digest in launch['fixture_dependencies'].items():assert sha((folder/name).read_bytes())==digest
 if failed:
  assert len(m['states'])==54 and len(m['checks'])==49 and len([x for x in m['checks']if not x['pass']])==4
  assert all(x['pass']for x in m['checks']if not x['label'].startswith('R64 '))
  if candidate:assert all(x['label'].startswith('R64 declared heading disposition')for x in m['checks']if not x['pass'])
  else:assert all(x['label'].startswith('R64 declared material states')for x in m['checks']if not x['pass'])
 else:
  assert all(x['pass']for x in m['checks'])
  assert (folder/'base_capture.gd').read_bytes()==(P/'base_capture.gd').read_bytes() and (folder/'capture_material.gd').read_bytes()==(P/'capture_material.gd').read_bytes()
  if candidate:
   candidate_checks+=len(m['checks']);assert (folder/'wardrobe_material_candidate.gd').read_bytes()==(P/'wardrobe_material_candidate.gd').read_bytes()
   if not adjunct:profiles.add((m['fairy_unlocked_profile'],m['aspect'][0]));assert len(m['checks'])==49 and len(m['states'])==54
   else:assert len(m['checks'])==23 and len(m['states'])==24
  else:control_checks+=len(m['checks']);assert len(m['checks'])==49
 for st in m['states']:
  x=frames[(case['case'],st['id'])];raw=(P/x['path']).read_bytes();assert sha(raw)==x['sha256']==st['sha256'];im=Image.open(io.BytesIO(raw));im.load();assert list(im.size)==m['aspect']==x['dimensions'] and sha(im.tobytes())==x['pixel_sha256']
  counts['native']+=1;excluded=failed or not candidate or st['id']in ['main_hall_checkpoint','fresh_main_checkpoint'];counts['excluded'if excluded else'bounded']+=1;assert x['classification'].startswith('EXCLUDED')==excluded
  snap=st['snapshot'];assert snap['quality']=='speedy' and snap['time_scale']==1 and snap['r64_candidate_enabled']==candidate
  if not failed:
   assert snap['r64_owner_script']==('res://export/flat_vector_r64/wardrobe_material_candidate.gd'if candidate else'res://scripts/wardrobe_ui.gd')
   mat=snap['r64_materials']
   if mat['active_legacy_picker']:
    candidate_states+=int(candidate);control_states+=int(not candidate);expected='StyleBoxTexture'if candidate else'StyleBoxFlat';assert len(mat['panels'])==2 and len(mat['buttons'])==5 and len(mat['ornaments'])==(0 if candidate else 5)
    assert all(z['style']['class']==expected for z in mat['panels']) and all(z['class']==expected for b in mat['buttons']for z in b['styles'].values()) and all(len(b['styles'])==6 and b['pressed_connections']>=1 for b in mat['buttons'])
    if candidate:assert mat['heading']['text']=='Pick your look!' and mat['heading']['size']=='(430.0, 64.0)' and mat['heading']['line_count']==mat['heading']['visible_line_count']==1 and mat['heading']['font_size']==42
 if not failed and not adjunct:
  byid={x['id']:x['snapshot']for x in m['states']};initial=byid['initial_caption_settled'];choice=byid['fairy_choice_early'];final=byid['final_royal_bedroom_classic'];assert initial['skin']=='classic' and initial['room']=='royal_bedroom' and len(initial['looks'])==3
  assert choice['skin']==('fairy'if m['fairy_unlocked_profile']else'classic') and byid['fairy_choice_settled']['feedback']['burst_count']==0
  assert byid['reload_caption_settled']['skin']==byid['reload_caption_settled']['disk']['skin']=='huluu' and byid['fashion_child_entry_only']['fashion_child'] and final['skin']==final['disk']['skin']=='classic' and final['disk']['fairyskin']==m['fairy_unlocked_profile']
assert counts=={'native':402,'bounded':231,'excluded':171} and (candidate_checks,control_checks,candidate_states,control_states)==(219,49,131,30) and profiles=={(False,1280),(False,1600),(True,1280),(True,1600)}
assert summary['retained_bounded']==5328+231==5559 and summary['retained_excluded']==2657+171==2828 and summary['retained_native_events']==7985+402==8387
marks=rd(P/'LIFECYCLE.json')['early_close_marks'];assert len(marks)==2 and all(x['source_tween_valid_before']and not x['source_tween_valid_after']and not x['old_burst_valid_after']and x['source_closed']and not x['wardrobe_block_after']for x in marks)
assert (P/'base_capture.gd').read_bytes()==git('show',B+':'+(O/'capture_wardrobe.gd').relative_to(R).as_posix())
source=(P/'wardrobe_material_candidate.gd').read_text(encoding='utf-8-sig');methods=set(re.findall(r'^func ([A-Za-z_0-9]+)\(',source,re.M));assert methods=={'_init','_card_style','_wardrobe_refresh','_paint_picker_buttons','_open_wardrobe'} and 'super._open_wardrobe()'in source and 'super._wardrobe_refresh()'in source and 'painted.region_rect = Rect2(9, 8, 223, 224)'in source
art=git('show',D+':assets/fashion/skin_engine_v2/ui/wardrobe_card.png');im=Image.open(io.BytesIO(art));assert im.getchannel('A').getbbox()==(9,8,232,232) and rd(P/'CANDIDATE_V1_FAILURE_V2_REPAIR.json')['preserved_all_alpha_positive_source_pixels']
assert rd(P/'REUSE_PROVENANCE.json')['candidate_script_sha256']==sha((P/'wardrobe_material_candidate.gd').read_bytes()) and not rd(P/'REUSE_PROVENANCE.json')['new_generation_calls']
refs=rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files'];assert len(refs)==65
for x in refs:
 raw=git('show',x['revision']+':'+x['path']);assert len(raw)==x['bytes'] and sha(raw)==x['sha256'] and x['http_status']==200
assert max(x['checked_at_utc']for x in rd(P/'SOURCE_REFERENCES.json')['files'])<min(launch_times)
for n in ['CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert(P/n).read_bytes()==(O/n).read_bytes()
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n)
 for k,v in old.items():
  if k not in ['revision','phase','publication','change_record','current_ci_snapshot']:assert d[k]==v,(n,k)
 cur=d['wardrobe_material_reuse'];assert cur['known_roles']==240 and cur['families']==32 and cur['catalogue_partial']==cur['catalogue_without_current_slice']==88 and cur['catalogue_complete']==cur['accepted_removed']==cur['new_alias_credits']==0 and not cur['mission_complete']
review=rd(P/'REVIEW.json');assert len(review['direct_passing_views'])==12 and len(review['direct_failed_v1_views'])==1 and review['human_review']is None and not review['creative_acceptance']
for role in review['per_piece_comparisons']:assert set(role['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'} and role['owner']is None and not role['accepted_removed']
assert rd(H/'CURRENT.json')['current_tally']=='r64_wardrobe_material_reuse/tally.json'
changes=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();assert not any(x.startswith(('assets/','scripts/','scenes/','shaders/','.codex/','.claude/','.github/'))or x in ['project.godot','AGENTS.md','SECURITY.md','ASSET_LICENSES.md']for x in changes)
assert summary['generation_calls']==summary['new_drawing_samples']==summary['approved']==summary['integrated']==summary['runtime_verified_replacements']==summary['accepted_removed']==0 and summary['all_game_artwork_total']is None and not summary['mission_complete']
print('R64_VALIDATION_PASS:402PNG/pixelhashes;219candidate+49controlchecks;131candidate30controlmaterialstates;231bounded171excluded;65refs/frozen/history/unions/acceptance preserved')
