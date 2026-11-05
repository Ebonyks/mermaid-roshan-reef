-- R126 complete painted token technical crops/resampling only; no painted pixel editing.
local original=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
original:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/note_atlas_native.aseprite")
original:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/note_atlas_native_roundtrip.png")
original:close()
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
spr:crop(Rectangle(15,21,414,414))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/red_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/red_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/red_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/exports/red_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
spr:crop(Rectangle(458,21,414,414))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/orange_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/orange_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/orange_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/exports/orange_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
spr:crop(Rectangle(902,21,414,414))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/yellow_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/yellow_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/yellow_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/exports/yellow_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
spr:crop(Rectangle(1345,21,414,414))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/green_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/green_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/green_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/exports/green_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
spr:crop(Rectangle(15,464,414,414))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/blue_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/blue_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/blue_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/exports/blue_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
spr:crop(Rectangle(458,464,414,414))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/indigo_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/indigo_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/indigo_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/exports/indigo_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/native/note_atlas_original.png")
spr:crop(Rectangle(902,464,414,414))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/violet_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/violet_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=256,height=256,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/masters/violet_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_note_20261102/exports/violet_painted.png")
spr:close()
end
