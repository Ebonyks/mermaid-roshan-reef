local s=app.open([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_safety_mat_20261031/native/native_take2.aseprite]])
local c=s.cels[1]
local n=Sprite(2167,390,ColorMode.RGB)
local im=Image(2167,390,ColorMode.RGB)
im:drawImage(c.image,Point(c.position.x,c.position.y-200))
n.cels[1].image=im
n:saveAs([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_safety_mat_20261031/whole_crop.aseprite]])
