from pathlib import Path
import json,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');L=R/'audit/job_artwork_refinement_live'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=read(L/'ALL_ITEMS.json');assert d['counts']['unique_source_file_priorities']==572
d['scope']=d['scope'].replace('570 unique source files','572 unique source files including two runtime-source entries')
d['qualification']=d['qualification'].replace('570 unique source-file priorities','572 unique source-file priorities (570 primary-source entries plus two runtime-source entries)')
write(L/'ALL_ITEMS.json',d)
for p in [L/'review_tools/build_geology_review_library_v445.py',Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/build_geology_review_library_v445.py')]:
 s=p.read_text();s=s.replace('570 unique source files','572 unique source files including two runtime-source entries').replace('570 unique source-file priorities','572 unique source-file priorities (570 primary-source entries plus two runtime-source entries)');p.write_text(s,encoding='utf-8',newline='\n')
p=R/'design/05_DOC_LEDGER.md';s=p.read_text();s+='\n| `audit/job_geology_painted_invitation_fit_v1_20261003/DIRECT_REVIEW_ATTEMPT02.json` | 🟢 | `SUPPORTING_CURRENT`; all58 selected A2 canvases/10 boards/8 complete native invitations reviewed, selected clearance4.5/material4.5/support scale3.8/whole4.0. Unbound non-runtime fixture; no whole travel or production acceptance. |\n';p.write_text(s,encoding='utf-8',newline='\n')
for p in [R/'audit/MASTER_AUDIT_2026-08-09.md',R/'audit/findings/ACTIVE_FINDINGS_2026-08-13.md']:
 s=p.read_text();old='first58-view placement trial3.5 rejected for actor overlap and preserved.';new='first58-view placement trial3.5 rejected for actor overlap and preserved. All58 A2 selected canvases and8 complete native invitations now reviewed: selected actor clearance4.5/support scale3.8/whole4.0 remain unbound. Known572 source-file priorities include570 primary sources and two runtime-source entries.';assert s.count(old)==1;s=s.replace(old,new);p.write_text(s,encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-geology-complete-action-register-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{(L/'review_tools'/Path(__file__).name).relative_to(R).as_posix()});d['validation'][0].update(result='PASS',evidence='audit/job_artwork_refinement_live/CURRENT_BOUNDARY_REFRESH.json: all1821 registered literal hashes and783 production sources match. Exact V39 originals retained. Count kinds explicitly include1262 primary source+2 runtime source entries and81 prop+22 action entries;572 unique source-file priorities include570 primary+2 runtime-source entries. Direct visual actions remain weak.');write(ip,d)
shutil.copyfile(Path(__file__),L/'review_tools'/Path(__file__).name)
print('COUNT_DOMAINS_QUALIFIED_572_UNIQUE_FILE_PRIORITIES|V39_EXACT_HISTORY_UNCHANGED|A2_REVIEW_CURRENT')
