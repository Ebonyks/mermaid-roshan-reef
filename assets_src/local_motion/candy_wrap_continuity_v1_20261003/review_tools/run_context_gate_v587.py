from pathlib import Path
import datetime,hashlib,json,subprocess,sys
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');G=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003/gates_v3';PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe';now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();sha=lambda raw:hashlib.sha256(raw).hexdigest()
commands={'authority':['tools/audit_document_authority.py'],'development':['tools/audit_development.py','--base','auto'],'document_tests':['-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'],'game2d':['tools/audit_game_2d.py','--regression-gate']}
label=sys.argv[1];assert label in commands;start=now();cmd=[PY,'-X','utf8','-B',*commands[label]]
r=subprocess.run(cmd,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=1800)
(G/(label+'.stdout.log')).write_bytes(r.stdout);(G/(label+'.stderr.log')).write_bytes(r.stderr)
receipt=dict(status='PASS' if r.returncode==0 else 'FAIL',command=cmd,working_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip(),exit_code=r.returncode,started_utc=start,finished_utc=now(),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr),review_source_snapshot='assets_src/local_motion/candy_wrap_continuity_v1_20261003/gates_v3/CANDIDATE_CONTEXT_SOURCE_V587.json',snapshot_sha256=sha((G/'CANDIDATE_CONTEXT_SOURCE_V587.json').read_bytes()),qualification='Exact actual process result/raw streams on expanded review working tree. Structural/no-regression evidence only; strict zero-2D, visual/action/owner acceptance independent.')
(G/(label+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(label=label,exit_code=r.returncode,stdout_tail=r.stdout.decode(errors='replace')[-1300:],stderr_tail=r.stderr.decode(errors='replace')[-600:])));sys.exit(r.returncode)
