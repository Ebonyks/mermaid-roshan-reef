local master = Sprite(512,512,ColorMode.RGB)
master.layers[1].name="Shared fin view keys"
do
local source = Image{fromFile="C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/shared-roshan-skin-swim-20261101/assets_src/animation/roshan_shared_swim_20261101/textures/anatomy/fin_broad.png"}
local image = Image(512,512,ColorMode.RGB)
image:drawImage(source,Point(57,133))
image:saveAs("C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/shared-roshan-skin-swim-20261101/assets_src/animation/roshan_shared_swim_20261101/textures/anatomy/fin_broad_registered.png")

master:newCel(master.layers[1],1,image,Point(0,0))
local tag = master:newTag(1,1)
tag.name="fin_broad"
end
do
local source = Image{fromFile="C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/shared-roshan-skin-swim-20261101/assets_src/animation/roshan_shared_swim_20261101/textures/anatomy/fin_edge.png"}
local image = Image(512,512,ColorMode.RGB)
image:drawImage(source,Point(45,207))
image:saveAs("C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/shared-roshan-skin-swim-20261101/assets_src/animation/roshan_shared_swim_20261101/textures/anatomy/fin_edge_registered.png")
master:newEmptyFrame()
master:newCel(master.layers[1],2,image,Point(0,0))
local tag = master:newTag(2,2)
tag.name="fin_edge"
end
do
local source = Image{fromFile="C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/shared-roshan-skin-swim-20261101/assets_src/animation/roshan_shared_swim_20261101/textures/anatomy/fin_cup.png"}
local image = Image(512,512,ColorMode.RGB)
image:drawImage(source,Point(65,137))
image:saveAs("C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/shared-roshan-skin-swim-20261101/assets_src/animation/roshan_shared_swim_20261101/textures/anatomy/fin_cup_registered.png")
master:newEmptyFrame()
master:newCel(master.layers[1],3,image,Point(0,0))
local tag = master:newTag(3,3)
tag.name="fin_cup"
end
master:saveAs("C:/Users/Peter/Documents/mermaid-roshan-reef/.worktrees/shared-roshan-skin-swim-20261101/assets_src/animation/roshan_shared_swim_20261101/masters/shared_fin_keys.aseprite")
master:close()
print("FIN_KEYS_REGISTERED_NATIVE 3")
