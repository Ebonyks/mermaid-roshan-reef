from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent/'bridge'
src=Image.open(P/'reference_locked.png').convert('RGBA'); a=np.array(src)
under=Image.open(P/'deck-underpaint-native.png').convert('RGBA').resize(src.size,Image.Resampling.LANCZOS)
# Source-space top surface; fixed edge beams are deliberately excluded.
deck=Image.new('L',src.size);d=ImageDraw.Draw(deck)
d.polygon([(77,957),(375,769),(593,775),(318,1000)],fill=255)
occ=Image.new('L',src.size);d=ImageDraw.Draw(occ)
# Tight front post shapes, not the former rectangular envelopes.
for x,y,r,bottom in [(350,899,20,980),(470,799,16,856),(524,770,14,816),(599,729,12,779)]:
 d.ellipse((x-r-2,y-r-2,x+r+2,y+r+2),fill=255)
 d.ellipse((x-r-4,y+r-7,x+r+4,y+r+8),fill=255)
 half=round(r*.75)
 d.rounded_rectangle((x-half-2,y+r-2,x+half+2,bottom+2),radius=3,fill=255)
 d.ellipse((x-half-5,bottom-7,x+half+5,bottom+7),fill=255)
# Chain spans follow their painted sag, with short pendant ropes retained.
for points in [[(370,902),(387,895),(407,878),(428,852),(451,817)],[(488,801),(502,789),(510,776)],[(538,768),(565,758),(589,738)],[(396,884),(397,913)],[(430,850),(432,871)],[(498,791),(501,827)],[(565,753),(566,790)]]:
 d.line(points,fill=255,width=10,joint='curve')
# The entire rail-side apron is a fixed structural strip, including its cast shadow.
# Complete the hidden deck beneath it rather than leaving fragments of gold.
d.polygon([(303,1023),(303,863),(396,835),(449,769),(627,710),(655,1023)],fill=255)
mask=np.array(deck)>0;fixed=np.array(occ)>0;visible=mask&~fixed
# Hidden pixels use the registered generated underpaint only. Every exposed rest pixel remains original.
floor=np.array(under);floor[visible]=a[visible];floor[~mask]=0
support=a.copy();support[visible]=0
Image.fromarray(floor).save(P/'deck-complete-v2.png');Image.fromarray(support).save(P/'castle-supports-v2.png');occ.save(P/'front-occlusion-mask-v2.png')
rest=Image.alpha_composite(Image.fromarray(floor),Image.fromarray(support));b=np.array(rest)
exact=bool(np.array_equal(b[:,:,3],a[:,:,3]) and np.array_equal(b[a[:,:,3]>0],a[a[:,:,3]>0]))
bg=Image.new('RGBA',src.size,'#31424d');bg.alpha_composite(Image.fromarray(floor));bg.crop((40,740,630,1024)).resize((1180,568)).convert('RGB').save(P/'deck-complete-v2-review.jpg',quality=94)
report={'status':'candidate masks; component contour review pending','source_visible_rest_exact':exact,'hidden_underpaint_source':'deck-underpaint-native.png','underpaint_registration':'whole image resized 1254 square to source 1022x1024; only concealed surface used; precise registration pending','mask_method':'manually placed source-space deck polygon, post silhouettes and chain paths','motion_authored':False,'runtime_integrated':False}
(P/'LAYERS_V2.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
