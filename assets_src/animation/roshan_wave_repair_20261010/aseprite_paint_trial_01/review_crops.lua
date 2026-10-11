local root=assert(app.params.root)
local study=app.fs.joinPath(root,"assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01")
local output=app.fs.joinPath(study,app.params.folder)
local index=tonumber(app.params.index) or 14
local top=tonumber(app.params.top) or 280
local height=tonumber(app.params.height) or 110
for _,name in ipairs({"source","draft"}) do
  local src=name=="source" and app.fs.joinPath(root,"assets_src/animation/roshan_wave_repair_20261010/native640_01/take_01/native_frames",string.format("%04d.png",index)) or app.fs.joinPath(output,string.format("%04d.png",index))
  local image=Image{fromFile=src};local pad=name=="source" and 0 or 128
  local crop=Image(100,height,ColorMode.RGB)
  crop:drawImage(image,Point(-150-pad,-top))
  crop:resize{width=600,height=height*6,method="nearest"}
  crop:saveAs(app.fs.joinPath(output,name.."_cuff_6x.png"))
end
