from pathlib import Path
import json,hashlib,subprocess,importlib.util,io,os,re
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r72_skyway_hand_reuse';B='e4ff0ae20c0edfc567221396d4613b1fc4b1d067';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
s=importlib.util.spec_from_file_location('b73validate',P/'bounded_json.py');A=importlib.util.module_from_spec(s);s.loader.exec_module(A)
def rd(p):return A.read_document(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
refs=rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files'];pairs=sorted({(r['revision'],r['path']) for r in refs});cache={};raw=git('cat-file','--batch') if False else subprocess.check_output(['git','cat-file','--batch'],input=''.join(v+':'+p+'\n' for v,p in pairs).encode(),cwd=R);stream=io.BytesIO(raw)
for pair in pairs:
 h=stream.readline().split();assert len(h)==3 and h[1]==b'blob',pair;b=stream.read(int(h[2]));assert stream.read(1)==b'\n';cache[pair]=b
assert stream.read()==b''
for row in refs:
 b=cache[(row['revision'],row['path'])];assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
x=rd(P/'SUMMARY.json');assert x['source_revision']==D and x['listed_root_paths']==384 and x['scanned_text_files']==318 and x['parsed_scripts']==312 and x['shared_asset_reference_files']==18 and x['candidate_rendering_source_files']==16 and x['probe_requirement_files']==2 and x['source_function_bindings']==127
for key in ['new_capture_events','new_context_credits','new_artwork_roles','new_families','generation_calls','new_drawing_samples','approved','integrated','runtime_verified_replacements','accepted_removed']:assert x[key]==0
assert x['known_roles']==243 and x['known_families']==34 and x['retained_bounded']==6122 and x['retained_excluded']==3223 and x['retained_native_events']==9345 and x['catalogue_partial']==92 and x['catalogue_without_current_slice']==84 and x['catalogue_complete']==0
for key in ['whole_game_artwork_total','distinct_screen_total','regression_total']:assert x[key] is None
assert not x['allcaller_closure'] and not x['mission_complete']
census=rd(P/'SOURCE_CENSUS.json');expected=git('ls-tree','-r','--name-only',D,'--','scripts','scenes','shaders','project.godot').decode().splitlines();selected=[p for p in expected if Path(p).suffix in ['.gd','.tscn','.tres','.gdshader','.godot']];assert len(expected)==384 and len(selected)==318 and len([p for p in selected if p.endswith('.gd')])==312 and {r['path'] for r in census['files']}==set(selected)
for row in census['files']:assert sha(cache[(D,row['path'])])==row['sha256'] and len(cache[(D,row['path'])])==row['bytes']
m=rd(P/'CONSUMER_MAP.json');actual=[]
for path in selected:
 for i,line in enumerate(cache[(D,path)].decode().splitlines(),1):
  if 'ghost_hand.png' in line:actual.append((path,i,line))
assert actual==[(r['path'],r['line'],r['text']) for r in m['literal_rows']] and len(actual)==18
full=[r for r in actual if 'res://assets/castle/training/ghost_hand.png' in r[2]];assert len(full)==17
old=rd(H/'r17_pointer_callers/SOURCE_AUDIT.json');oldpaths={r['path'] for r in old['old_hand_path_references']};current={r[0] for r in actual};added=current-oldpaths;assert len(oldpaths)==16 and oldpaths<=current and added=={'scripts/probe_day_one_bathroom_cleanup.gd','scripts/probe_opera_gesture_quality.gd'}
for row in m['consumers']:
 assert row['consumer_id']=='FVHC-'+sha((m['resource']+'\t'+row['path']).encode())[:12].upper()
 assert row['classification']==('PROBE_ASSET_REQUIREMENT' if Path(row['path']).name.startswith('probe_') else 'CANDIDATE_RENDERING_SOURCE_NOT_RUNTIME_PROOF')
 assert row['reachability_status']=='SOURCE_BRANCHES_ONLY_NO_RUNTIME_OR_ALLCALLER_CLOSURE'
 for edge in row['incoming_source_candidates']:
  lines=cache[(D,edge['path'])].decode().splitlines();assert lines[edge['line']-1]==edge['text']
  if edge['matched_as']=='SAME_FILE_TOP_LEVEL_SCRIPT_ALIAS':assert edge['script_alias'] in lines[edge['alias_declaration_line']-1]
bodies=rd(P/'SOURCE_BODIES.json')['functions'];review=rd(P/'REVIEWED_BRANCHES.json');assert len(bodies)==127 and len(review['functions'])==12 and len(review['findings'])==4 and not review['global_caller_closure'] and not review['new_native_captures'] and not review['new_artwork_reviews']
from gdtoolkit.parser import parser
parsed={}
for row in bodies+review['functions']:
 raw=cache[(D,row['path'])];ls=raw.decode().splitlines(keepends=True);body=''.join(ls[row['start_line']-1:row['end_line']]);assert sha(raw)==row['file_sha256'] and body==row['body'] and sha(body.encode())==row['body_sha256']
 if row['path'] not in parsed:parsed[row['path']]=parser.parse(raw.decode(),gather_metadata=True)
 assert any(t.data=='func_def' and str(t.children[0].children[0])==row['function'] and t.meta.line==row['start_line'] and t.meta.end_line==row['end_line'] for t in parsed[row['path']].iter_subtrees_topdown())
fn={(r['path'],r['function']):r['body'] for r in review['functions']}
assert 'draw_circle(anchor, 13.0' in fn[('scripts/encounter_gesture_guide_2d.gd','_draw')] and 'if hand_texture != null:' in fn[('scripts/encounter_gesture_guide_2d.gd','_draw')]
assert 'if _is_candymaker_pour() and pour_demo_hand_texture != null:' in fn[('scripts/opera_gesture_surface.gd','_draw_demo_finger')] and 'draw_circle(at, 14.5' in fn[('scripts/opera_gesture_surface.gd','_draw_demo_finger')]
assert 'tree_book_test = OperaTreeBookTest.new()' in fn[('scripts/opera_house_venue_2d.gd','open_tree_book')] and 'practice_book.pressed.connect(open_tree_book)' in fn[('scripts/opera_house_venue_2d.gd','_build_practice_book')]
assert 'target and help_level == 2' in fn[('scripts/opera_tree_book_test.gd','_draw')]
v=rd(P/'CURRENT_VS_R17.json');assert v['changed_source_files']==1 and v['same_source_files']==15
for row in v['rows']:
 a=cache[(row['prior_revision'],row['path'])];b=cache[(D,row['path'])];assert sha(a)==row['prior_sha256'] and sha(b)==row['current_sha256'] and (a==b)==row['raw_bytes_same']
dep=rd(P/'RETIREMENT_DEPENDENCIES.json');assert len(dep['preload_files'])==3 and not dep['file_deletion_is_removal_proof'] and not dep['filename_test_is_exclusion_proof'] and not dep['skyway_candidate_is_global_replacement_proof']
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert (H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 before=rd(O/n);after=rd(P/n)
 for k in before:
  if k not in ['revision','phase','publication']:assert before[k]==after[k],(n,k)
 assert after['hand_consumer_audit']['accepted_removed']==0 and not after['hand_consumer_audit']['allcaller_closure']
for n in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert (P/n).read_bytes()==(O/n).read_bytes()
assert rd(O/'NEW_ART_REVIEW_REQUEST.json')['owner_approval'] is False and rd(O/'NEW_ART_REVIEW_REQUEST.json')['generation_calls']==0
assert rd(H/'CURRENT.json')['current_tally']=='r73_hand_consumer_audit/tally.json'
allowed={'design/audit_impacts/flat-vector-hand-consumers-20261015.json','audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md','audit/MASTER_AUDIT_CHANGELOG_ROLLBACK_2026-08-10.md','design/05_DOC_LEDGER.md',(H/'README.md').relative_to(R).as_posix(),(H/'CURRENT.json').relative_to(R).as_posix()}
for path in set(git('diff','--name-only',B).decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()):assert path in allowed or path.startswith(P.relative_to(R).as_posix()+'/'),path
W=Path(r'C:/Users/Peter/.codex/worktrees/flat-vector-dev-context-20261015/mermaid-roshan-reef');base=rd(H/'r51_farmer_context/RUNTIME_BYTE_BASELINE.json');assert len(base['runtime_raw_hashes'])==4420 and all(sha((W/p).read_bytes())==v for p,v in base['runtime_raw_hashes'].items());side={}
for root,dirs,files in os.walk(W):
 dirs[:]=[n for n in dirs if n not in {'.git','.godot','__pycache__','.secrets','.aws','.codex','.claude'}]
 for n in files:
  f=Path(root)/n
  if f.suffix in {'.uid','.import'}:side[f.relative_to(W).as_posix()]=sha(f.read_bytes())
assert side==base['sidecars'] and len(side)==4041
normal=Path(os.environ['APPDATA'])/'Godot/app_userdata/Mermaid Roshan Reef of Light/reef_save.json';guard=rd(P/'SOURCE_GUARDS.json');assert guard['normal_save_names_checked']==11 and guard['runtime_files_checked']==4420 and guard['sidecars_checked']==4041 and not guard['source_byte_changes']
for suffix,d in guard['normal_save_hashes'].items():
 f=Path(str(normal)+suffix);assert (sha(f.read_bytes()) if f.is_file() else 'absent')==d
print('R73_EVIDENCE_PASS;318text312AST;18refs16same_render_candidates2probe_requirements;127function_bindings12branch_bodies;2conditional_primitive_fallbacks;0newcontext/art/removal;globalunknown')
