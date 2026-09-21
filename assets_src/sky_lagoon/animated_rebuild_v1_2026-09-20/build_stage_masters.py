from pathlib import Path
from PIL import Image
import numpy as np,json,zipfile,io,hashlib,sys
from xml.etree.ElementTree import Element,SubElement,tostring
from stage_component_layers import separate
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'stage_masters';P.mkdir(exist_ok=True)
E=Path(sys.argv[1]);data=json.loads((E/'scene-layers.json').read_text());layers=sorted(data['layers'],key=lambda r:(r['z'],r['order']))
# Export cells remain reproducible from Godot; masters bind original paths/hashes.
manifest={'canvas':[6144,2048],'source_layers':layers,'stage_masters':[],'component_sources':{},'scope':'native-resolution day/rest environment working masters; actors, HUD, interaction cues and shader output excluded','limits':'painted panorama preserved with source-owned concealed bough fill; remaining painted-in scenery is not individually separated; animation timelines remain in asset-family Aseprite files'}
for stage,name in enumerate(['arrival','meadow','castle']):
 left=stage*2048;out=[];base=Image.new('RGBA',(2048,2048));merged=Image.new('RGBA',(2048,2048))
 for row in layers:
  if not row['visible']:continue
  image=Image.open(E/row['cell']).convert('RGBA');a,b,c,d,e,f=row['transform'];c-=left
  determinant=a*e-b*d
  if abs(determinant)<1e-9:continue
  bounds=[(a*x+b*y+c,d*x+e*y+f) for x,y in [(0,0),(image.width,0),(0,image.height),(image.width,image.height)]]
  if max(p[0] for p in bounds)<=0 or min(p[0] for p in bounds)>=2048 or max(p[1] for p in bounds)<=0 or min(p[1] for p in bounds)>=2048:continue
  tint=np.array(row['tint']);pixels=np.array(image,dtype=float);pixels=np.clip(pixels*tint,0,255).astype('uint8');image=Image.fromarray(pixels)
  inverse=(e/determinant,-b/determinant,(b*f-e*c)/determinant,-d/determinant,a/determinant,(d*c-a*f)/determinant)
  canvas=image.transform((2048,2048),Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC)
  box=canvas.getbbox()
  if not box:continue
  if row['name'].startswith('SkyLagoonBackdrop_'):base=Image.alpha_composite(base,canvas)
  else:out.extend(separate(canvas,row['source'],inverse,image.size,row['name'],manifest['component_sources']))
 assert base.getextrema()[3]==(255,255),'native base does not cover whole stage'
 out.insert(0,(('Original background with concealed bough fill' if stage==0 else 'Original painted background preserved'),base,(0,0),'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'))
 tree=Element('image',w='2048',h='2048',name='Sky Lagoon '+name,version='0.0.3');stack=SubElement(tree,'stack');payload=[]
 for label,image,position,source in out:
  layer=Image.new('RGBA',(2048,2048));layer.alpha_composite(image,position);merged=Image.alpha_composite(merged,layer)
 with zipfile.ZipFile(P/f'{name}-editable.ora','w',compression=zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for n in reversed(range(len(out))):
   label,image,position,source=out[n];buf=io.BytesIO();image.save(buf,format='PNG');blob=buf.getvalue();path=f'data/layer{n:02}.png';z.writestr(path,blob);SubElement(stack,'layer',name=label,src=path,x=str(position[0]),y=str(position[1]),opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'});payload.append({'name':label,'path':path,'source':source,'position':list(position),'size':list(image.size),'sha256':hashlib.sha256(blob).hexdigest()})
  z.writestr('stack.xml',tostring(tree,encoding='utf-8'));buf=io.BytesIO();merged.save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue());buf=io.BytesIO();merged.resize((256,256)).save(buf,format='PNG');z.writestr('Thumbnails/thumbnail.png',buf.getvalue())
 merged.convert('RGB').resize((1024,1024)).save(P/f'{name}-review.jpg',quality=95)
 manifest['stage_masters'].append({'stage':name,'master_rect':[left,0,2048,2048],'path':f'{name}-editable.ora','layers':list(reversed(payload)),'layer_count':len(out),'sha256':hashlib.sha256((P/f'{name}-editable.ora').read_bytes()).hexdigest(),'merged_rgba_sha256':hashlib.sha256(merged.tobytes()).hexdigest()})
 print(name,'layers',len(out),'bytes',(P/f'{name}-editable.ora').stat().st_size)
(P/'STAGE_MASTERS.json').write_text(json.dumps(manifest,indent=2)+'\n')
