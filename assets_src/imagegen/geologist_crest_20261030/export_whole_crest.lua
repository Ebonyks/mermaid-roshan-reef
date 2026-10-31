local s=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_crest_20261030/crest_uniform216.png")
local n=Sprite(256,256,ColorMode.RGB)
local im=Image(256,256,ColorMode.RGB)
im:drawImage(s.cels[1].image,Point(20,20))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_crest_20261030/crest_whole256.aseprite")
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/opera/worlds/ui/crests/opera_crest_geologist.png")
n:close()
s:close()
