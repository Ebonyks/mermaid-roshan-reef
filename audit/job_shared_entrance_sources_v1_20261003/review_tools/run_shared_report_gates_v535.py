from pathlib import Path
import concurrent.futures,datetime,json,shutil,subprocess,sys,time
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');c=b/'audit/job_shared_entrance_sources_v1_20261003';folder=c/'gates_v1';py='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
def write(p,d):
 n=p.with_name(p.name+'.new');n.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');n.replace(p)
commands={'authority':[py,'-X','utf8','-B','tools/audit_document_authority.py'],'development':[py,'-X','utf8','-B','tools/audit_development.py','--base','auto'],'document_tests':[py,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'],'game2d':[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate']}
if sys.argv[1:]==['--prepare']:
 assert not folder.exists();folder.mkdir();shutil.copyfile(__file__,c/'review_tools/run_shared_report_gates_v535.py')
 for label in commands:
  write(folder/(label+'.receipt.json'),{'status':'PENDING'});(folder/(label+'.stdout.log')).write_bytes(b'');(folder/(label+'.stderr.log')).write_bytes(b'')
 ip=b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json';d=json.loads(ip.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in c.rglob('*') if p.is_file()});write(ip,d);print('Prepared fresh report gates without changing validators.');sys.exit(0)
assert sys.argv[1:]==['--run'] and all(json.loads((folder/(label+'.receipt.json')).read_text())['status']=='PENDING' for label in commands)
def run(label,args):
 start=time.monotonic();p=subprocess.run(args,cwd=b,capture_output=True,timeout=1800,creationflags=subprocess.CREATE_NO_WINDOW)
 (folder/(label+'.stdout.log')).write_bytes(p.stdout);(folder/(label+'.stderr.log')).write_bytes(p.stderr)
 r={'status':'PASS' if p.returncode==0 else 'FAIL','exit':p.returncode,'command':args,'elapsed_seconds':time.monotonic()-start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'qualification':'Machine structural/regression evidence only; exact raw streams preserved, no visual or strict-zero 2D acceptance.'};write(folder/(label+'.receipt.json'),r);print(label,r['status'],flush=True);return label,r
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(lambda v:run(*v),commands.items()))
ip=b/'design/audit_impacts/job-shared-entrance-source-review-20261003.json';d=json.loads(ip.read_text(encoding='utf-8'))
for label,r in results:d['validation'].append({'command':' '.join(commands[label]),'result':r['status'],'evidence':(folder/(label+'.receipt.json')).relative_to(b).as_posix()})
write(ip,d);sys.exit(0 if all(r['status']=='PASS' for _,r in results) else 1)
