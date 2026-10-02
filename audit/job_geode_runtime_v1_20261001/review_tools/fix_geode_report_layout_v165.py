from pathlib import Path
import json,shutil
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
p=b/'audit/job_geode_runtime_v1_20261001/index.html'
s=p.read_text(encoding='utf-8')
extra='html{box-sizing:border-box}*,*:before,*:after{box-sizing:inherit}body{overflow-wrap:anywhere}.grid>*{min-width:0}.grid{grid-template-columns:repeat(auto-fit,minmax(min(100%,270px),1fr))}.phone img{max-width:min(100%,480px)}figure{margin-inline:0}'
assert extra not in s
p.write_text(s.replace('</style>',extra+'</style>',1),encoding='utf-8',newline='\n')
dest=b/'audit/job_geode_runtime_v1_20261001/review_tools/fix_geode_report_layout_v165.py'
shutil.copyfile(__file__,dest)
ip=b/'design/audit_impacts/job-geode-painted-runtime-20261001.json';d=json.loads(ip.read_text());d['files']=sorted(set(d['files'])|{dest.relative_to(b).as_posix()});ip.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Fixed narrow-card identifier overflow and constrained the phone-size image to its container.')
