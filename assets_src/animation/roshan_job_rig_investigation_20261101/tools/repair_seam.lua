local root=assert(app.params.root)
local src=Image{fromFile=root.."/demo/art/detective_sleeve.png"};local out=Image(src)
-- Native upper-arm inverse map of the measured f48 tear: (435.13,436.76).
-- A six-pixel cloth underlap, copied from that same painted sleeve.
for y=429,453 do for x=426,452 do
 if app.pixelColor.rgbaA(src:getPixel(x,y))<192 then
  local best=99;local selected=0
  for dy=-6,6 do for dx=-6,6 do
   local p=src:getPixel(x+dx,y+dy);local d=dx*dx+dy*dy
   if app.pixelColor.rgbaA(p)>192 and d<best then selected=p;best=d end
  end end
  if best<=36 then out:drawPixel(x,y,selected) end
 end
end end
out:saveAs(root.."/demo/art/detective_sleeve.png")
print("SEAM_REPAIR_COMPLETE")
