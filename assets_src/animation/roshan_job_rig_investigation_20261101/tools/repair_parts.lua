local root=assert(app.params.root)
for _,name in ipairs({"detective","geologist"}) do
 local body=Image{fromFile=root.."/demo/art/"..name.."_body.png"}
 local sleeve=Image(1024,1024,ColorMode.RGB)
 for y=399,499 do for x=390,485 do
  if x < 486-(y-405)*0.08 then
   sleeve:drawPixel(x,y,body:getPixel(x,y))
   if y>416 then body:drawPixel(x,y,0) end
  end
 end end
 sleeve:saveAs(root.."/demo/art/"..name.."_sleeve.png")
 body:saveAs(root.."/demo/art/"..name.."_body.png")
end
-- Bounded source-pixel extension of the existing clean neck below a new V
-- collar. It fills the named source gap; the protected face is never redrawn.
local a=Image{fromFile=root.."/demo/art/investigation_anatomy.png"}
for y=346,372 do for x=516,570 do
 local half=27-(y-346)*0.60
 if math.abs(x-543)<half then
  local p=a:getPixel(x,340-math.floor((y-346)*0.13))
  if app.pixelColor.rgbaA(p)>128 then a:drawPixel(x,y,p) end
 end
end end
a:saveAs(root.."/demo/art/investigation_anatomy.png")
print("BOUNDED_SOURCE_REPAIRS_COMPLETE")
