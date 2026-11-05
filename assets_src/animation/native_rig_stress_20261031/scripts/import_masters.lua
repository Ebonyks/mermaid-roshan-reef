-- Lossless RGBA review masters. Native bone authoring stays in the Godot project.
local root=app.params.root
assert(root,"root parameter required")
for _,clip in ipairs({"arm_bend","blink","tail_bend"}) do
  local count=({arm_bend=97,blink=73,tail_bend=121})[clip]
  local target=Sprite(1024,1024,ColorMode.RGB)
  target.layers[1].name="Exact Godot Mobile render / whole RGBA figure"
  for i=0,count-1 do
    if i>0 then target:newEmptyFrame(i+1) end
    local image=Image{fromFile=root.."/evidence/render_v10/"..clip.."/"..string.format("%04d.png",i)}
    target:newCel(target.layers[1],i+1,image,Point(0,0))
    -- Aseprite stores integer ms; 33,33,34 repeats exactly one second per 30 frames.
    target.frames[i+1].duration=((i%3==2) and 34 or 33)/1000
  end
  target:saveAs(root.."/masters/"..clip..".aseprite")
  target:close()
end
