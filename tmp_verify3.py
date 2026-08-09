from PIL import Image, ImageDraw
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png").convert("RGB")
path=[(200,348),(300,362),(420,386),(590,440),(612,505),(700,545),(830,543),(960,528),(1048,512),(1082,458)]
stations=[("barn_doors",278,328),("pearl_clam",225,540),("blossom_arch",596,318),("seed_beds",858,487),("hay_bales",1050,280)]
clues=[("A_weathervane",263,90),("B_blossom_tree",490,236),("C_sun",762,189),("D_rock_arch",940,168),
       ("E_kelp",1115,465),("F_tube_coral",180,392),("G_pool_starfish",292,600),("H_barrel_sponge",915,578)]
d=ImageDraw.Draw(f)
d.line(path,fill=(255,0,255),width=2)
for x,y in path: d.ellipse([x-4,y-4,x+4,y+4],outline=(255,255,255),width=1,fill=(255,0,255))
for n,x,y in stations:
    d.ellipse([x-9,y-9,x+9,y+9],outline=(0,0,0),width=3,fill=(0,220,0)); d.text((x+11,y-6),n,fill=(0,0,0))
for n,x,y in clues:
    d.ellipse([x-6,y-6,x+6,y+6],outline=(255,255,255),width=2,fill=(0,60,255)); d.text((x+8,y-6),n,fill=(255,255,255))
f.save(f"{OUT}/farmer_marked3.png")
f.crop((580,380,1160,620)).resize((1740,720)).save(f"{OUT}/farmer_marked3_tail.png")
def rec(x,y): return [round((1.6*x-187)/1672,4), round(y/720,4)]
print("PATH",[rec(*p) for p in path])
print("ST",[[n]+rec(x,y) for n,x,y in stations])
print("CL",[rec(x,y) for n,x,y in clues])
