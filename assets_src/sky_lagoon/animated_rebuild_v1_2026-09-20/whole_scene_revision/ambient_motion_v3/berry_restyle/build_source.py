from pathlib import Path
import subprocess,json,hashlib,zipfile,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
import numpy as np
p=Path(__file__).resolve().parent
r=subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','source='+str((p/'rest-512.png').resolve()),'--script-param','out='+str(p.resolve()),'--script',str((p/'author.lua').resolve())],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120);assert r.returncode==0,r.stderr;(p/'author.log').write_text(r.stdout+r.stderr);frames=[Image.open(p/f'cel-{i:02d}.png').convert('RGBA') for i in range(8)];a=[np.asarray(f) for f in frames];orig=np.asarray(Image.open(p/'rest-512.png').convert('RGBA'));assert np.array_equal(a[0][orig[:,:,3]>0],orig[orig[:,:,3]>0]);assert np.array_equal(a[0][:,:,3],orig[:,:,3]);yy,xx=np.where(orig[:,:,3]>127);stop=int(yy.max())-8
for i in range(8):assert np.array_equal(a[i][stop:],a[0][stop:]);assert np.array_equal(a[i],np.asarray(Image.open(p/f'reopen-{i:02d}.png').convert('RGBA')))
atlas=Image.new('RGBA',(2048,1024));root=ET.Element('image',w='512',h='512',name='Restyled berry shrub pose alternatives');stack=ET.SubElement(root,'stack')
with zipfile.ZipFile(p/'huckleberry-restyled-eight-poses.ora','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for i,f in enumerate(frames):
  atlas.paste(f,(i%4*512,i//4*512));group=ET.SubElement(stack,'stack',name=f'Pose {i+1}',visibility='visible' if i==0 else 'hidden',opacity='1.0')
  for label,name in [('Fixed connected root','base-fixed.png'),('Whole canopy',f'upper-{i:02d}.png')]:
   path=f'data/{i}-{name}';z.write(p/name,path);ET.SubElement(group,'layer',name=label,src=path,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',ET.tostring(root));z.write(p/'cel-00.png','mergedimage.png')
atlas.save(p/'eight-cel-atlas.png');loop=[]
for f in frames:im=Image.new('RGBA',f.size,(71,118,96,255));im.alpha_composite(f);loop.append(im.convert('RGB'))
loop[0].save(p/'source-motion.webp',save_all=True,append_images=loop[1:],duration=[300,240,300,300,320,240,300,300],loop=0,lossless=True)
(p/'MOTION_REVIEW.json').write_text(json.dumps({'status':'ANIMATED_SOURCE_TRIAL_NOT_RUNTIME_ACCEPTED','frames':8,'layers':2,'cycle_seconds':2.3,'method':'Direct Aseprite bounded canopy deformation of one rest drawing; spatially varying phase across connected branches, fixed lower root. Not eight independent generated drawings or individually isolated leaves.','rest_visible_exact':True,'root_rows_fixed_from':stop,'native_reopen_exact':True,'unique_rgba_frames':len({hashlib.sha256(f.tobytes()).hexdigest() for f in frames}),'atlas_dimensions':[2048,1024],'runtime_anchor':[256,380],'limits':['Only rest pose has undergone gameplay comparison','Eight-frame contextual playback and color stability pending','ORA pose alternatives, not native Krita timeline','No production assets modified']},indent=2)+'\n');print(r.stdout)
