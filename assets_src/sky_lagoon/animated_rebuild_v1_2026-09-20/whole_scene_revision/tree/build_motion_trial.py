"""Whole visible original tree: twelve baked pose candidates and editable sources."""
from pathlib import Path
import json,io,zipfile,subprocess
from xml.etree.ElementTree import Element,SubElement,tostring
import numpy as np,cv2
from PIL import Image
P=Path('assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/tree');P.mkdir(parents=True,exist_ok=True)
source=Image.open('assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/tree/native-whole-tree-cutout.png').convert('RGBA')
a=np.array(source);h,w=a.shape[:2];y,x=np.indices((h,w),dtype=np.float32)
original=np.array(Image.open('assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png').convert('RGB').crop((0,0,w,h)))
mask=a[:,:,3]>0;under=cv2.inpaint(original,mask.astype('uint8')*255,7,cv2.INPAINT_TELEA);Image.fromarray(under).save(P/'underpaint-candidate.png');source.save(P/'original-tree-rest.png')
root_weight=np.clip((1090-y)/360,0,1);root_weight=root_weight**2*(3-2*root_weight)
branch=np.clip(np.abs(x-123)/160,0,1);height=np.clip((1050-y)/1000,0,1)
# Continuous displacement across all tiers; planted lower trunk never translates.
# Explicit baked deformation trial, not hand-redrawn acting or accepted delivery.
parts=['crown','upper_boughs','middle_boughs','lower_boughs','trunk_and_roots']
breaks=[0,300,490,700,860,1152]
frames=[]; previews=[]
premult=a.astype(np.float32);premult[:,:,:3]*=premult[:,:,3:4]/255
for k in range(12):
 phase=k*2*np.pi/12
 dx=np.clip(x/60,0,1)*root_weight*(8*height*np.sin(phase)+16*branch*(np.sin(phase-y/600)-np.sin(-y/600))*0.5)
 dy=np.clip(x/60,0,1)*root_weight*branch*3*(np.cos(phase-y/700)-np.cos(-y/700))
 warped=cv2.remap(premult,(x-dx).astype(np.float32),(y-dy).astype(np.float32),cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT)
 alpha=np.clip(warped[:,:,3:4],0,255);rgb=np.divide(warped[:,:,:3]*255,alpha,out=np.zeros_like(warped[:,:,:3]),where=alpha>0.1)
 out=np.concatenate([np.clip(rgb,0,255),alpha],axis=2).round().astype('uint8')
 if k==0:out=a.copy()
 frame=Image.fromarray(out);frame.save(P/f'frame-{k:02d}.png');frames.append(frame)
 for j,name in enumerate(parts):
  layer=out.copy();layer[:breaks[j]]=0;layer[breaks[j+1]:]=0;Image.fromarray(layer).save(P/f'{name}-{k:02d}.png')
 comp=Image.fromarray(under).convert('RGBA');comp.alpha_composite(frame);previews.append(comp.resize((300,864)))
previews[0].save(P/'whole-tree-motion-trial.gif',save_all=True,append_images=previews[1:],duration=200,loop=0)
root=Element('image',w=str(w),h=str(h),name='Original whole arrival tree',version='0.0.3');stack=SubElement(root,'stack')
with zipfile.ZipFile(P/'whole-tree-editable.ora','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for name in reversed(parts):
  path='data/'+name+'.png';z.writestr(path,(P/(name+'-00.png')).read_bytes());SubElement(stack,'layer',name=name,src=path,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',tostring(root));b=io.BytesIO();source.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
lua="local p=app.params.base\nlocal s=Sprite(400,1152,ColorMode.RGB)\nlocal names={'crown','upper_boughs','middle_boughs','lower_boughs','trunk_and_roots'}\nlocal layers={}\nfor j,n in ipairs(names) do local l=j==1 and s.layers[1] or s:newLayer();l.name=n;layers[j]=l end\nfor k=0,11 do\n if k>0 then s:newEmptyFrame() end\n s.frames[k+1].duration=.2\n for j,n in ipairs(names) do local t=app.open(p..'/'..n..string.format('-%02d.png',k));local im=Image(400,1152,ColorMode.RGB);local c=t.cels[1];im:drawImage(c.image,c.position);t:close();s:newCel(layers[j],k+1,im,Point(0,0)) end\nend\napp.activeSprite=s;s:newTag(1,12).name='whole_tree_breeze_trial';s:saveAs(p..'/whole-tree-12-cels.aseprite');s:close()\n"
(P/'assemble.lua').write_text(lua,encoding='utf-8')
subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','base='+str(P.resolve()).replace('\\','/'),'--script',str(P/'assemble.lua')],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
(P/'REVIEW.json').write_text(json.dumps({'status':'MOTION_TRIAL_NOT_RUNTIME_ACCEPTED','frames':12,'duration_seconds':2.4,'source':'original native panorama pixels, full visible tree','method':'Continuous branch/trunk displacement baked into twelve raster poses; Aseprite five-layer timeline. Not hand-drawn key poses.','root_rows_fixed':[1090,1151],'pending':['Moving silhouette matte and lower trunk mask review','Concealed underpaint review','In-context full-stage motion and GPU sampling','Adjust tier anatomy if bending reads rubbery'],'generated_rest_candidate_used':False},indent=2)+'\n',encoding='utf-8')
print('TREE_TRIAL|12 frames, 5 editable layers, Aseprite and ORA saved')
