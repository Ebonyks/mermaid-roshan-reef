-- R125 whole-object technical export; no redrawing/masking/recoloring.
do
 local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/native/cream_bulb_original.png")
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/cream_bulb_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/cream_bulb_native_roundtrip.png")
 spr:crop(Rectangle(136,140,961,961))
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/cream_bulb_crop_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/cream_bulb_crop_roundtrip.png")
 app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/cream_bulb_runtime.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/melody/theatre_bulb_cream_painted.png")
 spr:close()
end
do
 local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/native/gold_bulb_original.png")
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/gold_bulb_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/gold_bulb_native_roundtrip.png")
 spr:crop(Rectangle(134,138,965,965))
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/gold_bulb_crop_native.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/gold_bulb_crop_roundtrip.png")
 app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
 spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_bulbs_20261102/masters/gold_bulb_runtime.aseprite")
 spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets/melody/theatre_bulb_gold_painted.png")
 spr:close()
end
