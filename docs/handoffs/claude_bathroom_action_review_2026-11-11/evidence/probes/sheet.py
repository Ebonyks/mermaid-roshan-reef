import sys
from PIL import Image, ImageDraw
# usage: sheet.py out.jpg x0 y0 x1 y1 cols scale frame...
src=sys.argv[1]; out=sys.argv[2]; x0,y0,x1,y1=map(int,sys.argv[3:7]); cols=int(sys.argv[7]); sc=float(sys.argv[8]); frames=[int(f) for f in sys.argv[9:]]
w,h=int((x1-x0)*sc),int((y1-y0)*sc)
rows=(len(frames)+cols-1)//cols
sheet=Image.new('RGB',(cols*w,rows*(h+16)),(20,20,30))
d=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
    im=Image.open(f'{src}/f{f+1:04d}.jpg').crop((x0,y0,x1,y1)).resize((w,h))
    c,r=i%cols,i//cols
    sheet.paste(im,(c*w,r*(h+16)+16))
    d.text((c*w+4,r*(h+16)+2),f'#{f} {f/30:.2f}s',fill=(255,255,200))
sheet.save(out,quality=88)
