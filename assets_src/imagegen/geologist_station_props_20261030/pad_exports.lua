local s=app.open("C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-geologist-station-props-20261030/mint_scaled432.aseprite")
assert(s.width==432 and s.height==432)
local n=Sprite(512,512,ColorMode.RGB)
local im=Image(512,512,ColorMode.RGB)
local cel=s.cels[1]
im:drawImage(cel.image,Point(40+cel.position.x,40+cel.position.y))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_station_props_20261030/mint_runtime512.aseprite")
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/opera/worlds/props/geologist_station_tray_mint_painted.png")
n:close()
s:close()
local s=app.open("C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-geologist-station-props-20261030/blue_scaled432.aseprite")
assert(s.width==432 and s.height==432)
local n=Sprite(512,512,ColorMode.RGB)
local im=Image(512,512,ColorMode.RGB)
local cel=s.cels[1]
im:drawImage(cel.image,Point(40+cel.position.x,40+cel.position.y))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_station_props_20261030/blue_runtime512.aseprite")
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/opera/worlds/props/geologist_station_tray_blue_painted.png")
n:close()
s:close()
local s=app.open("C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-geologist-station-props-20261030/lavender_scaled432.aseprite")
assert(s.width==432 and s.height==432)
local n=Sprite(512,512,ColorMode.RGB)
local im=Image(512,512,ColorMode.RGB)
local cel=s.cels[1]
im:drawImage(cel.image,Point(40+cel.position.x,40+cel.position.y))
n.cels[1].image=im
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/geologist_station_props_20261030/lavender_runtime512.aseprite")
n:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/opera/worlds/props/geologist_station_tray_lavender_painted.png")
n:close()
s:close()
