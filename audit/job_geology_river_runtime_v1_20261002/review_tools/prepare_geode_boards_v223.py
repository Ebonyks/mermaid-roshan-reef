from pathlib import Path
import datetime, hashlib, json, shutil, subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geology_river_runtime_v1_20261002';prefix=f.relative_to(b).as_posix()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();boards=[];frames=[]
out=f/'timed_attempt_01/ordered_boards';out.mkdir(exist_ok=False)
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
for width in [1280,1600]:
 d=read(f/('timed_attempt_01/CAPTURE_%d.json'%width));assert len(d['motion_frames'])==156
 for x in d['motion_frames']:assert sha(b/x['path'])==x['sha256']
 frames+=d['motion_frames']
 args=[ffmpeg,'-hide_banner','-loglevel','error','-framerate','30','-i',str(f/('timed_attempt_01/native_views/geode_%d_%%04d.webp'%width)),'-vf','scale=480:-1:flags=lanczos,tile=3x4:nb_frames=12:padding=2:margin=2:color=white','-fps_mode','vfr',str(out/('geode_%d_board_%%02d.png'%width))]
 q=subprocess.run(args,cwd=b,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW);(out/('ffmpeg_%d.stderr.log'%width)).write_bytes(q.stderr)
 found=sorted(out.glob('geode_%d_board_*.png'%width));assert len(found)==13
 for index,p in enumerate(found):boards.append(dict(path=p.relative_to(b).as_posix(),sha256=sha(p),width=width,first_frame=index*12,last_frame=min(index*12+11,155),count=12,ordering='Row-major left to right/top to bottom. Every frame included once, no sampling.',direct_review=False))
write(f/'TIMED_CAPTURE_MANIFEST.json',dict(status='EVERY312_RENDERED_GEODE_FRAMES_PRESERVED_REVIEW_PENDING',frames=frames,boards=boards,qualification='Actual production renderer, normal four-phase touch advancement, no capture freeze or restore interruption. Readback slows wall-clock pacing; timestamps retained, no exact human/device timing acceptance. Every312 frames are native lossless WebP; boards are complete-scene downscale/tiling for review only, never delivery pixels. Not authored cinematic delivery.'))
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geology-river-painted-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
allow=b/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}))
print('Every312 native geode frames in26 complete ordered boards; visual review pending.')
