from pathlib import Path
import json,datetime,subprocess,concurrent.futures,hashlib,time
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');G=R/'tmp/geology_precommit_u_v475';G.mkdir(exist_ok=False);py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
commands=[('authority',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('game2d',[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'])]
def run(row):
 label,args=row;start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic();outs=[G/(label+'.'+ext) for ext in ['stdout.log','stderr.log']]
 with outs[0].open('wb') as out,outs[1].open('wb') as err:result=subprocess.run(args,cwd=R,stdout=out,stderr=err,timeout=1800,creationflags=subprocess.CREATE_NO_WINDOW)
 receipt=dict(status='PASS' if result.returncode==0 else 'FAIL_PRESERVED',command=args,process_exit=result.returncode,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,stdout_sha256=hashlib.sha256(outs[0].read_bytes()).hexdigest(),stderr_sha256=hashlib.sha256(outs[1].read_bytes()).hexdigest(),qualification='Fresh final scoped staged tree check. No source/motion/strict-zero2D/device/child/owner acceptance transfer.')
 (G/(label+'.receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(label,receipt['status'],flush=True);return label,receipt
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,commands))
assert all(x['status']=='PASS' for _,x in results),[(label,x['status']) for label,x in results]
print('U_FINAL_STAGED_PRECOMMIT_GATES_ALL_PASS')
