local root=app.params.root;local pc=app.pixelColor
app.fs.makeDirectory(root..'/native_on_black');app.fs.makeDirectory(root..'/sprite_on_black')
local board=Image(768,256,ColorMode.RGB);board:clear(pc.rgba(0,0,0,255))
for j,n in ipairs({14,26,40}) do
 for _,lane in ipairs({'native','sprite'}) do
  local im=Image{fromFile=root..string.format('/%s_rgba/%04d.png',lane,n)}
  local bg=Image(im.width,im.height,ColorMode.RGB);bg:clear(pc.rgba(0,0,0,255));bg:drawImage(im)
  bg:saveAs(root..string.format('/%s_on_black/%04d.png',lane,n));if lane=='sprite' then board:drawImage(bg,Point((j-1)*256,0)) end
 end
end
board:saveAs(root..'/contact_256_on_black.png')
