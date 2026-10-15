from pathlib import Path
import json,hashlib,subprocess,re
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r43_mewsha_whole_trial';B='ccbe6d60e4021977c520844797d4d36086ad6e73'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
idx=rd(P/'CAPTURE_INDEX.json');assert len(idx['cases'])==6 and len(idx['captures'])==73
assert idx['summary']['bounded_art_context_credits']==0 and idx['summary']['excluded_native']==73
for x in idx['captures']:
 p=R/x['path'];b=p.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'] and list(Image.open(p).size)==x['aspect'] and not x['art_context_credit']
for c in idx['cases']:
 m=rd(R/c['manifest']['path']);launch=rd(R/c['launch']['path']);assert m['errors']==[] and m['normal_before']==m['normal_after'] and len(m['normal_before'])==8 and m['art_context_credits']==0
 assert m['engine']['major']==4 and m['engine']['minor']==7 and m['engine']['patch']==2 and m['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079' and m['engine']['status']=='stable' and m['engine']['build']=='official' and m['renderer']=='mobile' and m['quality']=='speedy'
 for x in launch['source_bindings_before_launch']:assert sha((R/x['path']).read_bytes())==x['sha256']
 log=(R/c['manifest']['path']).parents[1]/'native.log';assert not re.search(r'(?m)^ERROR:|SCRIPT ERROR|SHADER ERROR|Shader compilation failed|[|]FAIL',log.read_text(encoding='utf-8'))
 states={s['id']:s for s in m['states']};idle=states['promenade_idle'];care=states['promenade_care'];hall=states['Castle_idle']
 assert care['source_calls']['tick_canvas_care']>idle['source_calls']['tick_canvas_care'] and care['source_calls'].get('_tick_follower',0)==idle['source_calls'].get('_tick_follower',0)
 assert hall['source_calls'].get('_tick_room',0)==0 and not hall['Studio']['present']
 assert states['forced_Studio_build']['Studio']['present'] and not states['forced_Studio_cleanup']['Studio']['present'] and states['forced_battle_start']['battle']['present'] and not states['forced_battle_cancel']['battle']['present']
 assert states['forced_battle_cancel']['stuffie_wins']==idle['stuffie_wins']
 assert states['retained_exit_requests_reef']['game']=='level2' and states['retained_exit_requests_reef']['phase']=='promenade'
 assert states['private_reload_promenade']['companion_id']==m['identity']
 assert idle['follower']['present'] and not idle['camera3D']['present']
graph=rd(P/'SOURCE_CALL_GRAPH.json');s=graph['summary'];assert s==dict(parsed_files=312,non_test_candidate_files=168,target_call_sites=49,non_test_candidate_target_call_sites=29,probe_target_call_sites=20,non_test_candidate_dynamic_target_sites_unresolved=95,non_test_candidate_named_start_stuffie_calls=0,non_test_candidate_named_tick_room_calls=0)
for x in graph['files']:assert sha(git('show',B+':'+x['path']))==x['sha256']
assert len({x['binding_id'] for x in graph['qualified_calls']})==49
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 d=rd(P/name);old=rd(O/name)
 for key in ['pieces','entries','observations','supplemental_piece_records','current_context_sample_lanes']:
  if key in old:assert d[key]==old[key],(name,key)
 assert d['creature_route_caller_audit']['source_scope_ids']==rd(P/'PLAN.json')['source_scope_ids']
 assert d['creature_route_caller_audit']['full_compositor_runtime_closures_added']==0 and d['creature_route_caller_audit']['generation_calls']==0
 if name=='tally.json':
  assert d['historical_totals'][:-1]==old['historical_totals'] and d['historical_totals'][-1]['immutable_final_byte_proof_revision']==B
  assert [d[x] for x in ['accepted_removed','integrated','runtime_verified']]==[0,0,0]
  assert d['all_game_individual_piece_total'] is None and d['regression_count'] is None and d['current_distinct_screen_total'] is None
  ctx=d['current_context'];assert ctx['exact_capture_count']==3821 and ctx['retained_native_capture_count']==5504 and ctx['retained_native_captures']==5504 and ctx['excluded_diagnostic_native_count']==1683
  assert d['known_named_design_records_including_supplemental']==230 and d['known_family_count_including_supplemental']==31
  assert d['current_context_sample_lanes']['unique_whole_drawing_samples']==3
assert len(rd(P/'REVIEW.json')['ten_axis_comparison'])==10 and len(rd(P/'REVIEW.json')['direct_views'])==8
assert rd(P/'SIDECAR_GUARD.json')['all_equal'] and rd(P/'SIDECAR_GUARD.json')['before_count']==4039
for x in rd(P/'REVIEW.json')['source_references']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256']
assert not git('diff','--name-only',B,'--','assets','scripts','scenes','shaders','addons','project.godot').strip()
for f in P.rglob('*.json'):assert f.stat().st_size<4*1024*1024,(str(f),f.stat().st_size)
print('R44 PASS:6actual source-bound Mobile cases,73excluded captures,312ASTfiles/49calls/95unresolved dynamictargets;source/save/frozen history parity,230roles31families3samples0accepted/globalunknown')
