from pathlib import Path
import json,re,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
family=r/'audit/job_review_v2_20261001'
ci=json.loads((family/'full_ci_candidate_retry_v2/RECEIPT.json').read_text(encoding='utf-8'))
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged'] and len(ci['probe_results'])==82
counts=json.loads((r/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8'))['counts']
p=family/'index.html';s=p.read_text(encoding='utf-8')
s=re.sub(r'contains\d+ source priorities',f"contains{counts['inclusive_current_source_priorities']} source priorities",s)
s=re.sub(r'and\d+ unassigned current source opinions',f"and{counts['unreviewed_current_source']} unassigned current source opinions",s)
old='Initial V2 authority/development gates pass and the full suite records80/82 passing probes, with two process127 failures preserved. Both unchanged probes pass direct retries; the full suite remains failed.'
new='Initial V2 authority/development gates pass. The first complete run retains80/82 passing probes and two process127 failures; unchanged direct retries also remain inspectable. The <a href="full_ci_candidate_retry_v2/RECEIPT.json">unmodified complete V2 retry</a> now passes82/82 with all325 literal source files unchanged;51 raw engine diagnostics are preserved. This is local machine verification, not visual or hosted acceptance.'
assert old in s;s=s.replace(old,new)
s=s.replace('the failed full suite remains preserved','the first failed full suite remains preserved')
p.write_text(s,encoding='utf-8',newline='\n')
p=r/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text(encoding='utf-8')
line=next(x for x in s.splitlines() if x.startswith('Distinct V2 review checkpoint (2026-10-01):'))
old='Its first local full suite records80 passing probes and two process127 failures; both unchanged probes pass direct isolated retries, but the complete suite remains failed.'
assert old in line
new='Its first local full suite records80 passing probes and two process127 failures; both unchanged probes pass direct isolated retries. The [unmodified complete V2 retry](job_review_v2_20261001/full_ci_candidate_retry_v2/RECEIPT.json) now passes82/82 with all325 literal sources unchanged and51 raw diagnostics retained. This is local source-bound machine verification, not hosted, visual or owner acceptance.'
s=s.replace(line,line.replace(old,new));p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,family/'review_tools/executed_update_verified_review_state_v21.py')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in family.rglob('*') if p.is_file()})
impact.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(full_ci=ci['status'],probe_processes=82,unchanged_sources=325,raw_diagnostics=ci['raw_diagnostic_count'],counts=counts)))
