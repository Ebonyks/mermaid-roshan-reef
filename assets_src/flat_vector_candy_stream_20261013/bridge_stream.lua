local s=assert(app.open(app.params.source))
assert(s.width==1024 and s.height==1536 and #s.frames==1 and #s.layers==1)
s.layers[1].name="Whole generated syrup ribbon; glow retained for review"
s:saveAs(app.params.native_master)
local native=Image(s.width,s.height,ColorMode.RGB);native:drawSprite(s,1);native:saveAs(app.params.roundtrip)
app.command.SpriteSize{ui=false,width=683,height=1024,method="bilinear"}
s:saveAs(app.params.master)
local output=Image(s.width,s.height,ColorMode.RGB);output:drawSprite(s,1);output:saveAs(app.params.output)
local f=assert(io.open(app.params.proof,"wb"));f:write(json.encode{native_size={1024,1536},normalized_size={683,1024},layers=#s.layers,frames=#s.frames,method="bilinear",crop=false,recolor=false,repaint=false,part_separation=false,glow_removed=false});f:close();s:close()
print("STREAM_ASEPRITE|Whole unchanged artwork; proportional1024 export")
