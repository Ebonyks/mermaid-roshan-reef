from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
f=b/'audit/job_geode_current_recheck_v1_20261002'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
snap=read(f/'SOURCE_CURRENT_BEFORE_CAPTURE.json')['source_files']
assert len(snap)==783 and all(sha(b/x['path'])==x['sha256'] for x in snap)
ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
folder=f/'attempt01/qa_boards';folder.mkdir(exist_ok=False);boards=[]
for width in [1280,1600]:
 assert read(f/f'runtime_gate/capture{width}_v1.receipt.json')['status']=='PASS'
 cap=read(f/f'attempt01/CAPTURE_{width}.json')
 for kind,limit in [('views',6),('motion_frames',12)]:
  rows=cap[kind]
  for start in range(0,len(rows),limit):
   subset=rows[start:start+limit];assert all(sha(b/x['path'])==x['sha256'] for x in subset)
   out=folder/f'{width}_{kind}_{start//limit+1:02d}.png'
   if kind=='views':
    lst=folder/f'{width}_{kind}_{start//limit+1:02d}.txt'
    lst.write_text(''.join("file '"+(b/x['path']).as_posix()+"'\n" for x in subset),encoding='utf-8',newline='\n')
    ins=['-f','concat','-safe','0','-i',str(lst)];size=640;grid='2x3'
   else:
    ins=['-framerate','1','-start_number',str(start),'-i',str(f/f'attempt01/native_frames/geode_{width}_%04d.webp')];size=480;grid='3x4'
   subprocess.run([ff,'-hide_banner','-loglevel','error',*ins,'-frames:v','1','-vf',f'scale={size}:-1,tile={grid}:nb_frames={len(subset)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
   boards.append(dict(path=out.relative_to(b).as_posix(),sha256=sha(out),width=width,kind=kind,first=start,last=start+len(subset)-1,count=len(subset),members=subset,direct_review=False,ordering='Consecutive row-major unchanged complete native canvases. Declared final partial board empty cells are not frames. Whole-canvas review thumbnails only; original bytes and dimensions preserved.'))
write(f/'QA_BOARD_MANIFEST_V1.json',dict(status='PREPARED_DIRECT_REVIEW_PENDING',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),views=58,motion_frames=sum(x['count'] for x in boards if x['kind']=='motion_frames'),boards=boards,qualification='No production pixels or mechanics changed. Exact source boundary unchanged. Thumbnail boards are QA displays, not regenerated art or cinematic delivery.'))
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-current-recheck-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print(json.dumps(dict(boards=len(boards),views=58,frames=sum(x['count'] for x in boards if x['kind']=='motion_frames'))))
