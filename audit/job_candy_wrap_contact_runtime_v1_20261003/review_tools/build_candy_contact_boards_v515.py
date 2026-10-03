from pathlib import Path
import json,hashlib,shutil,collections,datetime,subprocess
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');C=R/'audit/job_candy_wrap_contact_runtime_v1_20261003';A=C/'attempt05';Q=A/'qa_boards';Q.mkdir(exist_ok=False)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe';boards=[];stats={}
for lane in ('training',):
 for width in (1280,1600):
  assert read(C/f'runtime_gate_a05/{lane}_{width}.receipt.json')['status']=='PASS'
  cap=read(A/f'CAPTURE_{lane}_{width}.json');stats[f'{lane}_{width}']={'views':len(cap['views']),'frames':len(cap['motion_frames']),'phase_counts':dict(collections.Counter(str(x['state']['phase']) for x in cap['motion_frames']))}
  for kind,limit in [('views',6),('motion_frames',12)]:
   rows=cap[kind]
   for start in range(0,len(rows),limit):
    subset=rows[start:start+limit];assert all(sha(R/x['path'])==x['sha256'] for x in subset)
    out=Q/f'{lane}_{width}_{kind}_{start//limit+1:02d}.png';lst=out.with_suffix('.txt');lst.write_text(''.join("file '"+(R/x['path']).as_posix()+"'\n" for x in subset),encoding='utf-8',newline='\n')
    w=640 if kind=='views' else 480;grid='2x3' if kind=='views' else '3x4'
    subprocess.run([ff,'-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-frames:v','1','-vf',f'scale={w}:-1,tile={grid}:nb_frames={len(subset)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
    boards.append({'path':out.relative_to(R).as_posix(),'sha256':sha(out),'width':width,'lane':lane,'kind':kind,'first':start,'last':start+len(subset)-1,'count':len(subset),'members':subset,'direct_review':False})
write(C/'QA_BOARD_MANIFEST_CONTACT_A5.json',{'status':'PREPARED_DIRECT_REVIEW_PENDING','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stats':stats,'boards':boards,'qualification':'Explicit NON_RUNTIME connected source-key drawing substitution, visible-candy hub and valid circle radius declared, source A7, before-render ownership from true phase/task/panel. Static keys are not temporal in-betweens. Both training canvases/all4 phases earned/ordinary Kitchen return. Full circle actions only, all other phases selected views. Explicit isolated entry and prior Farmer/Chef saved prerequisites; desktop Mobile and slow readback, no device/child/owner acceptance. Consecutive complete canvases, row-major; empty final cells are not frames. QA thumbnails are never generation/production pixels.'})
shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(R).as_posix() for p in C.rglob('*') if p.is_file()});write(ip,d)
print(json.dumps({'boards':len(boards),'stats':stats}))
