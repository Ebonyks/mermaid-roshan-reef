from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage as nd
import numpy as np,json,hashlib,zipfile,io,xml.etree.ElementTree as ET
W=Path(__file__).resolve().parents[3];P=W/'assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/grass';image=Image.open(P/'native-four-pose-sheet.png').convert('RGBA');cw=image.width//4;records=[];frames=[]
for i in range(4):
 raw=image.crop((i*cw,0,(i+1)*cw,image.height));raw.save(P/f'native-cell-{i}.png');a=np.array(raw);solid=a[:,:,3]>100;labels,n=nd.label(solid);sizes=np.bincount(labels.ravel());sizes[0]=0;solid=labels==sizes.argmax();solid=nd.binary_opening(solid,iterations=1);inside=nd.distance_transform_edt(solid)>=4;indices=nd.distance_transform_edt(~inside,return_distances=False,return_indices=True);edge=solid&~inside;a[edge,:3]=a[indices[0][edge],indices[1][edge],:3];a[:,:,3]=np.minimum(a[:,:,3],np.clip(nd.gaussian_filter(solid.astype(float),.5)*255,0,255).astype('uint8'));a[a[:,:,3]==0,:3]=0
 ys,xs=np.where(solid);root_y=int(ys.max());bottom=solid.copy();bottom[:root_y-6]=False;root_x=float(np.where(bottom)[1].mean());scale=.48;im=Image.fromarray(a).resize((round(cw*scale),round(image.height*scale)),Image.Resampling.LANCZOS);canvas=Image.new('RGBA',(320,320));pos=(round(160-root_x*scale),round(292-root_y*scale));canvas.paste(im,pos);frames.append(canvas);records.append({'cell':i,'source_root':[root_x,root_y],'uniform_scale':scale,'translation':pos})
# Root is an explicit static part, not a per-frame morph. Upper cels own rows above it.
root=Image.new('RGBA',(320,320));root.paste(frames[0].crop((0,280,320,320)),(0,280));root.save(P/'root_fixed.png')
for i,frame in enumerate(frames):
 upper=frame.copy();upper.paste((0,0,0,0),(0,280,320,320));upper.save(P/f'upper_{i:02}.png');frame=Image.alpha_composite(upper,root);frame.save(P/f'frame_{i:02}.png');frames[i]=frame
sheet=Image.new('RGBA',(640,640))
for i,frame in enumerate(frames):sheet.paste(frame,((i%2)*320,(i//2)*320))
sheet.save(P/'review-atlas.png')
# The 640x640 sheet is copied unchanged to grass_breeze.png; use lossless import (longest side <=1024).
board=Image.new('RGB',(1280,350),'#dde1db');d=ImageDraw.Draw(board)
for i,frame in enumerate(frames):board.paste(frame,(i*320,20),frame);d.text((i*320+14,9),['rest','bend','strongest','recover'][i],fill='#233d38')
board.save(P/'pose-review.jpg',quality=92)
def png(im):b=io.BytesIO();im.save(b,format='PNG');return b.getvalue()
tree=ET.Element('image',w='320',h='320',name='Grass four cel review',version='0.0.3');stack=ET.SubElement(tree,'stack')
with zipfile.ZipFile(P/'grass-four-cels.ora','w') as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 z.writestr('data/root.png',png(root));ET.SubElement(stack,'layer',name='Root fixed - shared all cels',src='data/root.png',x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 for i in range(4):
  path=f'data/upper{i}.png';z.writestr(path,(P/f'upper_{i:02}.png').read_bytes());ET.SubElement(stack,'layer',name=f'Cel {i+1} - '+['rest','bend','strongest','recover'][i],src=path,x='0',y='0',opacity='1.0',visibility='visible' if i==0 else 'hidden',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',ET.tostring(tree));z.writestr('mergedimage.png',png(frames[0]));thumb=frames[0].copy();thumb.thumbnail((256,256));z.writestr('Thumbnails/thumbnail.png',png(thumb))
report={'source_sha256':hashlib.sha256((P/'native-four-pose-sheet.png').read_bytes()).hexdigest(),'generation_tool':'Codex built-in image_gen','generated_model_pin':None,'frame_count':4,'blade_count_review':[5,5,5,5],'frame_size':[320,320],'root_anchor':[160,292],'shared_root_rows':[280,320],'frame_normalization':records,'durations_ms':[240,200,240,260],'unique_rgba_frames':len({hashlib.sha256(f.tobytes()).hexdigest() for f in frames}),'status':'candidate_pending_temporal_scene_review','runtime_accepted':False}
(P/'CEL_MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
