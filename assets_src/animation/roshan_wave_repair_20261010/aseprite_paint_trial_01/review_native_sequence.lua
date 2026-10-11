-- Review-only native pixel crops; no crop enters delivery or source masters.
local root=assert(app.params.root);local folder=assert(app.params.folder)
local base=app.fs.joinPath(root,"assets_src/animation/roshan_wave_repair_20261010/aseprite_paint_trial_01",folder)
local out=app.fs.joinPath(base,"review");app.fs.makeAllDirectories(out)
for first=0,40,8 do
  local count=math.min(8,41-first);local sheet=Image(1280,960,ColorMode.RGB)
  local gc=sheet.context;gc.color=Color{r=230,g=230,b=230};gc:rect(Rectangle(0,0,1280,960));gc:fill()
  for j=0,count-1 do local n=first+j;local im=Image{fromFile=app.fs.joinPath(base,string.format("%04d.png",n))}
    local crop=Image(320,480,ColorMode.RGB);crop:drawImage(im,Point(-70,-125))
    sheet:drawImage(crop,Point((j%4)*320,math.floor(j/4)*480))
  end
  sheet:saveAs(app.fs.joinPath(out,string.format("native_arm_contact_%02d_%02d.png",first,first+count-1)))
end
