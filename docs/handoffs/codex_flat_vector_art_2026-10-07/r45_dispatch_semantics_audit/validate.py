"""Integrity/replay for the published source-semantics evidence; no artwork acceptance."""
from pathlib import Path
import json, hashlib, subprocess, zipfile, importlib.util, sys
P=Path(__file__).resolve().parent;R=P.parents[3];O=P.parent/'r44_creature_route_caller_audit';B='e17c929d22fdf749fffb1ad2acdaeff7059c21a1'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
spec=importlib.util.spec_from_file_location('r45_replay',P/'classify_dispatch.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
d=rd(P/'DISPATCH_SEMANTICS.json');assert d['classifier_module_sha256']==sha((P/'classify_dispatch.py').read_bytes());assert d['native_class_index_sha256']==sha((P/'engine/evidence/NATIVE_CLASS_INDEX.json').read_bytes())
old,scripts,equiv,current=audit.load_current();assert len(equiv)==312 and len(d['records'])==493
assert {x['binding_id']:x['r44_record'] for x in d['records']}=={x['binding_id']:x for x in old['dispatch_sites']}
index=rd(P/'engine/evidence/NATIVE_CLASS_INDEX.json');assert len(index['classes'])==97;native={}
for x in index['classes']:
 raw=(P/'engine/evidence'/x['file']).read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256'];assert Path(x['file']).name.startswith('class_');n=json.loads(raw);native[n['class_name']]=n
resolver=audit.Resolver(scripts,native)
for x in d['records']:
 script,row=current[x['binding_id']];assert resolver.classify(script,row)==x['classification'],x['binding_id']
summary=d['summary']['non_test_candidates'];assert summary['raw_expressions']==257 and summary['constructor_expressions']==100 and summary['invocation_expressions']==157 and summary['invocations_with_known_selector']==100 and summary['invocations_with_unresolved_selector_or_receiver']==57
assert summary['categories']=={'CALLABLE_INVOCATION':57,'CONSTRUCTOR_NAMED_BINDING':63,'CONSTRUCTOR_EMPTY':37,'OBJECT_LITERAL_DISPATCH':98,'CALLABLE_DEFERRED_INVOCATION':2}
r95=d['summary']['r44_raw95_reconciliation'];assert r95['raw_rows']==95 and r95['categories']=={'CALLABLE_INVOCATION':55,'CONSTRUCTOR_EMPTY':37,'CALLABLE_DEFERRED_INVOCATION':2,'OBJECT_LITERAL_DISPATCH':1};assert set(r95['literal_rows_reclassified_as_callable_data'])=={'FVC-F7F7F606D4C9','FVC-FA4D60EB3BFC'}
ports=rd(P/'CALLBACK_PORTS.json');assert ports['unresolved_invocation_sites']==57 and len(ports['ports'])==39 and len({x['id'] for x in ports['ports']})==39
site_ids=[site['binding_id'] for port in ports['ports'] for site in port['invocation_sites']];assert len(site_ids)==len(set(site_ids))==57
expected={x['binding_id'] for x in d['records'] if not x['r44_record']['probe'] and x['classification']['invocation_expression'] and x['classification']['method_selector'] is None};assert set(site_ids)==expected
assert all(not x['complete_write_caller_value_closure'] for x in ports['ports'])
examples=rd(P/'CALLBACK_BINDING_EXAMPLES.json')['examples'];assert len(examples)==2 and {x['candidate_callback_method'] for x in examples}=={'_end_combat','_end_stuffie_battle'} and all(not x['global_closure_credit'] and x['cancel_payload']=='' for x in examples)
probe=rd(P/'engine/evidence/SEMANTIC_PROOF.json');result=rd(P/'engine/RESULT.json');launch=rd(P/'engine/LAUNCH.json');assert result['exit_code']==0 and result['sidecars_exact'] and result['sidecars_before_count']==result['sidecars_after_count']==4039 and result['source_bindings_unchanged'];assert result['normal_before']==result['normal_after']==probe['normal_before']==probe['normal_after'] and len(probe['normal_before'])==8
assert probe['errors']==[] and len(probe['checks'])==13 and all(x['pass'] for x in probe['checks']);assert probe['engine']['hash']=='ed1daf0bf001b61586d9930840f2f1394092c079' and probe['engine']['status']=='stable' and probe['engine']['build']=='official';assert not probe['game_instantiated'] and probe['art_captures']==0
for x in launch['source_bindings_before_launch']:assert sha((R/x['path']).read_bytes())==x['sha256']
archive=rd(P/'prior_engine/ARCHIVE_PROVENANCE.json');raw=(R/archive['archive']).read_bytes();assert len(raw)==archive['bytes'] and sha(raw)==archive['sha256'] and len(archive['members'])==105
with zipfile.ZipFile(R/archive['archive']) as z:
 for x in archive['members']:b=z.read(x['member']);assert len(b)==x['bytes'] and sha(b)==x['sha256']
 original=rd(P/'ENGINE_EVIDENCE_SCOPE.json');assert original['current_vs_prior_native_class_data_bytes_exact']
for name in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 cur=rd(P/name);old=rd(O/name)
 for key in ['pieces','entries','observations','supplemental_piece_records','current_context_sample_lanes']:
  if key in old:assert cur[key]==old[key],(name,key)
 assert cur['dispatch_semantics_audit']['current_effective_unresolved_invocation_sites']==57 and cur['dispatch_semantics_audit']['full_compositor_runtime_closures_added']==0
 if name=='tally.json':
  assert cur['historical_totals'][:-1]==old['historical_totals'] and cur['historical_totals'][-1]['immutable_final_byte_proof_revision']==B
  assert [cur[x] for x in ['accepted_removed','integrated','runtime_verified']]==[0,0,0]
  assert all(cur[x] is None for x in ['all_game_individual_piece_total','current_distinct_screen_total','regression_count'])
  assert cur['known_named_design_records_including_supplemental']==230 and cur['known_family_count_including_supplemental']==31
  ctx=cur['current_context'];assert ctx['exact_capture_count']==3821 and ctx['retained_native_capture_count']==ctx['retained_native_captures']==5504 and ctx['excluded_diagnostic_native_count']==1683
  assert ctx['effective_dispatch_invocation_sites']==157 and ctx['effective_unresolved_callback_invocation_sites']==57 and cur['current_context_sample_lanes']['unique_whole_drawing_samples']==3
assert not git('diff','--name-only',B,'--','assets','scripts','scenes','shaders','addons','project.godot').strip()
assert not list(P.rglob('*.png'))
for x in P.rglob('*.json'):assert x.stat().st_size<4*1024*1024,(x.name,x.stat().st_size)
sys.path.insert(0,str(R));from tools.audit_game_2d import _token_counts
assert _token_counts((R/'design/audit_impacts/flat-vector-dispatch-semantics-20261015.json').read_text(encoding='utf-8'))=={},'impact prose/file paths must not masquerade as API class tokens; no gate change allowed'
print('R45 PASS:493 raw expressions/312 exact scripts;157 non-test invocations/57 callback selector gaps/39 scoped groups;13 actual headless checks/97 metadata records/20 boundary tests separately gated;frozen230roles31families3samples0accepted/globalunknown')
