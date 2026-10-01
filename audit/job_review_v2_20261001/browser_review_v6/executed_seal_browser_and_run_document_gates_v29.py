from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');family=r/'audit/job_review_v2_20261001';review=family/'browser_review_v6';review.mkdir(exist_ok=False)
old=Path(__file__).parent
proofs=['wash_route_browser_final_v29.png','doctor_motion_browser_v29.png']
rows=[]
for name in proofs:
 p=review/name;shutil.copyfile(old/name,p);rows.append({'path':p.relative_to(r).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
receipt={'status':'SCOPED_PASS_CURRENT_REGISTER_AND_TWO_REVIEW_PAGES','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'register_counts':{'sources':1150,'pose_cells':240,'prop_regions':38,'entries':1428,'inclusive_source_priorities':555,'unassigned_source_reviews':403},'wash_viewer':{'viewport':[1280,720],'selected_case':'opera_training_doctor_1280','selected_index':255,'displayed_frame':'256/256','measured_time_seconds':8.510,'frame_native_dimensions':[1280,720],'loaded_images':5,'horizontal_overflow':False,'control':'DOM-grounded range End selected the final exact recorded frame; next disabled.'},'motion_page':{'viewport':[1280,720],'loaded_images':4,'each_native_dimensions':[1122,1402],'horizontal_overflow':False},'proofs':rows,'qualification':'Browser resource/interaction and layout evidence only. Screenshots are viewport portions, not complete full-resolution source review or every recorded native frame. No new mounted/action score, device/child/owner acceptance, ordinary full Main/menu route or remote publication.'}
(review/'QUALIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,review/'executed_seal_browser_and_run_document_gates_v29.py')
license=r/'ASSET_LICENSES.md';s=license.read_text(encoding='utf-8')
for row in rows:
 assert row['path'] not in s
 s+='\n| '+row['path']+' | Codex browser review2026-10-01 | Project diagnostic screenshot; underlying artwork retains source provenance | Local explicit review pages | Unmodified viewport screenshot; source and action acceptance stay scoped separately. |\n'
license.write_text(s,encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-review-separate-v2-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'));d['scope']+=' Executed root-route study is machine PASS with only four doctor keys directly visually reviewed; prior preparation text describes the historical step. Current V8 register and two review pages verified at1280 desktop only.'
gates=family/'document_gates_v6';gates.mkdir(exist_ok=False)
commands=[['tools/audit_document_authority.py'],['tools/audit_development.py','--base','auto'],['tools/audit_game_2d.py','--regression-gate']]
gatepaths={str((gates/(str(i)+'_'+Path(cmd[0]).stem+'.'+ext)).relative_to(r)) for i,cmd in enumerate(commands) for ext in ['stdout.log','stderr.log']}
d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in family.rglob('*') if x.is_file()}|gatepaths|{'audit/job_review_v2_20261001/document_gates_v6/RECEIPT.json'})
d['validation'].append({'command':'Browser register and exact final-frame/motion-page controls','result':'PASS','evidence':'audit/job_review_v2_20261001/browser_review_v6/QUALIFICATION.json; desktop scoped only.'})
impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
paths=sorted(p for p in d['files'] if (r/p).is_file());stage=r/'tmp/v2_exact_owned_stage_v29.bin';stage.write_bytes(b'\0'.join(p.encode() for p in paths)+b'\0')
with (r/'tmp/v2_stage_v29.log').open('wb') as log:
 result=subprocess.run(['git','add','-f','--sparse','--pathspec-from-file='+str(stage),'--pathspec-file-nul'],cwd=r,stdout=log,stderr=subprocess.STDOUT)
assert result.returncode==0
def run(pair):
 i,command=pair;cmd=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B']+command
 stdout=gates/(str(i)+'_'+Path(command[0]).stem+'.stdout.log');stderr=gates/(str(i)+'_'+Path(command[0]).stem+'.stderr.log')
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with stdout.open('wb') as out,stderr.open('wb') as err: p=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
 return {'command':cmd,'exit_code':p.returncode,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':stdout.relative_to(r).as_posix(),'stderr':stderr.relative_to(r).as_posix(),'stdout_tail':stdout.read_text(encoding='utf-8',errors='replace')[-3500:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,enumerate(commands)))
receipt={'status':'PASS' if all(x['exit_code']==0 for x in results) else 'FAIL_PRESERVED','results':results,'qualification':'Document/current change coverage and2D non-regression only; strict2D remains UNSATISFIED and visual/device/child/owner/hosted gates separate.'}
(gates/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
d=json.loads(impact.read_text(encoding='utf-8'));d['validation'].extend({'command':' '.join(x['command'][4:]),'result':'PASS' if x['exit_code']==0 else 'FAIL','evidence':x['stdout']+'; '+x['stderr']+'; current document_gates_v6/RECEIPT.json'} for x in results);impact.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt,ensure_ascii=False));raise SystemExit(0 if receipt['status']=='PASS' else 1)
