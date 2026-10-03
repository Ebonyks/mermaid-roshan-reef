from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
from PIL import Image,ImageDraw
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=R/'assets_src/local_motion/nursery_connected_scrub_v2_20261002';A=P/'attempt01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
state=read(R/'build/nursery_local_scrub_a2_active_20261002/STATE.json')
assert state['status']=='ALL_MACHINE_RENDERS_DONE_VISUAL_REVIEW_PENDING'
receipt_path=Path(state['jobs'][0]['receipt_path']);receipt=read(receipt_path);m=read(P/'MANIFEST.json')
assert receipt['status']=='PASS' and receipt['source_sha256']==m['input_sha256'] and receipt['settings']==m['renderer']['settings']
assert receipt['prompt_sha256']==hashlib.sha256((P/m['prompt_path']).read_text(encoding='utf-8').encode()).hexdigest()
assert not A.exists();A.mkdir();(A/'native_frames').mkdir()
for name in ('RENDER_RECEIPT.json','workflow.api.json','COMFY_HISTORY.json'):shutil.copyfile(receipt_path.with_name(name),A/name)
shutil.copyfile(R/'build/nursery_local_scrub_a2_active_20261002/STATE.json',A/'DISPATCH_STATE.json')
shutil.copyfile(R/'build/nursery_local_scrub_a2_active_20261002/NUR-SCRUB-A2.log',A/'DISPATCH.log')
outputs=[]
for row in receipt['outputs']:
 s=Path(row['path']).resolve();assert s.is_relative_to(Path('H:/MermaidReefTools/LocalVideo/output').resolve()) and sha(s)==row['sha256']
 t=A/s.name;shutil.copyfile(s,t);assert sha(t)==row['sha256'];outputs.append(dict(path=t.relative_to(R).as_posix(),sha256=sha(t),native_source=str(s)))
video=next(R/x['path'] for x in outputs if x['path'].endswith('.webm'))
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
cmd=[ffmpeg,'-hide_banner','-loglevel','error','-n','-i',str(video),'-fps_mode','passthrough',str(A/'native_frames/frame_%03d.png')]
p=subprocess.run(cmd,cwd=R,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
(A/'decode.stdout.log').write_bytes(p.stdout);(A/'decode.stderr.log').write_bytes(p.stderr)
frames=sorted((A/'native_frames').glob('*.png'));assert len(frames)==41
rows=[]
for i,p in enumerate(frames):
 with Image.open(p) as im:assert im.size==(896,512)
 rows.append(dict(index=i,path=p.relative_to(R).as_posix(),sha256=sha(p),timestamp_seconds=i/24))
boards=[]
for offset in (0,16,32):
 part=rows[offset:offset+16];canvas=Image.new('RGB',(1792,1140),'#edf5fa');draw=ImageDraw.Draw(canvas)
 draw.text((10,6),'NURSERY SCRUB A2 - REFERENCE ONLY - native frames '+str(offset)+'-'+str(offset+len(part)-1),fill='#25344b')
 for j,row in enumerate(part):
  x=j%4*448;y=30+j//4*278
  with Image.open(R/row['path']) as im:im=im.resize((448,256));canvas.paste(im,(x,y))
  draw.text((x+6,y+259),'frame '+str(row['index'])+'  t='+format(row['timestamp_seconds'],'.3f'),fill='#25344b')
 p=A/('QA_BOARD_%02d.png'%offset);canvas.save(p);boards.append(dict(path=p.relative_to(R).as_posix(),sha256=sha(p),first=offset,count=len(part),qa_only=True,production_pixels=False,pitch=278,full_native_canvas=True))
write(A/'INDEX.json',dict(status='MACHINE_PASS_ALL41_NATIVE_FRAME_REVIEWS_PENDING',archived_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),prompt_id=receipt['prompt_id'],source_sha256=receipt['source_sha256'],outputs=outputs,frames=rows,boards=boards,decode_command=cmd,qualification='Direct unchanged decoding and labeled QA thumbnails only. Successful render/decoded frames do not grant action/visual/cinematic/owner acceptance.'))
shutil.copyfile(__file__,P/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-nursery-scrub-a2-20261002.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(R).as_posix() for p in P.rglob('*') if p.is_file()});d['validation'].append(dict(command='Developed local quiet-idle FIFO A2 and exact native output archival',result='PASS',evidence='assets_src/local_motion/nursery_connected_scrub_v2_20261002/attempt01/RENDER_RECEIPT.json; every41 visual review pending.'));write(ip,d)
print('A2_NATIVE_ARCHIVED|41 direct decoded896x512 frames|3 nonoverlap ordered QA sheets|visual scores pending')
