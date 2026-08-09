from PIL import Image, ImageDraw
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png").convert("RGB")
d=ImageDraw.Draw(f)
for n,x,y in [("C",770,188),("E",1132,470),("p9",1060,520)]:
    d.ellipse([x-6,y-6,x+6,y+6],outline=(255,255,255),width=2,fill=(0,60,255)); d.text((x+8,y-6),n,fill=(255,255,255))
f.crop((700,140,860,240)).resize((640,400)).save(f"{OUT}/chk_sun.png")
f.crop((1020,420,1170,560)).resize((600,560)).save(f"{OUT}/chk_kelp.png")
