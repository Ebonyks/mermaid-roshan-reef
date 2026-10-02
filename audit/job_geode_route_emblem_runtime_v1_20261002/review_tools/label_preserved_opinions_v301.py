from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');live=b/'audit/job_artwork_refinement_live';f=b/'audit/job_geode_route_emblem_runtime_v1_20261002'
p=live/'all_items.html';s=p.read_text(encoding='utf-8')
s=s.replace('<p>${esc(q.evaluation)}</p>','<p><strong>Recorded evaluation:</strong> ${esc(q.evaluation)}</p>')
s=s.replace('Later individual refinement</a><br>','Recorded individual refinement</a><br>')
s=s.replace("else if(c.binding_match===false||(q.id.startsWith('GEO-USE-')&&!stamp.geode_capture_boundary_match)){q.current_mounted_score=null;", "else if(c.binding_match===false||(q.id.startsWith('GEO-USE-')&&!stamp.geode_capture_boundary_match)){q.current_byte_status='MOUNTED_CONTEXT_CHANGED_REVIEW_REQUIRED';q.current_mounted_score=null;")
p.write_text(s,encoding='utf-8',newline='\n')
(b/'tmp/job_register_freshness_negative_v31/index.html').write_text(s.replace('<h1>Known job artwork: individual review register</h1>','<h1>QA-only injected stale-source negative control</h1>'),encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{(f/'review_tools'/Path(__file__).name).relative_to(b).as_posix()});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Preserved dated prose and current withheld score states explicitly labeled.')
