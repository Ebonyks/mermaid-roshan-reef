"""Four-pose original-painted grass blades with fixed soil and protected path boundaries.
Run from repository root with Pillow, numpy, scipy and OpenCV available.
"""
from pathlib import Path
import io,json,hashlib,zipfile,subprocess
from xml.etree.ElementTree import Element,SubElement,tostring
import numpy as np,cv2
from scipy import ndimage as nd
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]; BASE=Path(__file__).resolve().parent; OUT=BASE/'whole_scene_revision'/'grass';OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png';master=Image.open(source).convert('RGB');a=np.array(master)
# Authored clear lawn regions in 1536x512 overview coordinates; no path coverage.
regions=[('arrival_lawn',[(145,418),(256,414),(345,423),(322,450),(269,473),(220,497),(158,486)]),('arrival_front_edge',[(161,495),(211,502),(303,501),(339,511),(139,511)]),('meadow_upper_left',[(521,314),(595,305),(639,310),(671,320),(641,345),(585,363),(519,374)]),('meadow_upper_right',[(682,315),(736,307),(814,305),(884,314),(932,335),(921,358),(828,378),(700,372),(649,365)]),('meadow_lower_lawn',[(638,433),(697,429),(784,431),(890,421),(917,432),(875,453),(813,480),(734,505),(658,506)]),('castle_left_verge',[(1136,444),(1167,449),(1199,470),(1239,501),(1247,511),(1198,511),(1173,488)]),('castle_right_verge',[(1461,462),(1519,472),(1534,486),(1534,511),(1457,511),(1413,498)])]
records=[];composites=[master.convert('RGBA') for _ in range(4)]
for name,points in regions:
 pts=np.array(points)*4;x0,y0=pts.min(0)-8;x1,y1=pts.max(0)+9;x0=max(0,x0);y0=max(0,y0);x1=min(6144,x1);y1=min(2048,y1);crop=a[y0:y1,x0:x1];h,w=crop.shape[:2]
 poly=Image.new('L',(w,h));ImageDraw.Draw(poly).polygon([(int(x-x0),int(y-y0)) for x,y in pts],fill=255);allowed=np.array(poly)>0
 hsv=cv2.cvtColor(crop,cv2.COLOR_RGB2HSV);luma=crop.astype(float).mean(2);detail=luma-nd.gaussian_filter(luma,3)
 green=(hsv[:,:,0]>=22)&(hsv[:,:,0]<=43)&(hsv[:,:,1]>80)&(hsv[:,:,2]>105)
 raw=allowed&green&(detail>5.5);labels,n=nd.label(raw);sizes=np.bincount(labels.ravel());keep=np.where((sizes>=5)&(sizes<=250))[0];keep=keep[keep!=0];selection=np.isin(labels,keep)
 mask=nd.binary_dilation(selection,iterations=1)&allowed&green
 labels,n=nd.label(mask);slices=nd.find_objects(labels);blades=[]
 for i,sl in enumerate(slices,1):
  if sl is None:continue
  yy,xx=sl;count=int((labels[sl]==i).sum())
  if count<5 or count>400:continue
  blades.append((i,sl))
 mask=np.isin(labels,[i for i,_ in blades]);under=cv2.inpaint(crop,mask.astype('uint8')*255,3,cv2.INPAINT_TELEA)
 folder=OUT/name;folder.mkdir(exist_ok=True);Image.fromarray(under).save(folder/'soil-fixed.png')
 layers=[];frames=[]
 for k,pose in enumerate([0,1,.25,-.8]):
  moving=Image.new('RGBA',(w,h))
  for idx,sl in blades:
   yy,xx=sl;pad=5;left=max(0,xx.start-pad);top=max(0,yy.start-pad);right=min(w,xx.stop+pad);bottom=min(h,yy.stop+pad)
   src=crop[top:bottom,left:right];alpha=(labels[top:bottom,left:right]==idx).astype(np.float32)
   sy,sx=np.indices(alpha.shape,dtype=np.float32);root=yy.stop-top-1;height=max(3,yy.stop-yy.start)
   weight=np.clip((root-sy)/height,0,1);amp=2.6+min(2,height*.13);phase_scale=.75+.25*np.cos((x0+xx.start)/170)
   dx=pose*amp*weight*phase_scale
   premult=np.dstack([src.astype(np.float32)*alpha[:,:,None],alpha*255]);warped=cv2.remap(premult,(sx-dx).astype(np.float32),sy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT)
   aa=np.clip(warped[:,:,3:4],0,255);rgb=np.divide(warped[:,:,:3]*255,aa,out=np.zeros_like(warped[:,:,:3]),where=aa>0)
   pixels=np.concatenate([np.clip(rgb,0,255),aa],2).round().astype('uint8');moving.alpha_composite(Image.fromarray(pixels),(left,top))
  moving.save(folder/f'blades-{k:02d}.png');frame=Image.fromarray(under).convert('RGBA');frame.alpha_composite(moving);frame.save(folder/f'frame-{k:02d}.png');frames.append(frame);layers.append(moving)
  composites[k].paste(frame,(int(x0),int(y0)))
 rest_error=int(np.abs(np.array(frames[0])[:,:,:3].astype(int)-crop.astype(int)).max());assert rest_error==0,(name,rest_error)
 root=Element('image',w=str(w),h=str(h),name=name,version='0.0.3');stack=SubElement(root,'stack')
 with zipfile.ZipFile(folder/'grass-editable.ora','w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
  for lname,img in [('painted_blades',layers[0]),('soil_fixed',Image.fromarray(under))]:
   b=io.BytesIO();img.save(b,format='PNG');fn='data/'+lname+'.png';z.writestr(fn,b.getvalue());SubElement(stack,'layer',name=lname,src=fn,x='0',y='0',opacity='1.0',visibility='visible',**{'composite-op':'svg:src-over'})
  z.writestr('stack.xml',tostring(root));b=io.BytesIO();frames[0].save(b,format='PNG');z.writestr('mergedimage.png',b.getvalue())
 records.append({'id':name,'rect':[int(x0),int(y0),w,h],'blades':len(blades),'frames':4,'rest_max_error':rest_error,'moving_pixel_count':int(mask.sum()),'protected_outside_polygon':True})
# A full-canvas source review does not substitute for runtime composition.
for k,im in enumerate(composites):im.resize((1536,512)).convert('RGB').save(OUT/f'panorama-{k:02d}.jpg',quality=94)
small=[im.resize((1536,512)) for im in composites];small[0].save(OUT/'grass-motion-trial.gif',save_all=True,append_images=small[1:],duration=250,loop=0)
(OUT/'SOURCE.json').write_text(json.dumps({'status':'SOURCE_MOTION_TRIAL_NOT_ACCEPTED','source':source.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Original bright painted blade components, independent anchored bend poses; soil stays fixed. Four baked raster poses, not generated hand-drawn frames.','regions':records,'pending':['Check whether individual painted marks read as grass bending rather than texture shimmer','Live castle overlay visibility','Aseprite export and runtime integration','Background shrub animation']},indent=2)+'\n',encoding='utf-8')
print('GRASS_TRIAL',len(records),'regions',sum(r['blades'] for r in records),'painted blade groups')
