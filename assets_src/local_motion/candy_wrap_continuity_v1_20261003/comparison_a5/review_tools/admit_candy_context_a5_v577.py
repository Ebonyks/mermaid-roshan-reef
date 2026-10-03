from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
C=B/'assets_src/imagegen/candy_wrap_scene_context_v1_20261003'
Q=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003/comparison_a5'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()

p=C/'index.html'; text=p.read_text(encoding='utf-8'); assert '../../../local_motion/' in text
p.write_text(text.replace('../../../local_motion/','../../local_motion/'),encoding='utf-8',newline='\n')
m=read(Q/'MANIFEST.json')
review=dict(status='DIRECT_COMPLETE_NORMALIZED_INPUT_REVIEWED_REFERENCE_ONLY',reviewed_utc=now(),input_path=m['input_path'],input_sha256=m['input_sha256'],dimensions=[896,512],direct_complete_native_review=True,observations=['Entire room/table/character preserved without cropping; only4px whole-canvas black padding top and bottom.','Exactly two connected coral mittens remain readable; one partially covered red sweet rests on one gold sheet.','The central contact occupies a larger useful fraction of the canvas than the old neutral-mat input. Room machinery remains visually dense behind it.'],starting_still_score=4.5,source_score_transfer=False,motion_score=None,runtime_bound=False,owner_acceptance=None,qualification='Direct input admission for one local reference study only. No measured movement, runtime readability or complete-wrapper acceptance.')
write(Q/'INPUT_DIRECT_REVIEW.json',review)
m['input_visual_review']=dict(status=review['status'],evidence=(Q/'INPUT_DIRECT_REVIEW.json').relative_to(B).as_posix(),source_score_transfer=False)
m['status']='BOUND_CONTEXT_INPUT_DIRECTLY_REVIEWED_READY_FOR_CHECK_AND_QUIET_IDLE_DISPATCH'
write(Q/'MANIFEST.json',m)
cmd=['C:/Users/Peter/AppData/Local/Python/bin/python.exe','-X','utf8','-B',str(Q/'review_tools/queue_candy_context_fold_a5_v576.py'),'--check']
started=now(); result=subprocess.run(cmd,cwd=B,capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW)
(Q/'checks/admission.stdout.log').write_bytes(result.stdout);(Q/'checks/admission.stderr.log').write_bytes(result.stderr)
write(Q/'checks/ADMISSION_RECEIPT.json',dict(status='PASS' if result.returncode==0 else 'FAIL',command=cmd,started_utc=started,finished_utc=now(),exit_code=result.returncode,manifest_sha256=sha(Q/'MANIFEST.json'),stdout_sha256=sha(Q/'checks/admission.stdout.log'),stderr_sha256=sha(Q/'checks/admission.stderr.log'),qualification='Actual check-only execution, not a render or visual-motion pass.'))
shutil.copyfile(__file__,Q/'review_tools'/Path(__file__).name)
ip=B/'design/audit_impacts/job-candy-painted-context-source-20261003.json';d=read(ip)
d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for base in(C,Q) for p in base.rglob('*') if p.is_file()})
d['validation'].append(dict(command='Exact developed A5 check-only admission',result='PASS' if result.returncode==0 else 'FAIL',evidence=(Q/'checks/ADMISSION_RECEIPT.json').relative_to(B).as_posix()+'; actual raw stdout/stderr retained; no renderer submission by this check.'))
write(ip,d)
print(result.stdout.decode('utf-8',errors='replace'),end='');print(result.stderr.decode('utf-8',errors='replace'),end='');raise SystemExit(result.returncode)
