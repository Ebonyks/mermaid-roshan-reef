local s=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/trampoline_pad_20261102/native/trampoline_01.png")
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/trampoline_pad_20261102/aseprite/native_01.aseprite")
s:crop(Rectangle(174,88,1824,584))
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/trampoline_pad_20261102/aseprite/crop_01.aseprite")
s:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/trampoline_pad_20261102/aseprite/crop_roundtrip_01.png")
app.command.SpriteSize{ui=false,width=512,height=164,lockRatio=true,method="bilinear"}
s:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/trampoline_pad_20261102/aseprite/runtime_512x164.aseprite")
s:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/mg/trampoline_pad_painted.png")
s:close()
