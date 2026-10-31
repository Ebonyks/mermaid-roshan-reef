local s=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_geode_seams_20261030/seams_native.aseprite")
local original=s.cels[1].image
local n=Sprite(887,887,ColorMode.RGB)
local im=Image(887,887,ColorMode.RGB)
im:drawImage(original,Point(-27,-3))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_geode_seams_20261030/closed_crop.aseprite")
n:close()
local n=Sprite(887,887,ColorMode.RGB)
local im=Image(887,887,ColorMode.RGB)
im:drawImage(original,Point(-849,-3))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_geode_seams_20261030/done_crop.aseprite")
n:close()
s:close()
