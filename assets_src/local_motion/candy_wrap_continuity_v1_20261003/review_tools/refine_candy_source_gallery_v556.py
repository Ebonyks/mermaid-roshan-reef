from pathlib import Path
import json,shutil,subprocess
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003';f=P/'review_tools/build_candy_local_review_v554.py';s=f.read_text(encoding='utf-8');assert "sources+='<div class=\"source-grid\">'" not in s
s=s.replace('for extra_attempt in [12,13]:',"sources+='<div class=\"source-grid\">'\nfor extra_attempt in [12,13]:",1).replace("script='const TAKES=","sources+='</div>'\nscript='const TAKES=",1)
n=f.with_name(f.name+'.v556_next');n.write_text(s,encoding='utf-8');n.replace(f);shutil.copyfile(f,B/'tmp/build_candy_local_review_v554.py');shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json';d=json.loads(ip.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{(P/'review_tools'/Path(__file__).name).relative_to(B).as_posix()});n=ip.with_name(ip.name+'.v556_next');n.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');n.replace(ip)
subprocess.run(['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(B/'tmp/build_candy_local_review_v554.py')],cwd=B,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
print('New whole poses paired in responsive source grid; full original pixels unchanged.')
