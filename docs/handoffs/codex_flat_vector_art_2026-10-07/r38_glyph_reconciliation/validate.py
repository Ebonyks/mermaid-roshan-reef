"""Exact glyph source and additive canonical invariant checks; no visual acceptance."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r37_current_source_inventory';BASE='8f48a0003a8a098658a3414414bd3da3c94f29c2'
def rd(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a,**kw):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE,**kw)
s=rd(P/'GLYPH_SUMMARY.json');d=rd(P/'GLYPH_RECONCILIATION.json');src=rd(P/'GLYPH_SOURCE_FILES.json');stress=rd(P/'GLYPH_STRESS.json');old=rd(H/'glyph_inventory.json');assert s['baseline']==BASE and s['historical_source_baseline']==old['baseline'] and d['remaining_source_provenance_gap_count']==0
assert [x['id'] for x in d['rows']]==[x['id'] for x in old['sites']] and len(d['rows'])==348 and d['source_current_glyph_rows']==347 and d['retained_bounded_source_statement_retirements']==1
assert stress['case_count']==14 and all(x['result']=='PASS' for x in stress['cases']) and stress['reconciler_sha256']==sha((P/'reconcile_glyphs.py').read_bytes()) and stress['glyph_summary_sha256']==sha((P/'GLYPH_SUMMARY.json').read_bytes())
inputs=src['inputs'];assert len(inputs)==76 and len({(x['revision'],x['path']) for x in inputs})==76;req=''.join(x['revision']+':'+x['path']+'\n' for x in inputs).encode();out=git('cat-file','--batch',input=req);data={};pos=0
for x in inputs:
 end=out.index(b'\n',pos);head=out[pos:end].split();size=int(head[-1]);pos=end+1;b=out[pos:pos+size];pos+=size+1;assert size==x['bytes'] and sha(b)==x['sha256'] and head[0].decode()==x['git_blob'];data[(x['revision'],x['path'])]=b.decode('utf-8-sig')
assert pos==len(out);assert sum(x['ordered_literal_count_total'] for lane in ['historical_files','current_files'] for x in src[lane])==34555 and sum(len(x['strings']) for lane in ['historical_files','current_files'] for x in src[lane])==1003
for lane in ['historical_files','current_files']:
 revision=s['historical_source_baseline'] if lane=='historical_files' else BASE
 for f in src[lane]:
  assert f['retained_unicode_literal_count']==len(f['strings']) and [x['start_pos'] for x in f['strings']]==sorted(x['start_pos'] for x in f['strings'])
  for x in f['strings']:assert data[(revision,f['path'])][x['start_pos']:x['end_pos']]==x['literal'],(f['path'],x['line'])
for x in d['rows']:
 assert x['runtime_occurrence_count'] is None and x['visible_art_piece_count'] is None and x['accepted_removed']==0 and x['binding']['historical']
 for lane,revision in [('historical',s['historical_source_baseline'])]:
  for z in x['binding'][lane]:assert data[(revision,x['path'])][z['start_pos']:z['end_pos']]==z['literal']
 for group in x['binding']['current_candidates']:
  assert len({z['start_pos'] for z in group})==len(group) and [z['start_pos'] for z in group]==sorted(z['start_pos'] for z in group)
  for z in group:assert data[(BASE,x['path'])][z['start_pos']:z['end_pos']]==z['literal'] and z['scope']==x['binding']['historical'][0]['scope']
assert Counter(x['binding']['status'] for x in d['rows'])==s['source_binding_counts'];assert s['individual_piece_total'] is None and s['current_distinct_screen_total'] is None and s['new_accepted_artwork_removals']==0 and not s['mission_complete']
ret=rd(P/'RETAINED_SOURCE_RETIREMENT.json');assert ret['new_source_retirements']==ret['accepted_removed']==0 and len(ret['records'])==1
x=ret['records'][0];assert x['id']=='FVG-868EDDAC69D5' and x['known_piece_id']=='FV-619466CA433F';assert sha(git('show',x['retirement_payload_revision']+':'+x['path']))==x['retired_source_sha256']==x['current_source_sha256'];assert sha(git('show',x['before_revision']+':'+x['path']))==x['before_sha256'];assert sha(x['exact_diff_utf8'].encode())==x['diff_sha256_utf8']
b=rd(P/'GLYPH_ROLE_BACKLOG.json');assert b['glyph_rows']==347 and {x['glyph_id'] for x in b['items']}=={x['id'] for x in d['rows'] if x['binding']['current_candidates']};assert all(x['role_criticality']=='UNREVIEWED' and x['visible_art_piece_count'] is None and not x['context_review_complete'] for x in b['items'])
for name,array in [('per_piece.json','pieces'),('scene_coverage.json','entries'),('CONGRUENCY_BACKLOG.json','observations')]:
 a=rd(P/name);z=rd(O/name);assert a[array]==z[array] and a['revision']=='FV-AUDIT-20261014-R38' and a['current_source_inventory_reconciliation']==z['current_source_inventory_reconciliation']
a=rd(P/'per_piece.json');z=rd(O/'per_piece.json');assert a['supplemental_piece_records']==z['supplemental_piece_records'] and a['known_named_design_records_including_supplemental']==225 and a['known_family_count_including_supplemental']==30
T=rd(P/'tally.json');prev=rd(O/'tally.json')
for k in ['status_lanes','named_status_counts','supplemental_status_counts','current_partial_context_counts','current_context','current_partial_context_union','accepted_removed','integrated','runtime_verified','replaced','remaining_source_scopes_to_disposition','all_game_individual_piece_total','current_distinct_screen_total','regression_count']:assert T[k]==prev[k],k
assert T['historical_totals'][:-1]==prev['historical_totals'] and T['historical_totals'][-1]['immutable_final_byte_proof_revision']==BASE;assert T['accepted_removed']==T['integrated']==T['runtime_verified']==0 and T['all_game_individual_piece_total'] is None
C=rd(H/'CURRENT.json');assert C['revision']==T['revision'] and C['current_tally']==P.name+'/tally.json' and not C['mission_complete'];assert 'r38_glyph_reconciliation/README.md' in (H/'README.md').read_text(encoding='utf-8')
prod=['assets','assets_src','scripts','scenes','shaders','addons','project.godot'];assert not git('diff','--name-only',BASE,'--',*prod).strip();assert not git('diff','--name-only','ecb9839a374d3260161a19d44039325d561a3509',BASE,'--',*prod[:1],*prod[2:]).strip()
par=rd(P/'SOURCE_PARITY.json');assert git('rev-parse','origin/dev').decode().strip()==par['reconciled_origin_dev'];assert git('diff','--name-only','origin/dev','--','assets','scripts','scenes','shaders','project.godot').decode().splitlines()==par['production_diff_vs_origin_dev']
for key in ['retained_full_validation','retained_ci']:
 x=rd(P/'MACHINE_BASELINE.json')[key];assert sha((R/x['path']).read_bytes())==x['sha256']
ctx=rd(P/'CONTEXT_PREREQUISITE.json');assert ctx['file_count']==48 and ctx['revision']==BASE and len(ctx['checks'])==48 and all(x['http_status']==200 for x in ctx['checks'])
import importlib.util
_bspec=importlib.util.spec_from_file_location('bounded',P/'bounded_json.py');bounded=importlib.util.module_from_spec(_bspec);_bspec.loader.exec_module(bounded)
bstress=rd(P/'BOUNDED_JSON_STRESS.json');assert bstress['case_count']==11 and all(x['result']=='PASS' for x in bstress['cases']) and bstress['helper_sha256']==sha((P/'bounded_json.py').read_bytes())
format_repair=rd(P/'SOURCE_FORMAT_REPAIR.json');assert not format_repair['auditor_or_manifest_changed']
for x in format_repair['records']:
 raw=bounded.logical_bytes(R/x['path']);assert raw==git('show',x['revision']+':'+x['path']) and sha(raw)==x['sha256'] and len(raw)==x['bytes']
 for part in x['physical_files']:
  b=(R/part['path']).read_bytes();assert len(b)==part['bytes'] and sha(b)==part['sha256'] and len(b)<4*1024*1024
assert not git('diff','--name-only',BASE,'--','tools/audit_game_2d.py','tools/game_2d_migration_manifest.json').strip()
print('R38_ALL_OK:348 frozenIDs/sourcepositions;exact76Gitinputs/347current+1prior source retirement;no source/context/acceptance count conflation;225/30/captures/primitive dispositions preserved. Runtime/role/font/device/child/owner open.')
