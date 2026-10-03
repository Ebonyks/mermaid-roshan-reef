from pathlib import Path
import collections, datetime, hashlib, json, re
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'audit/job_final_action_consistency_v1_20261003';G=P/'gates_v1';IP=B/'design/audit_impacts/job-final-action-consistency-20261003.json'
sha=lambda data:hashlib.sha256(data).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def put(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
contract=read(P/'PRESENTATION_CONTRACT.json');coverage=read(P/'PHASE_COVERAGE.json');rows=coverage['rows']
assert contract==read(B/'design/animation/JOB_FINAL_ACTION_PRESENTATION_V1.json')
assert len(rows)==115 and len({r['id'] for r in rows})==115
assert coverage['counts']['base_phases']==61 and coverage['counts']['enabled_plan_instances']==21 and coverage['counts']['birthday_catalog_phases']==33
assert all(r['runtime_final_action_acceptance'] is None and r['presentation_migration']=='PENDING' for r in rows)
assert contract['resolution']['background_native_minimum_per_playable_screen']==[2048,2048]
assert contract['implementation']['runtime_changed'] is False and contract['implementation']['geometry'] is None and contract['implementation']['common_timing'] is None
assert len(contract['sequence'])==7 and contract['sequence'][3]['beat']=='finish'
for r in coverage['source_records']:assert sha((B/r['path']).read_bytes())==r['sha256']
boundary=read(P/'PRODUCTION_BOUNDARY.json');assert len(boundary['members'])==783
for r in boundary['members']:assert sha((B/r['path']).read_bytes())==r['sha256'],r['path']
for r in read(P/'REGISTER_BOUNDARY_BEFORE.json')['files']:assert sha((B/r['path']).read_bytes())==r['sha256'],r['path']
previous=(P/'previous_library_index.html').read_text();current=(B/'audit/job_artwork_refinement_live/index.html').read_text();links=lambda t:collections.Counter(re.findall(r'<a\b[^>]*href="([^"]+)"',t));oldlinks=links(previous);newlinks=links(current);assert all(newlinks[k]>=v for k,v in oldlinks.items())
refs=read(P/'ILLUSTRATION_REFERENCES.json')['images'];page=(P/'index.html').read_text();assert len(re.findall(r'<tr data-career=',page))==115 and len(re.findall(r'<img ',page))==4
for r in refs:assert sha((B/r['path']).read_bytes())==r['sha256']
authority=read(P/'AUTHORITY_START.json')['authority'];rules=read(IP)['rules'];lang=(B/'design/06_COMPREHENSIVE_DESIGN_LANGUAGE.md').read_text();assert all('`'+r+'`' in lang for r in rules)
put(P/'STRUCTURAL_VERIFY.json',dict(status='PASS_SOURCE_COUNTS_IDS_NULL_ACCEPTANCE_RESOLUTION_BOUNDARIES_REFERENCES_AND_LINK_PRESERVATION',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),planned_rows=115,unchanged_production_members=783,unchanged_register_members=len(read(P/'REGISTER_BOUNDARY_BEFORE.json')['files']),unchanged_native_image_references=4,all_old_library_links_preserved=True,browser_report_review='PENDING_LOCAL_PREVIEW_ACCESS',runtime_acceptance=None,qualification='Static/source checks only. Browser protocol file: is blocked; automatic approval rejected expanding preview access. No circumvention attempted.'))
runner=(B/'assets_src/imagegen/candy_wrap_transition_keys_v1_20261003/review_tools/run_transition_gate_v672.py').read_text().replace('assets_src/imagegen/candy_wrap_transition_keys_v1_20261003','audit/job_final_action_consistency_v1_20261003').replace('CANDIDATE_TRANSITION_SOURCE_V672.json','CANDIDATE_SOURCE.json')
runner=runner.replace("'register_parts':['audit/job_artwork_refinement_live/review_tools/test_register_parts_v51.py']","'register_parts':['audit/job_artwork_refinement_live/review_tools/test_register_parts_v51.py']")
path=P/'review_tools/run_consistency_gate_v683.py';path.write_text(runner,encoding='utf-8',newline='\n')
copy=P/'review_tools'/Path(__file__).name;copy.write_bytes(Path(__file__).read_bytes())
G.mkdir(exist_ok=True);impact=read(IP)
impact['files']=sorted(set(impact['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()}|{(G/(label+suffix)).relative_to(B).as_posix() for label in ['authority','development','document_tests','game2d','register_parts'] for suffix in ['.stdout.log','.stderr.log','.receipt.json']}|{(G/'CANDIDATE_SOURCE.json').relative_to(B).as_posix()})
impact['validation'].append(dict(command='Source-derived consistency/resolution/boundary/link checks',result='PASS',evidence='audit/job_final_action_consistency_v1_20261003/STRUCTURAL_VERIFY.json'))
impact['validation'].append(dict(command='Actual browser review of new report',result='PENDING',evidence='Local preview path addition rejected by automatic approval review; file: browser protocol blocked. No workaround or permission bypass.'))
put(IP,impact)
members=[]
for name in impact['files']:
 p=B/name
 if p.is_file() and not name.startswith(G.relative_to(B).as_posix()+'/'):members.append(dict(path=name,sha256=sha(p.read_bytes()),bytes=p.stat().st_size))
put(G/'CANDIDATE_SOURCE.json',dict(baseline=impact['baseline'],frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),member_count=len(members),members=members,qualification='Exact planning/source/library text before structural gates. Gate/impact/publication metadata and any later QA evidence sealed separately.'))
print(json.dumps(dict(status='READY_FOR_GATES',source_members=len(members),planned_rows=115,production_783_unchanged=True,scores_unchanged=True,browser_pending=True)))
