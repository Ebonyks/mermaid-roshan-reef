-- R127 whole painted pip-state technical crops and uniform resampling only. Native retained.
local original=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
original:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/pip_atlas_native.aseprite")
original:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/pip_atlas_native_roundtrip.png")
original:close()
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(66,23,239,239))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_red_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_red_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_red_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/idle_red_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(339,23,239,239))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_orange_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_orange_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_orange_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/idle_orange_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(604,23,239,239))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_yellow_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_yellow_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_yellow_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/idle_yellow_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(863,23,239,239))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_green_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_green_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_green_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/idle_green_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1123,22,240,240))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_blue_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_blue_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_blue_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/idle_blue_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1379,22,240,240))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_indigo_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_indigo_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_indigo_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/idle_indigo_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1634,23,239,239))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_violet_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_violet_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/idle_violet_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/idle_violet_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(50,281,262,262))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_red_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_red_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_red_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/current_red_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(323,281,260,260))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_orange_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_orange_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_orange_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/current_orange_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(588,282,259,259))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_yellow_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_yellow_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_yellow_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/current_yellow_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(848,281,260,260))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_green_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_green_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_green_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/current_green_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1107,281,260,260))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_blue_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_blue_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_blue_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/current_blue_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1364,281,261,261))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_indigo_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_indigo_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_indigo_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/current_indigo_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1623,281,260,260))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_violet_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_violet_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/current_violet_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/current_violet_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(53,559,250,250))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_red_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_red_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_red_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/filled_red_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(324,559,250,250))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_orange_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_orange_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_orange_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/filled_orange_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(586,559,250,250))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_yellow_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_yellow_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_yellow_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/filled_yellow_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(848,559,250,250))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_green_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_green_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_green_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/filled_green_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1108,559,251,251))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_blue_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_blue_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_blue_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/filled_blue_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1369,559,251,251))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_indigo_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_indigo_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_indigo_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/filled_indigo_painted.png")
spr:close()
end
do
local spr=app.open("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/native/pip_atlas_original.png")
spr:crop(Rectangle(1627,559,251,251))
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_violet_crop_native.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_violet_crop_roundtrip.png")
app.command.SpriteSize{ui=false,width=128,height=128,lockRatio=true,method='bilinear'}
spr:saveAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/masters/filled_violet_runtime.aseprite")
spr:saveCopyAs("C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/melody_progress_pips_20261102/exports/filled_violet_painted.png")
spr:close()
end
