from pathlib import Path
from PIL import Image,ImageDraw
V=Path(__file__).resolve().parent;O=V/'review_sheets';O.mkdir(exist_ok=True)
groups=[[0,1,2],list(range(3,9)),list(range(9,15)),list(range(15,21)),list(range(21,27)),list(range(27,33)),[33]]
for j,group in enumerate(groups,1):
 rows=2 if j==1 else (len(group)+1)//2;sheet=Image.new('RGB',(1512,rows*570),(239,243,245));d=ImageDraw.Draw(sheet)
 for k,n in enumerate(group):
  w=1512 if n==2 else 756;x=0 if n==2 else (k%2)*756;y=570 if n==2 else (k//2)*570
  p=Image.open(V/f'complete/page_{n:02}.png');p.thumbnail((w,540));sheet.paste(p,(x,y+30));d.text((x+8,y+6),f'PDF entry {n}',fill=(10,25,45))
 sheet.save(O/f'sheet_{j:02}.png')
print('Seven actual-proof review sheets refreshed.')
