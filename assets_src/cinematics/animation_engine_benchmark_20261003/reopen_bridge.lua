local s=app.open(app.params.input)
local layer=s.layers[2]
for frame=1,#s.frames do
 local cel=layer:cel(frame)
 local image=Image(s.width,s.height,ColorMode.RGB)
 image:clear(app.pixelColor.rgba(0,0,0,0))
 image:drawImage(cel.image,cel.position)
 image:saveAs(app.params.output..string.format('/reopened_%04d.png',frame))
end
s:close()
