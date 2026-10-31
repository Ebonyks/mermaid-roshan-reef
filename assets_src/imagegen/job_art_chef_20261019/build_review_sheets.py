"""Inspection sheets only; delivery artwork and original pixels are untouched."""
from pathlib import Path
import hashlib,json,math
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[3]
src=Path(__file__).resolve().parent
out=src/'review'
out.mkdir(exist_ok=True)
paths=sorted((root/'assets/opera/worlds/chef_quality_20261019').glob('*.png'))
paths.append(root/'assets/opera/worlds/widgets/widget_target_chef_piece_2.png')
rows=[]
for page in range(math.ceil(len(paths)/12)):
    sheet=Image.new('RGB',(1024,840),(44,38,50));draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(paths[page*12:page*12+12]):
        x=(i%4)*256;y=(i//4)*280
        image=Image.open(p).convert('RGBA');image.thumbnail((240,240),Image.Resampling.LANCZOS)
        sheet.paste(image,(x+(256-image.width)//2,y+(248-image.height)//2),image)
        draw.text((x+8,y+252),p.stem,fill='white')
        rows.append({'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sheet':page+1})
    sheet.save(out/('objects_%02d.png'%(page+1)))
for folder in ['review_current_06','review_chapter2_05']:
    paths=sorted((src/folder).glob('*.png'))
    for page in range(math.ceil(len(paths)/9)):
        sheet=Image.new('RGB',(1920,1152),(30,26,36));draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(paths[page*9:page*9+9]):
            image=Image.open(p).convert('RGB');image.thumbnail((640,360),Image.Resampling.LANCZOS)
            x=(i%3)*640;y=(i//3)*384
            sheet.paste(image,(x,y));draw.text((x+8,y+363),p.stem,fill='white')
        sheet.save(out/('%s_%02d.png'%(folder,page+1)))
(out/'sheet_sources.json').write_text(json.dumps({'purpose':'QA inspection arrangement/crops only; no delivery pixels authored or changed','object_inputs':rows,'all_current_source_frames':'review_current_06 plus review_chapter2_05; full PNGs and native-source/runtime/save isolation receipts retained'},indent=2)+'\n')
print('Prepared22object and88current-frame inspection bindings; originals unchanged')
