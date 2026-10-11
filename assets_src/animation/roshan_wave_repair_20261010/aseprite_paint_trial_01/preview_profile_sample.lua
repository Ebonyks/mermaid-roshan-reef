-- Review-only uniform whole-image mapping; neutral source field stays opaque.
local root=assert(app.params.root);local folder=assert(app.params.folder)
local base=app.fs.joinPath(root,"assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01",folder)
local f=assert(io.open(app.fs.joinPath(base,"joint_geometry.json"),"rb"));local data=json.decode(f:read("*a"));f:close()
local out=app.fs.joinPath(base,"review256");app.fs.makeAllDirectories(out)
local contact=Image(256*#data.frames,256,ColorMode.RGB)
for i,frame in ipairs(data.frames) do
  local source=Image{fromFile=app.fs.joinPath(base,string.format("%04d.png",frame.source_index))}
  source:resize{width=240,height=280,method="bilinear"}
  local whole=Image(256,256,ColorMode.RGB);local gc=whole.context;gc.color=Color{r=238,g=238,b=237};gc:rect(Rectangle(0,0,256,256));gc:fill()
  whole:drawImage(source,Point(15,-10));whole:saveAs(app.fs.joinPath(out,string.format("%04d.png",frame.source_index)))
  contact:drawImage(whole,Point((i-1)*256,0))
end
contact:saveAs(app.fs.joinPath(base,"contact256_opaque_native_field.png"))
