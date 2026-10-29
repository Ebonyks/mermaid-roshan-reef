from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
r=Path.cwd();s=r/'assets_src/imagegen/job_art_boxer_20261019';out=s/'review';out.mkdir(exist_ok=True)
rows=json.loads((s/'review_current02/capture.json').read_text())['captures'];manifest=[]
for start in range(0,len(rows),8):
 sheet=Image.new('RGB',(1280,1560),(42,46,60));d=ImageDraw.Draw(sheet)
 for j,row in enumerate(rows[start:start+8]):
  im=Image.open(r/row['path']).convert('RGB');im.thumbnail((630,350));x=j%2*640;y=j//2*390;sheet.paste(im,(x+(640-im.width)//2,y+30));d.text((x+7,y+7),row['id'],fill='white')
 p=out/f'current02_page_{start//8:02d}.png';assert not p.exists();sheet.save(p);manifest.append({'path':p.relative_to(r).as_posix(),'captures':[x['id'] for x in rows[start:start+8]],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
paths=sorted((r/'assets/opera/worlds/boxer_quality_20261019').glob('*.png'))+sorted((r/'assets/ui').glob('pearl_*.png'))+sorted((r/'assets/opera/worlds/props').glob('fx_invite*.png'))
sheet=Image.new('RGB',(1280,1050),(42,46,60));d=ImageDraw.Draw(sheet)
for i,p in enumerate(paths):
 im=Image.open(p).convert('RGBA');im.thumbnail((300,275));x=i%4*320;y=i//4*350;sheet.paste(im,(x+(320-im.width)//2,y+30),im);d.text((x+5,y+6),p.stem,fill='white')
sheet.save(out/'objects.png');(out/'sheet_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Built',len(manifest),'pages,',len(paths),'source images')
