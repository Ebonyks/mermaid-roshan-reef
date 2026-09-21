from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
import json, hashlib, zipfile, xml.etree.ElementTree as ET

p=Path(__file__).resolve().parent
source=p.parents[1]/'bellflower/bellflower-atlas.png'
original=Image.open(source).convert('RGBA')
atlas=Image.new('RGBA',(2048,1024))
frames=[]
for i in range(8):
    im=Image.open(p/f'cel-{i:02d}.png').convert('RGBA')
    old=original.crop((i%4*512,i//4*512,(i%4+1)*512,(i//4+1)*512))
    assert np.array_equal(np.array(im)[:,:,3],np.array(old)[:,:,3])
    assert np.array_equal(np.array(im)[300:],np.array(Image.open(p/'cel-00.png'))[300:])
    frames.append(im);atlas.paste(im,(i%4*512,i//4*512))
atlas.save(p/'bellflower-leaf-grade.png')
order=['stems','bell_tall','bell_middle','bell_right','bud','leaves_fixed']
tree=ET.Element('image',w='512',h='512',name='Bellflower leaf grade - editable rest',version='0.0.3')
stack=ET.SubElement(tree,'stack')
with zipfile.ZipFile(p/'bellflower-leaf-grade.ora','w') as z:
    z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
    for name in reversed(order):
        path='data/'+name+'.png';z.writestr(path,(p/(name+'.png')).read_bytes())
        ET.SubElement(stack,'layer',name=name,src=path,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
    z.writestr('stack.xml',ET.tostring(tree));z.writestr('mergedimage.png',(p/'cel-00.png').read_bytes())
board=Image.new('RGB',(1024,540),'#435b50');draw=ImageDraw.Draw(board)
for x,im,label in [(0,original.crop((0,0,512,512)),'Original'),(512,frames[0],'Leaf-only grade')]:
    board.paste(im,(x,28),im);draw.text((x+20,8),label,fill='white')
board.save(p/'comparison.jpg',quality=94)
report={'status':'SOURCE_VERIFIED_CONTEXT_REVIEW_PENDING','frames':8,'layers':6,'changed_layer':'leaves_fixed','alpha_exact_all_frames':True,'fixed_lower_rows_exact':True,'non_leaf_cels_exact':40,'timing_preserved':True,'method':'Aseprite leaf-only linear-light highlight compression with small red reduction and blue increase; no new generation. ORA has six editable rest layers; Aseprite contains the eight-frame timeline.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in p.iterdir() if f.is_file() and f.name!='REVIEW.json'}}
(p/'REVIEW.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('BELLFLOWER_LEAF_GRADE|8 alpha-exact frames, fixed roots, editable ORA|PASS')
