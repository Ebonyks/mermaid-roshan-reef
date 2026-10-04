local s=app.open(app.params.input);app.activeSprite=s
app.command.SpriteSize{ui=false,width=896,height=512,method='bilinear'}
s:saveAs(app.params.output..'/normalized_window.aseprite')
for frame=1,#s.frames do
 local image=Image(s.width,s.height,ColorMode.RGB);image:clear(app.pixelColor.rgba(0,0,0,0))
 for _,layer in ipairs(s.layers) do
  if layer.isVisible then local cel=layer:cel(frame);if cel then image:drawImage(cel.image,cel.position) end end
 end
 image:saveAs(app.params.output..string.format('/normalized_frames/%04d.png',frame-1))
end
s:close()
