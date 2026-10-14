"""Validate additive source evidence and canonical invariants without runtime/art acceptance."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r36_menu_ornament_retirement';BASE='01f670d7ab4933fe2c2e6605bbca4ef2105f200f'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a,**kw):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE,**kw)
s=rd(P/'SOURCE_SUMMARY.json');inv=rd(P/'CURRENT_SOURCE_INVENTORY.json');rec=rd(P/'SOURCE_SCOPE_RECONCILIATION.json');gly=rd(P/'GLYPH_SCOPE_GAPS.json');graph=rd(P/'RESOURCE_CALLER_GRAPH.json');stress=rd(P/'SOURCE_STRESS.json');assert s['baseline']==BASE and s['parse_failures']==0 and not inv['parse_failure_records']
assert stress['case_count']==18 and all(x['result']=='PASS' for x in stress['cases']) and stress['scanner_sha256']==sha((P/'scan_source_inventory.py').read_bytes()) and stress['source_summary_sha256']==sha((P/'SOURCE_SUMMARY.json').read_bytes())
inputs=inv['input_files'];assert len(inputs)==s['input_source_and_sidecar_files'] and len({x['path'] for x in inputs})==len(inputs)
raw=git('cat-file','--batch',input=''.join(BASE+':'+x['path']+'\n' for x in inputs).encode());pos=0
for x in inputs:
 end=raw.index(b'\n',pos);head=raw[pos:end].split();size=int(head[-1]);pos=end+1;b=raw[pos:pos+size];pos+=size+1;assert size==x['bytes'] and sha(b)==x['raw_sha256'] and head[0].decode()==x['git_blob'],x['path']
assert pos==len(raw)
old=rd(H/'source_scopes.json')['scopes'];oldg=rd(H/'glyph_inventory.json')['sites'];assert [x['id'] for x in rec['rows']]==[x['id'] for x in old] and [x['id'] for x in gly['rows']]==[x['id'] for x in oldg]
fm={x['path']:x for x in inv['scripts']};assert len(fm)==s['parsed_gd_files'];assert len({(x['path'],x['scope']) for x in rec['additional_source_candidates']})==s['additional_source_candidate_scopes']
for x in rec['rows']:
 assert x['inventory_disposition_unchanged'] and x['runtime_acceptance'] is None and x['binding_status']=='CURRENT_FUNCTION_REBOUND';assert x['current_functions']==[f for f in fm[x['path']]['functions'] if f['name']==x['scope']]
assert rec['disposition_change_count']==0 and len(rec['rows'])==369 and len(gly['rows'])==348
assert Counter(x['binding'] for x in graph['calls'])==s['caller_binding_counts'] and len(graph['calls'])==s['caller_rows'];assert Counter(x['resolution'] for x in graph['literal_references'])==s['reference_resolution_counts'] and len(graph['literal_references'])==s['literal_reference_rows']
assert len(gly['current_symbol_candidates'])==s['current_symbol_string_rows'] and len(gly['additional_glyph_only_function_scopes'])==s['additional_glyph_only_function_scopes'];assert s['additional_source_candidate_scopes']==s['additional_nonprobe_source_candidate_scopes']+s['additional_probe_source_candidate_scopes']
assert s['individual_piece_total'] is None and s['accepted_removed']==0 and not s['mission_complete'];assert all(x['individual_piece_count'] is None and x['instance_count'] is None for x in rec['additional_source_candidates'])
for name,array in [('per_piece.json','pieces'),('scene_coverage.json','entries'),('CONGRUENCY_BACKLOG.json','observations')]:
 new=rd(P/name);previous=rd(O/name);assert new[array]==previous[array] and new['revision']=='FV-AUDIT-20261014-R37'
 assert new['current_source_inventory_reconciliation']['new_piece_ids']==0
new=rd(P/'per_piece.json');old=rd(O/'per_piece.json');assert new['supplemental_piece_records']==old['supplemental_piece_records'] and new['known_named_design_records_including_supplemental']==225 and new['known_family_count_including_supplemental']==30
T=rd(P/'tally.json');prev=rd(O/'tally.json')
for k in ['status_lanes','named_status_counts','supplemental_status_counts','current_partial_context_counts','current_context','current_partial_context_union','accepted_removed','integrated','runtime_verified','replaced','remaining_source_scopes_to_disposition','all_game_individual_piece_total','current_distinct_screen_total','regression_count']:
 assert T[k]==prev[k],k
assert T['historical_totals'][:-1]==prev['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE
assert T['all_game_individual_piece_total'] is None and T['accepted_removed']==T['integrated']==T['runtime_verified']==0 and T['current_context']['exact_capture_count']==3197 and T['current_context']['retained_native_capture_count']==4005
C=rd(H/'CURRENT.json');assert C['revision']==T['revision'] and C['current_tally']==P.name+'/tally.json' and not C['mission_complete'];assert 'r37_current_source_inventory/README.md' in (H/'README.md').read_text(encoding='utf-8')
prod=['assets','assets_src','scripts','scenes','shaders','addons','project.godot'];assert not git('diff','--name-only',BASE,'--',*prod).strip();assert not git('diff','--name-only','ecb9839a374d3260161a19d44039325d561a3509',BASE,'--',*prod[:1],*prod[2:]).strip()
par=rd(P/'SOURCE_PARITY.json');assert git('rev-parse','origin/dev').decode().strip()==par['reconciled_origin_dev'];assert git('diff','--name-only','origin/dev','--','assets','scripts','scenes','shaders','project.godot').decode().splitlines()==par['production_diff_vs_origin_dev']
mb=rd(P/'MACHINE_BASELINE.json')
for key in ['retained_full_validation','retained_ci']:
 x=mb[key];assert sha((R/x['path']).read_bytes())==x['sha256']
ctx=rd(P/'CONTEXT_PREREQUISITE.json');assert ctx['file_count']==17 and ctx['revision']==BASE and len(ctx['checks'])==17 and all(x['http_status']==200 for x in ctx['checks'])
allowed={x['path'] for x in inv['input_files']};assert all(x['path'] in allowed and x['bytes']>0 for x in inv['files']);assert len(inv['ignored_ancestor_directories'])>0
print('R37_ALL_OK: exact1510inputGitbytes;369/348 frozenIDs;qualifiedmethods;sourceunits/canonicalhistory/unknowns/acceptance/sourceparity preserved. No runtime/visual acceptance.')
