from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');parent=b/'audit/job_geode_opening_states_v3_20261001';out=parent/'attempt_02';out.mkdir(exist_ok=False)
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
assert json.loads((parent/'PROCESS_RECEIPT.json').read_text())['status']=='FAIL_PRESERVED'
write(parent/'FAILURE_DIAGNOSIS.json',dict(status='FAILED_CAPTURE_PRESERVED_NOT_VISUAL_EVIDENCE',causes=['Inherited output path mistakenly retained older temporary destination','Obsolete24-view assertion after reducing to10 selected views caused script assertion and prevented normal exit'],owned_native_process_terminated=59644,original_archived_reviews_unchanged=True,production_source325_unchanged=True,correction='New attempt02 with exact isolated output path and expected10-view assertion. Keep original scripts/logs/failure, do not relabel the failed run as pass.'))
code=(parent/'capture.gd').read_text();old='res://tmp/geode_embedded_mount_v99/native_views/';assert old in code;code=code.replace(old,'res://tmp/geode_opening_v139/native_views/').replace('res://'+rel(parent/'study_surface.gd'),'res://'+rel(out/'study_surface.gd'));assert 'assert(records.size() == 24)' in code;code=code.replace('assert(records.size() == 24)','assert(records.size() == 10)');assert 'geode_embedded_mount_v99' not in code
(out/'.gdignore').write_text('');(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n');shutil.copyfile(parent/'study_surface.gd',out/'study_surface.gd');shutil.copyfile(parent/'PROFILE.json',out/'PROFILE.json');shutil.copyfile(parent/'SOURCE_BEFORE.json',out/'SOURCE_BEFORE.json');shutil.copyfile(__file__,out/'executed_retry_geode_opening_v139.py')
impact=b/'design/audit_impacts/job-geode-opening-continuity-20261001.json'
def cover():
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in parent.rglob('*') if p.is_file()});write(impact,d)
cover();native=b/'tmp/geode_opening_v139/native_views';native.mkdir(parents=True)
before=json.loads((out/'SOURCE_BEFORE.json').read_text());assert len(before)==325 and all(sha(b/p)==h for p,h in before.items())
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('analyzer',[godot,'--headless','--path',str(b),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(b),'--script','res://'+rel(out/'capture.gd')])];rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as c:
  try:p=subprocess.run(cmd,cwd=b,stdout=a,stderr=c,timeout=240 if name!='native' else 180,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed=False
  except subprocess.TimeoutExpired:code=None;timed=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:print(se.read_text(encoding='utf-8',errors='replace')[-1200:],flush=True);break
passed=len(rows)==4 and all(x['process_exit']==0 for x in rows) and (native/'CAPTURE_RECEIPT.json').is_file() and len(json.loads((native/'CAPTURE_RECEIPT.json').read_text())['views'])==10 and all(sha(b/p)==h for p,h in before.items())
if passed:shutil.copytree(native,out/'native_views')
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_MACHINE_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED',processes=rows,original325_sources_unchanged=all(sha(b/p)==h for p,h in before.items()),expected_views=10,qualification='New isolated run only. Every10 captured view requires direct review; failed first run remains failed. No naturally timed full ordinary action/route/device/child/owner acceptance.'));cover();d=json.loads(impact.read_text());d['validation'].append(dict(command='Corrected isolated10-view geode opening retry: parser/inference/official4.7.2 analyzer/native input',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d);raise SystemExit(0 if passed else 1)
