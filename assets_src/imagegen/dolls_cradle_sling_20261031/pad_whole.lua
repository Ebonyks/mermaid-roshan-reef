local s=app.open([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_cradle_sling_20261031/scaled_whole.aseprite]])
local c=s.cels[1]
local n=Sprite(512,512,ColorMode.RGB)
local im=Image(512,512,ColorMode.RGB)
im:drawImage(c.image,Point(c.position.x+56,c.position.y+56))
n.cels[1].image=im
n:saveAs([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_cradle_sling_20261031/cradle_sling_master.aseprite]])
n:saveAs([[C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/dolls_cradle_sling_20261031/cradle_sling_export.png]])
