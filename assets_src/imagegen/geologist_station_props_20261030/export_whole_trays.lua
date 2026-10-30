local s=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_station_props_20261030/station_trays_native.aseprite")
local original=s.cels[1].image
local n=Sprite(724,724,ColorMode.RGB)
local im=Image(724,724,ColorMode.RGB)
im:drawImage(original,Point(-4,0))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_station_props_20261030/mint_whole_crop.aseprite")
n:close()
local n=Sprite(724,724,ColorMode.RGB)
local im=Image(724,724,ColorMode.RGB)
im:drawImage(original,Point(-730,0))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_station_props_20261030/blue_whole_crop.aseprite")
n:close()
local n=Sprite(724,724,ColorMode.RGB)
local im=Image(724,724,ColorMode.RGB)
im:drawImage(original,Point(-1448,0))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_station_props_20261030/lavender_whole_crop.aseprite")
n:close()
s:close()
