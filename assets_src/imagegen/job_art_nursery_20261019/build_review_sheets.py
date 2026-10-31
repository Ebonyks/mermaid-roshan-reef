from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
r=Path.cwd();s=r/'assets_src/imagegen/job_art_boxer_20261019';out=Image.new('RGB',(1200,720),(40,44,64));d=ImageDraw.Draw(out)
for i,n in enumerate(['invite_ring','invite_open','pearl_empty','pearl_filling','pearl_full']):
 im=Image.open(s/(n+'_native.png')).convert('RGBA');b=im.getchannel('A').point(lambda a:255 if a>=16 else 0).getbbox();print(n,im.size,b)
 tile=im.copy();tile.thumbnail((380,290));x=i%3*400;y=i//3*360;out.paste(tile,(x+(400-tile.width)//2,y+28+(290-tile.height)//2),tile);d.text((x+8,y+8),n,fill='white')
 if n.startswith('pearl'):
  small=im.copy();small.thumbnail((28,28));out.paste(small,(x+30,y+318),small)
out.save(r/'tmp/boxer_native_candidates.png')
s=r/'assets_src/imagegen/job_art_nursery_20261019';reviews=s/'review';reviews.mkdir(exist_ok=True);o=r/'assets/opera/worlds/nursery_quality_20261019';paths=sorted(o.glob('*.png'))
for start in range(0,len(paths),9):
 sheet=Image.new('RGB',(900,870),(45,48,64));dr=ImageDraw.Draw(sheet)
 for j,p in enumerate(paths[start:start+9]):
  im=Image.open(p).convert('RGBA');im.thumbnail((288,255));x=j%3*300;y=j//3*290;sheet.paste(im,(x+(300-im.width)//2,y+28+(255-im.height)//2),im);dr.text((x+8,y+8),p.stem,fill='white')
 sheet.save(reviews/('objects_'+str(start//9)+'.png'))
records=json.loads((s/'review_current05/capture.json').read_text())['captures']
for start in range(0,len(records),8):
 sheet=Image.new('RGB',(1060,1180),(42,46,60));dr=ImageDraw.Draw(sheet)
 for j,row in enumerate(records[start:start+8]):
  im=Image.open(r/row['path']).convert('RGB');origin=row['surface_canvas_origin'];size=row['surface_size'];box=(int(origin[0])-12,int(origin[1])-12,int(origin[0]+size[0])+12,int(origin[1]+size[1])+48);crop=im.crop(box);crop.thumbnail((420,252));x=j%2*530;y=j//2*295;sheet.paste(crop,(x+4,y+28));mini=im.copy();mini.thumbnail((102,80));sheet.paste(mini,(x+424,y+28));dr.text((x+5,y+5),row['id'],fill='white')
 sheet.save(reviews/('current05_page_'+str(start//8).zfill(2)+'.png'))
print('Built3source and13current-context proof sheets from unaltered source screenshots')
