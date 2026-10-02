from pathlib import Path
import hashlib,json,shutil,subprocess,sys
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_coherent_runtime_v1_20261002';width=int(sys.argv[1])
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=read(f/('attempt_02/CAPTURE_%d.json'%width));frames=raw['motion_frames'];assert len(frames)==156 and all(sha(b/x['path'])==x['sha256'] for x in frames)
out=f/'attempt_02/ordered_boards';out.mkdir(exist_ok=True);assert not list(out.glob('geode_%d_board_*.png'%width))
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe';args=[ffmpeg,'-hide_banner','-loglevel','error','-framerate','30','-i',str(f/('attempt_02/native_views/geode_%d_%%04d.webp'%width)),'-vf','scale=480:-1:flags=lanczos,tile=3x4:nb_frames=12:padding=2:margin=2:color=white','-fps_mode','vfr',str(out/('geode_%d_board_%%02d.png'%width))]
q=subprocess.run(args,cwd=b,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW);(out/('ffmpeg_%d.stderr.log'%width)).write_bytes(q.stderr)
boards=[dict(path=p.relative_to(b).as_posix(),sha256=sha(p),width=width,first_frame=i*12,last_frame=min(i*12+11,155),count=12,ordering='Complete12 frames, row-major, no sampling.',direct_review=False) for i,p in enumerate(sorted(out.glob('geode_%d_board_*.png'%width)))];assert len(boards)==13
baseline=read(b/'audit/job_geode_coherent_runtime_v1_20261002/full_ci_v2/SOURCE_BEFORE.json')['source_files'];assert len(baseline)==368
checks=[dict(path=x['path'],before_sha256=x['sha256'],current_sha256=sha(b/x['path'])) for x in baseline];assert all(x['before_sha256']==x['current_sha256'] for x in checks)
write(f/('BOARD_MANIFEST_V2_%d.json'%width),dict(status='156_NATIVE_FRAMES13_ORDERED_BOARDS_REVIEW_PENDING',frames=frames,boards=boards,production_source_checks=checks,qualification='Actual production seven-state geode render through ordinary intentional career input. Every rendered frame preserved; no freeze/restore interruption. No injected surface, freeze, explicit JSON restore interruption or phase forcing. All368 current frozen source hashes unchanged; machine input/save/ordinary advancement does not establish visual/device/child/owner acceptance. Readback slows wall clock, empty callback tail does not exercise real production return. Boards review-only uniform whole-scene scaling/tiling, not cinematic or delivery art.'))
shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-coherent-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d)
print(str(width)+': every156 frames/13 ordered boards;368 current production source hashes unchanged.')
