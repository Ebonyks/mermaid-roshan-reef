"""Coordinate-only registration; Python never edits image pixels."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1]
ROOT=P.parents[2]
OLD=ROOT/'assets_src/cinematics/ltx25_8gb_wave_20261004'
sys.path.insert(0,str(OLD/'scripts'))
from measure_scale_landmarks import cc,landmarks

def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def measure(path,eye_roi=None):
    if eye_roi is None:return landmarks(path)[0]
    a=np.array(Image.open(path).convert('RGB')).astype(np.int16)
    x0,y0,x1,y1=eye_roi
    c=max(cc(np.max(a[y0:y1,x0:x1],axis=2)<145),key=lambda c:c['area'])
    assert 250<c['area']<1200,'Manual eye ROI lost correspondence'
    left=(c['center']+[y0,x0])[::-1].tolist();eyes=[]
    for c in cc(np.max(a[130:280,110:360],axis=2)<145):
        h,w=c['max']-c['min']+1;cy,cx=c['center']+[130,110]
        if 250<c['area']<1000 and 18<=w<=45 and 18<=h<=42 and 175<cy<235:
            if 45<cx-left[0]<90 and abs(cy-left[1])<12:eyes.append([float(cx),float(cy)])
    assert len(eyes)==1,'Ambiguous right eye'
    right=eyes[0];z=a[30:135,100:335]
    blue=(z[:,:,1]>z[:,:,0]+10)&(z[:,:,2]>z[:,:,0]+15)
    gem=max(cc(blue),key=lambda c:c['area'])['center']+[30,100]
    z=a[270:510,90:340]
    pink=(z[:,:,0]>z[:,:,1]+30)&(z[:,:,2]>z[:,:,1]+25)&(z[:,:,0]>190)&(z[:,:,2]>160)
    shirt=max((c for c in cc(pink) if c['min'][0]<80),key=lambda c:c['area'])
    tip=shirt['points'][shirt['points'][:,0]>=shirt['max'][0]-2].mean(0)+[270,90]
    center=(np.array(left)+right)/2;x,y=np.round(center).astype(int)
    z=a[y+65:y+129,x-7:x+8]
    skin=(z[:,:,0]>175)&(z[:,:,1]>95)&(z[:,:,0]>z[:,:,1]+15)&(z[:,:,1]>z[:,:,2]+4)
    rows=np.where(skin.mean(axis=1)>.6)[0];assert len(rows),'Missing neck'
    return {'crown_gem':gem[::-1].tolist(),'image_left_eye':left,'image_right_eye':right,
            'neck_base':[float(center[0]),float(y+65+rows.max())],'bodice_waist_tip':tip[::-1].tolist()}

def fit(src,tgt):
    names=list(tgt);x=np.array([src[n] for n in names]);y=np.array([tgt[n] for n in names])
    r=names.index('bodice_waist_tip');xc=x-x[r];yc=y-y[r]
    scale=float(np.sum(xc*yc)/np.sum(xc*xc));t=y[r]-scale*x[r]
    err=np.linalg.norm(scale*x+t-y,axis=1);pairs={}
    for u,v in [('image_left_eye','image_right_eye'),('crown_gem','image_left_eye'),('crown_gem','image_right_eye'),('crown_gem','bodice_waist_tip'),('neck_base','bodice_waist_tip')]:
        i,j=names.index(u),names.index(v);pairs[u+'__'+v]=float(scale*np.linalg.norm(x[i]-x[j])/np.linalg.norm(y[i]-y[j]))
    return {'uniform_scale':scale,'translation':t.tolist(),'anchor_residuals_px':dict(zip(names,err.tolist())),
            'max_anchor_residual_px':float(err.max()),'pair_scale_ratios':pairs,
            'anatomy_geometry_pass':bool(err.max()<=6 and all(abs(v-1)<=.03 for v in pairs.values()))}

def main():
    old=json.loads((OLD/'scale_continuity/decoded_registration_plan.json').read_text());rows=[]
    for original in old['frames']:
        i=original['index'];src=OLD/original['source'];assert digest(src)==original['source_sha256']
        roi=[154,193,189,232] if i==29 else None;observed=measure(src,roi)
        target={n:(np.array(xy)+[24,0]).tolist() for n,xy in original['target_landmarks'].items()}
        geometry=fit(observed,target)
        a=np.array(Image.open(src).convert('RGB')).astype(np.int16)
        yy,xx=np.where(np.max(np.abs(a-238),axis=2)>24)
        bounds=[int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]
        mapped=np.array(bounds).reshape(2,2)*geometry['uniform_scale']+np.array(geometry['translation'])
        safe=bool(np.all(mapped[0]>=0) and np.all(mapped[1]<=[575,831]));assert safe,('Clipping',i,mapped.tolist())
        rows.append({'index':i,'source':src.relative_to(ROOT).as_posix(),'source_sha256':digest(src),
                     'source_landmarks':observed,'target_landmarks':target,'manual_eye_roi_xyxy':roi,
                     'source_foreground_bounds':bounds,'mapped_foreground_bounds':mapped.tolist(),
                     'source_already_clipped':bool(bounds[0]==0),'no_new_clipping':safe,'apply_registration':True,**geometry})
    report={'status':'REGISTRATION_PLAN_NOT_ACCEPTANCE','canvas':[576,832],'fps':24,'layout_offset':[24,0],'fixed_root':[208.5,453.0],
            'layout_reason':'Constant 24px stage offset protects visible boundary pixels; does not reconstruct the hand already clipped in native frame29.',
            'sampling':'One same-frame bilinear uniform affine in Aseprite Lua; floating scale/translation; no temporal blending.',
            'source_packet_revision':'c51075fff13cfd8f4795b5ef7da232fc7462e7f4',
            'manual_anchor_review':{'index':29,'source_sha256':rows[29]['source_sha256'],'left_eye_roi_xyxy':[154,193,189,232],'dark_threshold':145,
                'reason':'Native visual inspection confirms eye region; eyelash touches hair in the broad detector. ROI isolates the corresponding left eye.',
                'review_scope':'Measurement correspondence only, no identity/art acceptance.'},
            'limits':{'root_error_px':1,'global_scale_residual':.003,'anatomy_max_anchor_residual_px':6,'pair_ratio_deviation':.03},
            'new_model_takes':0,'new_imagegen_calls':0,'frames':rows}
    (P/'registration_plan.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('PLAN',len(rows),'frames; anatomy failures',[r['index'] for r in rows if not r['anatomy_geometry_pass']],flush=True)

if __name__=='__main__':main()
