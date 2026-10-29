from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
r=Path.cwd();s=r/'assets_src/imagegen/job_art_support_careers_20261019';out=s/'review_objects02';assert not out.exists();out.mkdir()
rows=json.loads((s/'runtime_provenance04.json').read_text())['records'];pages=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for start in range(0,len(rows),8):
 sheet=Image.new('RGB',(1536,820),'#827b85');draw=ImageDraw.Draw(sheet);subset=rows[start:start+8]
 for i,row in enumerate(subset):
  x=(i%4)*384;y=(i//4)*410
  for yy in range(0,370,20):
   for xx in range(0,384,20):draw.rectangle((x+xx,y+yy,x+xx+19,y+yy+19),fill=('#d7cfc9' if (xx//20+yy//20)%2 else '#a6a0a5'))
  im=Image.open(r/row['path']).convert('RGBA');im.thumbnail((354,354));sheet.paste(im,(x+(384-im.width)//2,y+(370-im.height)//2),im)
  draw.text((x+5,y+374),Path(row['path']).name,fill='white')
  draw.text((x+5,y+390),str(row['dimensions'])+' '+row['sha256'][:16],fill='white')
 p=out/('objects_%02d.png'%(len(pages)+1));sheet.save(p);pages.append({'path':p.relative_to(r).as_posix(),'sha256':sha(p),'objects':[x['path'] for x in subset]})
(out/'manifest.json').write_text(json.dumps({'role':'diagnostic_only','review_status':'NOT_YET_REVIEWED','pages':pages},indent=2)+'\n',encoding='utf-8');print(len(rows),'objects',len(pages),'pages')
