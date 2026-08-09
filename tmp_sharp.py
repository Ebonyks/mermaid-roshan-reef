from PIL import Image
import numpy as np
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
m=np.asarray(Image.open(f"{OUT}/farmer_master.png").convert("L"),dtype=float)
# column energy over rows 448..1600
sub=m[448:1600,:]
d2=np.abs(np.diff(sub,2,axis=1)).mean(axis=0)
th=d2.max()*0.15
idx=np.where(d2>th)[0]
print("cols sharp",idx.min(),idx.max(), idx.min()/2048, idx.max()/2048)
# row energy over cols 187..1859
sub2=m[:,187:1859]
d2r=np.abs(np.diff(sub2,2,axis=0)).mean(axis=1)
thr=d2r.max()*0.15
idxr=np.where(d2r>thr)[0]
print("rows sharp",idxr.min(),idxr.max())
