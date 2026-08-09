from PIL import Image
import os
B="assets/opera/worlds/backdrops"
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
os.makedirs(OUT,exist_ok=True)
m=Image.new("RGB",(2048,2048))
for c in (0,1):
    for r in (0,1):
        t=Image.open(f"{B}/world_farmer_c{c}r{r}.png").convert("RGB")
        print(c,r,t.size)
        m.paste(t,(c*1024,r*1024))
m.save(f"{OUT}/farmer_master.png")
f=m.crop((0,448,2048,1600)).resize((1280,720),Image.LANCZOS)
f.save(f"{OUT}/farmer_frame.png")
print("ok")
