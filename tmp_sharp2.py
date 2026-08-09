from PIL import Image
import numpy as np
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
m=np.asarray(Image.open(f"{OUT}/farmer_master.png").convert("L"),dtype=float)
sub2=m[:,300:1700]
d2r=np.abs(np.diff(sub2,2,axis=0)).mean(axis=1)
for y in range(0,2048,32):
    print(y, round(d2r[min(y,len(d2r)-1)],3))
