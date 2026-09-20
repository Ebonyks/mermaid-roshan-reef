from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
from scipy import ndimage as nd
import numpy as np,json,hashlib,zipfile
from xml.etree.ElementTree import Element,SubElement,tostring
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'water';source=W/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png';im=Image.open(source).convert('RGB');mask=Image.open(P/'surface-mask-native.png').convert('L')
reports=[]
for name,box,size in [('arrival',(0,1180,640,1580),(256,256)),('castle',(4520,1000,6144,1640),(512,256))]:
 rgb=im.crop(box);a=np.array(rgb,dtype=float);water=np.array(mask.crop(box))>200;solid=nd.binary_fill_holes(nd.binary_closing(water,iterations=3));dist=nd.distance_transform_edt(solid)
 # Avoid artificial waves at the image/crop boundaries; authored shore only.
 valid=water.copy();valid[:6]=False;valid[-6:]=False;valid[:,:6]=False;valid[:,-6:]=False
 lum=a.mean(2);local=np.array(rgb.filter(ImageFilter.GaussianBlur(3)),dtype=float).mean(2);paint=np.clip((lum-local+12)/30,.2,1)
 radii=[2,4,7,10,8,5,3,1];strength=[.35,.6,.8,.7,.55,.4,.3,.25];frames=[]
 for n,(radius,gain) in enumerate(zip(radii,strength)):
  alpha=np.exp(-((dist-radius)/3.5)**2)*valid*paint*gain*135
  rgba=np.zeros((*water.shape,4),dtype='uint8');rgba[:,:,:3]=np.clip(a*.45+np.array([155,225,232])*.55,0,255);rgba[:,:,3]=alpha.astype('uint8');frame=Image.fromarray(rgba).resize(size,Image.Resampling.LANCZOS)
  # Strict water clipping after resampling: no stone/flower halo from Lanczos.
  arr=np.array(frame);safe=np.array(mask.crop(box).resize(size,Image.Resampling.BILINEAR))>250;arr[~safe]=0;frame=Image.fromarray(arr);frame.save(P/f'{name}-shore-{n:02}.png');frames.append(frame)
 tree=Element('image',w=str(size[0]),h=str(size[1]),name=name+' shoreline cels',version='0.0.3');stack=SubElement(tree,'stack')
 with zipfile.ZipFile(P/f'{name}-shoreline.ora','w') as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for n in reversed(range(8)):
   file=f'{name}-shore-{n:02}.png';z.writestr('data/'+file,(P/file).read_bytes());SubElement(stack,'layer',name=f'cel_{n+1}',src='data/'+file,x='0',y='0',opacity='1.0',visibility='visible' if n==0 else 'hidden',**{'composite-op':'svg:src-over'})
  z.writestr('stack.xml',tostring(tree));z.writestr('mergedimage.png',(P/f'{name}-shore-00.png').read_bytes())
 hashes=[hashlib.sha256(f.tobytes()).hexdigest() for f in frames];assert len(set(hashes))==8
 review=Image.new('RGB',(size[0]*2,size[1]*2));back=rgb.resize(size).convert('RGBA')
 for col,n in enumerate([0,2,3,6]):review.paste(Image.alpha_composite(back,frames[n]).convert('RGB'),((col%2)*size[0],(col//2)*size[1]))
 review.save(P/f'{name}-shore-review.jpg',quality=95)
 reports.append({'id':name,'master_rect':list(box),'cell_size':list(size),'frame_sha256':hashes,'all_frames_water_clipped':True})
(P/'SHORELINE.json').write_text(json.dumps({'source':source.relative_to(W).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'source-colour painted light bands derived within inspected water mask; eight advance/retreat cels; no scene geometry moved','frame_ms':320,'clips':reports,'status':'candidate; visual/device acceptance pending'},indent=2)+'\n');print('SHORE|8 unique water-clipped cels per pool')
