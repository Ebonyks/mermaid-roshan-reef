from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image
p=Path('assets_src/cinematics/ltx25_8gb_wave_20261004');out=p/'scale_continuity';out.mkdir(exist_ok=True)
def cc(mask):
 visited=np.zeros_like(mask,dtype=bool);rows=[]
 for y,x in zip(*np.nonzero(mask)):
  if visited[y,x]:continue
  stack=[(int(y),int(x))];visited[y,x]=True;points=[]
  while stack:
   yy,xx=stack.pop();points.append((yy,xx))
   for ny,nx in [(yy-1,xx),(yy+1,xx),(yy,xx-1),(yy,xx+1)]:
    if 0<=ny<mask.shape[0] and 0<=nx<mask.shape[1] and mask[ny,nx] and not visited[ny,nx]:visited[ny,nx]=True;stack.append((ny,nx))
  coords=np.array(points);rows.append({'min':coords.min(0),'max':coords.max(0),'area':len(points),'center':coords.mean(0),'points':coords})
 return rows
def landmarks(path):
 a=np.array(Image.open(path).convert('RGB')).astype(np.int16);eyes=[]
 for c in cc(np.max(a[130:280,110:310],axis=2)<145):
  h,w=c['max']-c['min']+1;cy,cx=c['center']+[130,110]
  if 250<c['area']<1000 and 18<=w<=45 and 18<=h<=42 and 175<cy<235:eyes.append([float(cx),float(cy)])
 pairs=[(a,b) for a in eyes for b in eyes if 45<b[0]-a[0]<90 and abs(a[1]-b[1])<12]
 if not pairs:raise ValueError('Eyes require manual review '+str(path))
 left,right=min(pairs,key=lambda pair:abs(pair[0][1]-pair[1][1]))
 z=a[30:135,100:335];blue=(z[:,:,1]>z[:,:,0]+10)&(z[:,:,2]>z[:,:,0]+15);gem=max(cc(blue),key=lambda c:c['area']);c=gem['center']+[30,100]
 z=a[270:510,90:340];pink=(z[:,:,0]>z[:,:,1]+30)&(z[:,:,2]>z[:,:,1]+25)&(z[:,:,0]>190)&(z[:,:,2]>160)
 shirt=max((c for c in cc(pink) if c['min'][0]<80),key=lambda c:c['area']);pts=shirt['points'];tip=pts[pts[:,0]>=shirt['max'][0]-2].mean(0)+[270,90];top=pts[pts[:,0]<=shirt['min'][0]+2].mean(0)+[270,90]
 center=(np.array(left)+right)/2;x,y=np.round(center).astype(int)
 z=a[y+65:y+129,x-7:x+8]
 skin=(z[:,:,0]>175)&(z[:,:,1]>95)&(z[:,:,0]>z[:,:,1]+15)&(z[:,:,1]>z[:,:,2]+4)
 rows=np.where(skin.mean(axis=1)>.6)[0]
 if not len(rows):raise ValueError('Neckline requires manual review '+str(path))
 neck=[float(center[0]),float(y+65+rows.max())]
 return {'crown_gem':[float(c[1]),float(c[0])],'image_left_eye':left,'image_right_eye':right,'neck_base':neck,'bodice_waist_tip':[float(tip[1]),float(tip[0])]},int(shirt['max'][0]-shirt['min'][0]+1)
def digest(f):
 with Path(f).open('rb') as h:return hashlib.file_digest(h,'sha256').hexdigest()
def main():
 keys=[0,3,7,17,22,27,36,40];guide=[]
 for i in keys:
  f=p/f'inputs/guide_{i:04d}.png';a,h=landmarks(f);guide.append({'index':i,'source':str(f),'source_sha256':digest(f),'landmarks':a,'bodice_color_component_height':h})
 rows={x['index']:x for x in guide};names=list(guide[0]['landmarks'])
 for row in guide:
  target=row['landmarks'] if row['index']!=22 else {name:((np.array(rows[17]['landmarks'][name])+rows[27]['landmarks'][name])/2).tolist() for name in names}
  X=np.array([row['landmarks'][n] for n in names]);Y=np.array([target[n] for n in names]);xc=X-X.mean(0);yc=Y-Y.mean(0);scale=float(np.sum(xc*yc)/np.sum(xc*xc));translation=Y.mean(0)-scale*X.mean(0);aligned=X*scale+translation;errors=np.linalg.norm(aligned-Y,axis=1)
  pairratios={}
  for u,v in [('image_left_eye','image_right_eye'),('crown_gem','image_left_eye'),('crown_gem','image_right_eye'),('crown_gem','bodice_waist_tip'),('neck_base','bodice_waist_tip')]:
   pairratios[u+'__'+v]=float(scale*np.linalg.norm(X[names.index(u)]-X[names.index(v)])/np.linalg.norm(Y[names.index(u)]-Y[names.index(v)]))
  row.update(target_landmarks=target,target_reason='Neighbor-coordinate midpoint at timeline 22; no image pixel interpolation' if row['index']==22 else 'Existing common-scale atlas-derived pose geometry; pose-specific motion retained',uniform_scale=scale,translation=translation.tolist(),max_anchor_residual_px=float(errors.max()),rms_anchor_residual_px=float(np.sqrt(np.mean(errors**2))),pair_scale_ratios=pairratios,preliminary_registration_pass=bool(errors.max()<=6 and all(abs(v-1)<=.03 for v in pairratios.values())))
  print('KEY',row['index'],'scale',round(scale,4),'translation',np.round(translation,2).tolist(),'max_residual',round(float(errors.max()),2),'ratios', {k:round(v,4) for k,v in pairratios.items()},'pass',row['preliminary_registration_pass'],flush=True)
 report={'status':'MEASURED_SOURCE_ONLY','landmark_definitions':'Color-component centers for dark eye/eyelash regions and crown gem, lower skin boundary at center of neckline, bottom center of connected pink bodice; native measurements require human anchor review. These are diagnostic coordinates, not proof of anatomy. The preliminary sleeve/color-edge proxy was replaced because it moved with the gesture.','canvas':[576,832],'tolerance':{'max_anchor_residual_px':6,'pair_scale_ratio_deviation':.03},'guides':guide,'output_frames':[],'no_image_pixels_modified_by_python':True}
 for take,count in [('base_two_pass',41),('temporal_retake',41),('anti_blur_nag',41),('temporal_48fps',81)]:
  frames=[]
  for i in range(count):
   f=p/f'results/{take}/refined_frames/{i:04d}.png'
   try:a,h=landmarks(f);frames.append({'index':i,'sha256':digest(f),'landmarks':a,'bodice_color_component_height':h})
   except ValueError as e:frames.append({'index':i,'sha256':digest(f),'status':'MANUAL_ANCHORS_REQUIRED','reason':str(e)})
  report['output_frames'].append({'take':take,'frames':frames})
 (out/'native_landmarks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

if __name__=="__main__":main()
