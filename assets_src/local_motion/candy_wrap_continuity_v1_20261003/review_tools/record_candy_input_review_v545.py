from pathlib import Path
import datetime, hashlib, json, shutil

B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_wrap_continuity_v1_20261003'
IP=B/'design/audit_impacts/job-candy-local-wrap-continuity-20261003.json'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):
    task_next=p.with_name(p.name+'.v545_next')
    task_next.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    task_next.replace(p)
review={'status':'DIRECT_NATIVE_INPUT_REVIEWED_FOR_REFERENCE_SUBMISSION','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'path':(P/'inputs/CANDY-WRAP-A1.png').relative_to(B).as_posix(),'sha256':sha(P/'inputs/CANDY-WRAP-A1.png'),'size':[896,512],'observations':'Complete painted opening cell is visible with intact hat, hair/rainbow ribbon, face, two connected quilted mittens, gold paper, one red oval sweet and lavender table. Neutral pale mat and uniform technical whole-cell scale preserve the source pose. Eyes begin forward and must visibly attend to the work in motion; this static view does not establish folding, sliding contact, twisting or release.','source_score_transfer':False,'runtime_binding':False,'owner_acceptance':None}
write(P/'INPUT_DIRECT_REVIEW.json',review)
m=read(P/'MANIFEST.json');assert m['status']=='BOUND_INPUT_READY_FOR_DIRECT_INPUT_REVIEW_AND_QUIET_IDLE_DISPATCH'
m['input_visual_review']={'status':review['status'],'evidence':(P/'INPUT_DIRECT_REVIEW.json').relative_to(B).as_posix(),'source_score_transfer':False}
m['status']='BOUND_INPUT_REVIEWED_READY_FOR_QUIET_IDLE_DISPATCH'
write(P/'MANIFEST.json',m)
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
d=read(IP);d['files']=sorted(set(d['files'])|{x.relative_to(B).as_posix() for x in P.rglob('*') if x.is_file()})
d['validation'].append({'command':'Direct complete native896x512 technical input review; developed queue worker --check','result':'PASS','evidence':(P/'INPUT_DIRECT_REVIEW.json').relative_to(B).as_posix()})
write(IP,d)
print('CANDY_INPUT_DIRECT_REVIEW_SAVED|whole pose/region intact|no motion score transfer|one reference job ready')
