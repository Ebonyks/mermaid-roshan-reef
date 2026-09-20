from pathlib import Path
from PIL import Image
import numpy as np,cv2
from scipy import ndimage as nd
p=Path('assets_src/sky_lagoon/animated_rebuild_v1_2026-09-20/whole_scene_revision/tree'); im=Image.open('assets_src/sky_lagoon/masters/sky_lagoon_panorama_master_v5_hd_3x1.png').convert('RGB').crop((0,0,400,1152)); a=np.array(im); hsv=cv2.cvtColor(a,cv2.COLOR_RGB2HSV)
y,x=np.indices(a.shape[:2]); permitted=(y<850)|((x<215)&(y<940))|((x<185)&(y<1010))|((x<155)&(y<1110))
seed=np.full(y.shape,cv2.GC_PR_BGD,np.uint8); seed[(hsv[:,:,0]<90)&(hsv[:,:,1]>75)&permitted]=cv2.GC_PR_FGD
seed[(hsv[:,:,0]<65)&(hsv[:,:,1]>100)&permitted]=cv2.GC_FGD
seed[~permitted]=cv2.GC_BGD;seed[:40]=cv2.GC_BGD;seed[:,365:]=cv2.GC_BGD
cv2.setRNGSeed(0);cv2.grabCut(a,seed,None,np.zeros((1,65)),np.zeros((1,65)),6,cv2.GC_INIT_WITH_MASK)
m=(seed==cv2.GC_FGD)|(seed==cv2.GC_PR_FGD);labs,n=nd.label(m); sizes=np.bincount(labs.ravel());sizes[0]=0;m=labs==sizes.argmax()
m[((y>835)&(x>155)&(hsv[:,:,0]>32))|((y>920)&(x<78)&(hsv[:,:,0]>32))]=False
card=Image.fromarray(np.dstack([a,m.astype('uint8')*255]));card.save(p/'native-whole-tree-cutout.png');white=Image.new('RGBA',card.size,'#dddddd');white.alpha_composite(card);white.save(p/'native-whole-tree-mask-review.png')
