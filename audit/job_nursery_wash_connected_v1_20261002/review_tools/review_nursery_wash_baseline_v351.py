from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json,datetime,shutil
R=Path('C:/Users/Peter/.codex/worktrees/job-art-review-v2-20261001/mermaid-roshan-reef')
F=R/'audit/job_nursery_wash_connected_v1_20261002'
S=R/'assets_src/imagegen/nursery_wash_connected_v1_20261002'
receipt=json.loads((F/'baseline_capture/native_frames/CAPTURE_RECEIPT.json').read_text())
assert receipt['status']=='PASS_EIGHT_NATIVE_ROOM_ROUTES'
qa=F/'baseline_visual';qa.mkdir()
boards=[];details=[]
for case in receipt['cases']:
    frames=[x for x in receipt['frames'] if x['case']==case['id']]
    if 'nursery' in case['id']:
        for offset in range(0,len(frames),48):
            part=frames[offset:offset+48]
            canvas=Image.new('RGB',(1440,1232),'#f0e9db');d=ImageDraw.Draw(canvas)
            d.text((8,6),case['id']+' ALL consecutive native frames '+str(offset)+'-'+str(offset+len(part)-1),fill='#243652')
            for j,row in enumerate(part):
                with Image.open(F/'baseline_capture/native_frames'/row['path']) as im: im.load();im.thumbnail((240,135));canvas.paste(im,(j%6*240,30+j//6*150))
                d.text((j%6*240+3,30+j//6*150+135),f"{row['capture_index']:04d} p={row['phase_progress']:.2f} {row['event'][:18]}",fill='#243652')
            p=qa/(case['id']+'_%02d.png'%(offset//48));canvas.save(p)
            boards.append({'path':p.relative_to(R).as_posix(),'case':case['id'],'first':offset,'count':len(part),'qa_only':True,'delivery_pixels':False})
    for index in [case['opened_frame']+10,case['accepted_frame']-5,case['advanced_frame']+7]:
        row=frames[index];p=qa/(case['id']+'_%04d.webp'%index)
        shutil.copyfile(F/'baseline_capture/native_frames'/row['path'],p)
        details.append({'path':p.relative_to(R).as_posix(),'case':case['id'],'frame':index,'event':row['event'],'phase_progress':row['phase_progress']})
(qa/'INDEX.json').write_text(json.dumps({'boards':boards,'native_details':details,'status':'DIRECT_VISUAL_REVIEW_PENDING','qualifications':'Read-only QA contact sheets; every Nursery frame represented, Doctor control details sampled. Original full native sequences preserved and separately inspectable. No generated production pixels.'},indent=2)+'\n',encoding='utf-8')
scores={'ready_attempt01':(4.5,'Clear initial joined hands, complete own-costume body, child-readable ceramic basin. Initial readiness is static; no actual action claim.'),'wet_attempt01':(4.5,'Flow leaves the correct spout and visibly meets hands in basin. Far fingers partly occluded; full action/mounted scale pending.'),'rub_attempt01':(4.4,'Soft lather and connected limbs pass material quality; same-direction fingers read as clasp/clap rather than an explicit rubbing movement. Preserve as weak transitional candidate.'),'rub_back_attempt01':(4.5,'Near palm clearly contacts far hand back, connected wrists and small lather. Static washing intent meets provisional source floor; movement pending.'),'rinse_attempt01':(4.5,'Correct stream-to-hand-to-basin contact; reduced lather leaves a small wrist bubble. Actual removal/time continuity requires mounted review.'),'clean_attempt01':(4.6,'Two legible clean palms, five fingers each, faucet off and no foam. Lift from rinse is a larger pose change requiring transition review.')}
for folder,(score,note) in scores.items():
    p=S/folder;native=p/'native.png';prompt=p/'PROMPT.json'
    with Image.open(native) as im:
        im.load();alpha=im.getchannel('A');metadata={'mode':im.mode,'size':list(im.size),'alpha_extrema':list(alpha.getextrema()),'alpha_bbox':list(alpha.getbbox())}
    with Image.open(R/('assets/opera/worlds/nursery/wash_connected_v1_20261002/'+{'ready_attempt01':'ready','wet_attempt01':'wet','rub_attempt01':'rub_palm','rub_back_attempt01':'rub_back','rinse_attempt01':'rinse','clean_attempt01':'clean'}[folder]+'.png')) as im:
        im.load();runtime={'size':list(im.size),'mode':im.mode,'alpha_extrema':list(im.getchannel('A').getextrema())}
    refs=json.loads(prompt.read_text());refpaths=refs.get('references',[refs.get('reference')])
    review={'status':'WEAK_SOURCE_REFINEMENT_REQUIRED' if score<4.5 else 'PROVISIONAL_STATIC_SOURCE_FLOOR_ONLY','score':score,'note':note,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Direct complete native images displayed by built-in imagegen and inspected by root; separate from mounted action.','native':metadata,'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'prompt_sha256':hashlib.sha256(prompt.read_bytes()).hexdigest(),'references':[{'path':x,'sha256':hashlib.sha256((R/x).read_bytes()).hexdigest()} for x in refpaths],'runtime_normalization':runtime,'mounted_score':None,'action_score':None,'owner_approval':False,'priority_inclusive':score<=4.5}
    (p/'SOURCE_REVIEW.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
license=R/'ASSET_LICENSES.md'
with license.open('a',encoding='utf-8') as out:
    out.write('\n<!-- Nursery washing connected source/reversible draft 2026-10-02; complete action/owner acceptance remains pending. -->\n')
    for folder in scores:
        out.write('| `assets_src/imagegen/nursery_wash_connected_v1_20261002/'+folder+'/native.png` | OpenAI built-in imagegen, own Nursery costume identity reference | Project generated art; OpenAI terms | https://openai.com/policies/terms-of-use/ | Fresh connected handwashing state; native RGBA preserved, prompts/reference SHA and provisional opinions in SOURCE_REVIEW.json. |\n')
    for name in ['ready','wet','rub_palm','rub_back','rinse','clean']:
        out.write('| `assets/opera/worlds/nursery/wash_connected_v1_20261002/'+name+'.png` | Corresponding native connected washing state above | Project generated art; OpenAI terms | https://openai.com/policies/terms-of-use/ | Uniform whole-canvas 1280 to1024 POT normalization; no crop, mask, subject translation or pixel repair. Reversible review draft, movement/owner acceptance pending. |\n')
print(json.dumps({'boards':len(boards),'nursery_consecutive_frames':sum(x['count'] for x in boards),'native_details':len(details),'all_eight_native_frames':len(receipt['frames']),'source_opinions':len(scores),'capture_bytes':sum(p.stat().st_size for p in (F/'baseline_capture/native_frames').rglob('*.webp'))}))
