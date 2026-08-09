from PIL import Image, ImageDraw
import sys
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png")
def zoom(name,x0,y0,x1,y1,scale=3,step=20):
    c=f.crop((x0,y0,x1,y1)).resize(((x1-x0)*scale,(y1-y0)*scale),Image.LANCZOS)
    d=ImageDraw.Draw(c)
    for x in range(x0-(x0%step)+step,x1,step):
        cx=(x-x0)*scale
        d.line([(cx,0),(cx,(y1-y0)*scale)],fill=(0,255,0),width=1)
        d.text((cx+2,2),str(x),fill=(0,0,0))
    for y in range(y0-(y0%step)+step,y1,step):
        cy=(y-y0)*scale
        d.line([(0,cy),((x1-x0)*scale,cy)],fill=(0,255,0),width=1)
        d.text((2,cy+2),str(y),fill=(0,0,0))
    c.save(f"{OUT}/z_{name}.png")
zoom("botleft",110,300,440,660,3,20)
zoom("plots",640,330,1060,540,3,20)
zoom("front",600,480,1160,650,2,20)
zoom("right",900,300,1170,560,3,20)
zoom("tail",930,420,1160,600,4,10)
