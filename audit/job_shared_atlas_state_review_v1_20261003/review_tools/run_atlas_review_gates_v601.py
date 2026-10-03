from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');S=B/'audit/job_shared_atlas_state_review_v1_20261003';PY='C:/Users/Peter/AppData/Local/Python/bin/python.exe';IP=B/'design/audit_impacts/job-shared-atlas-state-review-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda x:hashlib.sha256(x).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,d):
 n=p.with_name(p.name+'.v601_next');n.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode());n.replace(p)
commands={'authority':['tools/audit_document_authority.py'],'development':['tools/audit_development.py','--base','auto'],'document_tests':['-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'],'game2d':['tools/audit_game_2d.py','--regression-gate'],'register_parts':['audit/job_artwork_refinement_live/review_tools/test_register_parts_v51.py']}
phase=sys.argv[1]
if phase=='--prepare':
 (S/'gates_v1').mkdir(exist_ok=True);shutil.copyfile(__file__,S/'review_tools'/Path(__file__).name)
 d=read(IP);d['files']=sorted(set(d['files']+[p.relative_to(B).as_posix() for p in S.rglob('*') if p.is_file()]+['audit/job_shared_atlas_state_review_v1_20261003/gates_v1/'+label+suffix for label in commands for suffix in ['.stdout.log','.stderr.log','.receipt.json']]));write(IP,d)
 whitelist=B/'tmp/v2_preview_allowed.json';wl=read(whitelist);assert isinstance(wl,list);wl=sorted(set(wl+d['files']));write(whitelist,wl)
 print('PREPARED_5_FRESH_GATES_AND_PREVIEW_PATHS',len(wl),flush=True);sys.exit(0)
assert phase in commands
started=now();args=[PY,'-X','utf8','-B',*commands[phase]];r=subprocess.run(args,cwd=B,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out=S/'gates_v1';(out/(phase+'.stdout.log')).write_bytes(r.stdout);(out/(phase+'.stderr.log')).write_bytes(r.stderr)
write(out/(phase+'.receipt.json'),dict(status='PASS' if r.returncode==0 else 'FAIL',command=args,exit_code=r.returncode,started_utc=started,finished_utc=now(),working_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=B,text=True).strip(),stdout_sha256=sha(r.stdout),stderr_sha256=sha(r.stderr),qualification='Machine structural/regression evidence only. No new source/native art/motion/runtime/device/child/owner acceptance. Strict2D satisfaction remains separate from no-regression.'))
print(phase,r.returncode,r.stdout.decode('utf-8','replace')[-1900:],r.stderr.decode('utf-8','replace')[-1200:],flush=True);sys.exit(r.returncode)
