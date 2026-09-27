local f=assert(io.open(app.params.spec,"r"));local spec=json.decode(f:read("*a"));f:close()
for _,e in ipairs(spec.assets) do
 local s=assert(app.open(e.source));local before=Image(s);local out=Image(s.width,s.height,ColorMode.RGB)
 for _,frame in ipairs(e.frames) do
  local cell=Image(256,256,ColorMode.RGB)
  cell:drawImage(before,Point(-frame.source_xy[1],-frame.source_xy[2]))
  for _,span in ipairs(frame.erase_spans) do
   for x=span[2],span[3]-1 do cell:drawPixel(x,span[1],app.pixelColor.rgba(0,0,0,0)) end
  end
  out:drawImage(cell,Point(frame.target_xy[1],frame.target_xy[2]))
 end
 s.layers[1].name="Original atlas (hidden)";s.layers[1].isVisible=false
 local layer=s:newLayer();layer.name="Isolated frame ownership"
 s:newCel(layer,1,out,Point(0,0));s:saveAs(e.native);s:saveCopyAs(e.output);s:close()
end
