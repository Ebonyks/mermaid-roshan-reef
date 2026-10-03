from pathlib import Path
import json,datetime,subprocess,shutil,hashlib
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');L=R/'audit/job_artwork_refinement_live';F=R/'audit/job_geology_complete_actions_v1_20261003'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
p=L/'all_items.html';s=p.read_text();a="q.kind==='source'&&q.current_source_score";b="['source','runtime source'].includes(q.kind)&&q.current_source_score";assert s.count(a)>=2;s=s.replace(a,b);p.write_text(s,encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-geology-complete-action-register-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{(F/x).relative_to(R).as_posix() for x in ['BROWSER_LIBRARY_V450.png','BROWSER_ACTION_REPORT_V450.png','BROWSER_VERIFY_V450.json']}|{(L/'review_tools'/Path(__file__).name).relative_to(R).as_posix()});write(ip,d)
out=F/'previous_s_remote_verified';gh='C:/Program Files/GitHub CLI/gh.exe';receipts={}
for name,suffix in [('HOSTED_S_FINAL.json',''),('HOSTED_S_JOBS_FINAL.json','/jobs')]:
 result=subprocess.run([gh,'api','repos/Ebonyks/mermaid-roshan-reef/actions/runs/37086150331'+suffix],cwd=R,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW);p=out/name;assert not p.exists();p.write_bytes(result.stdout);receipts[name]=json.loads(result.stdout)
head='1652a9bb33af0d11a594b5996df66d2266c02d39';run=receipts['HOSTED_S_FINAL.json'];jobs=receipts['HOSTED_S_JOBS_FINAL.json']['jobs'];assert run['head_sha']==head and run['status']=='completed' and run['conclusion']=='success';assert jobs and all(x['status']=='completed' and x['conclusion']=='success' for x in jobs)
write(out/'HOSTED_S_VERIFICATION.json',dict(status='EXACT_S_HOSTED_SUCCESS',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head_sha=head,run_id=37086150331,url=run['html_url'],jobs=[dict(name=x['name'],conclusion=x['conclusion'],completed_at=x['completed_at']) for x in jobs],raw_files=[dict(path=(out/x).relative_to(R).as_posix(),sha256=hashlib.sha256((out/x).read_bytes()).hexdigest()) for x in receipts],qualification='Hosted exact S machine checks only. Current783 production bytes unchanged. Complete-action and source/placement/owner/device/child/finding acceptance remain separate. No dev integration or release.'))
d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(R).as_posix() for p in out.rglob('*') if p.is_file()});d['validation'].append(dict(command='gh api exactS run37086150331 and all jobs',result='PASS',evidence=(out/'HOSTED_S_VERIFICATION.json').relative_to(R).as_posix()));write(ip,d)
shutil.copyfile(Path(__file__),L/'review_tools'/Path(__file__).name)
print('VISIBLE_COUNT_KINDS_CORRECTED|EXACT_S_HOSTED_ALL_JOBS_SUCCESS|NEW_ART_SOURCE_AND_ACTION_ACCEPTANCE_SEPARATE')
