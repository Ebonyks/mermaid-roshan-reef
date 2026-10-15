"""Validate R63 original native input evidence, additive counters, explicit consumers and unchanged historical authority."""
from pathlib import Path
import json,hashlib,subprocess,re,io
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r62_catalogue_origin';B='db43af9e46f0b7f718225ffc03dd40206b8cc2de';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
summary=rd(P/'SUMMARY.json');index=rd(P/'CAPTURE_INDEX.json');case_map={x['case']:x for x in index['cases']};frame_map={(x['case'],x['id']):x for x in index['frames']};assert len(frame_map)==294
native=bounded=excluded=checks=0;profiles=set()
for case,row in case_map.items():
 folder=P/'native'/case;m=rd(folder/'capture_manifest.json');result=rd(folder/'RESULT.json');launch=rd(folder/'LAUNCH.json');failed=result['exit_code']!=0;adjunct='teardown' in case
 assert row['manifest_sha256']==sha((folder/'capture_manifest.json').read_bytes())
 assert m['source_revision']==D and m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079' and m['renderer']=='mobile' and m['display']=='Windows' and m['quality_requested']=='speedy' and m['time_scale']==1 and m['actual_child_data'] is False and m['normal_route_proved'] is False
 assert m['seed']['skin']=='classic' and m['seed']['fairyskin']==m['fairy_unlocked_profile']==launch['fairy_unlocked_profile']
 assert not result['timed_out'] and not result['source_byte_changes'] and not launch['source_before_byte_changes'] and not result['script_or_shader_errors'] and result['fixture_unchanged'] and result['normal_before']==result['normal_after']==m['normal_before']==m['normal_after']
 assert result['sidecar_before_count']==result['sidecar_after_count']==4041 and result['sidecars_exact'] and result['log_sha256']==sha((folder/'engine.log').read_bytes())
 if failed:
  assert case=='attempt1_wardrobe_locked_1280' and len([x for x in m['checks'] if not x['pass']])==3
 else:
  checks+=len(m['checks']);assert all(x['pass'] for x in m['checks'])
  if not adjunct:profiles.add((m['fairy_unlocked_profile'],m['aspect'][0]));assert len(m['checks'])==33 and len(m['states'])==54 and (folder/'fixture_source.gd').read_bytes()==(P/'capture_wardrobe.gd').read_bytes()
  else:assert len(m['checks'])==15 and len(m['states'])==24 and result['base_fixture_unchanged'] and (folder/'base_fixture_source.gd').read_bytes()==(P/'capture_wardrobe.gd').read_bytes()
 for st in m['states']:
  x=frame_map[(case,st['id'])];raw=(P/x['path']).read_bytes();assert sha(raw)==st['sha256']==x['sha256'];im=Image.open(io.BytesIO(raw));im.load();assert sha(im.tobytes())==x['pixel_sha256'] and list(im.size)==m['aspect'];native+=1
  ex=failed or st['id'] in ['main_hall_checkpoint','fresh_main_checkpoint'];excluded+=int(ex);bounded+=int(not ex);assert x['classification'].startswith('EXCLUDED')==ex
  snap=st['snapshot'];assert snap['quality']=='speedy' and snap['time_scale']==1
 assert any(x['type']=='touch' for x in m['events']) and any(x['type']=='ORIGINAL_HALL_DOOR' and x['room']=='family_gallery' for x in m['route_events']) and any(x['type']=='ORIGINAL_GALLERY_DOOR' and x['room']=='royal_bedroom' for x in m['route_events'])
 if not failed and not adjunct:
  byid={x['id']:x['snapshot'] for x in m['states']};initial=byid['initial_caption_settled'];choice=byid['fairy_choice_early'];settled=byid['fairy_choice_settled'];final=byid['final_royal_bedroom_classic']
  assert initial['room']=='royal_bedroom' and initial['navigation_top']=='wardrobe' and len(initial['looks'])==3 and initial['skin']=='classic'
  fairy=next(x for x in initial['looks'] if x['skin']=='fairy');assert fairy['locked']==(not m['fairy_unlocked_profile']) and fairy['style']=='StyleBoxFlat' and len(fairy['callbacks'])>=1
  assert choice['skin']==('fairy' if m['fairy_unlocked_profile'] else 'classic') and settled['feedback']['burst_count']==0
  item=next(x for x in initial['room_items'] if x['id']=='shell_wardrobe');assert item['source_object_id']=='royal_bedroom:shell_wardrobe' and item['roleplay_action']=='dress_up' and item['native_pack']==''
  assert byid['reload_caption_settled']['skin']=='huluu' and byid['reload_caption_settled']['disk']['skin']=='huluu' and final['skin']==final['disk']['skin']=='classic' and final['disk']['fairyskin']==m['fairy_unlocked_profile']
  assert byid['fashion_child_entry_only']['fashion_child']
assert profiles=={(False,1280),(False,1600),(True,1280),(True,1600)} and (native,bounded,excluded,checks)==(294,231,63,147)
assert summary['retained_bounded']==5097+bounded==5328 and summary['retained_excluded']==2594+excluded==2657 and summary['retained_native_events']==7691+native==7985
marks=rd(P/'LIFECYCLE.json')['early_close_marks'];assert len(marks)==2 and all(x['source_tween_valid_before'] and not x['source_tween_valid_after'] and not x['old_burst_valid_after'] and x['source_closed'] and not x['wardrobe_block_after'] for x in marks)
refs=rd(P/'DELIVERY_SOURCE_REFERENCES.json');assert len(refs['files'])==70
for x in refs['files']:
 b=git('show',x['revision']+':'+x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256'] and x['http_status']==200
for x in rd(P/'SOURCE_CALLER_BINDINGS.json')['functions']:
 b=git('show',D+':'+x['path']);assert sha(b)==x['source_sha256'] and sha(x['body'].encode())==x['body_sha256'] and x['body'] in b.decode('utf-8-sig')
orig=rd(O/'CATALOGUE_ORIGINS.json');current=json.loads(git('show',D+':design/reference/games.json'));bindings=rd(P/'CATALOGUE_BINDINGS.json')['bindings'];assert {x['id'] for x in bindings}=={'game.wardrobe','game.pearl_castle'}
for x in bindings:
 assert x['original_origin']==next(y for y in orig['rows'] if y['id']==x['id']);assert x['current_catalogue_row']==next(y for y in current['games'] if y['id']==x['id'][5:]);assert x['accepted_removed']==0 and not x['complete']
u=rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json');old=rd(O/'CURRENT_CATALOGUE_CONTEXT_UNION.json');assert set(u['current_partial_ids'])==set(old['current_partial_ids'])|{'game.wardrobe','game.pearl_castle'} and len(u['current_partial_ids'])==u['current_partial_count']==88 and u['without_current_slice_count']==88 and u['complete_count']==0
assert set(u['current_partial_ids'])<=set(x['id'] for x in orig['rows']);assert (P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix()),n
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);prior=rd(O/n);assert d['wardrobe_context']['accepted_removed']==0 and d['wardrobe_context']['mission_complete'] is False and d['wardrobe_context']['known_roles']==240 and d['wardrobe_context']['families']==32 and d['wardrobe_context']['catalogue_partial']==88
 for k,v in prior.items():
  if k not in ['revision','phase','publication','change_record','current_ci_snapshot']:assert d[k]==v,(n,k)
 assert d['wardrobe_context']['new_native_files']==294 and d['wardrobe_context']['new_bounded_contexts']==231 and d['wardrobe_context']['new_excluded_diagnostics']==63
review=rd(P/'REVIEW.json');assert len(review['direct_passing_native_views'])==14 and len(review['excluded_reader_diagnostic_views'])==5 and review['human_review'] is None and review['owner'] is None
for row in review['role_comparisons']:assert set(row['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'} and row['count_credit']==0 and row['owner'] is None
base=(P/'capture_wardrobe.gd').read_text(encoding='utf-8-sig');assert not re.search(r'm\.(skin_id|fairy_skin_unlocked)\s*=(?!=)',base) and 'pressed.emit' not in base and not re.search(r'Engine\.time_scale\s*=(?!=)',base)
assert rd(H/'CURRENT.json')['current_tally']=='r63_wardrobe_context/tally.json'
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();assert not any(x.startswith(('scripts/','scenes/','assets/','shaders/','.codex/','.github/','.claude/')) or x in ['project.godot','AGENTS.md','SECURITY.md','ASSET_LICENSES.md'] for x in changed)
assert summary['accepted_removed']==summary['generation_calls']==summary['new_roles']==summary['new_families']==0 and summary['all_game_artwork_total'] is None and not summary['mission_complete']
print('R63_VALIDATION_PASS:294originalPNG/pixelhashes,5cases147checks,63excluded,70currentrefs,explicit2partialIDs88/88/0,frozen5/history/source/save/acceptance preserved')
