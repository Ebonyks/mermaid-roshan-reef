local root=assert(app.params.root)
local mode=assert(app.params.mode)
local file=assert(io.open(root.."/sources.json","rb"))
local data=json.decode(file:read("*a"));file:close()
for _,group in ipairs(data.groups) do
 for _,theme in ipairs(group.themes) do
  if mode=="import" then
   local sprite=Sprite(1024,1024,ColorMode.RGB)
   sprite.layers[1].name="Native Mobile / "..theme.." / shared swimming"
   for index=0,53 do
    if index>0 then sprite:newEmptyFrame(index+1) end
    local path=root.."/raw_render/"..group.group.."/"..theme.."/loop/"..string.format("%04d.png",index)
    sprite:newCel(sprite.layers[1],index+1,Image{fromFile=path},Point(0,0))
    sprite.frames[index+1].duration=((index%3==2) and 34 or 33)/1000
   end
   sprite:saveAs(root.."/masters/"..theme..".aseprite")
   sprite:close()
  else
   local sprite=app.open(root.."/masters/"..theme..".aseprite")
   for index=0,53 do
    local image=Image(1024,1024,ColorMode.RGB)
    image:drawSprite(sprite,index+1)
    image:saveAs(root.."/raw_masters/"..theme.."/"..string.format("%04d.png",index))
   end
   sprite:close()
  end
  print("ASEPRITE_"..mode.."_OK "..theme)
 end
end
