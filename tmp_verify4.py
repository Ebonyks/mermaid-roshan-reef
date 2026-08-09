from PIL import Image, ImageDraw
import math
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png").convert("RGB")
path=[(200,348),(300,362),(420,386),(590,440),(612,505),(700,545),(830,543),(960,528),(1055,525),(1082,458)]
stations=[("barn_doors",278,328),("pearl_clam",225,540),("blossom_arch",596,318),("seed_beds",858,487),("hay_bales",1050,280)]
clues=[("A",263,90),("B",490,236),("C",762,189),("D",940,168),("E",1122,472),("F",180,392),("G",292,600),("H",915,578)]
segs=[math.dist(path[i],path[i+1]) for i in range(len(path)-1)]
tot=sum(segs)
def at(t):
    d=t*tot; acc=0
    for i,s in enumerate(segs):
        if acc+s>=d:
            u=(d-acc)/s
            return (path[i][0]+(path[i+1][0]-path[i][0])*u, path[i][1]+(path[i+1][1]-path[i][1])*u)
        acc+=s
    return path[-1]
print("t=0.12",at(0.12),"t=0.86",at(0.86))
d=ImageDraw.Draw(f)
d.line(path,fill=(255,0,255),width=2)
for x,y in path: d.ellipse([x-4,y-4,x+4,y+4],outline=(255,255,255),width=1,fill=(255,0,255))
for t,c in ((0.12,(255,140,0)),(0.86,(255,140,0))):
    x,y=at(t); d.ellipse([x-7,y-7,x+7,y+7],outline=(0,0,0),width=2,fill=c); d.text((x+9,y-6),f"t{t}",fill=(0,0,0))
for n,x,y in stations:
    d.ellipse([x-9,y-9,x+9,y+9],outline=(0,0,0),width=3,fill=(0,220,0)); d.text((x+11,y-6),n,fill=(0,0,0))
for n,x,y in clues:
    d.ellipse([x-6,y-6,x+6,y+6],outline=(255,255,255),width=2,fill=(0,60,255)); d.text((x+8,y-6),n,fill=(255,255,255))
f.save(f"{OUT}/farmer_marked4.png")
f.crop((950,400,1170,560)).resize((880,640)).save(f"{OUT}/farmer_marked4_tail.png")
def rec(x,y): return [round((1.6*x-187)/1672,4), round(y/720,4)]
print("PATH",[rec(*p) for p in path])
print("ST",[[n]+rec(x,y) for n,x,y in stations])
print("CL",[rec(x,y) for n,x,y in clues])
