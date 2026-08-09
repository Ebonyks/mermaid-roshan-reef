from PIL import Image, ImageDraw
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png")
# grid overlay version
g=f.copy(); d=ImageDraw.Draw(g)
for x in range(0,1280,64):
    d.line([(x,0),(x,720)],fill=(0,255,0) if x%128 else (255,0,0),width=1)
    d.text((x+2,2),str(x),fill=(0,0,0))
for y in range(0,720,60):
    d.line([(0,y),(1280,y)],fill=(0,255,0),width=1)
    d.text((2,y+2),str(y),fill=(0,0,0))
g.save(f"{OUT}/farmer_grid.png")
for name,box in [("L",(0,0,470,720)),("M",(420,0,880,720)),("R",(820,0,1280,720))]:
    c=g.crop(box).resize(((box[2]-box[0])*2,720*2),Image.LANCZOS)
    c.save(f"{OUT}/farmer_{name}.png")
print("ok")
