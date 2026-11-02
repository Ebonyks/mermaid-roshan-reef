-- R124 technical whole-object export. No appearance pixels are redrawn.
-- Aseprite sprite:crop and SpriteSize bilinear preserve the authored PNG pixels.
do
 local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/native/apron_body_original.png")
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/apron_body_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/apron_body_native_roundtrip.png")
 spr:crop(Rectangle(28,309,2112,152))
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/apron_body_crop_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/apron_body_crop_roundtrip.png")
 app.command.SpriteSize{ui=false,width=1024,height=74,lockRatio=true,method='bilinear'}
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/apron_body_runtime.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/melody/stage_apron_painted.png")
 spr:close()
end
do
 local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/native/rainbow_inset_original.png")
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/rainbow_inset_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/rainbow_inset_native_roundtrip.png")
 spr:crop(Rectangle(42,262,2088,240))
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/rainbow_inset_crop_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/rainbow_inset_crop_roundtrip.png")
 app.command.SpriteSize{ui=false,width=522,height=60,lockRatio=true,method='bilinear'}
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_apron_20261102/masters/rainbow_inset_runtime.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/melody/stage_apron_rainbow_painted.png")
 spr:close()
end
