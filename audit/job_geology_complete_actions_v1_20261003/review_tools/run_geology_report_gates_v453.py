from pathlib import Path
import json,datetime,hashlib,shutil,subprocess,concurrent.futures,time
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');F=R/'audit/job_geology_complete_actions_v1_20261003';P=R/'audit/job_geology_painted_invitation_fit_v1_20261003';T=R/'assets_src/imagegen/geologist_specimen_tray_v1_20261003';L=R/'audit/job_artwork_refinement_live'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
py='C:/Users/Peter/AppData/Local/Python/bin/python.exe';G=F/'gates';G.mkdir(exist_ok=False)
commands=[('authority',[py,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[py,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('game2d',[py,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate']),('document_tests',[py,'-X','utf8','-B','-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'])]
ip=R/'design/audit_impacts/job-geology-complete-actions-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{(F/'review_tools'/Path(__file__).name).relative_to(R).as_posix()}|{(G/(label+'.'+ext)).relative_to(R).as_posix() for label,_ in commands for ext in ['stdout.log','stderr.log','receipt.json']});write(ip,d);shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
def run(row):
 label,args=row;t=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat();out=G/(label+'.stdout.log');err=G/(label+'.stderr.log');print(label+'|START',flush=True)
 with out.open('wb') as o,err.open('wb') as e:p=subprocess.run(args,cwd=R,stdout=o,stderr=e,timeout=1800,creationflags=subprocess.CREATE_NO_WINDOW)
 receipt=dict(status='PASS' if p.returncode==0 else 'FAIL_PRESERVED',command=args,process_exit=p.returncode,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,stdout_sha256=sha(out),stderr_sha256=sha(err),qualification='Existing unchanged machine gate. No current graphics/action, strict-zero2D, device/child/owner/finding/integration/release acceptance transfer.')
 write(G/(label+'.receipt.json'),receipt);print(label+'|'+receipt['status'],flush=True);return label,receipt
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for f in concurrent.futures.as_completed([pool.submit(run,x) for x in commands]):results.append(f.result())
for packet,impact in [(F,'job-geology-complete-actions-20261003.json'),(P,'job-geology-painted-invitation-fit-20261003.json'),(T,'job-geology-specimen-tray-20261003.json')]:
 ip2=R/'design/audit_impacts'/impact;d=read(ip2);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in packet.rglob('*') if x.is_file()});
 if packet==F:d['validation'] += [dict(command=' '.join(x['command']),result='PASS' if x['status']=='PASS' else 'FAIL',evidence=(G/(label+'.receipt.json')).relative_to(R).as_posix()) for label,x in results]
 write(ip2,d)
assert all(x['status']=='PASS' for _,x in results),[(label,x['status']) for label,x in results]
print('FRESH_UNCHANGED_DOCUMENT_COVERAGE_2D_REGRESSION_AND_DOCUMENT_TESTS_PASS|VISUAL_WEAKNESSES_RETAINED')
