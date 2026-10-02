from pathlib import Path
import json,hashlib,shutil,subprocess,sys,time
b=Path(r'C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');parent=b/'audit/job_pan_painted_mount_v3_20261001';previous=parent/'attempt_02';out=parent/'attempt_03';out.mkdir(exist_ok=False)
def rel(p):return p.relative_to(b).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8',newline='\n')
code=(previous/'capture.gd').read_text().replace('tmp/pan_details_v116/native_views','tmp/pan_support_v118/native_views').replace('res://'+rel(previous/'study_surface.gd'),'res://'+rel(out/'study_surface.gd')).replace('invitation_support.z_index = -1','invitation_support.z_index = 0\n\t\t\t\t\tinvitation_support.show_behind_parent = true')
surface=(previous/'study_surface.gd').read_text().replace('base + Vector2(0.0, -2.0), Vector2(24.0, 6.0), Color(0.22, 0.60, 0.65, 0.35), Color(0.57, 0.89, 0.88, 0.72)','base + Vector2(0.0, 4.0), Vector2(27.0, 8.0), Color(0.22, 0.60, 0.65, 0.50), Color(0.57, 0.89, 0.88, 0.85)')
(out/'.gdignore').write_text('');(out/'capture.gd').write_text(code,encoding='utf-8',newline='\n');(out/'study_surface.gd').write_text(surface,encoding='utf-8',newline='\n');shutil.copyfile(__file__,out/'executed_capture_pan_support_v118.py')
snapshot=json.loads((b/'audit/job_review_v2_20261001/full_ci_candidate_retry_v2/SOURCE_BEFORE.json').read_text())['source_files'];before={x['path']:sha(b/x['path']) for x in snapshot};assert len(before)==325 and all(before[x['path']]==x['sha256'] for x in snapshot);write(out/'SOURCE_BEFORE.json',before)
write(out/'PROFILE.json',dict(status='PREPARED_NATIVE_SUPPORT_LAYER_REPAIR',views=18,changes='Correct hidden study-only invitation slab ownership to same Canvas layer behind cue parent. Make sparse mineral water contact visible in front of its base. All source pixels/production behavior unchanged.',qualification='Disposable fixture only; does not create a production defect or prove connected acting.'))
impact=b/'design/audit_impacts/job-pan-painted-placement-20261001.json'
def cover():
 d=json.loads(impact.read_text());d['files']=sorted(set(d['files'])|{rel(p) for p in out.rglob('*') if p.is_file()});write(impact,d)
cover();native=b/'tmp/pan_support_v118/native_views';native.mkdir(parents=True)
godot='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/Godot/4.7.2/godot_console.exe';cmds=[('parser',[sys.executable,'-X','utf8','-B','-m','gdtoolkit.parser',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('inference',[sys.executable,'-X','utf8','-B','tools/lint_inference.py',rel(out/'capture.gd'),rel(out/'study_surface.gd')]),('analyzer',[godot,'--headless','--path',str(b),'--check-only','--script','res://'+rel(out/'capture.gd')]),('native',[godot,'--path',str(b),'--script','res://'+rel(out/'capture.gd')])];rows=[]
for name,cmd in cmds:
 so=out/(name+'.stdout.log');se=out/(name+'.stderr.log');so.touch();se.touch();cover();start=time.monotonic()
 with so.open('wb') as a,se.open('wb') as c:
  try:p=subprocess.run(cmd,cwd=b,stdout=a,stderr=c,timeout=240 if name!='native' else 600,creationflags=subprocess.CREATE_NO_WINDOW);code=p.returncode;timed=False
  except subprocess.TimeoutExpired:code=None;timed=True
 rows.append(dict(name=name,command=cmd,process_exit=code,timed_out=timed,seconds=time.monotonic()-start,stdout=rel(so),stderr=rel(se)));print(name,code,flush=True)
 if code!=0:print(se.read_text(encoding='utf-8',errors='replace')[-1400:],flush=True);break
passed=len(rows)==4 and all(x['process_exit']==0 for x in rows) and all(sha(b/p)==h for p,h in before.items())
if passed:shutil.copytree(native,out/'native_views')
write(out/'PROCESS_RECEIPT.json',dict(status='PASS_MACHINE_NATIVE_CAPTURE' if passed else 'FAIL_PRESERVED',processes=rows,original325_sources_unchanged=all(sha(b/p)==h for p,h in before.items()),qualification='Machine capture only. Direct every-view review pending. No complete action, route or owner acceptance.'));cover();d=json.loads(impact.read_text());d['validation'].append(dict(command='Study-only support Canvas layer/contact clarity repair official4.7.2 analyzer and18-view native input capture',result='PASS' if passed else 'FAIL',evidence=rel(out/'PROCESS_RECEIPT.json')));write(impact,d);raise SystemExit(0 if passed else 1)
