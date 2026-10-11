local root=app.params.root
for _,pair in ipairs({{6,3},{14,12},{10,12}}) do
 local spr=Sprite(256,256,ColorMode.RGB);spr.layers[1].name='Complete whole-frame RIFE output'
 for i=0,2 do
  if i>0 then spr:newFrame() end
  local src=Image{fromFile=root..string.format('/take_01/pair_%04d_%04d/%04d.png',pair[1],pair[2],i)}
  spr.cels[i+1].image=src;spr.frames[i+1].duration=1/24
 end
 spr:saveAs(root..string.format('/pair_%04d_%04d.aseprite',pair[1],pair[2]));spr:close()
end
local source=Image{fromFile=root..'/hand_comparison_native_crop.png'}
local enlarged=Image(source.width*2,source.height*2,ColorMode.RGB)
for y=0,enlarged.height-1 do for x=0,enlarged.width-1 do enlarged:putPixel(x,y,source:getPixel(math.floor(x/2),math.floor(y/2))) end end
enlarged:saveAs(root..'/hand_comparison_2x_nearest.png')
