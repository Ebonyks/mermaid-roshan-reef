from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1]
for theme in ['ballet','magician']:
 rows=[]
 for clip in ['arm_bend','blink','tail_bend']:
  rows += [(clip,p) for p in sorted((R/f'evidence/render_{theme}_v8'/clip).glob('*.png'))]
 folder=R/'review'/theme;folder.mkdir(exist_ok=True)
 for start in range(0,len(rows),24):
  board=Image.new('RGB',(1440,1376),(32,38,48));draw=ImageDraw.Draw(board)
  for j,(clip,p) in enumerate(rows[start:start+24]):
   tile=Image.new('RGBA',(1024,1024),(244,244,244,255) if j%2==0 else (12,16,24,255));tile.alpha_composite(Image.open(p).convert('RGBA'))
   x=(j%6)*240;y=(j//6)*344
   board.paste(tile.crop((425,315,665,525)).convert('RGB'),(x,y))
   board.paste(tile.crop((390,735,670,855)).convert('RGB').resize((240,103)),(x,y+210))
   draw.text((x+3,y+316),f'{clip} {int(p.stem):04}',fill='white')
  board.save(folder/f'clothing_every_frame_{start:03}.jpg',quality=97)
 print(theme,len(rows),'frames',flush=True)
