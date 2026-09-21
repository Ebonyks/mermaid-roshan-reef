from pathlib import Path
from PIL import Image
import numpy as np,json,zipfile,hashlib
from xml.etree.ElementTree import Element,SubElement,tostring
P=Path(__file__).resolve().parent/'bridge';W=Path(__file__).resolve().parents[3];D=W/'assets/sprites/sky_lagoon/animated_v1'
src=Image.open(D/'bridge_front_rail.png').convert('RGBA');box=(48,28,272,220);patch=src.crop(box);patch.save(P/'chain-patch-source.png');fixed=np.array(src);fixed[28:220,48:272]=0;Image.fromarray(fixed).save(D/'bridge_front_rail_fixed.png')
a=np.array(patch);xx=np.indices(a.shape[:2])[1];groups=np.zeros(a.shape[:2],dtype='uint8')
for n,(lo,hi) in enumerate([(6,76),(121,139),(173,214)],1):groups[(xx>lo)&(xx<hi)]=n
names=['posts_and_attachments_fixed','chain_near','chain_middle','chain_far'];tree=Element('image',w='224',h='192',name='Bridge chain source',version='0.0.3');stack=SubElement(tree,'stack')
with zipfile.ZipFile(P/'bridge-chains-editable.ora','w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for n in reversed(range(4)):
  part=a.copy();part[groups!=n]=0;path=P/(names[n]+'.png');Image.fromarray(part).save(path);z.writestr('data/'+path.name,path.read_bytes());SubElement(stack,'layer',name=names[n],src='data/'+path.name,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',tostring(tree));z.writestr('mergedimage.png',(P/'chain-patch-source.png').read_bytes())
(P/'CHAINS_SOURCE.json').write_text(json.dumps({'source':'assets/sprites/sky_lagoon/animated_v1/bridge_front_rail.png','source_sha256':hashlib.sha256((D/'bridge_front_rail.png').read_bytes()).hexdigest(),'patch_rect':list(box),'cell_size':[224,192],'moving_x_intervals':[[6,76],[121,139],[173,214]],'method':'direct Aseprite column-wise chain sag; columns containing posts remain exact; fixed attachment boundaries','scope':'secondary contact motion, no idle loop','status':'candidate'},indent=2)+'\n')
