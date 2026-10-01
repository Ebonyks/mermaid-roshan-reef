from pathlib import Path
import hashlib,json,re,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
family=r/'audit/job_review_v2_20261001'
ci=json.loads((family/'full_ci_candidate_retry_v2/RECEIPT.json').read_text(encoding='utf-8'))
assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE' and ci['source_unchanged']
native=json.loads((r/'audit/day_two_wash_complete_action_v1_20261001/root_route_attempt_03/REVIEW_V3.json').read_text(encoding='utf-8'));assert native['frames']==2074
counts=json.loads((r/'audit/job_artwork_refinement_live/ALL_ITEMS.json').read_text(encoding='utf-8'))['counts']
p=family/'index.html';s=p.read_text(encoding='utf-8')
s=re.sub(r'Search[\d,]+ known source/pose/prop entries',f"Search{counts['registered_items']:,} known source/pose/prop entries",s)
s=re.sub(r'contains\d+ source priorities',f"contains{counts['inclusive_current_source_priorities']} source priorities",s)
s=re.sub(r'catalogues\d+ source files',f"catalogues{counts['unique_source_files']} source files",s)
section='<section><h2>Washing approach and consecutive key</h2><p><a href="../day_two_wash_complete_action_v1_20261001/root_route_attempt_03/index.html">Every one of2,074 naturally timed native viewport-route frames</a>: all8 unchanged-source training/story-catalog process cases pass. Four doctor keys directly reviewed retain workflow2.7, spatial contact2.3 and surface2.9. The remaining native frames, full Main/menu/story arrival, target-device, child and owner acceptance remain open.</p><p><a href="../../assets_src/imagegen/day2_doctor_wash_motion_v1_20261001/index.html">New consecutive hand-rubbing source</a> reaches4.5 as an unbound full-character draft. Exact prompt/input/native hashes and neutral alpha reviews are retained. Actual sink contact and continuous action are not passed.</p></section>'
assert 'Washing approach and consecutive key' not in s;s=s.replace('</main>',section+'</main>');p.write_text(s,encoding='utf-8',newline='\n')
p=r/'audit/MASTER_AUDIT_2026-08-09.md';s=p.read_text(encoding='utf-8')
line=next(x for x in s.splitlines() if x.startswith('Known individual job-art register'))
new=line.replace('1149 source files','1150 source files').replace('1427 addressable entries','1428 addressable entries').replace('554 source opinions','555 source opinions')
s=s.replace(line,new)
note='Viewport washing route supplement (2026-10-01): [all2,074 naturally timed native frames](day_two_wash_complete_action_v1_20261001/root_route_attempt_03/index.html) preserve8 actual viewport-touch approach/open/hold/advance process cases with unchanged sources and no star awards. Four doctor keys directly reviewed confirm workflow2.7/spatial contact2.3/surface2.9; remaining frames, full Main/menu/story arrival and target-device/child/owner acceptance are open. [One consecutive source key](../assets_src/imagegen/day2_doctor_wash_motion_v1_20261001/index.html) reaches an unbound source-only4.5, preserving exact input/prompt hashes and true-alpha interpretation. Existing painted sink reuse remains next. [Impact](../design/audit_impacts/job-review-separate-v2-20261001.json). No finding closure or complete-action pass.\n\n'
assert 'Viewport washing route supplement (2026-10-01):' not in s;s=s.replace('## 0. Planning entry\n','## 0. Planning entry\n\n'+note,1);p.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,family/'review_tools/executed_prepare_checkpoint_links_and_stage_v26.py')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
d['files']=sorted(set(d['files'])|{p.relative_to(r).as_posix() for p in family.rglob('*') if p.is_file()}|{'audit/job_review_v2_20261001/CURRENT_B_FILES_V1.json'})
impact.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
paths={p for p in d['files'] if (r/p).is_file()}
assert all(not p.startswith(('.git/','.secrets/','.aws/','.codex/','.claude/','.github/')) and Path(p).name.lower() not in {'agents.md','security.md','claude.md'} for p in paths)
stage=r/'tmp/v2_exact_owned_stage_v26.bin';stage.write_bytes(b'\0'.join(p.encode() for p in sorted(paths))+b'\0')
with (r/'tmp/v2_stage_v26.stdout.log').open('wb') as stdout,(r/'tmp/v2_stage_v26.stderr.log').open('wb') as stderr:
 result=subprocess.run(['git','add','-f','--sparse','--pathspec-from-file='+str(stage),'--pathspec-file-nul'],cwd=r,stdout=stdout,stderr=stderr)
assert result.returncode==0,(r/'tmp/v2_stage_v26.stderr.log').read_text(encoding='utf-8',errors='replace')[-2000:]
print(json.dumps(dict(status='EXACT_CURRENT_REVIEW_PATHS_STAGED',owned_refreshed_paths=len(paths),registered_items=counts['registered_items'],inclusive_source_priorities=counts['inclusive_current_source_priorities'],unassigned=counts['unreviewed_current_source'],current_B_file_index='Owned path recorded only; index generation pending.',publication='Not committed/pushed yet; no currentB remote acceptance.')))
