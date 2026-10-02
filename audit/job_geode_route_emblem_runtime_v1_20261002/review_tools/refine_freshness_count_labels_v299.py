from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
live=b/'audit/job_artwork_refinement_live';f=b/'audit/job_geode_route_emblem_runtime_v1_20261002'
html=live/'all_items.html';s=html.read_text(encoding='utf-8')
old="d.counts.inclusive_current_source_priorities=d.items.filter(q=>q.kind==='source'&&q.current_source_score!=null&&q.current_source_score<=4.5).length;"
new="d.counts.inclusive_current_source_priorities=d.items.filter(q=>!q.id.startsWith('GEO-USE-')&&q.current_source_score!=null&&q.current_source_score<=4.5).length;d.counts.unique_source_file_priorities=d.items.filter(q=>q.kind==='source'&&q.current_source_score!=null&&q.current_source_score<=4.5).length;d.counts.current_geode_mounted_priorities=d.items.filter(q=>q.id.startsWith('GEO-USE-')&&q.current_mounted_score!=null&&q.current_mounted_score<=4.5).length;"
assert s.count(old)==1;s=s.replace(old,new)
s=s.replace('${c.inclusive_current_source_priorities} current source priorities; ${c.unreviewed_current_source} current source reviews required.', '${c.inclusive_current_source_priorities} known source/cell/region priorities (${c.unique_source_file_priorities} unique source files); ${c.current_geode_mounted_priorities} additional current geode mounted priorities; ${c.unreviewed_current_source} source file reviews required.')
html.write_text(s,encoding='utf-8',newline='\n')
fixture=b/'tmp/job_register_freshness_negative_v31/index.html';fixture.write_text(s.replace('<h1>Known job artwork: individual review register</h1>','<h1>QA-only injected stale-source negative control</h1>'),encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{(f/'review_tools'/Path(__file__).name).relative_to(b).as_posix()});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Count labels distinguish676 known source/cell/region priorities,547 unique-source priorities and3 separate current mounted geode priorities; no saved opinions changed.')
