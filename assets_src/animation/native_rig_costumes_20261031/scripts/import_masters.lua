local root=assert(app.params.root)
for _,theme in ipairs({"ballet","magician"}) do
 for _,clip in ipairs({"arm_bend","blink","tail_bend"}) do
  local count=({arm_bend=97,blink=73,tail_bend=121})[clip]
  local sprite=Sprite(1024,1024,ColorMode.RGB)
  sprite.layers[1].name="Exact Godot Mobile / "..theme.." whole RGBA figure"
  for i=0,count-1 do
   if i>0 then sprite:newEmptyFrame(i+1) end
   local image=Image{fromFile=root.."/evidence/render_"..theme.."_v5/"..clip.."/"..string.format("%04d.png",i)}
   sprite:newCel(sprite.layers[1],i+1,image,Point(0,0))
   sprite.frames[i+1].duration=((i%3==2) and 34 or 33)/1000
  end
  sprite:saveAs(root.."/masters/"..theme.."/"..clip..".aseprite")
  sprite:close()
 end
end
