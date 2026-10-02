from pathlib import Path
import datetime,hashlib,json,shutil
from PIL import Image,ImageDraw
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
O=F/'doctor_dated_full_review_v1'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
ip=R/'design/audit_impacts/job-nursery-wash-connected-20261002.json';imp=read(ip)
imp['scope']+=' Complete direct review of every preserved Doctor baseline washing frame as dated historical supporting evidence, without claiming that the old source boundary renders current Doctor gameplay or constitutes a birthday route. No Doctor source/mechanics or opinion promotion; unresolved contacts remain priorities.'
write(ip,imp)
assert not O.exists();O.mkdir()
receipt=read(F/'baseline_capture/native_frames/CAPTURE_RECEIPT.json')
assert receipt['status']=='PASS_EIGHT_NATIVE_ROOM_ROUTES'
boards=[];cases=[];details=[]
oldindex=read(F/'baseline_visual/INDEX.json')
for case in receipt['cases']:
    if 'doctor' not in case['id']:continue
    rows=[x for x in receipt['frames'] if x['case']==case['id']]
    assert len(rows)==case['frame_count']
    cases.append({'id':case['id'],'frames':len(rows),'qualification':'Preserved initial direct training/authored catalog fixture; not normal birthday route, current rendered source or complete career reward. Original capture metadata and boundary qualify it.'})
    for offset in range(0,len(rows),48):
        part=rows[offset:offset+48]
        canvas=Image.new('RGB',(1440,1232),'#f0e9db');draw=ImageDraw.Draw(canvas)
        draw.text((8,6),case['id']+' DATED BASELINE, every frame '+str(offset)+'-'+str(offset+len(part)-1),fill='#243652')
        for j,row in enumerate(part):
            native=F/'baseline_capture/native_frames'/row['path']
            if row.get('sha256'):assert sha(native)==row['sha256']
            with Image.open(native) as image:image.load();image.thumbnail((240,135));canvas.paste(image,(j%6*240,30+j//6*150))
            draw.text((j%6*240+3,30+j//6*150+135),f"{row['capture_index']:04d} p={row['phase_progress']:.2f} {row['event'][:18]}",fill='#243652')
        p=O/(case['id']+'_%02d.png'%(offset//48));canvas.save(p)
        boards.append({'path':p.relative_to(R).as_posix(),'case':case['id'],'first':offset,'count':len(part),'sha256':sha(p),'qa_only':True,'production_pixels':False})
    for d in oldindex['native_details']:
        if d['case']==case['id']:
            d=dict(d,sha256=sha(R/d['path']));details.append(d)
write(O/'INDEX.json',{'status':'DIRECT_DATED_DOCTOR_REVIEW_PENDING','prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':cases,'boards':boards,'native_details':details,'frame_total':sum(x['frames'] for x in cases),'source_receipt':'audit/job_nursery_wash_connected_v1_20261002/baseline_capture/native_frames/CAPTURE_RECEIPT.json','claim_correction':'audit/job_nursery_wash_connected_v1_20261002/baseline_capture/CLAIM_CORRECTION.json','qualification':'New QA-only boards preserve the old captures unchanged. Direct review of dated frames is independent of current-render and machine/device/child/owner gates. Doctor/Nursery absent from actual birthday roster.'})
shutil.copyfile(Path(__file__),F/'review_tools'/Path(__file__).name)
imp=read(ip);imp['files']=sorted(set(imp['files'])|{p.relative_to(R).as_posix() for p in F.rglob('*') if p.is_file()});write(ip,imp)
print(json.dumps({'dated_doctor_frames':sum(x['frames'] for x in cases),'boards':len(boards),'native_details':len(details)}))
