from pathlib import Path
from PIL import Image,ImageDraw
from scipy import ndimage as nd
import numpy as np,json,hashlib,shutil
P=Path(__file__).resolve().parent/'huckleberry';W=Path(__file__).resolve().parents[3];atlas=Image.open(P/'huckleberry-atlas.png').convert('RGBA');assert atlas.size==(2048,1024)
frames=[];report=[];board=Image.new('RGB',(1024,400),'#dce3e8');draw=ImageDraw.Draw(board)
for n in range(8):
 f=atlas.crop(((n%4)*512,(n//4)*512,(n%4+1)*512,(n//4+1)*512));a=np.array(f);frames.append(a);lab,c=nd.label(a[:,:,3]>64);sizes=np.bincount(lab.ravel())[1:];assert sizes.max()==sizes.sum(),'detached plant fragment'
 berry=(a[:,:,0].astype(float)>a[:,:,1]*1.15)&(a[:,:,2].astype(float)>a[:,:,1]*1.35)&(a[:,:,3]>100)&(a[:,:,0]>65)
 lab,c=nd.label(nd.binary_dilation(berry,iterations=3));sz=np.bincount(lab.ravel());clusters=int(((sz>45)&(np.arange(len(sz))>0)).sum());assert clusters==5
 assert np.array_equal(a[375:],frames[0][375:]),'root drift'
 report.append({'frame':n,'sha256':hashlib.sha256(a.tobytes()).hexdigest(),'connected_fraction':1.0,'berry_clusters':clusters,'fixed_root':True})
 crop=f.crop((0,110,512,415)).resize((256,153));pos=((n%4)*256,(n//4)*200+24);board.paste(crop,pos,crop);draw.text((pos[0]+6,pos[1]-17),f'Pose {n+1}',fill='#203040')
assert len({r['sha256'] for r in report})==8
rest=np.array(Image.open(P/'rest-prepared.png'));assert np.array_equal(frames[0][:,:,3],rest[:,:,3]) and np.array_equal(frames[0][rest[:,:,3]>0],rest[rest[:,:,3]>0]),'visible rest does not match source'
board.save(P/'eight-cel-review.jpg',quality=95)
(P/'ANIMATION_REVIEW.json').write_text(json.dumps({'frames':report,'root_anchor':[256,380],'fixed_rows':[375,512],'durations_ms':[300,240,300,300,320,240,300,300],'method':'direct Aseprite source sampling with three smooth branch influence regions, no whole-card transform; fixed root','limits':'regional source layers are not complete independently extracted branches; visual/device temporal acceptance pending'},indent=2)+'\n')
shutil.copyfile(P/'huckleberry-atlas.png',W/'assets/sprites/sky_lagoon/animated_v1/huckleberry_breeze.png');print('HUCKLEBERRY|8 distinct connected cels; 5 berry groups; exact fixed root|PASS')
