from pathlib import Path
import json,hashlib,subprocess,importlib.util,io,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r75_tree_book_registration';B='e970602af8bf091bdcb7dea00a78fa9ada7ca224';D='dd799b2d43871b29d1d6e0503646308a194dad1e'
s=importlib.util.spec_from_file_location('a76validate',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
summary=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');roles=rd(P/'NEW_ROLE_RECORDS.json')['records'];review=rd(P/'REVIEW.json')
assert (idx['raw_frames'],idx['bounded_source_contexts'],idx['excluded_diagnostics'],idx['failed_attempt_frames'])==(88,32,56,36)
assert (summary['retained_bounded'],summary['retained_excluded'],summary['retained_native_events'])==(6310,3476,9786)
assert (summary['known_roles'],summary['known_families'],summary['new_roles'],summary['new_families'])==(261,35,7,0)
assert summary['healthy_observer_checks']==86 and summary['supplemental_partial_roles']==37
for x in idx['files']:
 raw=(R/x['path']).read_bytes();im=Image.open(io.BytesIO(raw));assert len(raw)==x['bytes']and sha(raw)==x['sha256']and list(im.size)==x['dimensions']and sha(im.convert('RGBA').tobytes())==x['decoded_rgba_sha256']
for c in sorted((P/'native').iterdir()):
 m=rd(c/'capture_manifest.json');res=rd(c/'RESULT.json');launch=rd(c/'LAUNCH.json');healthy=c.name.startswith('attempt3')
 assert not res['timed_out']and res['normal_before']==res['normal_after']and len(res['normal_after'])==11 and res['sidecars_exact']and res['sidecar_after_count']==4088 and not res['source_byte_changes']and not res['script_or_shader_errors']and res['fixture_dependency_unchanged']
 assert m['source_revision']==D and m['time_scale']==1 and not m['actual_child_data']and not m['production_changes']and m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079'
 assert m['renderer']=='mobile'and m['display']!='headless'and m['seed']['quality']=='speedy'and m['engine']['build']=='official'and m['engine']['patch']==2
 assert sha((c/'capture_care.gd').read_bytes())==launch['fixture_sha256']
 if healthy:
  assert res['exit_code']==0 and m['observer_status']=='PASS'and not m['errors']and len(m['checks'])==43 and all(x['pass']for x in m['checks'])and len(m['states'])==26
  states={x['id']:x['snapshot']for x in m['states']};assert states['neutral_points3']['care_points']==3 and states['requested_fulfilled_feedback']['care_points']==4 and states['new_main_reload_points4']['care_points']==4
  for st in states.values():
   assert st['game']=='level2'and st['phase']=='promenade'and st['companion']=='eagle'and st['pearls']==23
   assert st['disk']['unknown']==m['seed']['flat_vector_private_unknown']and st['disk']['custom_fish']==m['seed']['custom_fish']and st['disk']['custom_friends']==m['seed']['custom_friends']
  assert states['neutral_points3']['stars']==chr(0x2b50)and states['new_main_reload_points4']['stars']==chr(0x2b50)*2
  actions={n.get('text')for st in states.values()for n in st['nodes']if n['class']=='Button'and n.get('text')in {chr(x)for x in [0x1f34e,0x1f4a4,0x1fae7,0x2764,0x1f3be]}};assert len(actions)==5
  assert sum(x['down']for x in m['events'])==20
 else:
  assert res['exit_code']==1 and m['observer_status']=='FAIL'and len(m['errors'])==1
assert len(review['reviewed_native_images'])==7 and all(x in idx['files']for x in review['reviewed_native_images'])
assert set(review['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'}
assert not review['full_context_review_complete']and review['DL_QA_11']=='NOT_ESTABLISHED'and not review['approved']and not review['integrated']
ids=set()
for r in roles:
 assert r['id']=='FVR-'+sha(r['stable_id_input'].encode())[:12].upper()and r['id']not in ids;ids.add(r['id']);assert r['family']=='shared_ui'and not r['full_context_review_complete']and not r['approved']and not r['integrated']and not r['accepted_removed']and r['drawing_required']is None
 assert r['same_scene_references'][0]['path']=='assets/characters/companions/baby_eagle.png'
feedback=rd(P/'FEEDBACK_OBSERVATIONS.json');assert len(feedback['observations'])==16 and all(not x['intended_short_acknowledgement_observed']and not x['label_is_direct_child_of_stage']for x in feedback['observations'])
raw=git('show',D+':scripts/companion.gd');text=raw.decode();defs=list(re.finditer(r'^func (\w+)\(',text,re.M));bindings=rd(P/'SOURCE_BINDINGS.json')
for row in bindings['functions']:
 i=next(i for i,x in enumerate(defs)if x.group(1)==row['function']);body=text[defs[i].start():defs[i+1].start()if i+1<len(defs)else len(text)];assert sha(body.encode())==row['body_sha256']and sha(raw)==row['file_sha256']
for row in bindings['wants_literal_bindings']:assert text.splitlines(keepends=True)[row['line']-1]==row['exact_lf_line']and sha(row['exact_lf_line'].encode())==row['sha256']
for x in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 b=git('show',x['revision']+':'+x['path']);assert sha(b)==x['sha256']and len(b)==x['bytes']
repro=rd(P/'REPRODUCTION_CHECK.json');assert repro['scanner_sha256']==sha((P/'derive_evidence.py').read_bytes())and len(repro['outputs'])==3 and all(x['logical_exact']and sha((P/x['path']).read_bytes())==x['sha256']for x in repro['outputs'])
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n);assert d['stuffie_care_context']==summary
 for k,v in old.items():
  if k in ['revision','phase','publication']:continue
  if n=='per_piece.json'and k=='supplemental_piece_records':assert d[k][:-7]==v and d[k][-7:]==roles
  else:assert d[k]==v,(n,k)
u=rd(P/'CURRENT_KNOWN_ROLE_UNION.json');old=rd(O/'CURRENT_KNOWN_ROLE_UNION.json');assert u['records'][:-7]==old['records']and {x['id']for x in u['records'][-7:]}==ids and len(u['records'])==261 and len({x['family']for x in u['records']})==35
u=rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json');assert u['records']==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records']and u['supplemental_partial_records']==37
u=rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json');old=rd(O/'CURRENT_CATALOGUE_CONTEXT_UNION.json');assert all(u[k]==v for k,v in old.items())and(u['current_partial_count'],u['without_current_slice_count'],u['complete_count'])==(92,84,0)
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();prefix=P.relative_to(R).as_posix()+'/';allowed={'design/audit_impacts/flat-vector-stuffie-care-context-20261016.json','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','design/05_DOC_LEDGER.md',(H/'CURRENT.json').relative_to(R).as_posix(),(H/'README.md').relative_to(R).as_posix()};assert all(x.startswith(prefix)or x in allowed for x in changed)
guards=rd(P/'SOURCE_GUARDS.json');assert guards['runtime_count']==4425 and guards['sidecar_count']==4088 and guards['sidecars_exact']and not guards['runtime_changes']and guards['source_worktree_clean']
for n in ['FIXTURE_SYNTAX_GATES.json','FIXTURE_SYNTAX_GATES_ATTEMPT1.json','FIXTURE_SYNTAX_GATES_ATTEMPT2.json']:assert all(x['exit_code']==0 for x in rd(P/n)['checks'])
assert not re.search(r'\bm\.(care_points|companion_want|companion_want_queue|companion_want_cool|companion_care_t)\s*=(?!=)',(P/'capture_care.gd').read_text(encoding='utf-8'))
assert rd(H/'CURRENT.json')['current_tally']=='r76_stuffie_care_context/tally.json'and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval']is False
for k in ['approved','integrated','runtime_verified_replacements','accepted_removed','new_drawing_samples','generation_calls','new_runtime_assets']:assert summary[k]==0
assert all(summary[k]is None for k in ['all_game_artwork_total','distinct_screen_total','regression_total'])and not summary['mission_complete']
print('R76_VALIDATION_PASS 88raw32bounded56excluded;86healthychecks;7newroles261/35;feedbacksourcegap;history/source/import/private/normalguards;0production/art/acceptance;globalunknown',flush=True)
