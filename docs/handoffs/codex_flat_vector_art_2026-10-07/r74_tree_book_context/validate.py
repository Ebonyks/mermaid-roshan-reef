from pathlib import Path
import json,hashlib,subprocess,importlib.util,math,io
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r73_hand_consumer_audit';B='0f99b32d98729d11f114dbebcf5b90aba39ca545';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
s=importlib.util.spec_from_file_location('a74validate',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
summary=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');reviews=rd(P/'PIECE_CONTEXT_REVIEWS.json');roles=reviews['new_named_design_roles'];pm=rd(P/'POINTER_MEASUREMENTS.json')
assert len(idx['files'])==123 and idx['bounded']==78 and idx['excluded']==45
assert (summary['retained_bounded'],summary['retained_excluded'],summary['retained_native_events'])==(6200,3268,9468)
assert summary['retained_bounded']+summary['retained_excluded']==summary['retained_native_events'] and summary['healthy_checks']==96
for row in idx['files']:
 b=(R/row['path']).read_bytes();im=Image.open(io.BytesIO(b));assert len(b)==row['bytes'] and sha(b)==row['sha256'] and list(im.size)==row['dimensions'] and sha(im.convert('RGBA').tobytes())==row['decoded_rgba_sha256']
for case in idx['cases']:
 c=P/'native'/case['case'];m=rd(c/'capture_manifest.json');res=rd(c/'RESULT.json');healthy=res['exit_code']==0
 assert len(m['checks'])==48 and sum(x['pass']for x in m['checks'])==case['passing_checks'];assert case['bounded']==(39 if healthy else 0)
 assert res['normal_before']==res['normal_after'] and len(res['normal_after'])==11 and res['sidecars_exact'] and res['sidecar_after_count']==4041 and res['source_byte_changes']==[] and not res['script_or_shader_errors'] and not res['timed_out']
 assert res['log_sha256']==sha((c/'engine.log').read_bytes()) and rd(c/'LAUNCH.json')['fixture_sha256']==sha((c/'capture_tree_book.gd').read_bytes())
 if healthy:assert (c/'capture_tree_book.gd').read_bytes()==(P/'capture_tree_book.gd').read_bytes() and not m['errors'] and all(x['pass']for x in m['checks'])
 else:assert (c/'capture_tree_book.gd').read_bytes()==(P/'capture_tree_book_guard_v1.gd').read_bytes() and sum(not x['pass']for x in m['checks'])==1
 for cy in m['hint_cycles']:
  assert cy['outside']==cy['total']==len(cy['samples']) and cy['end_phase']-cy['start_phase']>=math.tau-0.25
  for q in cy['samples']:
   x,y,w,h=q['target'];phase=q['elapsed']*3
   expected_y=y+h-55-math.sin(phase)*9+447*80/512 if q['stage']<3 else y+78+math.sin(phase)*10+447*95/512
   expected_x=x+w-68+217*80/512 if q['stage']<3 else x+80+217*95/512
   assert abs(expected_y-q['local_tip'][1])<0.001 and abs(expected_x-q['local_tip'][0])<0.001 and expected_y>y+h and not q['inside']
 for ct in m['source_contracts']:assert not ct['input_advanced'] and ct['stage_before']==ct['stage_after'] and ct['dose_before']==ct['dose_after']
 if healthy:
  states={x['id']:x['snapshot']for x in m['states']};dose=states['treatment_partial_canceled']['book']['treatment'];assert 0<dose<1
  for name in ['partial_reopen_book_open','reload_book_open']:assert states[name]['book']['stage']==4 and abs(states[name]['book']['treatment']-dose)<1e-6
  assert states['healthy_complete']['book']['stage']==states['healthy_reopen_book_open']['book']['stage']==5 and states['replay_started']['book']['stage']==0
  assert all(x['main']['stars']==0 and x['main']['pearls']==23 and x['main']['opera_progress']==0 for x in states.values())
  assert states['final_venue_restored']['disk']['unknown']=={'keep':[4,7],'token':'R74_SYNTHETIC_ONLY'}
# Independently measure alpha64 bottom-tip from exact public original source hand, without editing it.
hand=Image.open(io.BytesIO(git('show',D+':assets/castle/training/ghost_hand.png'))).convert('RGBA');assert hand.size==(512,512)
a=hand.getchannel('A');bottom=max(y for y in range(512) if any(a.getpixel((x,y))>=64 for x in range(512)));xs=[x for x in range(512)if a.getpixel((x,bottom))>=64];assert bottom==447 and min(xs)<=217<=max(xs)
assert pm['healthy_cycles']==8 and pm['healthy_tip_input_misses']==8 and len(pm['cycles'])==12
source=git('show',D+':scripts/opera_tree_book_test.gd');binding=rd(P/'SOURCE_BINDINGS.json');assert binding['script_sha256']==sha(source) and binding['draw_body_sha256']==sha(b''.join(source.splitlines(keepends=True)[337:408]))
assert len(roles)==11 and len({x['id']for x in roles})==11 and {x['family']for x in roles}=={'tree_book_practice'}
for x in roles:
 assert x['id']=='FVR-'+sha(x['stable_id_input'].encode())[:12].upper() and x['source']['file_sha256']==sha(source) and x['drawing_required'] is None and not x['reuse_ready'] and x['acceptance_evidence']['accepted_removed']==0 and not x['acceptance_evidence']['full_context_review_complete']
 assert set(x['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'}
 assert x['context_references']
 for ref in x['context_references']:assert ref in idx['files'] and ref['classification']=='BOUNDED_CURRENT_CONTEXT'
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/n);old=rd(O/n);assert d['tree_book_context']==summary
 for k,v in old.items():
  if k in ['revision','phase','publication']:continue
  if n=='per_piece.json' and k=='supplemental_piece_records':assert d[k][:len(v)]==v and d[k][len(v):]==roles
  else:assert d[k]==v,(n,k)
assert rd(P/'scene_coverage.json')['entries']==rd(O/'scene_coverage.json')['entries']
known=rd(P/'CURRENT_KNOWN_ROLE_UNION.json');prior=rd(O/'CURRENT_KNOWN_ROLE_UNION.json');assert known['records'][:243]==prior['records'] and len(known['records'])==len({x['id']for x in known['records']})==254 and len({x['family']for x in known['records']})==35
assert rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records']==rd(O/'CURRENT_PARTIAL_CONTEXT_UNION.json')['records'] and rd(P/'CURRENT_PARTIAL_CONTEXT_UNION.json')['supplemental_partial_records']==30
assert rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json')['current_partial_count']==92 and rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json')['without_current_slice_count']==84 and rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json')['complete_count']==0
for key in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert summary[key] is None
assert summary['accepted_removed']==summary['generation_calls']==summary['integrated']==summary['runtime_verified_replacements']==0 and not summary['mission_complete']
for name in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/name).read_bytes()==git('show',B+':'+(H/name).relative_to(R).as_posix())
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();allowed={str((R/p).relative_to(R)).replace('\\','/')for p in ['design/audit_impacts/flat-vector-tree-book-context-20261015.json','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md','docs/handoffs/codex_flat_vector_art_2026-10-07/CURRENT.json','docs/handoffs/codex_flat_vector_art_2026-10-07/README.md']};prefix=P.relative_to(R).as_posix()+'/'
assert all(x.startswith(prefix)or x in allowed for x in changed),[x for x in changed if not(x.startswith(prefix)or x in allowed)]
assert rd(H/'CURRENT.json')['current_tally']=='r74_tree_book_context/tally.json' and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval'] is False
for n in ['FIXTURE_SYNTAX_GATES.json','ALL_FIXTURE_GATES.json']:assert all(x['exit_code']==0 for x in rd(P/n)['checks'])
guard=rd(P/'SOURCE_GUARDS.json');assert guard['runtime_count']==4420 and guard['sidecar_count']==4041 and guard['sidecars_exact'] and not guard['runtime_changes'] and guard['source_worktree_clean']
for row in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 raw=git('show',row['revision']+':'+row['path']);assert sha(raw)==row['sha256'] and len(raw)==row['bytes']
repro=rd(P/'REPRODUCTION_CHECK.json');assert repro['status']=='PASS_FRESH_SCRATCH_ANALYSIS' and len(repro['outputs'])==6 and repro['scanner_sha256']==sha((P/'analyze_evidence.py').read_bytes())
up=rd(P/'UPSTREAM_DELTA_REVIEW.json');assert up['audited_source_revision']==D and not up['new_head_runtime_reviewed'] and len(up['runtime_changed_paths'])==8 and up['requires_fresh_context_before_production_or_final_acceptance']
diffrecord=rd(P/'upstream_doorframe_delta.json');rawdiff=git('diff',D,up['origin_dev'],'--',*up['runtime_changed_paths']);assert diffrecord['raw_diff_utf8'].encode()==rawdiff and sha(rawdiff)==diffrecord['raw_sha256']
for x in up['selected_book_entry_art_and_save_byte_equal']:assert git('show',D+':'+x['path'])==git('show',up['origin_dev']+':'+x['path']) and x['exact_bytes']
print('R74_VALIDATION_PASS 123raw/78bounded/45excluded;96checks8misses;11newroles254/35;history/frozen/source/provenance guards;0acceptance;globalunknown',flush=True)
