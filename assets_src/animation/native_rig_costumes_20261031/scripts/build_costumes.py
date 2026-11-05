"""Register clothing paint onto the unchanged study silhouette and bind replaceable slots."""
from pathlib import Path
import json, hashlib, importlib.util
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates, distance_transform_edt
ROOT=Path(__file__).resolve().parents[1]; OLD=ROOT.parent/'native_rig_stress_20261031'; REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('original_builder',OLD/'scripts/build_study.py'); old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def save(p,v):p.write_text(json.dumps(v,separators=(',',':'))+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 base=Image.open(OLD/'art/body.png').convert('RGBA');a=np.array(base); y,x=np.mgrid[:1024,:1024]
 # Face/hair/skin and limbs are never accepted from a fitting generation.
 cloth=(a[:,:,2]>a[:,:,0]*.84)&(a[:,:,2]>a[:,:,1]*1.08)&(y>=327)&(y<505)&(x>430)&(x<641)
 skin=(a[:,:,0].astype(float)>a[:,:,2]+23.)&(a[:,:,1].astype(float)>a[:,:,2]+6.)
 rig=json.loads((OLD/'godot/rig.json').read_text(encoding='utf-8'))
 for m in rig['meshes']:m['texture']='../../native_rig_stress_20261031/art/'+Path(m['texture']).name
 registry={'schema':1,'rig_id':'roshan_front_native_v1','slots':['head','body','tail'],'themes':['original','ballet','magician'],'stable_catalog_ids':{},'replacement':'Replace native Canvas shader uniforms and head texture atomically; sample immutable base plus body/tail RGB masks. Seven fixed resident textures, no Cartesian cache or skeleton/timeline recreation.','fitting':{},'source_hashes':{}}
 heads=[]
 for theme in ['ballet','magician']:
  src=Image.open(ROOT/'native'/f'{theme}_fit.png').convert('RGBA');sa=np.array(src)
  body_poly=([[550,450],[575,444],[706,444],[735,450],[717,561],[741,608],[640,639],[558,606],[573,561]] if theme=='ballet' else [[589,452],[610,448],[730,448],[755,454],[736,553],[785,618],[668,658],[570,617],[601,553]])
  tail_poly=([[558,592],[738,592],[790,700],[827,850],[810,990],[760,1085],[660,1145],[530,1145],[450,1100],[480,1065],[550,1070],[604,1030],[625,950],[610,850],[570,750],[550,650]] if theme=='ballet' else [[580,630],[780,630],[818,735],[828,870],[805,1000],[750,1085],[655,1120],[535,1120],[477,1090],[486,1058],[555,1065],[610,1030],[641,960],[630,850],[595,760]])
  pm=Image.new('L',src.size);dd=ImageDraw.Draw(pm);dd.polygon(body_poly,fill=255);dd.polygon(tail_poly,fill=255)
  valid=(np.array(pm)>0)&(sa[:,:,3]>240)
  near=distance_transform_edt(~valid,return_distances=False,return_indices=True);fabric=sa[near[0],near[1]]
  offset=np.array([126,66] if theme=='ballet' else [112,78]);mapped=(np.stack([x,y],axis=-1)-offset)/.66
  paint=np.stack([map_coordinates(fabric[:,:,k].astype(float),[mapped[:,:,1],mapped[:,:,0]],order=1,mode='nearest') for k in range(3)],axis=-1).astype('uint8');body_paint=paint;tail_paint=paint
  body_mask=(cloth & ~((y<390)&((x<491)|(x>615)))).astype(float)*np.clip((505-y)/25,0,1)
  leftlimit=np.interp(y,[0,735,770,790,805,850],[475,475,470,448,435,460])
  tail_mask=((y>=465)&(x<670)&~skin).astype(float)*np.clip((x-leftlimit)/8,0,1)
  # Clothing is an overlay over the approved undergarment, never stretched edge pixels.
  distance=distance_transform_edt(~valid)
  coverage=np.clip((8-map_coordinates(distance,[mapped[:,:,1],mapped[:,:,0]],order=1,mode='nearest'))/8,0,1)
  body_mask*=coverage;tail_mask*=coverage
  # Store replacement RGB plus explicit mask. Runtime preserves original alpha exactly.
  for slot,selection in [('body',body_mask),('tail',tail_mask)]:
   im=np.dstack([body_paint if slot=='body' else tail_paint,np.uint8(selection*255)]);Image.fromarray(im).save(ROOT/'art'/f'{theme}_{slot}.png')
  # Headwear reuses the actual wardrobe bitmap directly, no new face/head pixels.
  hp=REPO/f'assets_src/fashion_designer/beta_20261025/native/{theme}_head.png';h,head_cleanup=old.clean_source(hp);h=h.crop(h.getbbox())
  width=215 if theme=='magician' else 210;h=h.resize((width,round(h.height*width/h.width)),Image.Resampling.LANCZOS)
  head=Image.new('RGBA',(1024,1024));head.alpha_composite(h,(445,48 if theme=='magician' else 52));head.save(ROOT/'art'/f'{theme}_head.png');heads.append(head)
  registry['stable_catalog_ids'][theme]={s:f'{s}_{theme}_v1' for s in ['head','body','tail']}
  registry['fitting'][theme]={'uniform_scale':.66,'offset':offset.tolist(),'garment_source_polygons':[body_poly,tail_poly],'offline_mapping':'Uniform .66 fitting-plate garment registration only, explicit per-theme offsets; nearest fabric RGB extension limited to an eight-source-pixel feather; approved undergarment and iridescent tail remain visible beyond the fitted garment. Original identity alpha and non-clothing pixels retained. Shared waist overlap and feathered fin boundary. No face/skin/hair/arm/fin replacements. Original body alpha retained; original violet shoulder ruffles stay as undergarment.','headwear_matte_cleanup':head_cleanup,'headwear':'Uniformly scaled original wardrobe source. Original tiara remains underneath as identity ornament.','body_texture_sha256':sha(ROOT/'art'/f'{theme}_body.png'),'tail_texture_sha256':sha(ROOT/'art'/f'{theme}_tail.png')}
  for s in ['head','body','tail']:
   f=REPO/f'assets_src/fashion_designer/beta_20261025/native/{theme}_{s}.png';registry['source_hashes'][str(f.relative_to(REPO)).replace('\\','/')]=sha(f)
 union=heads[0].copy();union.alpha_composite(heads[1]);mesh=old.make_mesh(union,old.bone_specs(),rigid='Head');rig['meshes'].append(dict(mesh,name='Headwear',texture='../art/ballet_head.png',z=1))
 save(ROOT/'godot/rig.json',rig);save(ROOT/'godot/costumes.json',registry)
 # Audit-visible material variants have exactly the same mesh and weights.
 for theme in ['ballet','magician']:
  variant=json.loads(json.dumps(rig)); b=np.array(base).copy()
  for s in ['tail','body']:
   layer=np.array(Image.open(ROOT/'art'/f'{theme}_{s}.png'));mix=layer[:,:,3:4]/255.;b[:,:,:3]=np.uint8(b[:,:,:3]*(1-mix)+layer[:,:,:3]*mix)
  Image.fromarray(b).save(ROOT/'art'/f'{theme}_composed.png')
  variant['meshes'][0]['texture']=f'../art/{theme}_composed.png';variant['meshes'][-1]['texture']=f'../art/{theme}_head.png';save(ROOT/'godot'/f'rig_{theme}.json',variant)
  preview=Image.open(OLD/'art/forearm.png').convert('RGBA');preview.alpha_composite(Image.open(OLD/'art/upper_arm.png').convert('RGBA'));preview.alpha_composite(Image.fromarray(b));preview.alpha_composite(Image.open(ROOT/'art'/f'{theme}_head.png'));preview.save(ROOT/'review'/f'{theme}_neutral.png')
 print('COSTUME_PREPARATION_OK')
if __name__=='__main__':main()
