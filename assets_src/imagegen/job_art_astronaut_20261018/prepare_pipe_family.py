from pathlib import Path
import json,hashlib
from collections import deque
import numpy as np
from PIL import Image,ImageDraw
root=Path.cwd();src=root/'assets_src/imagegen/job_art_astronaut_20261018';out=root/'assets/opera/worlds/widgets';out.mkdir(parents=True,exist_ok=True)
regions={'h':{'W':(0,.3,.2,.7),'E':(.8,.3,1,.7)},'v':{'N':(.3,0,.7,.25),'S':(.3,.75,.7,1)},'ne':{'N':(.1,0,.55,.3),'E':(.75,.45,1,.85)},'nw':{'N':(.55,0,1,.3),'W':(0,.5,.3,1)},'se':{'S':(.12,.7,.62,1),'E':(.7,.15,1,.6)},'sw':{'S':(.55,.7,1,1),'W':(0,.15,.35,.6)}}
targets={'N':np.array([128.,16.]),'S':np.array([128.,240.]),'W':np.array([16.,128.]),'E':np.array([240.,128.])}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def port_center(image,region):
    pixels=np.array(image);h,w=pixels.shape[:2];r,g,b,a=[pixels[:,:,i].astype(float) for i in range(4)]
    mask=(a>128)&(g>r*1.25)&(b>r*1.2)&(r<80)&(g<125)&(b<180)
    x0,y0,x1,y1=[round(v*s) for v,s in zip(region,[w,h,w,h])]
    mask=mask[y0:y1,x0:x1].copy();largest=[]
    for yy,xx in zip(*np.nonzero(mask)):
        if not mask[yy,xx]:continue
        queue=deque([(yy,xx)]);mask[yy,xx]=False;component=[]
        while queue:
            y,x=queue.popleft();component.append((x+x0,y+y0))
            for ny,nx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx]:
                    mask[ny,nx]=False;queue.append((ny,nx))
        if len(component)>len(largest):largest=component
    assert len(largest)>100
    return np.mean(largest,axis=0)
records=[];sheet=Image.new('RGB',(768,512),'#342e49');draw=ImageDraw.Draw(sheet)
for index,(face,regions_for_face) in enumerate(regions.items()):
    paths=[src/('pipe_'+face+'_'+state+'_native.png') for state in ['rest','fueled']]
    images=[Image.open(p).convert('RGBA') for p in paths]
    assert images[0].size==images[1].size
    source=np.array([port_center(images[0],box) for box in regions_for_face.values()]);target=np.array([targets[k] for k in regions_for_face])
    native_delta=source[1]-source[0];target_delta=target[1]-target[0]
    scale=float(np.dot(native_delta,target_delta)/np.dot(native_delta,native_delta));offset=target.mean(axis=0)-source.mean(axis=0)*scale
    boxes=[im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox() for im in images]
    box=(max(0,min(b[0] for b in boxes)-4),max(0,min(b[1] for b in boxes)-4),min(images[0].width,max(b[2] for b in boxes)+4),min(images[0].height,max(b[3] for b in boxes)+4))
    # Minimax rigid registration with explicit contour bounds. Shrinking about
    # canvas center needlessly unbalances the two ports on an asymmetric elbow.
    best=None
    grid=np.array([(x,y) for x in np.linspace(-4,4,17) for y in np.linspace(-4,4,17)])
    for candidate_scale in np.linspace(scale*.90,scale*1.05,121):
        low=np.array([4.,4.])-np.array(box[:2])*candidate_scale
        high=np.array([252.,252.])-np.array(box[2:])*candidate_scale
        if np.any(low>high):continue
        ideal=target.mean(axis=0)-source.mean(axis=0)*candidate_scale
        offsets=np.clip(ideal+grid,low,high)
        errors=np.linalg.norm(source[None,:,:]*candidate_scale+offsets[:,None,:]-target[None,:,:],axis=2).max(axis=1)
        winner=int(np.argmin(errors));score=float(errors[winner])
        if best is None or score<best[0]:best=(score,float(candidate_scale),offsets[winner])
    assert best is not None
    _,scale,offset=best
    residuals=np.linalg.norm(source*scale+offset-target,axis=1)
    a=np.array(images[0].getchannel('A'))>=16;b=np.array(images[1].getchannel('A'))>=16
    iou=float(np.logical_and(a,b).sum()/np.logical_or(a,b).sum())
    assert iou>=.98,(face,'state silhouette drift',iou)
    # A measured candidate may fail registration; retain the number rather than warp it.
    geometry_status='PASS_TRIAL' if max(residuals)*124/256 <= 4 else 'FAIL_REGENERATE_GEOMETRY'
    for state,image,path in zip(['rest','fueled'],images,paths):
        crop=image.crop(box);small=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
        xy=tuple(round(v) for v in (offset+np.array(box[:2])*scale));canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(small,xy)
        suffix='tile_'+face if len(face)==1 else 'elbow_'+face
        runtime=out/('widget_pipe_'+suffix+('_fueled' if state=='fueled' else '')+'.png');canvas.save(runtime)
        record={'id':face+'_'+state,'native':path.relative_to(root).as_posix(),'native_sha256':sha(path),'output':runtime.relative_to(root).as_posix(),'output_sha256':sha(runtime),'source_ports':{k:source[j].tolist() for j,k in enumerate(regions_for_face)},'target_ports':{k:target[j].tolist() for j,k in enumerate(regions_for_face)},'uniform_scale':scale,'translation':offset.tolist(),'source_crop':list(box),'residual_pixels_at124px_draw':(residuals*124/256).tolist(),'rest_fueled_silhouette_iou':iou,'geometry_trial':geometry_status,'method':'Uniform downsample, transparent crop/pad and translation only; no warp/rotation/repaint. Shared rest/fueled registration.'}
        records.append(record)
        if state=='rest':
            annotated=canvas.copy();ad=ImageDraw.Draw(annotated)
            for point in target:ad.ellipse((point[0]-3,point[1]-3,point[0]+3,point[1]+3),outline='#ffff00',width=1)
            sheet.paste(annotated,(index%3*256,index//3*256),annotated);draw.text((index%3*256+6,index//3*256+224),face+' residual '+str(round(float(max(residuals)*108/256),2)),fill='white')
    print(face,geometry_status,'screen residual',residuals*124/256,'IoU',iou)
(src/'pipe_registration.json').write_text(json.dumps({'records':records,'acceptance':'Technical trial only; current puzzle-grid appearance and Mobile context still required at4.5/5.'},indent=2)+'\n')
sheet.save(root/'tmp/artwork-quality-20261018/pipe_registration_review.png')
