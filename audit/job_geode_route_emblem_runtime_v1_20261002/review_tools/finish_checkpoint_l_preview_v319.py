from pathlib import Path
import ast,json,shutil
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
root=Path('C:/Users/Peter/Documents/mermaid-roshan-reef')
f=r/'audit/job_geode_route_emblem_runtime_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
for n in ['current_review_landing_machine_pass_v318.png','current_register_machine_pass_v318.png']:shutil.copyfile(root/'tmp'/n,f/n)
p=f/'review_tools/seal_geology_checkpoint_l_v315.py';s=p.read_text();s=s.replace("'authorityv3','developmentv3'","'authorityv4','developmentv4'");ast.parse(s);p.write_text(s,encoding='utf-8',newline='\n');shutil.copyfile(p,root/'tmp'/p.name)
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=r/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in f.rglob('*') if x.is_file()});write(ip,d)
allow=r/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|set(d['files'])))
p=r/'design/05_DOC_LEDGER.md';rows=[line for line in p.read_text().splitlines() if line.startswith('| `audit/job_geode_route_emblem_runtime_v1_20261002/index.html`')];print('\n'.join(rows));assert len(rows)==1
print('Final review screenshots preserved; sealer will require final authority/development v4 receipts and repeat the current checks.')
