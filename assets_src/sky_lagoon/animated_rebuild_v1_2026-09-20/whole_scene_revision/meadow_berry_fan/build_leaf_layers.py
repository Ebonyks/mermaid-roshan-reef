from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,binary_erosion,binary_closing,binary_fill_holes,label
import numpy as np,json
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
base=Path(__file__).resolve().parent;out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
im=Image.open(base/'berry-fan-rest-native.png').convert('RGBA');a=np.array(im);h,w=a.shape[:2]
# Curves follow visible painted boundaries. Control points remain editable source data.
paths={'front_main': [(654, 640), ((520, 645), (365, 761), (332, 963)), ((324, 1010), (351, 1062), (367, 1074)), ((541, 1010), (641, 909), (687, 776)), ((709, 707), (686, 662), (654, 640))], 'small_front_pair': [(665, 645), ((710, 602), (792, 651), (788, 726)), ((781, 785), (748, 835), (741, 854)), ((709, 816), (697, 789), (685, 760)), ((676, 795), (670, 816), (668, 826)), ((623, 774), (612, 686), (665, 645))], 'left_broad': [(546, 613), ((416, 524), (242, 589), (141, 682)), ((99, 735), (76, 824), (76, 871)), ((250, 821), (437, 790), (526, 684)), ((546, 661), (552, 635), (546, 613))], 'right_broad': [(783, 635), ((901, 629), (1046, 731), (1097, 858)), ((1125, 903), (1110, 959), (1098, 974)), ((946, 898), (846, 819), (800, 729)), ((780, 692), (768, 657), (783, 635))], 'right_rear_tip': [(932, 568), ((1102, 526), (1375, 593), (1381, 848)), ((1241, 788), (1090, 750), (993, 667)), ((960, 632), (937, 596), (932, 568))]}
def polygon(seq):
 pts=[seq[0]];start=np.array(seq[0],float)
 for p1,p2,p3 in seq[1:]:
  p1,p2,p3=map(lambda p:np.array(p,float),(p1,p2,p3))
  for t in np.linspace(0,1,50)[1:]:pts.append(tuple((1-t)**3*start+3*(1-t)**2*t*p1+3*(1-t)*t*t*p2+t**3*p3))
  start=p3
 return pts
owned=np.zeros((h,w),bool);layers=[]
# Front-to-back ownership, including compact stem/bud cluster.
hsv=np.array(im.convert('HSV'));purple=(hsv[:,:,0]>128)&(hsv[:,:,0]<250)&(a[:,:,3]>0)
y,x=np.indices((h,w));purple&=(x>450)&(x<1000)&(y<710)
# Painted green stem core stays part of bud assembly; roots are later locked by motion pivot.
stem=Image.new('1',im.size);ImageDraw.Draw(stem).polygon([(563,393),(623,426),(711,369),(716,456),(852,390),(879,425),(827,470),(900,526),(832,571),(767,614),(709,663),(646,650),(588,590),(528,541),(570,515),(613,528),(609,477)],fill=1)
purple=binary_fill_holes(binary_closing(purple,iterations=3)); lab,nlab=label(purple); counts=np.bincount(lab.ravel()); purple=(counts[lab]>140)&(lab>0)
bud=purple|np.asarray(stem)
sprig=Image.new('1',im.size);ImageDraw.Draw(sprig).polygon([(620,10),(660,15),(683,110),(730,151),(745,240),(773,157),(828,166),(829,230),(776,286),(750,323),(699,353),(669,414),(661,485),(626,476),(615,352),(558,339),(504,293),(513,250),(557,250),(543,200),(544,168),(586,186),(567,143),(572,111),(610,118),(604,75)],fill=1)
regions=[('bud_cluster',bud),('sprigs',np.asarray(sprig)|((x>500)&(x<840)&(y<310)))]
for n,path in paths.items():
 m=Image.new('1',im.size);ImageDraw.Draw(m).polygon(polygon(path),fill=1);regions.append((n,np.asarray(m)))
for n,m in regions:
 m=m&~owned&(a[:,:,3]>0);owned|=m;layers.append((n,m))
remaining=(a[:,:,3]>0)&~owned
# Assign low outer-contour residuals to their nearest actual leaf, not the rear fan.
low=remaining&(y>610)
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
board=Image.new('RGB',(1200,960),(47,58,70));draw=ImageDraw.Draw(board)
for k,(n,m) in enumerate(layers):
 tile=Image.open(out/(n+'.png'));tile.thumbnail((290,270));px=(k%4)*300+(300-tile.width)//2;py=(k//4)*320+35;board.paste(tile,(px,py),tile);draw.text(((k%4)*300+8,(k//4)*320+8),n,fill='white')
board.save(out/'leaf-ownership-review.jpg',quality=94)
(out/'LAYERS.json').write_text(json.dumps({'layers_front_to_back':[n for n,m in layers],'size':[w,h],'pivot':[688,635],'curves':paths,'overlap_extension_native_px':24,'status':'MASK_AND_OVERLAP_STUDY_NOT_ACCEPTED'},indent=2)+'\n',encoding='utf-8')
print(out)
