local s=app.open(app.params.master)
assert(#s.frames==41 and s.width==576 and s.height==832)
local total=0
for i,f in ipairs(s.frames) do
 local image=Image(s.width,s.height,ColorMode.RGB)
 image:drawSprite(s,f.frameNumber)
 image:saveAs(app.params.output..'/'..string.format('%04d.png',i-1))
 total=total+math.floor(f.duration*1000+.5)
end
assert(total==1708)
s:close()
print('ROUNDTRIP41 frames576x832 timing1708ms')
