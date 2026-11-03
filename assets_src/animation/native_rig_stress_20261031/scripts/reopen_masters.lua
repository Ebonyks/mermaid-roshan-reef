-- Reopen native review masters and export each exact whole RGBA frame for comparison.
local root=app.params.root
for _,clip in ipairs({"arm_bend","blink","tail_bend"}) do
  local s=assert(app.open(root.."/masters/"..clip..".aseprite"))
  for i,frame in ipairs(s.frames) do
    local image=Image(s.width,s.height,ColorMode.RGB)
    image:drawSprite(s,i)
    image:saveAs(root.."/masters/reopened/"..clip.."/"..string.format("%04d.png",i-1))
  end
  s:close()
end
