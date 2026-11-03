local s=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowman_coal_20261103/native/coal_01.png")
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowman_coal_20261103/masters/native_1254.aseprite")
s:crop(Rectangle(-14,-18,1280,1280))
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowman_coal_20261103/masters/registered_canvas1280.aseprite")
s:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowman_coal_20261103/registered_canvas_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method="bilinear"}
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowman_coal_20261103/masters/runtime_256.aseprite")
s:saveCopyAs("C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-snowman-coal-20261103/runtime_snowman_coal.png")
s:close()
