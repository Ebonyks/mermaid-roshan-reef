-- Whole-frame source bridge. References and rejected attempts are separate files,
-- never hidden layers, pasted limbs, tweened pixels, or a duplicate drawing.
local file=assert(io.open(app.params.input,"rb"))
local data=json.decode(file:read("*a"));file:close()
app.fs.makeDirectory(data.output.."/frames")
local s=Sprite(data.canvas[1],data.canvas[2],ColorMode.RGB)
s.layers[1].name="Complete authored figure"
for i,path in ipairs(data.frames) do
 if i>1 then s:newFrame() end
 local frame=Image{fromFile=path}
 assert(frame.width==s.width and frame.height==s.height,"Native canvas mismatch")
 s.cels[i].image=frame
 s.frames[i].duration=data.durations_ms[i]/1000
end
if data.delivery_canvas then
 assert(s.width*data.delivery_canvas[2]==s.height*data.delivery_canvas[1],"Nonuniform scaling forbidden")
 app.command.SpriteSize{ui=false,width=data.delivery_canvas[1],height=data.delivery_canvas[2],method="bilinear"}
end
for _,phase in ipairs(data.phases) do
 local tag=s:newTag(phase.from+1,phase.to+1);tag.name=phase.name
end
s:saveAs(data.output.."/whole_sprite.aseprite");s:close()
local reopened=app.open(data.output.."/whole_sprite.aseprite")
local durations={}
for i,frame in ipairs(reopened.frames) do
 local image=Image(reopened.width,reopened.height,ColorMode.RGB)
 image:drawSprite(reopened,frame.frameNumber)
 image:saveAs(data.output..string.format("/frames/%04d.png",i-1))
 durations[i]=math.floor(frame.duration*1000+.5)
end
local proof=assert(io.open(data.output.."/master_proof.json","wb"))
proof:write(json.encode{layers=#reopened.layers,count=#reopened.frames,durations_ms=durations})
proof:close();reopened:close()
print("Whole-frame master reopened and exported")
