local root=app.params.root
local function read(path) local f=assert(io.open(path,'r'));local t=f:read('*a');f:close();return json.decode(t) end
local function inside(x,y,poly)
 local on=false;local j=#poly
 for i=1,#poly do local a=poly[i];local b=poly[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then on=not on end;j=i end
 return on
end
local spec=read(root..'/registration.json')
for name,e in pairs(spec.parts) do
 if not app.params.only or name==app.params.only then
 local native=assert(app.open(root..'/native/'..e.source));local original=Image(native)
 local isolated=Image(original.width,original.height,ColorMode.RGB)
 local function spans(y,poly)
  local xs={};local j=#poly
  for i=1,#poly do local a,b=poly[i],poly[j]
   if ((a[2]>y)~=(b[2]>y)) then xs[#xs+1]=(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] end;j=i
  end
  table.sort(xs);return xs
 end
 for y=0,original.height-1 do
  local xs=spans(y+.5,e.polygon)
  for k=1,#xs-1,2 do for x=math.max(0,math.ceil(xs[k]-.5)),math.min(original.width-1,math.floor(xs[k+1]-.5)) do
   local yes=true
   if e.holes then for _,hole in ipairs(e.holes) do if inside(x+.5,y+.5,hole) then yes=false end end end
   if yes and e.clip_axis then local a=e.clip_axis;if (x-a.origin[1])*a.axis[1]+(y-a.origin[2])*a.axis[2]>a.maximum then yes=false end end
   if yes then local c=original:getPixel(x,y);if e.skin_only then local rr,gg,bb=app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c);if not (rr>175 and gg>115 and bb>85 and (rr-bb)/math.max(rr,1)<0.44 and rr>gg and gg>bb) then c=0 end end;if not e.remove_navy or not (app.pixelColor.rgbaR(c)<35 and app.pixelColor.rgbaB(c)>app.pixelColor.rgbaR(c)*1.5) then isolated:drawPixel(x,y,c) end end
  end end
 end
 local s=Sprite(original.width,original.height,ColorMode.RGB);s.cels[1].image=isolated;s.layers[1].name='Isolated source garment (RGBA)'
 app.command.SpriteSize{ui=false,width=math.floor(original.width*e.scale+.5),height=math.floor(original.height*e.scale+.5),method='bilinear'}
 local registered=Image(e.size or 1024,e.size or 1024,ColorMode.RGB);registered:drawImage(Image(s),Point(e.offset[1],e.offset[2]));s:close()
 if e.fill_polygon then
  -- Bilinear reuse of a continuous painted skin window; no scanline color bands.
  for y=320,410 do for x=450,635 do
   if inside(x+.5,y+.5,e.fill_polygon) then
    local u=634+(x-465)/155*63;local v=412+(y-331)/74*35
    u=math.max(634,math.min(697,u));v=math.max(412,math.min(447,v))
    local x0,y0=math.floor(u),math.floor(v);local tx,ty=u-x0,v-y0
    local rr,gg,bb=0,0,0
    for dy=0,1 do for dx=0,1 do
     local c=original:getPixel(x0+dx,y0+dy);local w=(dx==0 and (1-tx) or tx)*(dy==0 and (1-ty) or ty)
     rr=rr+app.pixelColor.rgbaR(c)*w;gg=gg+app.pixelColor.rgbaG(c)*w;bb=bb+app.pixelColor.rgbaB(c)*w
    end end
    registered:drawPixel(x,y,app.pixelColor.rgba(math.floor(rr+.5),math.floor(gg+.5),math.floor(bb+.5),255))
   else registered:drawPixel(x,y,0) end
  end end
 end
 local master=Sprite(e.size or 1024,e.size or 1024,ColorMode.RGB);master.layers[1].name='Registered garment; new silhouette';master.cels[1].image=registered
 master:saveAs(root..'/masters/'..name..'.aseprite');master:saveCopyAs(root..'/art/'..name..'.png');master:close();native:close()
 print('GARMENT '..name)
 end
end
