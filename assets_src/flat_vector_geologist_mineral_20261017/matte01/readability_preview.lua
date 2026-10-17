local im = Image{fromFile=app.params.source}
local canvas = Image(720, 280, ColorMode.RGB)
canvas:clear(app.pixelColor.rgba(221, 179, 127, 255))
for y=0,279 do for x=0,359 do canvas:drawPixel(x,y,app.pixelColor.rgba(65,202,204,255)) end end
local sizes = {44,64,128}
for panel=0,1 do
 for i,h in ipairs(sizes) do
  local sprite = Image(im)
  local w = math.floor(im.width*h/im.height+0.5)
  sprite:resize{width=w,height=h,method="bilinear"}
  canvas:drawImage(sprite,Point(panel*360+18+(i-1)*96,140-math.floor(h/2)))
 end
end
canvas:saveAs(app.params.output)
