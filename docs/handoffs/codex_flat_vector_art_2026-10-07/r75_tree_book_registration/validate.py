from pathlib import Path
import json,hashlib,subprocess,importlib.util,math,io,zipfile,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r74_tree_book_context';B='715c7a230c159e70acae1cd0ddad727e88910cb9';D='dd799b2d43871b29d1d6e0503646308a194dad1e'
s=importlib.util.spec_from_file_location('a75validate',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
summary=rd(P/'SUMMARY.json');idx=rd(P/'CAPTURE_INDEX.json');pm=rd(P/'POINTER_MEASUREMENTS.json');semantic=rd(P/'SEMANTIC_TARGET_CHECK.json')
assert (idx['raw_frames'],idx['bounded_source_contexts'],idx['excluded_diagnostics'])==(230,78,152) and len(idx['files'])==230
assert (summary['retained_bounded'],summary['retained_excluded'],summary['retained_native_events'])==(6278,3420,9698) and summary['all_observer_checks']==324
assert summary['source_control_checks']==96 and summary['rejected_first_variant_checks']==summary['final_variant_checks']==114 and summary['source_hint_tip_misses']==summary['final_variant_input_advances']==8
for x in idx['files']:
 raw=(R/x['path']).read_bytes();im=Image.open(io.BytesIO(raw));assert len(raw)==x['bytes'] and sha(raw)==x['sha256'] and list(im.size)==x['dimensions'] and sha(im.convert('RGBA').tobytes())==x['decoded_rgba_sha256']
for c in sorted((P/'native').iterdir()):
 m=rd(c/'capture_manifest.json');res=rd(c/'RESULT.json');launch=rd(c/'LAUNCH.json');control=m['mode']=='control';v2=c.name.startswith('attempt2')
 assert res['exit_code']==0 and not res['timed_out'] and res['normal_before']==res['normal_after'] and len(res['normal_after'])==11 and res['sidecars_exact'] and res['sidecar_after_count']==4088 and not res['source_byte_changes'] and not res['script_or_shader_errors'] and res['fixture_dependency_unchanged']
 assert m['source_revision']==D and m['time_scale']==1 and not m['actual_child_data'] and not m['production_changes'] and all(x['pass']for x in m['checks']) and not m['errors']
 assert len(m['states'])==(41 if control else 37) and len(m['checks'])==(48 if control else 57)
 for n,h in launch['fixture_dependencies'].items():assert sha((c/n).read_bytes())==h
 for cy in m['hint_cycles']:
  assert cy['outside']==(cy['total']if control else 0) and len(cy['samples'])==cy['total'] and cy['end_phase']-cy['start_phase']>=math.tau-0.25
  for q in cy['samples']:
   x,y,w,h=q['target'];phase=q['elapsed']*3;dx=0 if control or q['stage']<3 or not v2 else-51;dy=0 if control else-36 if q['stage']<3 else-114 if v2 else-44;size=80 if q['stage']<3 else 95
   expected=[x+w-68+dx+217*size/512,y+h-55-math.sin(phase)*9+dy+447*size/512]if q['stage']<3 else[x+80+dx+217*size/512,y+78+math.sin(phase)*10+dy+447*size/512]
   assert all(abs(a-b)<0.001 for a,b in zip(expected,q['local_tip'])) and q['pointer_visible_by_source_branch'] and q['inside']is(not control)
 for ct in m['source_contracts']:assert ct['input_advanced']is(not control)
 if v2:
  assert len(m['comparisons'])==5 and all(x['before']==x['after'] and x['source_signature_unchanged']for x in m['comparisons'])
 if not control:assert len(m['teardown_checks'])==4 and all(x['source_teardown_disposed_preview']for x in m['teardown_checks'])
 states={x['id']:x['snapshot']for x in m['states']};dose=states['treatment_partial_canceled']['book']['treatment'];assert 0<dose<0.9
 for n in ['partial_reopen_book_open','reload_book_open']:assert abs(states[n]['book']['treatment']-dose)<1e-6 and states[n]['book']['stage']==4
 assert states['healthy_complete']['book']['stage']==states['healthy_reopen_book_open']['book']['stage']==5 and states['replay_started']['book']['stage']==0
 assert all(x['main']['stars']==0 and x['main']['pearls']==23 and x['main']['opera_progress']==0 for x in states.values())
 assert states['final_venue_restored']['disk']['unknown']=={'keep':[4,7],'token':'R75_SYNTHETIC_ONLY'}
assert len(pm['cycles'])==24 and len(pm['contracts'])==24
for row in pm['cycles']:assert row['maximum_projection_error_px']<0.001
leafraw=git('show',D+':assets/opera/tree_book_test/leaves_medicine.png');assert sha(leafraw)==semantic['source_atlas_sha256'];alpha=Image.open(io.BytesIO(leafraw)).getchannel('A');pts={(x,y)for y in range(249)for x in range(255,513)if alpha.getpixel((x,y))>=64};groups=[]
while pts:
 start=min(pts);pts.remove(start);todo=[start];group=set()
 while todo:
  x,y=todo.pop();group.add((x,y))
  for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if n in pts:pts.remove(n);todo.append(n)
 groups.append(group)
groups.sort(key=lambda x:(-len(x),min(x)));assert [len(x)for x in groups]==[20509,6585] and sha(json.dumps(sorted(groups[0]),separators=(',',':')).encode())==semantic['primary_coordinate_sha256']
b=semantic['actual_source_atlas_binding'];bx,by,bw,bh=b['fit_box'];tw,th=b['texture_size'];f=min(bw/tw,bh/th);ox=bx+(bw-tw*f)/2;oy=by+(bh-th*f)/2
final_semantic=[x for x in semantic['cases']if x['variant']=='LEAF_SILHOUETTE_V2'];assert len(final_semantic)==2
for record in final_semantic:
 m=rd(P/'native'/record['case']/'capture_manifest.json');points=m['hint_cycles'][-1]['samples'];assert record['component_counts']=={'PRIMARY_SPOTTED_LEAF':len(points)}
 for q in points:
  x,y=q['local_tip'];rx,ry,rw,rh=b['region'];pixel=(int(rx+(x-ox)/(tw*f)*rw),int(ry+(y-oy)/(th*f)*rh));assert pixel in groups[0] and alpha.getpixel(pixel)>=64
for record in semantic['cases']:
 if record['variant']!='LEAF_SILHOUETTE_V2':assert record['component_counts'].get('PRIMARY_SPOTTED_LEAF',0)==0
review=rd(P/'REVIEW.json');assert len(review['reviewed_native_images'])==11 and set(review['comparison'])=={'contour','material','palette','light','perspective','scale','contact','occlusion','readability','action_state'}
for x in review['reviewed_native_images']:assert x in idx['files']
assert not review['approved'] and not review['integrated'] and not review['full_context_review_complete'] and review['DL_QA_11']=='NOT_ESTABLISHED'
repro=rd(P/'REPRODUCTION_CHECK.json');assert repro['scanner_sha256']==sha((P/'derive_evidence.py').read_bytes()) and len(repro['outputs'])==6
for row in repro['outputs']:assert row['logical_exact'] and row['index_or_raw_bytes_exact'] and sha((P/row['path']).read_bytes())==row['sha256']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/name);old=rd(O/name);assert d['tree_book_registration']==summary
 for k,v in old.items():
  if k in ['revision','phase','publication']:continue
  if name=='per_piece.json'and k=='supplemental_piece_records':
   assert len(d[k])==len(v)
   for new,prior in zip(d[k],v):
    assert all(new[key]==value for key,value in prior.items())
    if prior['id']==summary['stable_id']:assert new['registration_preview']['accepted_removed']==0
  else:assert d[k]==v,(name,k)
for name in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:
 new=rd(P/name);old=rd(O/name);assert all(new[k]==v for k,v in old.items())
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
changed=git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines();prefix=P.relative_to(R).as_posix()+'/';allowed={'design/audit_impacts/flat-vector-tree-book-registration-20261015.json','audit/MASTER_AUDIT_2026-08-09.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md','docs/handoffs/codex_flat_vector_art_2026-10-07/CURRENT.json','docs/handoffs/codex_flat_vector_art_2026-10-07/README.md'};assert all(x.startswith(prefix)or x in allowed for x in changed)
for record in ['FIXTURE_SYNTAX_GATES.json','FIXTURE_SYNTAX_GATES_EDGE_V1.json','ALL_FIXTURE_GATES.json']:assert all(x['exit_code']==0 for x in rd(P/record)['checks'])
base=rd(P/'RUNTIME_BYTE_BASELINE.json');guards=rd(P/'SOURCE_GUARDS.json');proof=rd(P/'SOURCE_GIT_OBJECT_PROOF.json');assert len(base['runtime_raw_hashes'])==guards['runtime_count']==proof['count']==4425 and len(base['sidecars'])==guards['sidecar_count']==4088 and guards['sidecars_exact'] and guards['source_worktree_clean'] and not guards['runtime_changes']
assert proof['non_eol_differences']==0 and all(base['runtime_raw_hashes'][x['path']]==x['sha256']for x in proof['files'])
eol=rd(P/'IMPORT_EOL_RECOVERY.json');assert eol['changed_import_count']==len(eol['changes'])==1102 and eol['normal_before']==eol['normal_after'] and sha((P/eol['backup_archive_path']).read_bytes())==eol['backup_archive_sha256']
old=rd(H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json')
with zipfile.ZipFile(P/eol['backup_archive_path'])as z:
 for row in eol['changes']:
  raw=z.read(row['path']);assert sha(raw)==row['generated_sha256'] and sha(raw.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))==row['restored_sha256']==old['runtime_raw_hashes'][row['path']]
side=rd(P/'IMPORT_SIDECAR_DELTA.json');assert side['added_count']==47 and not side['changed_existing_files'] and not side['removed_existing_files'] and all(base['sidecars'][p]==v for p,v in old['sidecars'].items())
code=(P/'registration_preview.gd').read_text(encoding='utf-8');assert 'source_book.hand = original_hand'in code and 'host.hand = null'in code
for text in ['set_script','Engine.time_scale','_gui_input','func _input']:assert text not in code
assert not re.search(r'\bsource_book\.(stage|treatment|help_level|elapsed)\s*=(?!=)',code)
for x in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 raw=git('show',x['revision']+':'+x['path']);assert sha(raw)==x['sha256'] and len(raw)==x['bytes']
assert rd(H/'CURRENT.json')['current_tally']=='r75_tree_book_registration/tally.json' and rd(H/'r72_skyway_hand_reuse/NEW_ART_REVIEW_REQUEST.json')['owner_approval']is False
assert summary['new_roles']==summary['new_families']==summary['new_drawing_samples']==summary['generation_calls']==summary['integrated']==summary['runtime_verified_replacements']==summary['accepted_removed']==0 and summary['known_roles']==254 and summary['known_families']==35 and not summary['mission_complete']
for k in ['all_game_artwork_total','distinct_screen_total','regression_total']:assert summary[k]is None
print('R75_VALIDATION_PASS 230raw78bounded152excluded;324checks;source8miss/final8advance+primaryleaf;V1rejected;state/source/import/frozen/history guards;0art/acceptance;globalunknown',flush=True)
