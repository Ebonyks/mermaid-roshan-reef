from PIL import Image, ImageDraw
OUT=r"C:/Users/Peter/AppData/Local/Temp/claude/C--Users-Peter-Documents-mermaid-roshan-reef/a592cfd2-f199-49d3-be53-e7bb8067670e/scratchpad"
f=Image.open(f"{OUT}/farmer_frame.png").convert("RGB")
path=[(200,348),(300,362),(420,386),(515,408),(590,440),(615,495),(700,543),(820,545),(940,528),(1095,440)]
stations=[("barn_doors",278,325),("pearl_clam",250,528),("blossom_arch",596,318),("seed_beds",858,487),("hay_bales",1058,300)]
clues=[("A_weathervane",263,90),("B_blossom_tree",490,236),("C_sun",787,186),("D_rock_arch",940,168),
       ("E_bale_starfish",1082,287),("F_tube_coral",180,392),("G_pool_starfish",360,600),("H_urn_coral",873,570)]
d=ImageDraw.Draw(f)
d.line(path,fill=(255,0,255),width=3)
for i,(x,y) in enumerate(path):
    d.ellipse([x-6,y-6,x+6,y+6],outline=(255,255,255),width=2,fill=(255,0,255))
    d.text((x+8,y-16),f"p{i+1}",fill=(255,255,255))
for n,x,y in stations:
    d.ellipse([x-11,y-11,x+11,y+11],outline=(0,0,0),width=3,fill=(0,200,0))
    d.text((x+13,y-6),n,fill=(0,0,0))
for n,x,y in clues:
    d.ellipse([x-8,y-8,x+8,y+8],outline=(255,255,255),width=2,fill=(0,60,255))
    d.text((x+10,y-6),n,fill=(255,255,255))
f.save(f"{OUT}/farmer_marked.png")
def rec(x,y): return (round((1.6*x-187)/1672,4), round(y/720,4))
print("PATH",[rec(*p) for p in path])
print("STATIONS",[(n,)+rec(x,y) for n,x,y in stations])
print("CLUES",[(n,)+rec(x,y) for n,x,y in clues])
