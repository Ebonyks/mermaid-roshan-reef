from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,collections
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');C=R/'audit/job_candy_workflow_current_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
A=C/'attempt02';Q=A/'qa_boards';Q.mkdir(exist_ok=False);boards=[];stats={}
for width in (1280,1600):
 assert read(C/f'runtime_gate_a2/training_{width}.receipt.json')['status']=='PASS'
 cap=read(A/f'CAPTURE_training_{width}.json');stats[str(width)]={'views':len(cap['views']),'frames':len(cap['motion_frames']),'phase_counts':dict(collections.Counter(str(x['state']['phase']) for x in cap['motion_frames']))}
 for kind,limit in [('views',6),('motion_frames',12)]:
  rows=cap[kind]
  for start in range(0,len(rows),limit):
   subset=rows[start:start+limit];assert all(sha(R/x['path'])==x['sha256'] for x in subset)
   out=Q/f'training_{width}_{kind}_{start//limit+1:02d}.png';lst=out.with_suffix('.txt');lst.write_text(''.join("file '"+(R/x['path']).as_posix()+"'\n" for x in subset),encoding='utf-8',newline='\n')
   w=640 if kind=='views' else 480;grid='2x3' if kind=='views' else '3x4'
   subprocess.run([ff,'-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-frames:v','1','-vf',f'scale={w}:-1,tile={grid}:nb_frames={len(subset)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
   boards.append({'path':out.relative_to(R).as_posix(),'sha256':sha(out),'width':width,'lane':'training','kind':kind,'first':start,'last':start+len(subset)-1,'count':len(subset),'members':subset,'direct_review':False})
write(C/'QA_BOARD_MANIFEST_TRAINING_A2.json',{'status':'PREPARED_DIRECT_REVIEW_PENDING','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stats':stats,'boards':boards,'qualification':'Consecutive complete canvases, row-major; empty final cells are not frames. QA thumbnails only; preserve original native canvases. Complete wrapping only, other phases selected views. Story A2 failed before opening because its phase names have no mapped physical stations; no story action pass.'})
shutil.copyfile(Path(__file__),C/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-candy-workflow-current-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in C.rglob('*') if x.is_file()});write(ip,d)
print(json.dumps({'boards':len(boards),'stats':stats}))
