"""Original-art shrub canopy motion studies. Run at repository root."""
from pathlib import Path
import json,io,zipfile,subprocess
from xml.etree.ElementTree import Element,SubElement,tostring
import numpy as np,cv2
from scipy import ndimage as nd
from PIL import Image,ImageDraw
B=Path(__file__).resolve().parent;R=B.parents[2];O=B/'whole_scene_revision/shrubs';O.mkdir(parents=True,exist_ok=True)
source=R/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png';master=np.array(Image.open(source).convert('RGB'))
regions=[('arrival_bank_left',[(74,238),(99,220),(122,236),(133,268),(119,297),(82,293)]),('arrival_bank_right',[(336,293),(370,278),(398,282),(425,298),(464,304),(494,322),(494,346),(445,342),(390,328),(350,320)]),('meadow_hedge_left',[(517,282),(546,268),(590,266),(609,276),(609,301),(554,304),(520,302)]),('meadow_hedge_right',[(711,285),(758,270),(806,278),(846,268),(896,280),(922,300),(879,307),(823,301),(770,306),(721,307)]),('castle_approach_bank',[(1027,291),(1051,274),(1080,286),(1103,301),(1122,318),(1109,337),(1070,326),(1036,327)]),('castle_far_bank',[(1394,251),(1420,238),(1446,244),(1490,243),(1528,250),(1534,273),(1514,286),(1472,275),(1435,267),(1400,266)])]
records=[]
for name,points in regions:
 pts=np.array(points)*4;x0,y0=pts.min(0)-16;x1,y1=pts.max(0)+17;x0=max(0,x0);y0=max(0,y0);x1=min(6144,x1);y1=min(2048,y1);crop=master[y0:y1,x0:x1];h,w=crop.shape[:2];p=O/name;p.mkdir(exist_ok=True)
 polygon=Image.new('L',(w,h));ImageDraw.Draw(polygon).polygon([(int(x-x0),int(y-y0)) for x,y in pts],fill=255);region=np.array(polygon)>0
 hsv=cv2.cvtColor(crop,cv2.COLOR_RGB2HSV);green=(hsv[:,:,0]>=30)&(hsv[:,:,0]<=87)&(hsv[:,:,1]>65);berry=(hsv[:,:,0]>115)&(hsv[:,:,1]>45)&(hsv[:,:,2]<210)
 foliage=region&(green|berry);foliage=nd.binary_closing(foliage,iterations=2)&region
 # The fixed perimeter and roots avoid moving paths, stones and adjoining cards.
 edge=np.clip(nd.distance_transform_edt(foliage)/7,0,1);outer=np.clip(nd.distance_transform_edt(region)/20,0,1)
 yy,xx=np.indices((h,w),dtype=np.float32);root=np.clip((h-24-yy)/(h*.65),0,1);root=root*root*(3-2*root)
 weights=(outer*root).astype(np.float32);Image.fromarray((weights*255).astype('uint8')).save(p/'canopy-motion-mask.png')
 under=cv2.inpaint(crop,foliage.astype('uint8')*255,5,cv2.INPAINT_TELEA)
 src=np.dstack([crop.astype(np.float32)*foliage[:,:,None],foliage.astype(np.float32)*255])
 frames=[];moving=[];fixed=Image.fromarray(under).convert('RGBA')
 for k,pose in enumerate([0,.8,.2,-.65]):
  dx=weights*pose*(7+3*np.sin(xx/80));dy=weights*pose*1.6*np.sin(xx/110)
  warped=cv2.remap(src,(xx-dx).astype(np.float32),(yy-dy).astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
  alpha=np.clip(warped[:,:,3:4],0,255);rgb=np.divide(warped[:,:,:3]*255,alpha,out=np.zeros_like(warped[:,:,:3]),where=alpha>0)
  card=Image.fromarray(np.concatenate([np.clip(rgb,0,255),alpha],2).round().astype('uint8'));card.save(p/f'canopy-{k:02d}.png');moving.append(card)
  frame=fixed.copy();frame.alpha_composite(card);frames.append(frame);frame.save(p/f'frame-{k:02d}.png')
 base=np.dstack([under,np.full((h,w),255,np.uint8)]);Image.fromarray(base).save(p/'fixed-surroundings.png')
 rootxml=Element('image',w=str(w),h=str(h),name=name,version='0.0.3');stack=SubElement(rootxml,'stack')
 with zipfile.ZipFile(p/'shrubs-editable.ora','w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for label,img in [('canopy',moving[0]),('fixed_surroundings',Image.fromarray(base))]:
   buf=io.BytesIO();img.save(buf,format='PNG');fn='data/'+label+'.png';z.writestr(fn,buf.getvalue());SubElement(stack,'layer',name=label,src=fn,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
  z.writestr('stack.xml',tostring(rootxml));buf=io.BytesIO();frames[0].save(buf,format='PNG');z.writestr('mergedimage.png',buf.getvalue())
 lua=f"local p=app.params.base;local s=Sprite({w},{h},ColorMode.RGB);local fixed=s.layers[1];fixed.name='fixed_surroundings';local canopy=s:newLayer();canopy.name='painted_canopy'\nfor k=0,3 do if k>0 then s:newEmptyFrame() end;s.frames[k+1].duration=.45;for j,n in ipairs({{'fixed-surroundings.png',string.format('canopy-%02d.png',k)}}) do local t=app.open(p..'/'..n);local c=t.cels[1];local im=Image({w},{h},ColorMode.RGB);im:drawImage(c.image,c.position);t:close();s:newCel(j==1 and fixed or canopy,k+1,im,Point(0,0)) end end;app.activeSprite=s;s:newTag(1,4).name='canopy_breeze_trial';s:saveAs(p..'/shrubs-four-cels.aseprite');s:close()"
 (p/'assemble.lua').write_text(lua,encoding='utf-8');subprocess.run(['C:/Program Files/Aseprite/Aseprite.exe','-b','--script-param','base='+str(p).replace('\\','/'),'--script',str(p/'assemble.lua')],check=True,creationflags=subprocess.CREATE_NO_WINDOW)
 assert np.array_equal(np.array(frames[0])[:,:,:3],crop)
 records.append({'id':name,'rect':[int(x0),int(y0),w,h],'frames':4,'moving_pixels':int((weights>0).sum()),'rest_exact':True})
(O/'SOURCE.json').write_text(json.dumps({'status':'CANOPY_MOTION_STUDY_NOT_ACCEPTED','regions':records,'method':'Four baked canopy bend poses, including green/berry silhouettes; concealed underpaint, fixed root and outer region boundaries. Broad connected hedge regions, not individually redrawn bushes.','limitations':['Inspect moving contour gaps and concealed fill; dense connected foliage requires seam review at region joins.','Not a substitute for larger isolated foreground plant animation.','No runtime or device validation yet.']},indent=2)+'\n',encoding='utf-8');print('SHRUB_STUDY',len(records),'regions, 24 cels')
