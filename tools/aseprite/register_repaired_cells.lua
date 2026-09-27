local f=assert(io.open(app.params.spec,"r"));local spec=json.decode(f:read("*a"));f:close()
for _,e in ipairs(spec.assets) do
 local s=assert(app.open(e.source));local before=Image(s);local out=Image(s.width,s.height,ColorMode.RGB);local w=e.cell_size[1];local h=e.cell_size[2]
 for i,d in ipairs(e.frame_translations) do
  local x=((i-1)%4)*w;local y=math.floor((i-1)/4)*h
  local old=Image(w,h,ColorMode.RGB);old:drawImage(before,Point(-x,-y))
  local moved=Image(w,h,ColorMode.RGB);moved:drawImage(old,Point(d[1],d[2]));out:drawImage(moved,Point(x,y))
 end
 s.layers[1].name="Unregistered repaired source (hidden)";s.layers[1].isVisible=false
 local layer=s:newLayer();layer.name="Fixed original pivot, whole-frame translation"
 s:newCel(layer,1,out,Point(0,0));s:saveAs(e.native);s:saveCopyAs(e.output);s:close()
end
