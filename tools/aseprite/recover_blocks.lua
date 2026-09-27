local f=assert(io.open(app.params.spec,"r"));local e=json.decode(f:read("*a"));f:close()
local master=assert(app.open(e.source));local source=Image(master)
-- Reviewed magenta-only pixels. Foreground RGB is copied, never repainted.
for y=0,source.height-1 do for x=0,source.width-1 do
 local c=source:getPixel(x,y);local r=app.pixelColor.rgbaR(c);local g=app.pixelColor.rgbaG(c);local b=app.pixelColor.rgbaB(c)
 if r>160 and b>150 and g<90 then source:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0)) end
end end
local out=Image(1024,778,ColorMode.RGB)
for i,r in ipairs(e.rectangles) do
 local left=r[3];local top=r[4];local right=r[1];local bottom=r[2]
 for y=r[2],r[4]-1 do for x=r[1],r[3]-1 do
  if app.pixelColor.rgbaA(source:getPixel(x,y))>0 then left=math.min(left,x);right=math.max(right,x);top=math.min(top,y);bottom=math.max(bottom,y) end
 end end
 local w=right-left+1;local h=bottom-top+1;local cell=Sprite(w,h,ColorMode.RGB);local im=Image(w,h,ColorMode.RGB);im:drawImage(source,Point(-left,-top));cell.cels[1].image=im
 app.command.SpriteSize{ui=false,width=math.floor(w*e.uniform_scale+0.5),height=math.floor(h*e.uniform_scale+0.5),method="bilinear"}
 local scaled=Image(cell);cell:close()
 out:drawImage(scaled,Point(((i-1)%4)*256+128-math.floor(scaled.width/2),math.floor((i-1)/4)*389+383-scaled.height))
end
-- Clear invisible resampling residue; visible RGBA remains unchanged.
for y=0,out.height-1 do for x=0,out.width-1 do
 if app.pixelColor.rgbaA(out:getPixel(x,y))==0 then out:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0)) end
end end
local s=assert(app.open(e.original));s.layers[1].name="Original clipped states (hidden)";s.layers[1].isVisible=false
local layer=s:newLayer();layer.name="Whole source-owned three-block states";s:newCel(layer,1,out,Point(0,0));s:saveAs(e.native);s:saveCopyAs(e.output);s:close();master:close()
