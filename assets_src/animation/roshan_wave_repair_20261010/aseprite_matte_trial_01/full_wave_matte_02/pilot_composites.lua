local root=app.params.root;local pc=app.pixelColor
for _,name in ipairs({'outline_seed_pilot_01','wide_boundary_pilot_01','neutral_fit_pilot_01'}) do
 local folder=root..'/'..name
 for _,lane in ipairs({'native_rgba','frames'}) do
  local im=Image{fromFile=folder..'/'..lane..'/0014.png'}
  for _,field in ipairs({{name='black',r=0,g=0,b=0},{name='light',r=245,g=245,b=245}}) do
   local bg=Image(im.width,im.height,ColorMode.RGB);bg:clear(pc.rgba(field.r,field.g,field.b,255));bg:drawImage(im)
   bg:saveAs(folder..'/'..lane..'_on_'..field.name..'_0014.png')
  end
 end
end
