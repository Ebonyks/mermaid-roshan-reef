"""Validate R61 isolated native roles, source reuse and additive evidence; no acceptance claims."""
from pathlib import Path
import json,hashlib,subprocess,io
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r60_critter_saved_context';B='2db770402f9ec00c332b8def6a83aada9ccc6bd9';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
s=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');pre=rd(P/'CONTEXT_PREREQUISITE.json');assert(pre['files'],pre['bytes'])==(494,71899709) and pre['source_reference_sha256']==sha((P/'SOURCE_REFERENCES.json').read_bytes())
assert(s['new_native_files'],s['new_bounded_contexts'],s['new_excluded_diagnostics'],s['passing_checks'],s['passing_control_checks'],s['expected_negative_checks'])==(222,175,47,172,43,36)
assert s['retained_bounded']==4922+175 and s['retained_excluded']==2547+47 and s['retained_native_events']==7469+222
assert len(idx['states'])==len(list(P.rglob('*.png')))==222 and sum(x['lane']=='BOUNDED_NATIVE_CONTEXT'for x in idx['states'])==175
for x in idx['states']:
 b=(P/x['path']).read_bytes();assert sha(b)==x['sha256'];assert list(Image.open(io.BytesIO(b)).size)==x['size']
assert len(idx['jobs'])==6
bookcounts={'insect':0,'fixed':0,'legacy':0};checks={'insect':0,'fixed':0,'legacy':0};collisions=0
for job in idx['jobs']:
 c=rd(P/job['manifest']);q=rd(P/job['result']);launch=rd(P/job['launch']);mode=c['case_mode'];checks[mode]+=len(c['checks']);assert c['source_revision']==D and c['renderer']=='mobile' and c['time_scale']==1 and not c['actual_child_data'] and not c['normal_route_proved'] and not c['errors'] and all(x['pass']for x in c['checks'])
 assert c['engine']['string']=='4.7.2-stable (official)' or (c['engine']['major']==4 and c['engine']['minor']==7 and c['engine']['patch']==2 and c['engine']['status']=='stable' and c['engine']['build']=='official')
 assert q['exit_code']==0 and not q['timed_out'] and q['sidecars_exact'] and q['sidecar_before_count']==q['sidecar_after_count']==4041 and q['normal_before']==q['normal_after'] and not q['source_byte_changes'] and q['fixture_unchanged'] and q['dependencies_unchanged'] and not q['script_or_shader_errors']
 case=(P/job['manifest']).parent
 for src,stored in [('capture_reuse.gd','fixture_source.gd'),('capture_critter_saved.gd','base_fixture_source.gd'),('legacy_visual.gd','legacy_fixture_source.gd')]:assert(P/src).read_bytes()==(case/stored).read_bytes()
 assert len(c['states'])==37 and c['expected_caught']==(6 if c['saved_mode']=='partial' else 18) and c['seed']['critters']['r60_future_species']is False
 m=c['candidate_metrics'];assert m['books']==20
 if mode=='legacy':assert m['caught_role_collisions']==120 and not m['roles_ok'];collisions+=120
 else:assert m['caught_role_collisions']==0 and all(m[k]for k in ['roles_ok','counts_ok','frames_ok','geometry_ok','inputs_ok','names_fit','pictures_ok','selection_ok'])
 assert m['source_flat_card_observations']==0
 for st in c['states']:
  if not st['card_bindings']:continue
  bookcounts[mode]+=1;snap=st['snapshot'];assert snap['category']in['fish','insect','bird'] and snap['quality']=='speedy'and snap['time_scale']==1 and snap['caught_count']==c['expected_caught'] and snap['collection_nodes']==0
  assert snap['collection']==c['seed']['critters'] and snap['disk']['critters']==c['seed']['critters'];bs=snap['candidate']['button_invariants'];assert len(bs)==3
  for button in bs:
   assert all(button[k]for k in ['callbacks_unchanged','mouse_filter_unchanged','size_unchanged','declared_trial_rect_matches'])
   if mode!='legacy':assert button['selected']==button['selection_picture_visible']==(button['source_category']==snap['category'])
   target=mode=='insect'and button['source_category']=='insect'
   assert button['display_text']==(button['source_text'].replace('🦋','').strip()if target else button['source_text'])
   if target:assert button['category_picture']['source']=='res://assets/mg/butterfly.png' and button['category_picture']['stretch_mode']==5 and button['category_picture']['mouse_filter']==2
  assert len(st['card_bindings'])==6
  for card in st['card_bindings']:
   assert card['panel_id']==card['source_id'] and len(card['labels'])==3
   if mode=='legacy':continue
   assert card['size']=='(356.0, 132.0)'and card['style_class']=='StyleBoxEmpty'
   roles={l['role']:l for l in card['labels']};assert set(roles)=={'category_or_unknown_status','species_name','habitat'}
   for k,pos in [('category_or_unknown_status','(16.0, 18.0)'),('species_name','(98.0, 32.0)'),('habitat','(64.0, 74.0)')]:
    l=roles[k];assert l['id']==l['source_id'] and l['text']==l['source_text']and l['position']==pos
   name=roles['species_name'];assert name['font_size']==24 and name['text_width']<=232
   target=mode=='insect'and card['category']=='insect'and card['caught'];icon=roles['category_or_unknown_status'];assert icon['visible']is(not target)
   if target:
    pic=card['category_picture'];assert pic['source']=='res://assets/mg/butterfly.png'and pic['stretch_mode']==5 and pic['mouse_filter']==2 and pic['visible']and pic['modulate']=='(1.0, 1.0, 1.0, 1.0)'
   else:assert not card['category_picture']
   if not card['caught']:assert icon['text']=='?'and icon['visible']
assert bookcounts=={'insect':80,'fixed':20,'legacy':20}and checks=={'insect':172,'fixed':43,'legacy':36}and collisions==120
rv=rd(P/'REVIEW.json');assert len(rv['native_direct_views'])==15 and len(rv['comparison'])==10 and not rv['human_reviews']
for v in rv['native_direct_views']:assert sha((P/v['path']).read_bytes())==v['sha256']
for v in rd(P/'SOURCE_IMAGE_IDENTITY.json')['direct_source_views']:
 b=git('show',D+':'+v['path']);assert sha(b)==v['sha256'] and list(Image.open(io.BytesIO(b)).size)==v['size']
line=rd(P/'FIXTURE_LINEAGE.json');legacy=git('show',B+':'+(H/'r59_critter_book_reuse/capture_reuse.gd').relative_to(R).as_posix());assert sha(legacy)==line['legacy']['source_sha256']and legacy.splitlines()[1:]==(P/'legacy_visual.gd').read_bytes().splitlines()[1:]
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert git('show',B+':'+(H/name).relative_to(R).as_posix())==(H/name).read_bytes()
allowed={'revision','phase','publication','change_record','current_ci_snapshot'}
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/name);new=rd(P/name);assert new['revision']=='FV-AUDIT-20261015-R61'and new['critter_saved_reuse']['summary']=='SUMMARY.json'
 for k,v in old.items():
  if k not in allowed:assert new[k]==v,(name,k)
 assert new['critter_saved_reuse']['accepted_removed']==0
assert (O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
before=json.loads(git('show',B+':'+(H/'CURRENT.json').relative_to(R).as_posix()));after=rd(H/'CURRENT.json');routing={'revision','current_entry','current_per_piece','current_scene_coverage','current_tally','current_backlog','current_manifest','current_ci_evidence'}
assert before['schema']==after['schema']and after['current_tally']=='r61_critter_saved_reuse/tally.json'
for k,v in before.items():
 if k not in routing:assert after[k]==v
for k in ['approved','integrated','runtime_verified_replacements','accepted_removed','new_roles','new_families','new_alias_credits','generation_calls']:assert s[k]==0
assert s['known_roles']==240 and s['families']==32 and s['catalogue_partial']==85 and s['catalogue_without_current_slice']==91 and s['catalogue_complete']==0 and s['all_game_artwork_total']is None and not s['mission_complete']
print('R61_VALIDATED222native175bounded47excluded;172final43control36negative;120oldcollisions0new;original roles/input/count/unknown/hash/history preserved;0acceptance/globalunknown')
