"""Read-only native scale/quiet-face diagnostics; no raster editing or artwork acceptance."""
from pathlib import Path
import json,sys,math
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parents[1];ROOT=P.parents[2]
sys.path.insert(0,str(ROOT/'assets_src/cinematics/ltx25_8gb_wave_20261004/scripts'))
from measure_scale_landmarks import cc
def measure(f):
 with Image.open(f) as im:a=np.asarray(im.convert('RGB'),dtype=np.int16)
 # Read-only coordinate view removes the declared32px canvas padding for the old detector.
 a=a[32:864,32:608];eyes=[]
 for c in cc(np.max(a[130:280,110:310],axis=2)<145):
  h,w=c['max']-c['min']+1;cy,cx=c['center']+[130,110]
  if 250<c['area']<1000 and 18<=w<=45 and 18<=h<=42 and 175<cy<235:eyes.append([float(cx),float(cy)])
 pairs=[(x,y) for x in eyes for y in eyes if 45<y[0]-x[0]<90 and abs(x[1]-y[1])<12]
 if not pairs:raise ValueError('Manual eye correspondence required')
 left,right=min(pairs,key=lambda x:abs(x[0][1]-x[1][1]))
 z=a[30:135,100:335];blue=(z[:,:,1]>z[:,:,0]+10)&(z[:,:,2]>z[:,:,0]+15)
 gem=max(cc(blue),key=lambda c:c['area'])['center']+[30,100]
 z=a[270:510,90:340];pink=(z[:,:,0]>z[:,:,1]+30)&(z[:,:,2]>z[:,:,1]+25)&(z[:,:,0]>190)&(z[:,:,2]>160)
 shirt=max((c for c in cc(pink) if c['min'][0]<80),key=lambda c:c['area']);pts=shirt['points']
 tip=pts[pts[:,0]>=shirt['max'][0]-2].mean(0)+[270,90]
 center=(np.array(left)+right)/2;x,y=np.round(center).astype(int);z=a[y+65:y+129,x-7:x+8]
 skin=(z[:,:,0]>175)&(z[:,:,1]>95)&(z[:,:,0]>z[:,:,1]+15)&(z[:,:,1]>z[:,:,2]+4);indices=np.where(skin.mean(axis=1)>.6)[0]
 if not len(indices):raise ValueError('Manual neck correspondence required')
 points={'left_eye':np.array(left)+32,'right_eye':np.array(right)+32,'gem':gem[::-1]+32,'waist':tip[::-1]+32,'neck':np.array([center[0],y+65+indices.max()])+32}
 d={k:v.tolist() for k,v in points.items()}
 d['eye_distance']=float(np.linalg.norm(points['left_eye']-points['right_eye']))
 d['gem_waist_distance']=float(np.linalg.norm(points['gem']-points['waist']))
 d['neck_waist_distance']=float(np.linalg.norm(points['neck']-points['waist']))
 return d
def focus(f):
 with Image.open(f) as im:a=np.asarray(im.convert('RGB'),dtype=np.float32)
 # Same fixed native face rectangle used in the prior diagnostics, translated by32px.
 g=a[197:282,177:317]@np.array([.2126,.7152,.0722],dtype=np.float32)
 lap=4*g[1:-1,1:-1]-g[:-2,1:-1]-g[2:,1:-1]-g[1:-1,:-2]-g[1:-1,2:]
 dx=g[1:-1,2:]-g[1:-1,:-2];dy=g[2:,1:-1]-g[:-2,1:-1]
 bg=a[20:60,590:620]@np.array([.2126,.7152,.0722],dtype=np.float32)
 bl=4*bg[1:-1,1:-1]-bg[:-2,1:-1]-bg[2:,1:-1]-bg[1:-1,:-2]-bg[1:-1,2:]
 return {'face_laplacian_variance':float(lap.var()),'face_gradient_energy':float(np.mean(dx*dx+dy*dy)),'empty_background_laplacian_variance':float(bl.var())}
def main():
 lanes=[]
 for folder in sorted(P.glob('take_*')):
  if not (folder/'refined_frames/0040.png').is_file():continue
  rows=[]
  for i in range(41):
   f=folder/f'refined_frames/{i:04d}.png';row={'index':i,'focus':focus(f)}
   try:row['geometry']=measure(f)
   except ValueError as e:row['geometry_status']='MANUAL_CORRESPONDENCE_REQUIRED';row['reason']=str(e)
   rows.append(row)
  valid=[x for x in rows if 'geometry' in x];summ={}
  for name in ['eye_distance','gem_waist_distance','neck_waist_distance']:
   vals=[x['geometry'][name] for x in valid];base=valid[0]['geometry'][name]
   summ[name]={'min':min(vals),'max':max(vals),'peak_to_peak_relative_first':(max(vals)-min(vals))/base}
  roots=[x['geometry']['waist'] for x in valid];summ['root_max_distance_from_first_px']=max(math.dist(x,roots[0]) for x in roots)
  summ['root_max_distance_from_declared_guide_px']=max(math.dist(x,[216.5,485]) for x in roots)
  vals=[x['focus']['face_laplacian_variance'] for x in rows]
  summ.update(face_laplacian_min=min(vals),face_laplacian_max=max(vals),face_laplacian_max_min_ratio=max(vals)/min(vals),first_face_laplacian=vals[0],last_face_laplacian=vals[-1],empty_background_laplacian_median=float(np.median([x['focus']['empty_background_laplacian_variance'] for x in rows])))
  lane={'take':folder.name,'automatic_geometry_frames':len(valid),'manual_correspondence_frames':[x['index'] for x in rows if 'geometry' not in x],'summary':summ,'frames':rows};lanes.append(lane)
  print('DIAGNOSTIC',folder.name,json.dumps(summ),flush=True)
 (P/'native_diagnostics.json').write_text(json.dumps({'status':'DIAGNOSTIC_ONLY_NOT_ACCEPTANCE','lanes':lanes,'limits':'Painted edge/color changes, pose and detector correspondence confound metrics. Root/proportion comparisons are native, unregistered output; no guide-plan PASS inferred. Quiet-face edge energy can reward noise. Python reads numeric ROIs only; no visual crops/resize/images saved.'},indent=2)+'\n')
if __name__=='__main__':main()
