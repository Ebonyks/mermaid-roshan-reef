from pathlib import Path
import concurrent.futures,datetime,hashlib,json,shutil,subprocess,sys
r=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
out=r/'audit/job_review_v2_20261001/current_supplement_gates_v1';assert not out.exists();out.mkdir()
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
impact=r/'design/audit_impacts/job-review-current-remote-receipt-20261001.json';d=json.loads(impact.read_text(encoding='utf-8'))
image=Path('C:/Users/Peter/Documents/mermaid-roshan-reef/tmp/day2_graphics_audit_20260930/tmp/doctor_motion_review_browser_v50.png');target=out/'doctor_motion_review_browser_v50.png';shutil.copyfile(image,target);assert image.read_bytes()==target.read_bytes()
browser={'status':'SCOPED_DESKTOP_REPORT_PREVIEW','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'motion_page':'http://127.0.0.1:8880/assets_src/local_motion/day2_doctor_wash_rub_study_v1_20261001/index.html','cards':41,'native_video_dimensions':[896,512],'native_video_duration':1.708333,'horizontal_overflow':False,'register_counts':{'sources':1151,'pose_cells':240,'prop_regions':38,'entries':1429,'source_priorities':556,'unassigned_source_scores':403},'screenshot_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'qualification':'Browser screenshot shows the desktop viewport portion of the report; it is not a full native action frame or device/child/owner acceptance. All41 native frames were directly reviewed separately.'}
write(out/'BROWSER_PREVIEW.json',browser)
license=r/'ASSET_LICENSES.md';s=license.read_text(encoding='utf-8');path=target.relative_to(r).as_posix();assert path not in s;s+='\n| '+path+' | Codex in-app browser desktop report screenshot2026-10-02 | Project diagnostic screenshot, underlying art provenance preserved | Viewport screenshot of motion report and preview | Report layout proof only; not full native gameplay or device/owner acceptance. |\n';license.write_text(s,encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'executed_run_current_review_gates_v51.py')
d['files']=sorted(set(d['files'])|{'ASSET_LICENSES.md',*[x.relative_to(r).as_posix() for x in out.iterdir() if x.is_file()]})
write(impact,d)
commands=[('authority',[sys.executable,'-X','utf8','-B','tools/audit_document_authority.py']),('development',[sys.executable,'-X','utf8','-B','tools/audit_development.py','--base','auto']),('2d',[sys.executable,'-X','utf8','-B','tools/audit_game_2d.py','--regression-gate'])]
def run(job):
 name,cmd=job
 with (out/(name+'.stdout.log')).open('wb') as so,(out/(name+'.stderr.log')).open('wb') as se:
  p=subprocess.run(cmd,cwd=r,stdout=so,stderr=se,creationflags=subprocess.CREATE_NO_WINDOW,timeout=180)
 return {'name':name,'command':cmd,'process_exit':p.returncode,'stdout':(out/(name+'.stdout.log')).relative_to(r).as_posix(),'stderr':(out/(name+'.stderr.log')).relative_to(r).as_posix()}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,commands))
passed=all(x['process_exit']==0 for x in rows)
receipt={'status':'PASS_CURRENT_WORKING_REVIEW_GATES' if passed else 'FAIL_PRESERVED','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline':'fb03e0ac3dda1658e9ea188d33cc6e084871642b','processes':rows,'qualification':'Working review authority/development and2D no-regression. Exact staged/committed coverage is verified separately before publication. Strict2D, whole actions, device/child/owner and hosted acceptance remain open.'};write(out/'RECEIPT.json',receipt)
d=json.loads(impact.read_text(encoding='utf-8'));d['files']=sorted(set(d['files'])|{x.relative_to(r).as_posix() for x in out.iterdir() if x.is_file()});d['validation'] += [{'command':' '.join(x['command']),'result':'PASS' if x['process_exit']==0 else 'FAIL','evidence':x['stdout']+'; '+x['stderr']} for x in rows];write(impact,d)
for x in rows:
 lines=(r/x['stdout']).read_text(encoding='utf-8',errors='replace').splitlines();print(json.dumps({'name':x['name'],'exit':x['process_exit'],'first_lines':lines[:4],'last_lines':lines[-4:]},ensure_ascii=False))
raise SystemExit(0 if passed else 1)
