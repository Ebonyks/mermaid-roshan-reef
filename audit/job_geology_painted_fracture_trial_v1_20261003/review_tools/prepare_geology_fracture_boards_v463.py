from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,collections,sys,re
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');J=R/'audit/job_geology_painted_fracture_trial_v1_20261003'
attempt=int(sys.argv[1]) if len(sys.argv)>1 else 1
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
A=J/('attempt%02d'%attempt);folder=A/'qa_boards';folder.mkdir(exist_ok=False);boards=[];stats={}
for width in [1280,1600]:
 assert read(J/f'runtime_gate_a{attempt}/capture{width}.receipt.json')['status']=='PASS'
 cap=read(A/f'CAPTURE_{width}.json');stats[str(width)]={'views':len(cap['views']),'frames':len(cap['motion_frames']),'phase_counts':dict(collections.Counter(str(x['phase_index']) for x in cap['motion_frames']))}
 for kind,limit in [('views',6),('motion_frames',12)]:
  rows=cap[kind]
  for start in range(0,len(rows),limit):
   subset=rows[start:start+limit];assert all(sha(R/x['path'])==x['sha256'] for x in subset)
   out=folder/f'{width}_{kind}_{start//limit+1:02d}.png';lst=folder/f'{width}_{kind}_{start//limit+1:02d}.txt'
   lst.write_text(''.join("file '"+(R/x['path']).as_posix()+"'\n" for x in subset),encoding='utf-8',newline='\n')
   cell_width=640 if kind=='views' else 480;grid='2x3' if kind=='views' else '3x4'
   subprocess.run([ff,'-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-frames:v','1','-vf',f'scale={cell_width}:-1,tile={grid}:nb_frames={len(subset)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
   boards.append({'path':out.relative_to(R).as_posix(),'sha256':sha(out),'width':width,'kind':kind,'first':start,'last':start+len(subset)-1,'count':len(subset),'members':subset,'direct_review':False,'ordering':'Consecutive full canvases, row-major. Final blank cells are not frames; QA thumbnails only, never generation or production pixels.'})
write(J/f'QA_BOARD_MANIFEST_A{attempt}.json',{'status':'PREPARED_DIRECT_REVIEW_PENDING','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stats':stats,'boards':boards,'qualification':'Explicit non-runtime inherited draw-only fracture trial, original pixels and mechanics. All selected views and each complete fossil frame need independent direct review. Pan/geode work remain selected views only.'})
shutil.copyfile(Path(__file__),J/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-painted-fracture-trial-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in J.rglob('*') if x.is_file()});write(ip,d)
print(json.dumps({'boards':len(boards),'stats':stats,'attempt':attempt}))
