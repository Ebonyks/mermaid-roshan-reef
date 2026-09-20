from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,binary_erosion,binary_closing,binary_fill_holes,label
import numpy as np,json
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
base=Path(__file__).resolve().parent;out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
im=Image.open(base/'generated-rest-native.png').convert('RGBA');a=np.array(im);h,w=a.shape[:2]
# Curves follow visible painted boundaries. Control points remain editable source data.
paths={
'front_main':[(690,524),((563,480),(415,574),(393,716)),((370,828),(423,935),(465,980)),((607,937),(741,835),(773,724)),((814,617),(754,548),(690,524))],
'front_small_right':[(756,497),((856,483),(963,604),(938,714)),((939,742),(935,758),(931,774)),((842,721),(746,645),(715,552)),((712,527),(729,507),(756,497))],
'left_broad':[(568,463),((481,384),(346,394),(235,457)),((114,526),(75,663),(80,747)),((237,716),(414,709),(487,599)),((531,542),(550,491),(568,463))],
'right_broad':[(877,478),((1031,456),(1232,601),(1253,756)),((1261,798),(1253,831),(1235,843)),((1085,802),(939,730),(877,611)),((842,546),(847,497),(877,478))],
'lower_hanging':[(805,678),((916,734),(1099,941),(993,1077)),((874,1037),(712,939),(721,823)),((728,752),(764,705),(805,678))],
'right_rear_tip':[(940,436),((1100,362),(1357,437),(1336,679)),((1269,653),(1152,585),(1077,544)),((1010,503),(954,468),(940,436))]
}
def polygon(seq):
 pts=[seq[0]];start=np.array(seq[0],float)
 for p1,p2,p3 in seq[1:]:
  p1,p2,p3=map(lambda p:np.array(p,float),(p1,p2,p3))
  for t in np.linspace(0,1,50)[1:]:pts.append(tuple((1-t)**3*start+3*(1-t)**2*t*p1+3*(1-t)*t*t*p2+t**3*p3))
  start=p3
 return pts
owned=np.zeros((h,w),bool);layers=[]
# Front-to-back ownership, including compact stem/bud cluster.
hsv=np.array(im.convert('HSV'));purple=(hsv[:,:,0]>128)&(hsv[:,:,0]<205)&(a[:,:,3]>0)
y,x=np.indices((h,w));purple&=(x>450)&(x<910)&(y<535)
# Painted green stem core stays part of bud assembly; roots are later locked by motion pivot.
stem=Image.new('1',im.size);ImageDraw.Draw(stem).polygon([(636,344),(694,338),(737,415),(723,487),(690,542),(659,518),(654,450)],fill=1)
purple=binary_fill_holes(binary_closing(purple,iterations=3)); lab,nlab=label(purple); counts=np.bincount(lab.ravel()); purple=(counts[lab]>140)&(lab>0)
bud=purple|np.asarray(stem);regions=[('bud_cluster',bud)]
for n,path in paths.items():
 m=Image.new('1',im.size);ImageDraw.Draw(m).polygon(polygon(path),fill=1);regions.append((n,np.asarray(m)))
for n,m in regions:
 m=m&~owned&(a[:,:,3]>0);owned|=m;layers.append((n,m))
remaining=(a[:,:,3]>0)&~owned
# Assign low outer-contour residuals to their nearest actual leaf, not the rear fan.
low=remaining&(y>545)
labels=np.zeros((h,w),np.int16)
for k,(n,m) in enumerate(layers[1:],start=1):labels[m]=k
_,nearest=distance_transform_edt(labels==0,return_indices=True)
nearest_label=labels[nearest[0],nearest[1]]
for k in range(1,len(layers)):
 n,m=layers[k];layers[k]=(n,m|(low&(nearest_label==k)))
remaining&=~low
layers.append(('back_leaf_fan',remaining))
# Extend every owned region by 24 native pixels behind neighbours, but never beyond
# the original outside silhouette. This is concealed color extension, not new anatomy.
front_owned=np.zeros((h,w),bool)
for n,m in layers:
 dist,inds=distance_transform_edt(~m,return_indices=True);ext=(dist<=24)&(a[:,:,3]>0);pix=np.zeros_like(a);pix[m]=a[m];extra=ext&~m&front_owned;pix[extra]=a[inds[0][extra],inds[1][extra]];pix[extra,3]=a[extra,3]
 Image.fromarray(pix).save(out/(n+'.png'));front_owned|=m
 Image.fromarray((m*255).astype('uint8')).save(out/(n+'-ownership.png'))
# Forward layer ordering restores original visible ownership.
rest=Image.new('RGBA',im.size)
for n,m in reversed(layers):rest=Image.alpha_composite(rest,Image.open(out/(n+'.png')))
rest.save(out/'rest-overlaps.png')
board=Image.new('RGB',(1200,640),(47,58,70));draw=ImageDraw.Draw(board)
for k,(n,m) in enumerate(layers):
 tile=Image.open(out/(n+'.png'));tile.thumbnail((290,270));px=(k%4)*300+(300-tile.width)//2;py=(k//4)*320+35;board.paste(tile,(px,py),tile);draw.text(((k%4)*300+8,(k//4)*320+8),n,fill='white')
board.save(out/'leaf-ownership-review.jpg',quality=94)
(out/'LAYERS.json').write_text(json.dumps({'layers_front_to_back':[n for n,m in layers],'size':[w,h],'pivot':[690,530],'curves':paths,'overlap_extension_native_px':24,'status':'MASK_AND_OVERLAP_STUDY_NOT_ACCEPTED'},indent=2)+'\n',encoding='utf-8')
print(out)
