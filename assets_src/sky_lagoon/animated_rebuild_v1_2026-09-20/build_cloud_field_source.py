"""Source-preserving cloud separation for whole-scene motion review, not runtime delivery."""
from pathlib import Path
import io,json,hashlib,zipfile
from xml.etree.ElementTree import Element,SubElement,tostring
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as nd
import cv2
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
OUT=BASE/'whole_scene_revision'/'clouds'; OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png'
im=Image.open(source).convert('RGB'); a=np.array(im); healed=a.copy()
# Bounds measured on 1536x512 overview, scaled back to native 6144x2048.
boxes=[('arrival_high_left',(69,61,161,99)),('arrival_high_right',(326,114,448,163)),('arrival_small_center',(174,177,238,203)),('arrival_small_right',(274,194,334,217)),('arrival_mid_right',(286,168,360,197)),('meadow_high_left',(498,77,632,132)),('meadow_high_right',(931,76,1070,126)),('meadow_small_left',(449,164,537,184)),('meadow_mid_right',(805,145,905,187)),('meadow_small_center',(746,180,800,208)),('meadow_small_far',(801,188,841,206)),('castle_high',(1304,27,1475,94))]
entries=[]; layers=[]
for name,box in boxes:
 x0,y0,x1,y1=[v*4 for v in box]; crop=a[y0:y1,x0:x1]; hsv=cv2.cvtColor(crop,cv2.COLOR_RGB2HSV)
 # Clouds are pale warm/blue-white; surrounding sky is strongly cyan.
 rgb=crop.astype('int16')
 mask=(rgb[:,:,1]-rgb[:,:,0]<38)&(rgb[:,:,2]-rgb[:,:,0]<86)&(rgb[:,:,0]>125)
 labs,n=nd.label(mask); sizes=np.bincount(labs.ravel()); keep=np.where(sizes>50)[0]
 boundary=set(np.concatenate([labs[0],labs[-1],labs[:,0],labs[:,-1]]).tolist()); keep=[v for v in keep if v!=0 and v not in boundary]
 mask=np.isin(labs,keep)
 mask=nd.binary_fill_holes(mask); mask=nd.binary_dilation(mask,iterations=2)
 if mask.sum()<150: raise ValueError('No complete cloud in '+name)
 mask[:2]=False;mask[-2:]=False;mask[:,:2]=False;mask[:,-2:]=False
 tree_path=BASE/'whole_scene_revision/tree/original-tree-rest.png'
 if tree_path.exists() and x0<400 and y0<1152:
  tree_alpha=np.array(Image.open(tree_path).getchannel('A'));overlap=np.zeros(mask.shape,dtype=bool)
  oh=min(y1,1152)-y0;ow=min(x1,400)-x0
  if oh>0 and ow>0: overlap[:oh,:ow]=tree_alpha[y0:y0+oh,x0:x0+ow]>0
  mask &= ~overlap
 # Preserve the original two-pixel edge context; motion review must catch halos.
 rgba=np.dstack((crop,mask.astype('uint8')*255)); card=Image.fromarray(rgba)
 card.save(OUT/(name+'.png'))
 filled=cv2.inpaint(crop,mask.astype('uint8')*255,9,cv2.INPAINT_TELEA)
 healed[y0:y1,x0:x1]=filled
 entries.append({'id':name,'rect':[x0,y0,x1-x0,y1-y0],'file':name+'.png','masked_pixels':int(mask.sum()),'edge_guard_pixels':2})
 layers.append((name,card,x0,y0))
Image.fromarray(healed).save(OUT/'sky-clouds-removed-candidate.png')
composite=Image.fromarray(healed).convert('RGBA')
for name,card,x,y in layers:composite.alpha_composite(card,(x,y))
error=int(np.abs(np.array(composite)[:,:,:3].astype(int)-a.astype(int)).max()); assert error==0,error
# One editable canvas, original source at rest reconstructed exactly.
root=Element('image',w='6144',h='2048',name='Sky Lagoon original cloud masses',version='0.0.3'); stack=SubElement(root,'stack')
with zipfile.ZipFile(OUT/'cloud-field-editable.ora','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
 for name,card,x,y in list(reversed(layers))+[('healed_base_candidate',Image.fromarray(healed),0,0)]:
  b=io.BytesIO();card.save(b,format='PNG'); path='data/'+name+'.png';z.writestr(path,b.getvalue());SubElement(stack,'layer',name=name,src=path,x=str(x),y=str(y),opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
 z.writestr('stack.xml',tostring(root));b=io.BytesIO();composite.save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
# In-context maximum drift trial, three phases. It exposes underpaint defects.
board=Image.new('RGB',(1536,1536),'white')
for row,phase in enumerate([0,1,-1]):
 frame=Image.fromarray(healed).convert('RGBA')
 for i,(name,card,x,y) in enumerate(layers):frame.alpha_composite(card,(x+phase*(14+i%3*5),y))
 board.paste(frame.convert('RGB').resize((1536,512)),(0,row*512))
board.save(OUT/'rest-and-drift-review.jpg',quality=94)
(OUT/'SOURCE.json').write_text(json.dumps({'source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'status':'SEPARATION_CANDIDATE_NOT_ANIMATION_DELIVERY','clouds':entries,'rest_max_channel_error':error,'review_limits':['Rest equality does not verify moving edges or concealed fill.','Mountain-overlapping clouds and low cloud sea are not yet separated.','No runtime integration or native animation timeline yet.'],'method':'Original pixel masks and concealed inpaint; local image processing authorized by owner.'},indent=2)+'\n',encoding='utf-8')
print('CLOUD_SOURCE',len(entries),'whole clouds; rest error',error)
