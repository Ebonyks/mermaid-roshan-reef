from PIL import Image, ImageDraw
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png")
def zoom(name,x0,y0,x1,y1,scale=4,step=10):
    c=f.crop((x0,y0,x1,y1)).resize(((x1-x0)*scale,(y1-y0)*scale),Image.LANCZOS)
    d=ImageDraw.Draw(c)
    for x in range(x0-(x0%step)+step,x1,step):
        cx=(x-x0)*scale; d.line([(cx,0),(cx,(y1-y0)*scale)],fill=(0,255,0)); d.text((cx+2,2),str(x),fill=(0,0,0))
    for y in range(y0-(y0%step)+step,y1,step):
        cy=(y-y0)*scale; d.line([(0,cy),((x1-x0)*scale,cy)],fill=(0,255,0)); d.text((2,cy+2),str(y),fill=(0,0,0))
    c.save(f"{OUT}/z2_{name}.png")
zoom("bale",1000,240,1160,340)
zoom("poolstar",320,560,440,640)
zoom("urn",820,530,960,620)
zoom("sun",740,150,860,230)
zoom("clam",190,490,320,580)
zoom("star2",250,565,350,635)
