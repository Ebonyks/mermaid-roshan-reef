from pathlib import Path
import subprocess,json,hashlib,zipfile,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw
import numpy as np
w=Path.cwd();base=w/'assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/clouds/cleaned';root=w/'tmp/sky-lagoon-whole-scene-v2/direct-clouds';report=[]
for row in json.loads((root/'jobs.json').read_text()):
 p=root/row['id'];p.mkdir(exist_ok=True);src=base/row['file'];original=Image.open(src).convert('RGBA');W,H=original.size
 r=subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','source='+str(src),'--script-param','out='+str(p),'--script',str(root/'author.lua')],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=120);assert r.returncode==0,r.stderr
 (p/'author.log').write_text(r.stdout);frames=[Image.open(p/f'cel-{k:02d}.png').convert('RGBA') for k in range(4)];arr=[np.asarray(f) for f in frames];o=np.asarray(original);visible=o[:,:,3]>0;assert np.array_equal(arr[0][visible],o[visible]);assert np.array_equal(arr[0][:,:,3],o[:,:,3])
 for k in range(4):assert np.array_equal(arr[k],np.asarray(Image.open(p/f'reopen-{k:02d}.png')))
 masks=[f[:,:,3]>127 for f in arr];iou=[float(np.logical_and(masks[i],masks[(i+1)%4]).sum()/np.logical_or(masks[i],masks[(i+1)%4]).sum()) for i in range(4)];stats=[]
 for f,m in zip(frames,masks):
  rgb=np.asarray(f)[:,:,:3][m]/255;lin=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4);yy,xx=np.where(m);stats.append({'bounds':[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)],'median_linear_luminance':float(np.median(lin@np.array([.2126,.7152,.0722]))),'median_saturation':float(np.median(np.asarray(f.convert('HSV'))[:,:,1][m])/255)})
 doc=ET.Element('image',w=str(W),h=str(H),name=row['id']+' four pose alternatives');stack=ET.SubElement(doc,'stack')
 with zipfile.ZipFile(p/'cloud-four-poses.ora','w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for k in range(4):
   group=ET.SubElement(stack,'stack',name=f'Pose {k+1}',visibility='visible' if k==0 else 'hidden',opacity='1.0')
   for label,filename in [('Fixed base','base-fixed.png'),('Moving upper lobes',f'upper-{k:02d}.png')]:
    path=f'data/{k}-{filename}';z.write(p/filename,path);ET.SubElement(group,'layer',name=label,src=path,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
  z.writestr('stack.xml',ET.tostring(doc));z.write(p/'cel-00.png','mergedimage.png')
 board=Image.new('RGB',(W*2,(H+20)*2),'#51b3d2');dr=ImageDraw.Draw(board);loop=[]
 for k,f in enumerate(frames):
  board.paste(f,(k%2*W,k//2*(H+20)),f);dr.text((k%2*W+4,k//2*(H+20)+H),f'Cel {k+1}',fill='white');im=Image.new('RGBA',f.size,(81,179,210,255));im.alpha_composite(f);loop.append(im.convert('RGB'))
 board.save(p/'keyframes.jpg',quality=95);loop[0].save(p/'loop.webp',save_all=True,append_images=loop[1:],duration=900,loop=0,lossless=True)
 item={'id':row['id'],'source':src.relative_to(w).as_posix(),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'frames':4,'layers':2,'cycle':3.6,'source_rest_visible_exact':True,'native_reopen_exact':True,'neighbor_iou':iou,'poses':stats,'method':'Direct Aseprite Lua-authored horizontal lobe deformation, fixed base, no vertical scaling; existing painted RGB sampled with premultiplied alpha. Not independently redrawn frames.','status':'SOURCE_TRIAL_PENDING_CONTEXTUAL_REVIEW','limitations':['ORA pose alternatives are not native Krita animation timeline','Small-cloud motion may be subpixel at gameplay scale','Full drift and seam review pending']};(p/'REVIEW.json').write_text(json.dumps(item,indent=2)+'\n');report.append(item);print(row['id'],min(iou),flush=True)
(root/'REVIEW.json').write_text(json.dumps(report,indent=2)+'\n')
