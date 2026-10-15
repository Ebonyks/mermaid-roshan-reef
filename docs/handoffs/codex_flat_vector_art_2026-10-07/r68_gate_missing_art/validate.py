from pathlib import Path
import json,hashlib,subprocess
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r67_painted_gate_cue';B='348116d6dc82c5a4f9e0a6a0b856de0ff6416349';D='5120b6d59885dd057937aaf284e73681d8eac9f5'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
s=rd(P/'SUMMARY.json');assert(s['native_cases'],s['passing_functional_cases'],s['passing_functional_checks'],s['new_native_frames'],s['new_bounded_contexts'],s['new_excluded_diagnostics'])==(8,4,88,52,32,20);assert s['source_walking_entry_survives']and s['premature_entry_assertions_retracted']==2 and s['black_excluded_frames']==2 and s['accepted_removed']==0 and s['all_game_artwork_total']is None
versions=rd(P/'FIXTURE_VERSIONS.json');frames=rd(P/'CAPTURE_INDEX.json')['frames'];assert len(frames)==52 and len({x['path']for x in frames})==52
for f in frames:
 raw=(R/f['path']).read_bytes();im=Image.open(R/f['path']).convert('RGBA');assert sha(raw)==f['sha256']and list(im.size)==f['size']and sha(im.tobytes())==f['decoded_rgba_sha256'];black=im.convert('RGB').getextrema()==((0,0),(0,0),(0,0));assert black==f['black_pixels'];assert not black or(f['fixture_version']=='v1'and'baseline_missing'in f['case']and f['state']=='05_failed_activation'and f['classification'].startswith('EXCLUDED'))
for row in s['cases']:
 Q=P/'native'/row['case'];m=rd(Q/'capture_manifest.json');result=rd(Q/'RESULT.json');launch=rd(Q/'LAUNCH.json');v=versions[row['fixture_version']];assert len(m['normal_before'])==11 and m['normal_before']==m['normal_after']==result['normal_before']==result['normal_after'];assert result['sidecars_exact']and not result['source_byte_changes']and result['fixture_dependencies_unchanged'];assert len(m['bindings'])==1 and m['bindings'][0]['before_ready']
 for n,digest in launch['fixture_dependencies'].items():assert sha((Q/n).read_bytes())==digest
 assert launch['fixture_dependencies']['capture_gate.gd']==v['capture_sha256']==sha((P/v['capture']).read_bytes())
 for n in versions['unchanged_functional_fixture_helpers']:assert(Q/n).read_bytes()==(P/n).read_bytes()
 if m['mode']=='baseline_missing':
  assert result['exit_code']==1 and m['functional_status']=='FAIL'and m['artwork_status']=='FAIL_MISSING_CUE_ARTWORK';assert len(m['errors'])==(3 if row['fixture_version']=='v1'else 2)
  if row['fixture_version']=='v2':
   assert m['states'][-1]['snapshot']['phase']=='hall'and m['states'][-1]['snapshot']['castle_room']=='main_hall'and not m['states'][-1]['snapshot']['movie']['active'];assert m['states'][3]['snapshot']['source_motion']['walk_goal']!='<null>'
 else:
  assert result['exit_code']==0 and not result['script_or_shader_errors']and not m['errors']and all(x['pass']for x in m['checks'])and len(m['states'])==8
  ss=m['states'];assert ss[0]['snapshot']['gate']['anchor_id']!=ss[5]['snapshot']['gate']['anchor_id'];assert ss[4]['snapshot']['gate']=={}and ss[7]['snapshot']['gate']=={}
  for i in [0,1,2,3,5,6]:
   g=ss[i]['snapshot']['gate'];assert g['target_registered']and g['radius_px']==128 and g['anchor_class']=='Node2D'and g['anchor_source_owned']and g['target_count']==4
   if m['mode']=='normal':assert g['glow_present']and g['rgb']==[1,1,1]and g['texture']=='res://assets/opera/worlds/props/fx_stolen_sparkle.png'
   else:assert not g['glow_present']and not g['texture']and g['art_status']=='MISSING_CUE_ARTWORK_FAILED'
  private=rd(Q/'PRIVATE_SYNTHETIC_FINAL.json');assert private['unknown']=={'token':'R68_PRIVATE_ONLY','keep':[3,7]}and all(x is False for x in private['won'].values())and all(x is False for x in private['found'].values())and private['actual_child_data']is False
 for state in m['states']:
  assert state['snapshot']['quality']=='speedy'and state['snapshot']['time_scale']==1.0
  for n in state['selected_canvas_nodes']:
   texture=n.get('texture',{});assert not isinstance(texture,dict)or texture.get('path')!='res://assets/sprites/sky_lagoon/sky_lagoon_castle_door_focus_v1.png'
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:
 path=(P.parent/n).relative_to(R).as_posix();assert(R/path).read_bytes()==git('show',B+':'+path)
for n in ['CURRENT_KNOWN_ROLE_UNION.json','CURRENT_PARTIAL_CONTEXT_UNION.json','CURRENT_CATALOGUE_CONTEXT_UNION.json']:assert(P/n).read_bytes()==(O/n).read_bytes()
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 old=rd(O/n);new=rd(P/n)
 for k,v in old.items():
  if k not in ['revision','phase','publication']:assert new[k]==v,(n,k)
 assert new['gate_missing_art_repair']['accepted_removed']==0 and new['gate_missing_art_repair']['source_walking_entry_survives']
review=rd(P/'REVIEW.json');assert len(review['axes'])==10 and review['view_count']==11
for x in review['viewed_native_frames']:assert sha((P/x['path']).read_bytes())==x['sha256']
for x in rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files']:
 raw=git('show',x['revision']+':'+x['path']);assert len(raw)==x['bytes']and sha(raw)==x['sha256']
c=rd(P/'DIRECT_CALLER_CENSUS.json');assert(c['script_paths_enumerated'],len(c['references']),c['production_references'],c['probe_references'])==(312,103,33,70);raw=git('grep','-n','-E','SkyLagoonPromenade|_sky_lagoon_promenade|_lagoon_promenade_ref|lagoon_promenade_targets',D,'--','scripts/');assert raw==(P/'DIRECT_REFERENCE_CENSUS.txt').read_bytes()and sha(raw)==c['independent_git_grep_sha256']
e=rd(P/'CASTLE_ENTRY_CALLERS.json');raw=git('grep','-n','_enter_castle_interior(',D,'--','scripts/');assert raw==(P/'CASTLE_ENTRY_CALLERS.txt').read_bytes()and sha(raw)==e['raw_sha256'];assert(e['production_calls'],e['definitions'],e['probe_calls'])==(7,1,10)
old=(O/'painted_gate.gd').read_text(encoding='utf-8');base=(P/'baseline_gate.gd').read_text(encoding='utf-8');assert base==old.replace('load(PAINTED_CUE) as Texture2D','_gate_cue_texture()')+'\nfunc _gate_cue_texture() -> Texture2D:\n\treturn null\n';new=(P/'painted_gate.gd').read_text(encoding='utf-8');assert old[old.index('func _tick_target_affordances('):].rstrip()==new[new.index('func _tick_target_affordances('):new.index('func _gate_cue_texture(')].rstrip();assert new.index('node.set_meta("interaction_id", id)')>new.index('push_warning(')
assert rd(P/'FIXTURE_SYNTAX_GATES.json')['status']=='PASS_BEFORE_NATIVE'and rd(P/'FIXTURE_SYNTAX_V1.json')['status']=='PASS_BEFORE_NATIVE';assert rd(P.parent/'CURRENT.json')['current_tally']=='r68_gate_missing_art/tally.json'
print('R68 evidence consistency PASS:4 repaired cases88checks;52PNG32bounded20excluded; walking-entry correction and raw baseline failures retained. Frozen5/history/unions and exact caller census preserved; no art/integration/QA11/device/child/owner credit.')
