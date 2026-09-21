from pathlib import Path
from PIL import Image
from scipy import ndimage as nd
import numpy as np,json,zipfile,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent/'bellflower';im=Image.open(P/'source-matte.png').convert('RGBA');a=np.array(im);h,w=a.shape[:2]
parts={};remaining=a.copy();boxes={'bell_tall':(218,149,478,368),'bell_middle':(389,350,625,570),'bell_right':(728,480,957,688),'bud':(870,363,958,497)}
for name,(x0,y0,x1,y1) in boxes.items():
 area=remaining[y0:y1,x0:x1];labels,count=nd.label(area[:,:,3]>8);sizes=np.bincount(labels.ravel());sizes[0]=0;owned=nd.binary_dilation(labels==sizes.argmax(),iterations=1)&(area[:,:,3]>0)
 layer=np.zeros_like(a);piece=layer[y0:y1,x0:x1];piece[owned]=area[owned];area[owned]=0;parts[name]=Image.fromarray(layer)
yy,xx=np.indices((h,w));fixed=(yy>=690)|((yy>=600)&(xx<648));base=remaining.copy();base[~fixed]=0;remaining[fixed]=0;parts['stems']=Image.fromarray(remaining);parts['leaves_fixed']=Image.fromarray(base)
scale=480/max(w,h);ox=(512-round(w*scale))//2;oy=(512-round(h*scale))//2
for name,part in parts.items():
 out=Image.new('RGBA',(512,512));out.paste(part.resize((round(w*scale),round(h*scale)),Image.Resampling.LANCZOS),(ox,oy));out.save(P/(name+'.png'))
order=['stems','bell_tall','bell_middle','bell_right','bud','leaves_fixed'];rest=Image.new('RGBA',(512,512))
for name in order:rest=Image.alpha_composite(rest,Image.open(P/(name+'.png')))
rest.save(P/'rest-prepared.png');tree=ET.Element('image',w='512',h='512',name='Bellflower editable source',version='0.0.3');stack=ET.SubElement(tree,'stack')
with zipfile.ZipFile(P/'bellflower-editable.ora','w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for name in reversed(order):
  path='data/'+name+'.png';z.writestr(path,(P/(name+'.png')).read_bytes());ET.SubElement(stack,'layer',name=name,src=path,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',ET.tostring(tree));z.writestr('mergedimage.png',(P/'rest-prepared.png').read_bytes())
print('Prepared six source-owned bellflower layers; disconnected stem fragments remain in stem layer')
