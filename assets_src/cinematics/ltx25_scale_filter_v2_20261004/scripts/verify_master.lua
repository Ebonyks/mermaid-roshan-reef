local s=app.open(app.params.master)
assert(#s.frames==41 and #s.slices==205 and #s.tags==41,'Master metadata missing')
local rows={}
for i,f in ipairs(s.frames) do
 local im=Image(s.width,s.height,ColorMode.RGB);im:drawSprite(s,f.frameNumber)
 im:saveAs(app.params.output..string.format('/%04d.png',i-1))
 rows[#rows+1]={index=i-1,duration_ms=f.duration*1000,tag=s.tags[i].name}
end
local f=assert(io.open(app.params.report,'wb'))
f:write(json.encode{frames=#s.frames,slices=#s.slices,tags=#s.tags,rows=rows});f:close();s:close()
