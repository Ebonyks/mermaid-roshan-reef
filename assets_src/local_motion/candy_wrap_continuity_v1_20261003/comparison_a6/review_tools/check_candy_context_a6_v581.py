from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');Q=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a6'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
cmd=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(Q/'review_tools/queue_candy_context_fold_a6_v580.py'),'--check']
start=now();r=subprocess.run(cmd,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
(Q/'checks/admission.stdout.log').write_bytes(r.stdout);(Q/'checks/admission.stderr.log').write_bytes(r.stderr)
d=dict(status='PASS' if r.returncode==0 else 'FAIL',command=cmd,started_utc=start,finished_utc=now(),exit_code=r.returncode,manifest_sha256=sha(Q/'MANIFEST.json'),stdout_sha256=sha(Q/'checks/admission.stdout.log'),stderr_sha256=sha(Q/'checks/admission.stderr.log'),qualification='Actual exact developed check-only process; no render or action acceptance.')
(Q/'checks/ADMISSION_RECEIPT.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,Q/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';impact=json.loads(ip.read_text(encoding='utf-8-sig'));impact['files']=sorted(set(impact['files'])|{p.relative_to(B).as_posix() for p in Q.rglob('*') if p.is_file()});impact['validation'].append(dict(command='Exact A6 developed source/input/prompt/workflow admission',result=d['status'],evidence=(Q/'checks/ADMISSION_RECEIPT.json').relative_to(B).as_posix()+'; actual raw process streams.'))
ip.write_text(json.dumps(impact,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print(r.stdout.decode('utf-8',errors='replace'),end='');print(r.stderr.decode('utf-8',errors='replace'),end='');raise SystemExit(r.returncode)
