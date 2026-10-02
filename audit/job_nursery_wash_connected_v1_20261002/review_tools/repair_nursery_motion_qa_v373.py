from pathlib import Path
import hashlib,json,shutil,datetime
from PIL import Image,ImageDraw
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
P=R/'assets_src/local_motion/nursery_connected_scrub_v1_20261002'
A=P/'attempt01'
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
d=read(A/'INDEX.json')
for board in d['boards']:
    p=R/board['path'];shutil.copyfile(p,p.with_name(p.stem+'_failed_overlap.original.png'))
    part=d['frames'][board['first']:board['first']+board['count']]
    canvas=Image.new('RGB',(1792,1706),'#edf5fa');draw=ImageDraw.Draw(canvas)
    draw.text((10,5),'NURSERY SCRUB A1 — LOCAL MOTION REFERENCE, all complete native frames '+str(board['first'])+'-'+str(board['first']+len(part)-1),fill='#25334b')
    for j,row in enumerate(part):
        with Image.open(R/row['path']) as im:im.thumbnail((448,256));canvas.paste(im,(j%4*448,28+j//4*278))
        draw.text((j%4*448+6,28+j//4*278+256),str(row['index']),fill='#25334b')
    canvas.save(p);board['sha256']=sha(p)
d['qa_layout_repair']={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reason':'Initial QA thumbnail row pitch178 was smaller than full thumbnail height256; preserve those unreviewed overlap sheets and rebuild with278 pitch. Native generated video and all41 decoded frames unchanged. No visual acceptance from either layout.'}
write(A/'INDEX.json',d)
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for base in [F,P] for p in base.rglob('*') if p.is_file()});write(ip,imp)
print('QA overlap repaired and failed sheets preserved;41 native frames unchanged.')
