from PIL import Image, ImageDraw
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png").convert("RGB")
path=[(200,348),(300,362),(420,386),(515,408),(590,440),(615,495),(700,543),(820,545),(940,528),(1095,440)]
stations=[("barn_doors",278,328),("pearl_clam",225,540),("blossom_arch",596,318),("seed_beds",858,487),("hay_bales",1050,280)]
clues=[("A_weathervane",263,90),("B_blossom_tree",490,236),("C_sun",775,188),("D_rock_arch",940,168),
       ("E_kelp",1115,465),("F_tube_coral",180,392),("G_pool_starfish",292,600),("H_barrel_sponge",915,578)]
d=ImageDraw.Draw(f)
d.line(path,fill=(255,0,255),width=3)
for i,(x,y) in enumerate(path):
    d.ellipse([x-5,y-5,x+5,y+5],outline=(255,255,255),width=2,fill=(255,0,255))
for n,x,y in stations:
    d.ellipse([x-10,y-10,x+10,y+10],outline=(0,0,0),width=3,fill=(0,220,0))
    d.text((x+12,y-6),n,fill=(0,0,0))
for n,x,y in clues:
    d.ellipse([x-7,y-7,x+7,y+7],outline=(255,255,255),width=2,fill=(0,60,255))
    d.text((x+9,y-6),n,fill=(255,255,255))
f.save(f"{OUT}/farmer_marked2.png")
f.crop((100,60,700,660)).resize((1200,1200)).save(f"{OUT}/farmer_marked2_L.png")
f.crop((640,60,1180,660)).resize((1080,1200)).save(f"{OUT}/farmer_marked2_R.png")
def rec(x,y): return [round((1.6*x-187)/1672,4), round(y/720,4)]
print("PATH",[rec(*p) for p in path])
print("ST",[[n]+rec(x,y) for n,x,y in stations])
print("CL",[rec(x,y) for n,x,y in clues])
