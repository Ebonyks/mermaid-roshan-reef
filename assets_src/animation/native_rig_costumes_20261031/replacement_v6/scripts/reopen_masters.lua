local root=assert(app.params.root)
for _,theme in ipairs({"ballet","magician"}) do
 for _,clip in ipairs({"arm_bend","blink","tail_bend"}) do
  local sprite=app.open(root.."/masters_v8/"..theme.."/"..clip..".aseprite")
  assert(sprite)
  for i,frame in ipairs(sprite.frames) do
   local image=Image(sprite.width,sprite.height,ColorMode.RGB)
   image:drawSprite(sprite,frame)
   image:saveAs(root.."/masters_v8/reopened/"..theme.."/"..clip.."/"..string.format("%04d.png",i-1))
  end
  sprite:close()
 end
end
