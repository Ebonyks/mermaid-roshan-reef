from pathlib import Path
import datetime,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');family=r/'audit/job_review_v2_20261001';out=family/'document_gates_v7';out.mkdir(exist_ok=False)
prior=json.loads((family/'document_gates_v6/RECEIPT.json').read_text(encoding='utf-8'));assert [x['exit_code'] for x in prior['results']]==[0,1,0]
shutil.copyfile(__file__,out/'executed_correct_impact_separators_and_retry_v31.py')
shutil.copyfile(Path(__file__).with_name('build_current_staged_file_index_v30.py'),family/'review_tools/executed_build_current_staged_file_index_v30.py')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));invalid=[x for x in d['files'] if '\\' in x];assert len(invalid)==6 and all(x.startswith('audit\\job_review_v2_20261001\\document_gates_v6\\') for x in invalid)
d['files']=sorted({x.replace('\\','/') for x in d['files']}|{x.relative_to(r).as_posix() for x in family.rglob('*') if x.is_file()}|{'audit/job_review_v2_20261001/document_gates_v7/stdout.log','audit/job_review_v2_20261001/document_gates_v7/stderr.log','audit/job_review_v2_20261001/document_gates_v7/RECEIPT.json'})
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
paths=sorted(x for x in d['files'] if (r/x).is_file());stage=r/'tmp/v2_exact_owned_stage_v31.bin';stage.write_bytes(b'\0'.join(x.encode() for x in paths)+b'\0')
with (r/'tmp/v2_stage_v31.log').open('wb') as log:p=subprocess.run(['git','add','-f','--sparse','--pathspec-from-file='+str(stage),'--pathspec-file-nul'],cwd=r,stdout=log,stderr=subprocess.STDOUT)
assert p.returncode==0
cmd=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B','tools/audit_development.py','--base','auto'];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (out/'stdout.log').open('wb') as stdout,(out/'stderr.log').open('wb') as stderr:p=subprocess.run(cmd,cwd=r,stdout=stdout,stderr=stderr)
result={'command':cmd,'exit_code':p.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':'audit/job_review_v2_20261001/document_gates_v7/stdout.log','stderr':'audit/job_review_v2_20261001/document_gates_v7/stderr.log','stdout_tail':(out/'stdout.log').read_text(encoding='utf-8')[-2000:]}
receipt={'status':'PASS' if p.returncode==0 else 'FAIL_PRESERVED','retried':result,'still_applicable_passes':[x for x in prior['results'] if x['exit_code']==0],'repair':'Six predeclared log paths created with Windows separators were normalized to exact repository POSIX paths. All first failures/raw evidence retained; validator unchanged.','qualification':'Traceability only. No visual, strict2D, device/child/owner or hosted acceptance.'}
(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
d=json.loads(impact.read_text(encoding='utf-8'));d['validation'].append({'command':'python -B tools/audit_development.py --base auto','result':'PASS' if p.returncode==0 else 'FAIL','evidence':result['stdout']+'; document_gates_v6 first failure preserved; exact path separators corrected.'});impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt));raise SystemExit(p.returncode)
