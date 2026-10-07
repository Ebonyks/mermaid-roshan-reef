local s=app.open(app.params.master);local total=0
for i,f in ipairs(s.frames) do
 local image=Image(s.width,s.height,ColorMode.RGB);image:drawSprite(s,f.frameNumber)
 image:saveAs(app.params.output..'/'..string.format('%04d.png',i-1));total=total+math.floor(f.duration*1000+.5)
end
assert(#s.frames==41 and total==1708);s:close()
print('Roundtrip41 frames1708ms')
