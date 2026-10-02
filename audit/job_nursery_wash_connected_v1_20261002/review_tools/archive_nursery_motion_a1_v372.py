from pathlib import Path
import datetime,hashlib,json,shutil,subprocess
from PIL import Image,ImageDraw
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
A=P/'attempt01'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
state=read(R/'build/nursery_local_scrub_active_20261002/STATE.json')
native=Path(state['jobs'][0]['receipt_path'])
receipt=read(native);manifest=read(P/'MANIFEST.json')
assert receipt['status']=='PASS' and receipt['source_sha256']==manifest['input_sha256']
assert receipt['prompt_sha256']==hashlib.sha256((P/manifest['prompt_path']).read_text(encoding='utf-8').encode()).hexdigest()
assert receipt['settings']==manifest['renderer']['settings']
assert not A.exists();A.mkdir();(A/'native_frames').mkdir()
for name in ['RENDER_RECEIPT.json','workflow.api.json','COMFY_HISTORY.json']:shutil.copyfile(native.with_name(name),A/name)
outputs=[]
for row in receipt['outputs']:
    source=Path(row['path']).resolve()
    assert source.is_relative_to(Path('H:/MermaidReefTools/LocalVideo/output').resolve())
    assert sha(source)==row['sha256']
    destination=A/source.name;shutil.copyfile(source,destination)
    outputs.append({'path':destination.relative_to(R).as_posix(),'sha256':sha(destination),'native_source':str(source)})
video=next(R/x['path'] for x in outputs if x['path'].endswith('.webm'))
ffmpeg='C:/Users/Peter/AppData/Local/Programs/MermaidReefTools/FFmpeg/8.1.2/bin/ffmpeg.exe'
command=[ffmpeg,'-hide_banner','-loglevel','error','-n','-i',str(video),'-fps_mode','passthrough',str(A/'native_frames/frame_%03d.png')]
result=subprocess.run(command,cwd=R,capture_output=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
(A/'decode.stdout.log').write_bytes(result.stdout);(A/'decode.stderr.log').write_bytes(result.stderr)
frames=sorted((A/'native_frames').glob('*.png'));assert len(frames)==41
rows=[]
for i,p in enumerate(frames):
    with Image.open(p) as im:assert im.size==(896,512)
    rows.append({'index':i,'path':p.relative_to(R).as_posix(),'sha256':sha(p),'timestamp_seconds':i/24})
boards=[]
for offset in [0,24]:
    part=rows[offset:offset+24]
    canvas=Image.new('RGB',(1792,1100),'#edf5fa');draw=ImageDraw.Draw(canvas)
    draw.text((10,5),'NURSERY SCRUB A1 — LOCAL MOTION REFERENCE, all native frames '+str(offset)+'-'+str(offset+len(part)-1),fill='#25334b')
    for j,row in enumerate(part):
        with Image.open(R/row['path']) as im:im.thumbnail((448,256));canvas.paste(im,(j%4*448,28+j//4*178))
        # Thumbnail cell retains the full canvas at its native aspect.
        draw.text((j%4*448+6,28+j//4*178+160),str(row['index']),fill='#25334b')
    p=A/('QA_BOARD_%02d.png'%offset);canvas.save(p)
    boards.append({'path':p.relative_to(R).as_posix(),'sha256':sha(p),'first':offset,'count':len(part),'qa_only':True,'production_pixels':False})
write(A/'INDEX.json',{'status':'MACHINE_PASS_EVERY_NATIVE_FRAME_VISUAL_REVIEW_PENDING','archived_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prompt_id':receipt['prompt_id'],'source_sha256':receipt['source_sha256'],'outputs':outputs,'frames':rows,'boards':boards,'decode_command':command,'qualification':'Unchanged native generated reference video archived with exact hashes. PNG frames are ordinary direct decoding, not individually regenerated full-frame cinematic evidence. QA contact sheets do not grant acceptance.'})
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,P] for p in base.rglob('*') if p.is_file()})
write(ip,imp)
write(R/'tmp/v2_preview_allowed.json',sorted(set(read(R/'tmp/v2_preview_allowed.json'))|set(imp['files'])))
print('NURSERY_REFERENCE_A1|41 unchanged native frames decoded; 2 QA sheets; successful native render archived; visual score pending.')
