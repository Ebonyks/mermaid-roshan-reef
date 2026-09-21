from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage as nd
import numpy as np,json,hashlib
W=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parent/'water';D=W/'assets/sprites/sky_lagoon/animated_v1'
source=W/'assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png';im=Image.open(source).convert('RGB');hsv=np.array(im.convert('HSV'))
polygons=[[(0,1180),(620,1180),(620,1580),(0,1580)],[(4520,1000),(6143,1000),(6143,1620),(4520,1620)]]
domain=Image.new('L',im.size);draw=ImageDraw.Draw(domain)
for poly in polygons:draw.polygon(poly,fill=255)
water=(np.array(domain)>0)&(hsv[:,:,0]>=118)&(hsv[:,:,0]<=153)&(hsv[:,:,1]>=70)&(hsv[:,:,2]>=110)
labels,count=nd.label(water);sizes=np.bincount(labels.ravel());keep=(sizes>5000)&(np.arange(len(sizes))>0);water=keep[labels]
closed=nd.binary_closing(water,iterations=1);holes=nd.binary_fill_holes(closed)&~closed;labels,count=nd.label(holes);sizes=np.bincount(labels.ravel());fill=(sizes<500)&(np.arange(len(sizes))>0);highlight=((hsv[:,:,0]>=118)&(hsv[:,:,0]<=153))|((hsv[:,:,1]<35)&(hsv[:,:,2]>200));water=closed|(fill[labels]&highlight)
mask=Image.fromarray(water.astype('uint8')*255);mask.save(P/'surface-mask-native.png');small=mask.resize((1024,512),Image.Resampling.LANCZOS);rgba=Image.new('RGBA',small.size,'white');rgba.putalpha(small);rgba.save(D/'water_surface_mask.png')
review=im.resize((1536,512)).convert('RGBA');overlay=Image.new('RGBA',review.size,(240,40,190,0));overlay.putalpha(mask.resize(review.size,Image.Resampling.NEAREST).point(lambda a:a//2));review=Image.alpha_composite(review,overlay);review.convert('RGB').save(P/'surface-mask-review.jpg',quality=94)
report={'source':source.relative_to(W).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'master_size':list(im.size),'runtime_mask_size':[1024,512],'polygons':polygons,'method':'bounded painted-water hue/value classification; tiny highlight-hole fill; runtime alpha mask','interaction':'direct finger ripple only, no reward/job/actor action claim','frame_count':8,'frame_count_reason':'reuse accepted fixed-pivot eight-frame shared ripple atlas; within owner 6-24 range','status':'mask candidate requires rendered shore and blocker tests'};(P/'WATER_PLAN.json').write_text(json.dumps(report,indent=2)+'\n');print('WATER_MASK|native water pixels',int(water.sum()))
