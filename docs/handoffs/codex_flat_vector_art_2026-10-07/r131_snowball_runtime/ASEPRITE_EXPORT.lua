local s=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowball_20261103/native/snowball_01.png")
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowball_20261103/masters/native_1254.aseprite")
s:crop(Rectangle(134,144,980,980))
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowball_20261103/masters/crop_980.aseprite")
s:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowball_20261103/crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=512,height=512,lockRatio=true,method="bilinear"}
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowball_20261103/masters/runtime_512.aseprite")
s:saveCopyAs("C:/Users/Peter/AppData/Local/Temp/reef-flat-vector-snowballs-20261103/runtime_snowball.png")
s:close()
