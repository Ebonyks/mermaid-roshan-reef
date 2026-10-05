local s=app.open(app.params.master)
for i,f in ipairs(s.frames) do local image=Image(s.width,s.height,ColorMode.RGB);image:drawSprite(s,f.frameNumber);image:saveAs(app.params.destination..'/'..string.format('%04d.png',i-1)) end
s:close()
