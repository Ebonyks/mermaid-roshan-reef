local root = app.params["packet"]
do local s=Sprite(384, 512, ColorMode.RGB)
local layer=s.layers[1]
layer.name="fir_crown"
for i=0,31 do
if i>0 then s:newEmptyFrame() end
local image=Image{fromFile=root.."/demo_project/fir_crown/"..string.format("%02d.png",i)}
s:newCel(layer,i+1,image,Point(0,0))
s.frames[i+1].duration=0.125
end
s:saveAs(root.."/fir_crown.aseprite")
s:close() end
do local s=Sprite(384, 384, ColorMode.RGB)
local layer=s.layers[1]
layer.name="meadow_flowers"
for i=0,31 do
if i>0 then s:newEmptyFrame() end
local image=Image{fromFile=root.."/demo_project/meadow_flowers/"..string.format("%02d.png",i)}
s:newCel(layer,i+1,image,Point(0,0))
s.frames[i+1].duration=0.125
end
s:saveAs(root.."/meadow_flowers.aseprite")
s:close() end
do local s=Sprite(384, 384, ColorMode.RGB)
local layer=s.layers[1]
layer.name="lakeside_lupines"
for i=0,31 do
if i>0 then s:newEmptyFrame() end
local image=Image{fromFile=root.."/demo_project/lakeside_lupines/"..string.format("%02d.png",i)}
s:newCel(layer,i+1,image,Point(0,0))
s.frames[i+1].duration=0.125
end
s:saveAs(root.."/lakeside_lupines.aseprite")
s:close() end
do local s=Sprite(384, 384, ColorMode.RGB)
local layer=s.layers[1]
layer.name="lake_ripples"
for i=0,31 do
if i>0 then s:newEmptyFrame() end
local image=Image{fromFile=root.."/demo_project/lake_ripples/"..string.format("%02d.png",i)}
s:newCel(layer,i+1,image,Point(0,0))
s.frames[i+1].duration=0.125
end
s:saveAs(root.."/lake_ripples.aseprite")
s:close() end
