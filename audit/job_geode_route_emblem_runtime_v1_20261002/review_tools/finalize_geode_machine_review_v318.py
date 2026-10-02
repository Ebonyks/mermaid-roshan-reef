from pathlib import Path
import datetime,hashlib,json,re,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=r/'audit/job_geode_route_emblem_runtime_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ci=read(f/'full_ci_v2/RECEIPT.json')
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['overall_process_exit']==0 and ci['source_unchanged']
assert len(ci['source_checks'])==373 and len(ci['probe_results'])==82 and all(x['process_exit']==0 for x in ci['probe_results'])
assert all(hashlib.sha256((r/x['path']).read_bytes()).hexdigest()==x['before_sha256'] for x in ci['source_checks'])
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
prior=read(f/'full_ci_v1/RECEIPT.json');assert prior['status'].startswith('FAIL')
probe=r/'scripts/probe_opera_2d.gd';fix=read(f/'CREST_LOCATION_REPAIR_V303.json')
assert hashlib.sha256(probe.read_bytes()).hexdigest()==fix['failure']['probe_sha256']
assert (r/fix['fix']).read_bytes()==(r/fix['original_goal_metadata']).read_bytes()
fix.update(status='UNCHANGED_CREST_CONTRACT_REVALIDATED_FULL_SUITE2_PASS',checked_utc=now,current_full_suite='full_ci_v2/RECEIPT.json',current_probe_unchanged=True,current_frozen_source_count=373,current_probe_count=82)
write(f/'CREST_LOCATION_REPAIR_V303.json',fix)
review=read(f/'REVIEW.json');old='Full CI is separately pending on 373 frozen literal files;'
assert old in review['qualification'];review['qualification']=review['qualification'].replace(old,'Current unmodified official Godot 4.7.2 full suite 2 separately passes all 82 probes on 373 unchanged frozen literal files; raw diagnostics remain recorded;')
review['machine_verification']=dict(receipt='full_ci_v2/RECEIPT.json',status=ci['status'],probe_count=82,source_count=373,raw_diagnostic_count=ci['raw_diagnostic_count'],qualification='Exact literal local source machine evidence, separate from visual scores, hosted CI, device/child/owner acceptance or integration.')
write(f/'REVIEW.json',review)
p=f/'PLAN.json';d=read(p);d.update(status='CURRENT_ROUTE_DIRECT_REVIEW_RECORDED_UNMODIFIED_FULL_SUITE2_PASS_VISUAL_PRIORITIES_OPEN',machine_verified_utc=now);write(p,d)
p=f/'index.html';s=p.read_text();s=s.replace('Fresh full regression suite: pending on 373 frozen literal source files.',f'Current unmodified full suite 2: 82/82 probes pass, all 373 frozen literal sources unchanged; {ci["raw_diagnostic_count"]} raw diagnostics retained. Machine verification does not establish visual acceptance.')
p.write_text(s,encoding='utf-8',newline='\n')
p=r/'audit/job_review_v2_20261001/index.html';s=p.read_text();s=s.replace('Current unmodified full suite: PENDING. This is machine evidence; visual acceptance remains separate.',f'Current unmodified full suite 2: 82/82 probes pass; all 373 frozen sources unchanged. {ci["raw_diagnostic_count"]} raw diagnostics are retained. Visual, device, child and owner acceptance remain separate.')
p.write_text(s,encoding='utf-8',newline='\n')
for rel in ['audit/MASTER_AUDIT_2026-08-09.md','audit/findings/ACTIVE_FINDINGS_2026-08-13.md']:
 p=r/rel;s=p.read_text();old='second full suite pending on 373 frozen literal sources.';assert old in s;s=s.replace(old,f'second unmodified official Godot 4.7.2 full suite passes 82/82 with all 373 frozen literal sources unchanged; {ci["raw_diagnostic_count"]} raw diagnostics retained.',1);p.write_text(s,encoding='utf-8',newline='\n')
p=r/'design/05_DOC_LEDGER.md';lines=p.read_text().splitlines()
for i,line in enumerate(lines):
 if line.startswith('| `audit/job_geode_route_emblem_runtime_v1_20261002/index.html`'):
  lines[i]=line.replace('full suite pending','full suite 2 passes 82/82 on 373 unchanged literal sources').replace('full CI pending','full CI 2 passes 82/82 on 373 unchanged literal sources')
p.write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
for rel in ['audit/job_artwork_refinement_live/all_items.html','audit/job_artwork_refinement_live/index.html']:
 p=r/rel;s=p.read_text();assert 'id="current-route-reports-v318"' not in s
 i=s.index('</h1>')+len('</h1>');s=s[:i]+'<p id="current-route-reports-v318"><a href="../job_review_v2_20261001/index.html">Current illustrated review and geode route evidence</a> · <a href="../job_wash_root_remaining_sequences_v1_20261002/index.html">Complete dated washing-route review</a>. All eight preserved WASH cases now have direct frame review; current washing rerender and repair remain open.</p>'+s[i:];p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
p=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(p);d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in f.rglob('*') if p.is_file()}|{'audit/job_artwork_refinement_live/index.html','audit/job_artwork_refinement_live/all_items.html'});d['acceptance_gaps']=d['acceptance_gaps'].replace('Fresh fullCI pending373 source files',f'Unmodified current fullCI2 passes82/82 on373 unchanged literal files, {ci["raw_diagnostic_count"]} raw diagnostics retained');write(p,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(d['files'])))
print(json.dumps(dict(status=ci['status'],probes=82,frozen_source_files=373,source_unchanged=True,raw_diagnostics=ci['raw_diagnostic_count'],prior_failure_preserved=True,existing_probe_unchanged=True)))
