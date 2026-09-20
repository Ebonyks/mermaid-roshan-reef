from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,shutil
P=Path(__file__).resolve().parent/'conifer';W=Path(__file__).resolve().parents[3];atlas=Image.open(P/'conifer-atlas.png').convert('RGBA');assert atlas.size==(768,768);rest=np.array(Image.open(P/'rest-prepared.png'));yy,xx=np.indices((384,256));fixed=(yy>=240)|(abs(xx-128)<=12);rows=[];board=Image.new('RGB',(768,430),'#383f55');draw=ImageDraw.Draw(board)
for n in range(6):
 f=atlas.crop(((n%3)*256,(n//3)*384,(n%3+1)*256,(n//3+1)*384));a=np.array(f);assert np.array_equal(a[fixed,3],rest[fixed,3]);v=fixed&(rest[:,:,3]>0);assert np.array_equal(a[v],rest[v]);rows.append({'frame':n,'sha256':hashlib.sha256(a.tobytes()).hexdigest(),'root_and_trunk_exact':True})
 small=f.resize((128,192));pos=(n*128,24);board.paste(small,pos,small);draw.text((pos[0]+5,7),str(n+1),fill='white')
assert len({r['sha256'] for r in rows})==6
board.crop((0,0,768,222)).save(P/'six-cel-review.jpg',quality=95)
(P/'ANIMATION_REVIEW.json').write_text(json.dumps({'frames':rows,'cell_size':[256,384],'atlas_size':[768,768],'frame_ms':360,'fixed_root_and_trunk':True,'status':'candidate; runtime and temporal/device acceptance pending'},indent=2)+'\n');shutil.copyfile(P/'conifer-atlas.png',W/'assets/sprites/sky_lagoon/animated_v1/conifer_breeze.png');print('CONIFER|six distinct frames; exact fixed trunk and base|PASS')
