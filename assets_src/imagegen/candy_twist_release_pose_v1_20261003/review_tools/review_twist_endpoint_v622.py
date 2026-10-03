from pathlib import Path
import datetime,hashlib,json,shutil,sys
from PIL import Image
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');T=B/'assets_src/imagegen/candy_twist_release_pose_v1_20261003'
sha=lambda raw:hashlib.sha256(raw).hexdigest();read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,raw):
 t=p.with_name(p.name+'.v622_next');t.write_bytes(raw);t.replace(p)
def write(p,d):put(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
s=read(Path(sys.argv[1]));d=T/s['attempt_directory'];native=d/'native.png';assert not native.exists()
src=Path(s['generated_original']);shutil.copyfile(src,native)
with Image.open(native) as im:dimensions=list(im.size);mode=im.mode
refs=read(d/'PLAN.json')['references'];assert all(sha((B/r['path']).read_bytes())==r['sha256'] for r in refs)
write(d/'SOURCE.json',dict(generation_method='built_in_imagegen_precise_object_edit',native_path=native.relative_to(B).as_posix(),native_sha256=sha(native.read_bytes()),dimensions=dimensions,mode=mode,default_generated_original=str(src),prompt_path=(d/'SENT_PROMPT.txt').relative_to(B).as_posix(),prompt_sha256=sha((d/'SENT_PROMPT.txt').read_bytes()),references=refs,copied_without_pixel_changes=True,recorded_utc=now(),runtime_bound=False))
reviews=[dict(id=k,score=score,evaluation=v) for k,score,v in s['reviews']]
write(d/'DIRECT_REVIEW.json',dict(reviewed_utc=now(),review_method='direct_complete_native_original_imagegen_output_compared_with_exact_preceding_source',native_sha256=sha(native.read_bytes()),status=s['status'],components=reviews,source_pose_score=s['score'],motion_score=None,current_game_wrap_score=2.8,runtime_bound=False,owner_acceptance=None,required_revision=s.get('required_revision')))
plan=read(T/'PLAN.json');plan['status']=s['plan_status'];plan['attempts'].append(dict(stage=s['stage'],attempt=s['attempt'],source_pose_score=s['score'],status=s['status'],review=s['attempt_directory']+'/DIRECT_REVIEW.json'))
if s.get('provisional_accepted'):plan[s['stage']+'_source_score']=s['score'];plan[s['stage']+'_source']=native.relative_to(B).as_posix()
write(T/'PLAN.json',plan)
out=dict(status=s['status'],native_sha256=sha(native.read_bytes()))
if 'next' in s:
 nxt=s['next'];a=T/nxt['directory'];a.mkdir();(a/'SENT_PROMPT.txt').write_bytes(nxt['prompt'].encode())
 refpath=B/nxt.get('reference_path',native.relative_to(B).as_posix());ref=dict(path=refpath.relative_to(B).as_posix(),sha256=sha(refpath.read_bytes()),role=nxt['reference_role'])
 nextrefs=[ref]
 if nxt.get('second_reference_role'):
  second=B/nxt.get('second_reference_path',native.relative_to(B).as_posix());nextrefs.append(dict(path=second.relative_to(B).as_posix(),sha256=sha(second.read_bytes()),role=nxt['second_reference_role']))
 write(a/'PLAN.json',dict(status=nxt['status'],references=nextrefs,prompt_sha256=sha(nxt['prompt'].encode()),runtime_bound=False))
 out.update(prompt=nxt['prompt'],prompt_sha256=sha(nxt['prompt'].encode()),reference=str(refpath),references=[str(B/r['path']) for r in nextrefs])
put(T/'review_tools'/Path(__file__).name,Path(__file__).read_bytes());put(T/'review_tools'/Path(sys.argv[1]).name,Path(sys.argv[1]).read_bytes())
ip=B/'design/audit_impacts/job-candy-twist-release-pose-20261003.json';impact=read(ip);impact['files']=sorted(set(impact['files'])|{p.relative_to(B).as_posix() for p in T.rglob('*') if p.is_file()});impact['validation'][1]=dict(command='Native endpoint generation and individual direct opinions',result='PASS' if s.get('provisional_accepted') else 'FAIL',evidence=native.relative_to(B).parent.as_posix()+'/DIRECT_REVIEW.json;source '+str(s['score'])+'. Specific opinions only;whole action/motion/runtime/owner remain unassigned.');write(ip,impact)
print(json.dumps(out,ensure_ascii=False))
