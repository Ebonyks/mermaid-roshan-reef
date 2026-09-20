from pathlib import Path
from PIL import Image
from scipy import ndimage as nd
import numpy as np,zipfile,json
from xml.etree.ElementTree import Element,SubElement,tostring
P=Path(__file__).resolve().parent/'huckleberry';im=Image.open(P/'source-rest.png').convert('RGBA');a=np.array(im)
# Remove a one-pixel matte fringe only at the outside edge; preserve native file.
a[:,:,3]=np.minimum(a[:,:,3],nd.minimum_filter(a[:,:,3],size=3));im=Image.fromarray(a)
size=(480,round(im.height*480/im.width));rest=Image.new('RGBA',(512,512));rest.paste(im.resize(size,Image.Resampling.LANCZOS),(16,128));rest.save(P/'rest-prepared.png');a=np.array(rest);yy,xx=np.indices((512,512))
# Source ownership groups. These are editable regions; the shared deformation
# samples the complete source so branch boundaries never develop cutout holes.
group=np.where(yy>=375,3,np.where(xx<195,0,np.where(xx<328,1,2)))
order=['branch_left','branch_middle','branch_right','root_fixed'];tree=Element('image',w='512',h='512',version='0.0.3',name='Huckleberry source groups');stack=SubElement(tree,'stack')
with zipfile.ZipFile(P/'huckleberry-editable.ora','w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for n in reversed(range(4)):
  part=a.copy();part[group!=n]=0;path=P/(order[n]+'.png');Image.fromarray(part).save(path);z.writestr('data/'+path.name,path.read_bytes());SubElement(stack,'layer',name=order[n],src='data/'+path.name,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',tostring(tree));z.writestr('mergedimage.png',(P/'rest-prepared.png').read_bytes())
(P/'PARTS.json').write_text(json.dumps({'canvas':[512,512],'root_anchor':[256,380],'fixed_rows':[375,512],'groups':order,'matte_cleanup':'one native pixel alpha erosion; RGB unchanged before uniform resampling','method_limit':'groups are regional editing ownership, not independently extracted complete branches; shared continuous branch field preserves seams'},indent=2)+'\n')
print('HUCKLEBERRY|four editable groups prepared')
