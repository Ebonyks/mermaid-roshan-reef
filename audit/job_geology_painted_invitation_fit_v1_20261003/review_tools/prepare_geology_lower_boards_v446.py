from pathlib import Path
import json,hashlib,datetime,subprocess,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=R/'audit/job_geology_painted_invitation_fit_v1_20261003'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ff='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
folder=P/'attempt02/qa_boards';folder.mkdir(exist_ok=False);boards=[]
for width in [1280,1600]:
 assert read(P/f'runtime_gate_lower_a2/capture{width}.receipt.json')['status']=='PASS'
 rows=read(P/f'attempt02/CAPTURE_{width}.json')['views'];assert len(rows)==29
 for start in range(0,len(rows),6):
  sub=rows[start:start+6];assert all(sha(R/x['path'])==x['sha256'] for x in sub)
  out=folder/f'{width}_views_{start//6+1:02d}.png';lst=out.with_suffix('.txt')
  lst.write_text(''.join("file '"+(R/x['path']).as_posix()+"'\n" for x in sub),encoding='utf-8',newline='\n')
  subprocess.run([ff,'-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(lst),'-frames:v','1','-vf',f'scale=640:-1,tile=2x3:nb_frames={len(sub)}:padding=2:margin=2:color=white',str(out)],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  boards.append(dict(path=out.relative_to(R).as_posix(),sha256=sha(out),width=width,first=start,last=start+len(sub)-1,members=sub,direct_review=False))
write(P/'QA_BOARD_MANIFEST_A2.json',dict(status='PREPARED_DIRECT_REVIEW_PENDING',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),boards=boards,qualification='All58 selected native full canvases of lower-foreground A2 non-runtime prop-fit fixture. A1 exact failed layout preserved separately. No whole motion, current production or owner acceptance. Empty final board cells are not images.'))
shutil.copyfile(Path(__file__),P/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-geology-painted-invitation-fit-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{x.relative_to(R).as_posix() for x in P.rglob('*') if x.is_file()});write(ip,d)
print(json.dumps([dict(path=x['path'],first=x['first'],last=x['last'],width=x['width']) for x in boards]))
