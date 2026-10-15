"""Validate R62 source reconstruction, narrow reused-book credit and untouched historical representations."""
from pathlib import Path
import json,hashlib,subprocess,importlib.util
P=Path(__file__).resolve().parent;R=P.parents[3];H=P.parent;O=H/'r61_critter_saved_reuse';B='d0f2e17433557d5775463f44576fe7ebf03cf3df'
def rd(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
spec=importlib.util.spec_from_file_location('catalogue_origin62_validation',P/'audit_catalogue_origin.py');M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M);outputs={};old_write=M.write
try:
 M.write=lambda path,data:outputs.setdefault(Path(path).name,data);summary=M.analyze(P)
finally:M.write=old_write
assert summary==rd(P/'ANALYSIS_SUMMARY.json')
for name,data in outputs.items():assert json.loads(json.dumps(data))==rd(P/name),name
orig=rd(P/'CATALOGUE_ORIGINS.json');assert orig['frozen_id_count']==176 and orig['origin_counts']=={'REGISTERED_STAGE_ROW':100,'AUDIT_AUTHORED_UI_OVERLAY':12,'REFERENCE_GAME_CATALOGUE_LABEL':60,'GIT_SCENE_PATH':4};assert not orig['original_published_collector']['executed']
for n in ['audit_register.py','build_index.py','build_review_packet.py']:assert(P/'historical_source'/(n+'.txt')).read_bytes()==git('show','5e5140fb0f0b636825354b6db8d28da0e9c07446:'+H.relative_to(R).as_posix()+'/'+n)
pre=rd(P/'CONTEXT_PREREQUISITE.json');assert(pre['files'],pre['bytes'])==(27,5178949)and pre['source_reference_sha256']==sha((P/'SOURCE_REFERENCES.json').read_bytes())
refs=rd(P/'DELIVERY_SOURCE_REFERENCES.json')['files'];assert len(refs)==153 and sum(x['bytes']for x in refs)==14450905 and len({(x['revision'],x['path'])for x in refs})==153
for rev in {x['revision']for x in refs}:
 rows=[x for x in refs if x['revision']==rev];raws=M.batch(R,rev,[x['path']for x in rows])
 for x in rows:assert raws[x['path']]is not None and sha(raws[x['path']])==x['sha256']and len(raws[x['path']])==x['bytes']and x['http_status']==200
c=rd(P/'CATALOGUE_SOURCE_BINDINGS.json');assert c['catalogue_rows']==60 and c['declared_source_host_paths']==105 and c['declared_source_host_evidence_paths']==108 and c['historical_evidence_references']==209 and c['unique_historical_path_hash_pairs']==170 and c['current_exact_raw_matches']==c['current_exact_lf_matches']==67;assert sum(not x['raw_match']for x in c['historical_evidence'])==142
union=rd(P/'CURRENT_CATALOGUE_CONTEXT_UNION.json');assert len(union['prior_partial_ids'])==85 and union['new_partial_ids']==['game.critters']and len(union['current_partial_ids'])==86 and'ui.collection'in union['prior_partial_ids'];assert(union['current_partial_count'],union['without_current_slice_count'],union['complete_count'],union['entry_count'],union['all_entries_still_incomplete'])==(86,90,0,176,176)
bind=rd(P/'CRITTER_ALIAS_BINDING.json');assert bind['partial_only']and not bind['acquisition_closed']and not bind['normal_route_closed']and bind['existing_book_states']==80 and bind['new_native_frames']==0;assert len(bind['original_saved_book_cases'])==4 and sum(x['checks']for x in bind['original_saved_book_cases'])==140
for k in ['QA11','device','child','owner']:assert bind[k]is None
rv=rd(P/'REVIEW.json');assert not rv['human_reviews']and not rv['new_context_visual_review_claim']and len(rv['original_native_direct_reinspections'])==4
for x in rv['original_native_direct_reinspections']:assert sha(git('show',x['revision']+':'+x['path']))==x['sha256']
s=rd(P/'SUMMARY.json');assert(s['known_roles'],s['families'],s['catalogue_partial'],s['catalogue_without_current_slice'],s['catalogue_complete'])==(240,32,86,90,0);assert(s['retained_bounded'],s['retained_excluded'],s['retained_native_events'])==(5097,2594,7691);assert s['new_alias_credits']==1 and s['reused_original_book_states']==80 and s['targeted_tests']==12
for k in ['new_native_files','new_bounded_contexts','new_excluded_diagnostics','passing_checks','new_roles','new_families','approved','integrated','runtime_verified_replacements','accepted_removed','generation_calls','new_drawing_samples']:assert s[k]==0
assert s['all_game_artwork_total']is None and s['distinct_screen_total']is None and s['regression_total']is None and not s['mission_complete']and not list(P.rglob('*.png'))
for n in ['per_piece.json','scene_coverage.json','tally.json','source_scopes.json','glyph_inventory.json']:assert(H/n).read_bytes()==git('show',B+':'+(H/n).relative_to(R).as_posix())
allowed={'revision','phase','publication','change_record','current_ci_snapshot'}
for n in ['per_piece.json','scene_coverage.json','tally.json','CONGRUENCY_BACKLOG.json']:
 a=rd(O/n);b=rd(P/n);assert b['revision']=='FV-AUDIT-20261015-R62'and b['catalogue_origin']['catalogue_partial']==86 and b['catalogue_origin']['catalogue_without_current_slice']==90 and b['catalogue_origin']['accepted_removed']==0
 for k,v in a.items():
  if k not in allowed:assert b[k]==v,(n,k)
assert(P/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()==(O/'CURRENT_PARTIAL_CONTEXT_UNION.json').read_bytes()
a=json.loads(git('show',B+':'+(H/'CURRENT.json').relative_to(R).as_posix()));b=rd(H/'CURRENT.json');routing={'revision','current_entry','current_per_piece','current_scene_coverage','current_tally','current_backlog','current_manifest','current_ci_evidence'};assert b['schema']==a['schema']and b['current_tally']=='r62_catalogue_origin/tally.json'
for k,v in a.items():
 if k not in routing:assert b[k]==v
assert not git('diff','--name-only',B,'--','scripts','scenes','assets','shaders','project.godot').strip();par=rd(P/'SOURCE_PARITY.json');assert not par['runtime_changed_paths']and par['no_new_godot_run']and par['old_frozen5_exact']and not par['normal_profile_read_or_write']
rep=rd(P/'REPRODUCTION_INPUTS.json');assert rep['analyzer_sha256']==sha((P/'audit_catalogue_origin.py').read_bytes())
print('R62_VALIDATED176origins60cataloguelabels108sourcepaths209refs67current142different;explicit saved-book subset86partial90without0complete;0newnative/art/removal;frozen history exact')
