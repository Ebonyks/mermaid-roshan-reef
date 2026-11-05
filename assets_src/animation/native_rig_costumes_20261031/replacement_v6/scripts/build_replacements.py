"""Prepare actual wardrobe cutouts and an anatomy-only native skin base.
Uniform source registration, semantic extraction and matte decontamination only.
Original clothes are physically absent from anatomy.png. No garment RGB warp.
"""
from pathlib import Path
import json,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,gaussian_filter1d,map_coordinates
R=Path(__file__).resolve().parents[1];P=R.parent;O=P.parent/'native_rig_stress_20261031'
spec=importlib.util.spec_from_file_location('old',O/'scripts/build_study.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def save(p,d):p.write_text(json.dumps(d,separators=(',',':'))+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 # Restore the genuinely missing bare shoulder from the original authored
 # shoulder repair; the old arm extraction had retained a sleeve-edge matte.
 arm,_=old.clean_source(O/'native/shoulder_arm.png');factor=194/520
 cap=Image.new('RGBA',Image.open(O/'native/neutral.png').size)
 cap.alpha_composite(arm.resize((round(arm.width*factor),round(arm.height*factor)),Image.Resampling.LANCZOS),(round(589-735*factor),round(436-390*factor)))
 cap=old.canvas_image(cap);upper=np.array(Image.open(O/'art/upper_arm.png').convert('RGBA'));yy,xx=np.mgrid[:1024,:1024];u=upper.astype(float)
 old_fabric=(u[:,:,2]>u[:,:,0]*.95)&(u[:,:,2]>u[:,:,1]*1.08)&(yy<410)&(upper[:,:,3]>0);upper[old_fabric]=0
 contact=cap.copy();contact.alpha_composite(Image.fromarray(upper));combined=np.array(contact);window=(xx-474.74)**2+(yy-379.76)**2<=25**2;upper[window]=combined[window];Image.fromarray(upper).save(R/'art/upper_clean.png')
 a=np.array(Image.open(O/'art/body.png').convert('RGBA'));ownership=np.array(Image.open(R/'native/original_clothing_domains.png').convert('RGBA'));top=ownership[:,:,0]>128;tail=ownership[:,:,1]>128;cloth=top|tail
 anatomy=a.copy();anatomy[cloth]=0;Image.fromarray(anatomy).save(R/'art/anatomy.png')
 for slot,m in [('body',top),('tail',tail)]:
  part=a.copy();part[~m]=0;Image.fromarray(part).save(R/'art'/f'original_{slot}.png')
 ownership[:,:,3]=((a[:,:,3]>0)&~cloth)*255
 Image.fromarray(ownership).save(R/'art/ownership.png')
 regions=json.loads((R/'native/source_clothing_regions.json').read_text(encoding='utf-8'));details={};union=Image.fromarray(a)
 for theme in ['ballet','magician']:
  src,cleanup=old.clean_source(P/'native'/f'{theme}_fit.png');sa=np.array(src);points=regions[theme]['source_clothing_polygon']
  # Extend only the newly exposed neckline window up under original neck/hair;
  # the shader restores original anatomy in front of clothing at all contacts.
  if theme=='ballet':points=points[:1]+[(559,400),(585,375),(648,370),(711,375),(754,400)]+points[6:]
  else:points=points[:1]+[(610,383),(673,375),(729,383)]+points[4:]
  mask=Image.new('L',src.size);ImageDraw.Draw(mask).polygon(points,fill=255);inside=np.array(mask)>0
  valid=inside&(sa[:,:,3]>240);near=distance_transform_edt(~valid,return_distances=False,return_indices=True)
  # Preserve actual source alpha. Only RGB hidden beneath soft alpha is cleaned.
  edge=sa[:,:,3]<=240;sa[edge,:3]=sa[near[0],near[1],:3][edge];sa[~inside]=0
  split=640 if theme=='ballet' else 680
  offset=(126,66) if theme=='ballet' else (112,78);parts={}
  image=Image.fromarray(sa).resize((round(src.width*.66),round(src.height*.66)),Image.Resampling.LANCZOS)
  canvas=Image.new('RGBA',(1024,1024));canvas.alpha_composite(image,offset);raw=np.array(canvas)
  # Register the complete painted cutout to the established torso/tail centre
  # using smooth row translations. Preserve cross-section widths and use one
  # field for both slots; never stretch RGB onto the old garment silhouette.
  rows=[];values=[]
  for yy in range(1024):
   target=np.flatnonzero(cloth[yy]&(a[yy,:,3]>96));source=np.flatnonzero(raw[yy,:,3]>96)
   if len(target) and len(source):rows.append(yy);values.append((target[0]+target[-1]-source[0]-source[-1])/2)
  dx=gaussian_filter1d(np.interp(np.arange(1024),rows,values),sigma=10)
  t=np.clip((np.arange(1024)-700)/75,0,1);t=t*t*(3-2*t);dx-=28*t
  gy,gx=np.mgrid[:1024,:1024];pm=raw.astype(float);pm[:,:,:3]*=pm[:,:,3:4]/255
  shifted=np.stack([map_coordinates(pm[:,:,k],[gy,gx-dx[:,None]],order=1,mode='constant',cval=0) for k in range(4)],axis=-1)
  shifted[:,:,:3]=np.divide(shifted[:,:,:3]*255,shifted[:,:,3:4],out=np.zeros_like(shifted[:,:,:3]),where=shifted[:,:,3:4]>0)
  raw=np.uint8(np.clip(shifted,0,255));valid=raw[:,:,3]>240;nearest=distance_transform_edt(~valid,return_distances=False,return_indices=True);raw[:,:,:3]=raw[nearest[0],nearest[1],:3]
  cutoff=round(split*.66+offset[1]);yy=np.arange(1024)[:,None]
  for slot,selection in [('body',yy<=cutoff+1),('tail',yy>=cutoff-1)]:
   q=raw.copy();q[:,:,3]*=selection;canvas=Image.fromarray(q);canvas.save(R/'art'/f'{theme}_{slot}.png');parts[slot]=canvas;union.alpha_composite(canvas)
  # Full static preview is the actual skin recipe: clean anatomy, selected tail
  # and body, then exact original exposed anatomy in front and crown replacement.
  b=Image.fromarray(anatomy);b.alpha_composite(parts['tail']);b.alpha_composite(parts['body']);bb=np.array(b);protect=ownership[:,:,3]>128;bb[protect]=a[protect]
  crown=ownership[:,:,2]>128;scalp=np.array(Image.open(R/'art'/f'{theme}_scalp.png'));bb[crown]=scalp[crown];composed=Image.fromarray(bb);composed.save(R/'art'/f'{theme}_composed.png')
  preview=Image.open(O/'art/forearm.png').convert('RGBA');preview.alpha_composite(Image.open(R/'art/upper_clean.png').convert('RGBA'));preview.alpha_composite(composed);preview.alpha_composite(Image.open(R/'art'/f'{theme}_head.png').convert('RGBA'));preview.save(R/'review'/f'{theme}_neutral.png')
  details[theme]={'source':str(P/'native'/f'{theme}_fit.png').replace('\\','/'),'source_sha256':sha(P/'native'/f'{theme}_fit.png'),'uniform_scale':.66,'offset':offset,'native_garment_polygon':points,'body_tail_split_y':split,'source_alpha_preserved':True,'registration':'Whole RGBA cutout smooth lateral row translation, sigma10; common body/tail field, unchanged row widths. Premultiplied sampling, no RGB-only projection or edge extrusion.','fin_contact_registration':{'target_socket':[434.48,793.58],'extra_lateral_px':-28,'ramp_y':[700,775],'method':'Smooth whole-cutout row translation to meet the unchanged original fin socket; row widths/paint preserved.'},'lateral_dx_per_row':dx.tolist(),'RGB_only_warp':False,'matte_cleanup':cleanup}
 rig=json.loads((P/'godot/rig.json').read_text(encoding='utf-8'))
 original=rig['meshes'][0];newmesh=old.make_mesh(union,old.bone_specs());index={tuple(v):i for i,v in enumerate(original['vertices'])};common=0
 for j,p in enumerate(newmesh['vertices']):
  if tuple(p) in index:
   common+=1;i=index[tuple(p)]
   for name in newmesh['weights']:newmesh['weights'][name][j]=original['weights'][name][i]
 rig['meshes'][0]=dict(newmesh,name='Body',texture='../../../native_rig_stress_20261031/art/body.png',z=0)
 for m in rig['meshes'][1:]:m['texture']=('../art/ballet_head.png' if m['name']=='Headwear' else '../../../native_rig_stress_20261031/art/'+Path(m['texture']).name)
 save(R/'godot/rig.json',rig)
 for theme in ['ballet','magician']:
  v=json.loads(json.dumps(rig));v['meshes'][0]['texture']=f'../art/{theme}_composed.png';v['meshes'][1]['texture']='../art/upper_clean.png';v['meshes'][-1]['texture']=f'../art/{theme}_head.png';save(R/'godot'/f'rig_{theme}.json',v)
 save(R/'fitting.json',{'method':'Actual complete painted garment cutouts with authentic silhouettes; uniform scale plus declared smooth whole-cutout lateral registration. Original clothing removed from anatomy base; selected pieces skinned on native Polygon2D, anatomy restored at contacts. No RGB warp or immutable clothing-alpha requirement.','original_clothing_pixels_removed':int(((a[:,:,3]>0)&cloth).sum()),'original_body_mesh_vertices':len(original['vertices']),'expanded_body_mesh_vertices':len(newmesh['vertices']),'original_vertices_preserved':common,'original_weights_exact_at_common_vertices':True,'fitting':details,'shoulder_contact_repair':{'source':'../native_rig_stress_20261031/native/shoulder_arm.png','source_sha256':sha(O/'native/shoulder_arm.png'),'window_center':[474.74,379.76],'radius_px':25,'whole_arm_scale_change':False,'original_fabric_removed':int(old_fabric.sum())},'generation_calls_aggregate':3})
 print('ACTUAL_GARMENT_SKINS_BUILT')
if __name__=='__main__':main()
