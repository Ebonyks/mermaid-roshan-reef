local s=app.open([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_safety_mat_20261031/scaled_whole.aseprite]])
local c=s.cels[1]
local n=Sprite(1024,256,ColorMode.RGB)
local im=Image(1024,256,ColorMode.RGB)
im:drawImage(c.image,Point(c.position.x+92,c.position.y+52))
n.cels[1].image=im
n:saveAs([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_safety_mat_20261031/safety_mat_master.aseprite]])
n:saveAs([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_safety_mat_20261031/safety_mat_export.png]])
