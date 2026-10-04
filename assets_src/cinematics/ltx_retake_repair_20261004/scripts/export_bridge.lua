local root=app.params.packet
local s=Sprite{fromFile=root..'/inputs/repair_keys.aseprite'}
for _,layer in ipairs(s.layers) do layer.isVisible=(layer.name=='Complete-figure clean guides; no fixed-body composite') end
for i,name in ipairs({'original_0040.png','corrected_0048.png','original_0064.png'}) do
 local image=Image(s.width,s.height,s.colorMode)
 image:drawSprite(s,i)
 image:saveAs(root..'/inputs/exported_'..name)
end
s:close()
