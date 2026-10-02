from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001/hosted_current_b_failure_v1';assert not out.exists();out.mkdir()
gh='C:/Program Files/GitHub CLI/gh.exe';base=[gh,'run','view','36941786030','--repo','Ebonyks/mermaid-roshan-reef']
commands=[('state',base+['--json','status,conclusion,headSha,jobs,createdAt,updatedAt,url']),('failed_steps',base+['--log-failed'])]
processes=[]
for name,cmd in commands:
 with (out/(name+'.stdout.log')).open('wb') as so,(out/(name+'.stderr.log')).open('wb') as se:
  p=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120)
 processes.append({'name':name,'process_exit':p.returncode,'command':cmd})
 assert p.returncode==0
state=json.loads((out/'state.stdout.log').read_text(encoding='utf-8'));assert state['headSha']=='fb03e0ac3dda1658e9ea188d33cc6e084871642b' and state['conclusion']=='failure'
failed=[{'job':j['name'],'conclusion':j['conclusion'],'step':s['name'],'step_number':s['number']} for j in state['jobs'] for s in j['steps'] if s['conclusion']=='failure']
log=(out/'failed_steps.stdout.log').read_text(encoding='utf-8',errors='replace')
interesting=[line for line in log.splitlines() if any(x in line.lower() for x in ['error:','fatal:','::error','failed','g2d-','uncovered','coverage','oversiz','too large','scan limit','timeout','unable to','does not','invalid'])]
receipt={'status':'HOSTED_CURRENT_B_FAILURE_PRESERVED','run_id':36941786030,'head_sha':state['headSha'],'run_url':state['url'],'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'failed_steps':failed,'processes':processes,'log_sha256':hashlib.sha256((out/'failed_steps.stdout.log').read_bytes()).hexdigest(),'qualification':'Hosted failure is separate from local82/82 and anonymous currentB byte verification. No gate weakening, retroactive pass or dev integration.'}
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');shutil.copyfile(__file__,out/'executed_read_hosted_current_failure_v45.py')
impact=r/'design/audit_impacts/job-review-current-remote-receipt-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in out.iterdir() if x.is_file()});d['validation'].append({'command':'Hosted Probe suite run36941786030 exact currentBfb03','result':'FAIL','evidence':(out/'RECEIPT.json').relative_to(r).as_posix()+'; exact failed-step log retained. Earlier pending observation remains historical.'});impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'failed_steps':failed,'interesting_lines':interesting[:30],'failed_log_bytes':(out/'failed_steps.stdout.log').stat().st_size},ensure_ascii=False)[:9000])
