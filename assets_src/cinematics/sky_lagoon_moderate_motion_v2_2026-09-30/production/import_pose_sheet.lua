-- Fresh generated pose keys imported and cleaned in Aseprite.
-- Native inputs stay separate. No source-art deformation or motion interpolation.
local root=app.params.root
local id=app.params.id
local pc=app.pixelColor
local f=io.open(root..'/objects/'..id..'/IMPORT_PARAMETERS.json','r')
local cfg=json.decode(f:read('*a'));f:close()
local dir=root..'/objects/'..id
local native=Image{fromFile=dir..'/'..cfg.input}
local sprite=Sprite(512,512,ColorMode.RGB)
local layer=sprite.layers[1];layer.name='Clean authored animation keys'
local reference=sprite:newLayer();reference.name='Native first pose - hidden reference';reference.isVisible=false
local function mask(runs,width)
 local out={}
 for _,r in ipairs(runs) do for x=r[2],r[3] do out[r[1]*width+x+1]=true end end
 return out
end
local function over(a,b)
 local aa=pc.rgbaA(a)/255;local ba=pc.rgbaA(b)/255;local out=aa+ba*(1-aa)
 if out==0 then return 0 end
 local function ch(c)return math.floor((c(a)*aa+c(b)*ba*(1-aa))/out+.5)end
 return pc.rgba(ch(pc.rgbaR),ch(pc.rgbaG),ch(pc.rgbaB),math.floor(out*255+.5))
end
local function import(n)
 local p=cfg.poses[n+1];local keep=mask(p.keep_runs,cfg.cell_width)
 local out=Image(512,512,ColorMode.RGB)
 for y=0,511 do for x=0,511 do
  local sx=math.floor((x-p.offset[1])/p.scale);local sy=math.floor((y-p.offset[2])/p.scale)
  if sx>=0 and sx<cfg.cell_width and sy>=0 and sy<cfg.cell_height and keep[sy*cfg.cell_width+sx+1] then
   local color=native:getPixel(p.origin[1]+sx,p.origin[2]+sy)
   local cutoff=cfg.kind=='smoke' and 64 or 192
   if pc.rgbaA(color)>=cutoff then
    if cfg.kind~='smoke' then color=pc.rgba(pc.rgbaR(color),pc.rgbaG(color),pc.rgbaB(color),255) end
    out:drawPixel(x,y,color)
   end
  end
 end end
 -- Tiny clipped huckleberry leaf tips are outdrawn in the new padding only.
 -- These local caps repair a crop edge; they supply no animation pose.
 for _,cap in ipairs(p.border_caps or {}) do
  local side=cap[1];local y0=math.floor(p.offset[2]+cap[2]*p.scale)
  local y1=math.floor(p.offset[2]+cap[3]*p.scale)
  local edge=math.floor(p.offset[1]+(side=='right' and cfg.cell_width-1 or 0)*p.scale)
  local mid=(y0+y1)/2;local half=math.max(1,(y1-y0)/2)
  for y=y0,y1 do
   local reach=math.floor(5*math.max(0,1-math.abs(y-mid)/half))
   local base=out:getPixel(math.max(0,math.min(511,edge+(side=='right' and -2 or 2))),y)
   for k=0,reach do
    local x=edge+(side=='right' and k or -k)
    if x>=0 and x<512 and y>=0 and y<512 and pc.rgbaA(base)>0 then
     local c=k==reach and pc.rgba(25,74,62,255) or base
     out:drawPixel(x,y,c)
    end
   end
  end
 end
 return out
end
local poses={}
for n=0,#cfg.poses-1 do poses[n+1]=import(n) end
if cfg.fixed_bottom_y then
 for n=2,#poses do for y=cfg.fixed_bottom_y,511 do for x=0,511 do
  poses[n]:drawPixel(x,y,poses[1]:getPixel(x,y))
 end end end
end
if cfg.fixed_base_rect then
 local r=cfg.fixed_base_rect
 for n=2,#poses do for y=r[2],r[4]-1 do for x=r[1],r[3]-1 do
  poses[n]:drawPixel(x,y,poses[1]:getPixel(x,y))
 end end end
end
if cfg.door_runs then
 local door=mask(cfg.door_runs,512)
 for n=2,#poses do for y=0,511 do for x=0,511 do
  if not door[y*512+x+1] then poses[n]:drawPixel(x,y,poses[1]:getPixel(x,y)) end
 end end end
end
if cfg.kind=='swing' then
 local frame=Image{fromFile=dir..'/identity_source.png'}
 local fixed=Image(512,512,ColorMode.RGB)
 for y=0,511 do for x=0,511 do
  local sx=math.floor((x-16)/cfg.frame_scale);local sy=math.floor((y-40)/cfg.frame_scale)
  if sx>=0 and sx<frame.width and sy>=0 and sy<frame.height then
   local clear=(x>=140 and x<=374 and y>=126)
    or (y>=118 and ((x>=188 and x<=201) or (x>=313 and x<=325)))
   local c=frame:getPixel(sx,sy)
   local keep_wood=pc.rgbaG(c)>pc.rgbaR(c)*1.15 and pc.rgbaB(c)>pc.rgbaR(c)*1.10
   if (not clear or keep_wood) and pc.rgbaA(c)>0 then fixed:drawPixel(x,y,c) end
  end
 end end
 local function rope(image,ax,ay,bx,by)
  local dx,dy=bx-ax,by-ay;local len=math.sqrt(dx*dx+dy*dy)
  for y=ay,by+2 do for x=math.min(ax,bx)-3,math.max(ax,bx)+3 do
   local t=math.max(0,math.min(1,((x-ax)*dx+(y-ay)*dy)/(len*len)))
   local distance=math.sqrt((x-ax-t*dx)^2+(y-ay-t*dy)^2)
   local alpha=math.max(0,math.min(1,1.7-distance))
   if alpha>0 and x>=0 and x<512 and y>=0 and y<512 then
    local braid=math.sin(t*len*2.2)*.5+.5
    local c=pc.rgba(math.floor(175+65*braid),math.floor(119+75*braid),math.floor(48+65*braid),math.floor(alpha*255))
    image:drawPixel(x,y,over(c,image:getPixel(x,y)))
   end
  end end
 end
 for n,seat in ipairs(poses) do
  local p=cfg.poses[n];local out=Image(fixed)
  local lx=p.offset[1]+p.scale*cfg.seat_sockets[n][1]
  local rx=p.offset[1]+p.scale*cfg.seat_sockets[n][3]
  local yy=cfg.socket_target_y[n]
  rope(out,193,118,math.floor(lx),yy);rope(out,320,118,math.floor(rx),yy)
  for y=0,511 do for x=0,511 do out:drawPixel(x,y,over(seat:getPixel(x,y),out:getPixel(x,y))) end end
  poses[n]=out
 end
 fixed:saveAs(dir..'/fixed_frame.png')
end
if cfg.kind=='glass' then
 local base=poses[1];poses={}
 for n=0,11 do
  local out=Image(base);local center=222+n*29
  for y=0,511 do for x=0,511 do
   local c=base:getPixel(x,y);local strength=math.max(0,1-math.abs(x+.45*y-center)/34)*.17
   if pc.rgbaA(c)>0 and math.max(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c))>80 and strength>0 then
    local function ch(v)return math.floor(v+(255-v)*strength+.5)end
    out:drawPixel(x,y,pc.rgba(ch(pc.rgbaR(c)),ch(pc.rgbaG(c)),ch(pc.rgbaB(c)),pc.rgbaA(c)))
   end
  end end
  poses[n+1]=out
 end
end
app.transaction('Import clean moderate-resolution animation keys',function()
 for n,out in ipairs(poses) do
  local frame=n==1 and sprite.frames[1] or sprite:newEmptyFrame()
  frame.duration=(cfg.duration_units[n] or 2)/12
  sprite:newCel(layer,frame,out,Point(0,0))
  out:saveAs(dir..string.format('/frames/frame_%02d.png',n-1))
 end
 -- Only one hidden reference cel; never replicate a native sheet per frame.
 local raw=Image(512,512,ColorMode.RGB)
 for y=0,511 do for x=0,511 do
  if x<native.width and y<native.height then raw:drawPixel(x,y,native:getPixel(x,y)) end
 end end
 sprite:newCel(reference,sprite.frames[1],raw,Point(0,0));reference.isVisible=false
end)
local tag=sprite:newTag(sprite.frames[1],sprite.frames[#poses]);tag.name=cfg.kind=='gate' and 'Open - six fresh keys' or 'Reference cycle'
sprite:saveAs(dir..'/'..id..'.aseprite')
print(id..': '..#poses..' clean 512px Aseprite states; reference only.')
