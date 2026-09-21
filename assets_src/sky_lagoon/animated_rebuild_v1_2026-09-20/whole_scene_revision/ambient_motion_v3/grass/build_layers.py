from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt
import numpy as np,json
w=Path.cwd();p=w/'tmp/sky-lagoon-whole-scene-v2/grass-pointed-trial';o=p/'blade-layers';o.mkdir(exist_ok=True)
a=np.array(Image.open(p/'rest-graded.png').convert('RGBA'));a[:,:,3][a[:,:,3]>=250]=255;a[a[:,:,3]<=2]=0;im=Image.fromarray(a);im.save(o/'normalized-source.png');h,ww=a.shape[:2];yy,xx=np.indices((h,ww))
polys={'left_mid': [(173, 565), (295, 518), (422, 563), (551, 689), (645, 882), (452, 909), (335, 838), (242, 718)], 'right_mid': [(967, 886), (1060, 740), (1196, 610), (1369, 525), (1428, 558), (1323, 720), (1219, 869), (1099, 906)], 'left_upper': [(378, 407), (457, 399), (579, 472), (676, 611), (765, 779), (802, 918), (649, 882), (560, 752), (475, 587)], 'right_upper': [(803, 918), (882, 723), (1010, 545), (1174, 390), (1165, 522), (1113, 697), (989, 849), (952, 889)], 'center': [(635, 556), (680, 423), (773, 264), (845, 322), (907, 435), (958, 553), (920, 674), (801, 917), (746, 759)], 'left_outer': [(55, 776), (137, 700), (259, 679), (338, 728), (451, 889), (337, 929), (196, 886), (111, 818)], 'right_outer': [(1127, 902), (1223, 787), (1301, 721), (1373, 710), (1467, 751), (1532, 820), (1397, 858), (1275, 918)]}
regions=[('roots_fixed',(yy>=875)&(a[:,:,3]>0))]
for n,pts in polys.items():
 mask=Image.new('1',(ww,h));ImageDraw.Draw(mask).polygon(pts,fill=1);regions.append((n,np.asarray(mask)))
owned=np.zeros((h,ww),bool);layers=[];labels=np.zeros((h,ww),np.int16)
for i,(n,m) in enumerate(regions):
 m=m&~owned&(a[:,:,3]>0);owned|=m;layers.append((n,m));labels[m]=i+1
_,idx=distance_transform_edt(labels==0,return_indices=True);near=labels[idx[0],idx[1]];remaining=(a[:,:,3]>0)&~owned
layers=[(n,m|(remaining&(near==i+1))) for i,(n,m) in enumerate(layers)]
front=np.zeros((h,ww),bool);rest=Image.new('RGBA',(ww,h));parts={}
for n,m in layers:
 dist,ix=distance_transform_edt(~m,return_indices=True);extra=(dist<=18)&~m&front&(a[:,:,3]==255);part=np.zeros_like(a);part[m]=a[m];part[extra]=a[ix[0][extra],ix[1][extra]];part[extra,3]=255;front|=m;parts[n]=Image.fromarray(part);parts[n].save(o/(n+'.png'));parts[n].resize((640,426),Image.Resampling.LANCZOS).save(o/(n+'-working.png'))
for n,m in reversed(layers):rest=Image.alpha_composite(rest,parts[n])
err=np.abs(np.asarray(rest).astype(int)-a.astype(int));assert err.max()==0,int(err.max())
board=Image.new('RGB',(1200,480),'#334536');d=ImageDraw.Draw(board)
for i,(n,m) in enumerate(layers):
 thumb=parts[n].copy();thumb.thumbnail((290,205));pos=(i%4*300,i//4*240+25);board.paste(thumb,pos,thumb);d.text((pos[0]+5,pos[1]-17),n,fill='white')
board.save(o/'ownership.jpg',quality=95)
(o/'LAYERS.json').write_text(json.dumps({'status':'CONTOUR_STUDY_NOT_ACCEPTED','layers_front_to_back':[n for n,m in layers],'rest_rgba_error':int(err.max()),'alpha_normalization':'body alpha>=250 to255; alpha<=2 tozero; native source retained','concealed_extension_px':18,'polygons':polys,'working_size':[640,426]},indent=2)+'\n',encoding='utf-8')
print('GRASS_LAYERS|8 layers, normalized rest RGBA exact|PASS')
