from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
b=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef');f=b/'audit/job_geode_route_emblem_runtime_v1_20261002';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
folder=f/'attempt_01/native_still_boards';folder.mkdir(exist_ok=False);boards=[]
for width in [1280,1600]:
 assert read(f/f'runtime_gate/capture{width}v1.receipt.json')['status']=='PASS';cap=read(f/f'attempt_01/CAPTURE_{width}.json');assert len(cap['views'])==29
 for i in range(0,29,6):
  views=cap['views'][i:i+6];assert all(sha(b/x['path'])==x['sha256'] for x in views);lst=folder/f'{width}_{i//6+1:02d}.txt';lst.write_text(''.join("file '"+(b/x['path']).as_posix()+"'\n" for x in views),encoding='utf-8',newline='\n');out=folder/f'{width}_{i//6+1:02d}.png'
  subprocess.run(['C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-frames:v','1','-vf',f'scale=640:-1,tile=2x3:nb_frames={len(views)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  boards.append(dict(path=out.relative_to(b).as_posix(),sha256=sha(out),width=width,index=i//6+1,views=views,count=len(views),ordering='Row-major; each full unchanged captured native canvas, uniform whole-frame display normalization only; final board has five images and one blank cell.',direct_review=False))
write(f/'STILL_BOARD_MANIFEST.json',dict(status='ALL58_NATIVE_STILLS_BOARDS_READY_REVIEW_PENDING',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),boards=boards,qualification='Native originals/hashes preserved. Every individual source still and ordered-frame review remains required. No game art edits or pixels inserted; report contact sheets only.'));shutil.copyfile(__file__,f/'review_tools'/Path(__file__).name)
ip=b/'design/audit_impacts/job-geode-route-emblem-runtime-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()});write(ip,d);allow=b/'tmp/v2_preview_allowed.json';write(allow,sorted(set(read(allow))|{p.relative_to(b).as_posix() for p in f.rglob('*') if p.is_file()}));print('Prepared ten ordered still boards containing every58 complete captured native views; review pending.',flush=True)
