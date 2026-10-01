from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
r=next(p for p in Path(__file__).resolve().parents if (p/'project.godot').is_file())
live=r/'audit/day_two_boxing_live_refinement_v1_20261001';out=live/'current_document_gates_v5'
python='C:/Users/Peter/AppData/Local/Python/bin/python.exe'
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
families=[('day-one-pool-live-refinement-v2-20261001','audit/day_one_pool_live_refinement_v2_20261001'),('day-one-playroom-sign-v2-20261001','assets_src/imagegen/day1_playroom_sign_v2_20261001'),('day-two-boxing-puff-reuse-v1-20261001','audit/day_two_boxing_puff_reuse_v1_20261001'),('day-two-boxing-single-gloves-v1-20261001','assets_src/imagegen/day2_boxing_single_gloves_v1_20261001'),('day-two-boxing-live-refinement-v1-20261001','audit/day_two_boxing_live_refinement_v1_20261001')]
def stage():
 paths=set()
 for ident,prefix in families:
  p=r/'design/audit_impacts'/f'{ident}.json';d=json.loads(p.read_text());d['files']=sorted(set(d['files'])|{q.relative_to(r).as_posix() for q in (r/prefix).rglob('*') if q.is_file()})
  if ident.startswith('day-two-boxing-live'):d['files']=sorted(set(d['files'])|{q.relative_to(r).as_posix() for q in (r/'audit/job_artwork_refinement_live').rglob('*') if q.is_file()})
  write(p,d);paths.update(d['files']);paths.add(p.relative_to(r).as_posix())
 paths=sorted(paths)
 for i in range(0,len(paths),70):
  subprocess.run(['git','add','-f','--sparse','--',*paths[i:i+70]],cwd=r,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  if i%1400==0:print('STAGE_CURRENT',min(i+70,len(paths)),len(paths),flush=True)
 return paths
assert not out.exists(),'Preserve earlier fresh gate attempt.'
ci=json.loads((r/'audit/day_one_pool_live_refinement_v2_20261001/full_ci_current_retry_v3/RECEIPT.json').read_text());assert ci['status']=='PASS_UNMODIFIED_CURRENT_FULL_SUITE'
out.mkdir()
commands=[('authority',['tools/audit_document_authority.py']),('development',['tools/audit_development.py','--base','auto']),('contract_tests',['-m','unittest','tools.tests.test_audit_document_authority','tools.tests.test_audit_development'])]
for name,_ in commands:
 for stream in ['stdout','stderr']:(out/f'{name}.{stream}.log').write_text('')
write(out/'RECEIPT.json',dict(status='PENDING'))
for name in ['run_current_document_gates_v5.py','seal_current_job_art_review_v5.py','verify_current_job_art_remote_v5.py','prepare_current_review_publication_v5.py','record_current_item_register_v1.py']:
 shutil.copyfile(r/'tmp'/name,live/'review_tools'/name)
paths=stage();results=[]
for name,args in commands:
 with (out/f'{name}.stdout.log').open('wb') as stdout,(out/f'{name}.stderr.log').open('wb') as stderr:
  p=subprocess.run([python,'-X','utf8','-B',*args],cwd=r,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
 results.append(dict(command=args,process_exit=p.returncode,stdout=f'{name}.stdout.log',stderr=f'{name}.stderr.log'))
 print('CURRENT_DOCUMENT_GATE',name,p.returncode,flush=True)
passed=all(x['process_exit']==0 for x in results)
write(out/'RECEIPT.json',dict(status='PASS' if passed else 'FAIL_PRESERVED',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),commands=results,coverage_paths=len(paths),qualification='Fresh current authority/development/52 contract tests after report/register updates. Full325-source engine run retains its own source boundary. No creative or external acceptance.'))
stage();raise SystemExit(0 if passed else 1)
