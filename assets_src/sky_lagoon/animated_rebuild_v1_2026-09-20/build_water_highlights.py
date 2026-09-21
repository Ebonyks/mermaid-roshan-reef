from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np,json,hashlib,zipfile,io
from xml.etree.ElementTree import Element,SubElement,tostring
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'water'
source=W/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
im=Image.open(source).convert('RGB');mask=Image.open(P/'surface-mask-native.png').convert('L')
specs=[('arrival',(0,1180,640,1580),(256,256)),('castle',(4520,1000,6144,1640),(512,256))]
report=[]
for name,box,size in specs:
 rgb=im.crop(box).resize(size,Image.Resampling.LANCZOS); a=np.array(rgb,dtype=float);water=np.array(mask.crop(box).resize(size,Image.Resampling.LANCZOS),dtype=float)/255
 luminance=a.mean(axis=2);blur=np.array(rgb.filter(ImageFilter.GaussianBlur(4)),dtype=float).mean(axis=2)
 # Only the existing short painted light ridges; no relocated or mirrored marks.
 strength=np.clip((luminance-blur-3)/18,0,1)*np.clip((luminance-100)/60,0,1)*water
 # Leave shoreline edge untouched, including resampling halo.
 from scipy.ndimage import distance_transform_edt
 strength*=np.clip(distance_transform_edt(water>.98)/4,0,1)
 yy,xx=np.indices((size[1],size[0]));group=((yy//13)+(xx//47))%4
 layers=[]
 for n in range(4):
  rgba=np.zeros((size[1],size[0],4),dtype=np.uint8);rgba[:,:,:3]=np.clip(a*.68+np.array([176,241,245])*.32,0,255).astype('uint8');rgba[:,:,3]=(strength*(group==n)*180).astype('uint8')
  layer=Image.fromarray(rgba);path=P/f'{name}-highlight-{n}.png';layer.save(path);layers.append(layer)
 tree=Element('image',w=str(size[0]),h=str(size[1]),name=name+' painted light groups');stack=SubElement(tree,'stack');merged=Image.new('RGBA',size)
 with zipfile.ZipFile(P/f'{name}-highlights.ora','w') as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for n,layer in reversed(list(enumerate(layers))):
   b=io.BytesIO();layer.save(b,format='PNG');z.writestr(f'data/layer{n}.png',b.getvalue());SubElement(stack,'layer',name=f'painted_ridges_{n}',src=f'data/layer{n}.png',x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
  for layer in layers:merged=Image.alpha_composite(merged,layer)
  z.writestr('stack.xml',tostring(tree));b=io.BytesIO();merged.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
 review=Image.alpha_composite(rgb.convert('RGBA'),merged);review.resize((size[0]*2,size[1]*2)).convert('RGB').save(P/f'{name}-highlights-review.jpg',quality=94)
 report.append({'id':name,'master_rect':list(box),'cell_size':list(size),'groups':4,'frames':12,'duration_ms':180,'role':'light-only painted ridge accent; fixed shoreline and texture coordinates','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'HIGHLIGHTS.json').write_text(json.dumps({'source':source.relative_to(W).as_posix(),'method':'existing painted ridges separated into four light groups; direct Aseprite per-cel opacity authorship; no spatial warping','status':'candidate, requires temporal and device acceptance','clips':report},indent=2)+'\n')
print('HIGHLIGHTS|two editable sources ready')
