"""Isolate fixed near-side rail shapes; never promote a broad floor band to foreground."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
import cv2
from scipy import ndimage as nd
P=Path(__file__).resolve().parent/'bridge';W=Path(__file__).resolve().parents[3];D=W/'assets/sprites/sky_lagoon/animated_v1'
src=Image.open(P/'reference_locked.png').convert('RGBA');a=np.array(src)
mask=Image.new('L',src.size);d=ImageDraw.Draw(mask)
# Source-space outlines inspected against a 3x coordinate-grid review.
d.polygon([(349,872),(359,874),(367,882),(370,890),(369,900),(372,903),(374,910),(370,916),(367,919),(367,971),(372,976),(374,982),(370,986),(361,990),(342,990),(332,987),(327,982),(328,976),(332,972),(332,919),(327,915),(325,908),(327,902),(330,900),(327,891),(330,882),(338,876)],fill=255)
for sphere,collar,shaft,foot in [
 ((451,784,482,815),(447,804,486,820),(456,816,479,854),(449,848,487,866)),
 ((509,751,536,778),(507,770,540,785),(514,780,535,817),(507,812,541,829)),
 ((586,716,610,742),(582,736,613,748),(589,743,609,777),(582,772,617,787))]:
 d.ellipse(sphere,fill=255);d.ellipse(collar,fill=255);d.rectangle(shaft,fill=255);d.ellipse(foot,fill=255)
chains=[([(369,905),(387,897),(403,886),(420,870),(437,848),(454,817)],9), ([(482,808),(497,801),(510,788),(513,781)],8), ([(537,775),(551,774),(571,765),(587,749)],6), ([(401,887),(397,898),(398,918)],7), ([(429,853),(426,865),(429,881)],6), ([(496,804),(496,818),(500,834)],6), ([(562,774),(562,787),(564,795)],5), ([(573,767),(573,782),(573,790)],4)]
for points,width in chains:d.line(points,fill=255,width=width,joint='curve')
rough=np.array(mask)>0
region=nd.binary_dilation(rough,iterations=5)
seeds=nd.binary_erosion(rough,iterations=5)
# Thin chains need explicit interior seeds; erosion would erase them entirely.
core=Image.new('L',src.size);cd=ImageDraw.Draw(core)
for points,width in chains:cd.line(points,fill=255,width=1,joint='curve')
seeds |= np.array(core)>0
labels=np.zeros(rough.shape,np.uint8)
labels[region]=cv2.GC_PR_BGD;labels[rough]=cv2.GC_PR_FGD;labels[seeds]=cv2.GC_FGD
# Floor islands between chain and pendants are explicitly background.
for x,y in [(410,887),(416,881),(421,876),(580,780),(582,781),(391,902)]:
 cv2.circle(labels,(x,y),2,cv2.GC_BGD,-1)
cv2.setRNGSeed(0)
cv2.grabCut(a[:,:,:3].copy(),labels,None,np.zeros((1,65),np.float64),np.zeros((1,65),np.float64),8,cv2.GC_INIT_WITH_MASK)
owned=((labels==cv2.GC_FGD)|(labels==cv2.GC_PR_FGD))&(a[:,:,3]>0)
# Reject warm peach floor pixels only inside inspected chain-gap windows.
hsv=cv2.cvtColor(a[:,:,:3],cv2.COLOR_RGB2HSV)
peach=(hsv[:,:,0]<16)&(hsv[:,:,1]<153)&(hsv[:,:,2]>140)
for x0,y0,x1,y1 in [(385,889,400,914),(409,862,429,885),(574,773,584,787)]:
 owned[y0:y1,x0:x1] &= ~peach[y0:y1,x0:x1]
rail=a.copy();rail[~owned]=0
mask=Image.fromarray(owned.astype('uint8')*255)
Image.fromarray(rail).save(P/'front-rail-full.png');mask.save(P/'front-rail-mask.png')
box=(320,710,624,996);Image.fromarray(rail).crop(box).save(D/'bridge_front_rail.png')
bg=Image.new('RGBA',src.size,'#61435a');bg.alpha_composite(Image.fromarray(rail));bg.crop(box).resize((608,572)).convert('RGB').save(P/'front-rail-review.jpg',quality=94)
(P/'FRONT_RAIL.json').write_text(json.dumps({'status':'GrabCut-refined candidate contour inspection required','source_crop':list(box),'output_size':[304,286],'source_pixel_ownership':'mask pixels removed from castle and all contact cels; moved to foreground once','includes':'near-side posts and chain spans only; no broad floor polygon','source_pixels':int(owned.sum())},indent=2)+'\n')
print('FRONT_RAIL|source pixels',int(owned.sum()))
