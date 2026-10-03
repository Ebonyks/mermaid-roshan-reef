from pathlib import Path
import argparse,datetime,hashlib,json,subprocess
from PIL import Image,ImageDraw
B=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
P=B/'assets_src/local_motion/candy_twist_release_components_v1_20261003'
stage=argparse.ArgumentParser();stage.add_argument('stage',choices=['release','twist']);stage=stage.parse_args().stage
M=P/(stage+'_a1');A=M/'attempt01';S=B/('build/candy_'+stage+'_component_a1_20261003')
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,data):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.v641_next');t.write_bytes(data);t.replace(p)
def write(p,d):put(p,(json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
state=read(S/'STATE.json');assert state['status']=='ALL_MACHINE_RENDERS_DONE_VISUAL_REVIEW_PENDING'
receipt_path=Path(state['jobs'][0]['receipt_path']);receipt=read(receipt_path);m=read(M/'checks/SUBMITTED_MANIFEST.exact.json')
assert receipt['status']=='PASS' and receipt['source_sha256']==m['input_sha256'] and receipt['settings']==m['renderer']['settings']
assert receipt['prompt_sha256']==hashlib.sha256((M/m['prompt_path']).read_text(encoding='utf-8').encode()).hexdigest()
assert state['manifest_sha256']==sha(M/'checks/SUBMITTED_MANIFEST.exact.json')
assert not A.exists();A.mkdir();(A/'native_frames').mkdir()
for name in ('RENDER_RECEIPT.json','workflow.api.json','COMFY_HISTORY.json'):
 put(A/name,receipt_path.with_name(name).read_bytes())
put(A/'DISPATCH_STATE.json',(S/'STATE.json').read_bytes())
put(A/'DISPATCH.log',(S/(m['jobs'][0]['id']+'.log')).read_bytes())
outputs=[]
for row in receipt['outputs']:
 s=Path(row['path']).resolve();assert s.is_relative_to(Path('H:/MermaidReefTools/LocalVideo/output').resolve()) and sha(s)==row['sha256']
 t=A/s.name;put(t,s.read_bytes());assert sha(t)==row['sha256'];outputs.append(dict(path=t.relative_to(B).as_posix(),sha256=sha(t),native_source=str(s)))
video=next(B/x['path'] for x in outputs if x['path'].endswith('.webm'))
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
cmd=[ffmpeg,'-hide_banner','-loglevel','error','-n','-i',str(video),'-fps_mode','passthrough',str(A/'native_frames/frame_%03d.png')]
r=subprocess.run(cmd,cwd=B,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
put(A/'decode.stdout.log',r.stdout);put(A/'decode.stderr.log',r.stderr)
frames=sorted((A/'native_frames').glob('*.png'));assert len(frames)==41
rows=[]
for i,p in enumerate(frames):
 with Image.open(p) as im:assert im.size==(896,512)
 rows.append(dict(index=i,path=p.relative_to(B).as_posix(),sha256=sha(p),timestamp_seconds=i/24))
boards=[]
for offset in range(0,41,6):
 part=rows[offset:offset+6];canvas=Image.new('RGB',(1792,1640),'#edf5fa');draw=ImageDraw.Draw(canvas)
 draw.text((10,6),'CANDY '+stage.upper()+' A1 - COMPONENT REFERENCE ONLY - native frames '+str(offset)+'-'+str(offset+len(part)-1),fill='#25344b')
 for j,row in enumerate(part):
  x=j%2*896;y=32+j//2*536
  with Image.open(B/row['path']) as im:canvas.paste(im,(x,y))
  draw.text((x+6,y+514),'frame '+str(row['index'])+'  t='+format(row['timestamp_seconds'],'.3f'),fill='#25344b')
 p=A/('QA_BOARD_%02d.png'%offset);canvas.save(p);boards.append(dict(path=p.relative_to(B).as_posix(),sha256=sha(p),first=offset,count=len(part),qa_only=True,production_pixels=False,pitch=536,full_native_canvas=True,source_pixels_resampled=False))
write(A/'INDEX.json',dict(status='MACHINE_PASS_ALL41_NATIVE_FRAME_REVIEWS_PENDING',archived_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stage=stage,prompt_id=receipt['prompt_id'],source_sha256=receipt['source_sha256'],submitted_manifest_sha256=sha(M/'checks/SUBMITTED_MANIFEST.exact.json'),outputs=outputs,frames=rows,boards=boards,decode_command=cmd,qualification='Direct unchanged decoding and labeled native-size QA boards only. Successful render/decoded frames do not grant action/visual/cinematic/owner acceptance.'))
put(P/'review_tools'/Path(__file__).name,Path(__file__).read_bytes())
ip=B/'design/audit_impacts/job-candy-twist-release-components-20261003.json';d=read(ip);d['files']=sorted(set(d['files'])|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()});d['validation'].append(dict(command='Guarded developed local '+stage+' component, exact submitted manifest and direct native decoding',result='PASS',evidence=(A/'RENDER_RECEIPT.json').relative_to(B).as_posix()+'; every41 visual review pending.'));write(ip,d)
allow=B/'tmp/v2_preview_allowed.json';a=read(allow);assert isinstance(a,list);a=sorted(set(a)|{p.relative_to(B).as_posix() for p in P.rglob('*') if p.is_file()});write(allow,a)
print(stage.upper()+'_NATIVE_ARCHIVED|41 direct decoded896x512 frames|7 ordered original-size QA boards|visual scores pending',flush=True)
