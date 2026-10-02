from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002';prefix=f.relative_to(b).as_posix();width=int(sys.argv[1]);assert width in [1280,1600]
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
snap=read(f/'SOURCE_CURRENT_BEFORE_CAPTURES.json')['source_files'];assert len(snap)==372 and all(sha(b/x['path'])==x['sha256'] for x in snap)
assert read(f/f'runtime_gate/capture{width}v1.receipt.json')['status']=='PASS'
cap=read(f/f'attempt_01/CAPTURE_{width}.json');boards=[]
folder=f/'attempt_01/ordered_boards';folder.mkdir(exist_ok=True)
ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
for n in range(0,len(cap['motion_frames']),12):
 frames=cap['motion_frames'][n:n+12];assert all(sha(b/x['path'])==x['sha256'] for x in frames)
 out=folder/f'geode_{width}_board_{n//12+1:02d}.png';assert not out.exists()
 subprocess.run([ff,'-hide_banner','-loglevel','error','-framerate','1','-start_number',str(n),'-i',str(f/f'attempt_01/native_frames/geode_{width}_%04d.webp'),'-frames:v','1','-vf',f'scale=480:-1,tile=3x4:nb_frames={len(frames)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 boards.append(dict(path=out.relative_to(b).as_posix(),sha256=sha(out),width=width,first_frame=n,last_frame=n+len(frames)-1,count=len(frames),direct_review=False,ordering='Every consecutive rendered frame in row-major order; final partial board has declared count and remaining empty cells.'))
write(f/f'BOARD_MANIFEST_{width}.json',dict(status='ALL_RENDERED_FRAMES_BOARDS_READY_REVIEW_PENDING',source_files=snap,additional_review_fixture=dict(path=prefix+'/capture.gd',sha256=sha(f/'capture.gd')),views=cap['views'],frames=cap['motion_frames'],boards=boards,qualification=cap['qualification']+' Fresh current full CI remains pending; previousK receipt applies only to its prior368 source boundary.'))
if Path(__file__).resolve() != (f/'review_tools'/Path(__file__).name).resolve():shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print(json.dumps(dict(width=width,views=len(cap['views']),frames=len(cap['motion_frames']),boards=len(boards))))
