from pathlib import Path
from PIL import Image
from scipy.ndimage import minimum_filter
import numpy as np,json,hashlib,zipfile
from xml.etree.ElementTree import Element,SubElement,tostring
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'conifer';P.mkdir(exist_ok=True);src=W/'assets/sprites/sky_lagoon/sky_lagoon_tree_sticker_slender_v1.png';im=Image.open(src).convert('RGBA');a=np.array(im);a[:,:,3]=minimum_filter(a[:,:,3],size=3);rest=Image.new('RGBA',(256,384));rest.paste(Image.fromarray(a),(1,2));rest.save(P/'rest-prepared.png');a=np.array(rest);yy,xx=np.indices((384,256));fixed=(yy>=240)|(abs(xx-128)<=12);groups=np.where(fixed,0,np.where(xx<128,1,2));names=['trunk_and_garden_fixed','left_boughs','right_boughs'];tree=Element('image',w='256',h='384',name='Conifer editable source',version='0.0.3');stack=SubElement(tree,'stack')
with zipfile.ZipFile(P/'conifer-editable.ora','w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for n in reversed(range(3)):
  part=a.copy();part[groups!=n]=0;path=P/(names[n]+'.png');Image.fromarray(part).save(path);z.writestr('data/'+path.name,path.read_bytes());SubElement(stack,'layer',name=names[n],src='data/'+path.name,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',tostring(tree));z.writestr('mergedimage.png',(P/'rest-prepared.png').read_bytes())
(P/'SOURCE.json').write_text(json.dumps({'source':src.relative_to(W).as_posix(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'native_size':[253,380],'cell_size':[256,384],'source_offset':[1,2],'matte_cleanup':'one native pixel alpha erosion removes white outer fringe; source preserved','fixed':'center columns116..140 and garden rows240..383','status':'candidate'},indent=2)+'\n')
