-- Editable environment motion study. This is not a cinematic delivery frame.
local root=app.params.root
local f=io.open(root..'/scene/SCENE_PARAMETERS.json','r')
local cfg=json.decode(f:read('*a'));f:close()
local pc=app.pixelColor
local sprite=Sprite(cfg.width,cfg.height,ColorMode.RGB)
local function resize(src,w,h)
 local out=Image(src);out:resize{width=math.floor(w+.5),height=math.floor(h+.5)};return out
end
local function over(a,b)
 local aa=pc.rgbaA(a)/255;local ba=pc.rgbaA(b)/255;local oa=aa+ba*(1-aa)
 if oa==0 then return 0 end
 local function ch(c)return math.floor((c(a)*aa+c(b)*ba*(1-aa))/oa+.5)end
 return pc.rgba(ch(pc.rgbaR),ch(pc.rgbaG),ch(pc.rgbaB),math.floor(oa*255+.5))
end
local function draw(out,src,x0,y0)
 x0=math.floor(x0+.5);y0=math.floor(y0+.5)
 for y=0,src.height-1 do for x=0,src.width-1 do
  local dx,dy=x+x0,y+y0
  if dx>=0 and dx<out.width and dy>=0 and dy<out.height then
   local c=src:getPixel(x,y)
   if pc.rgbaA(c)>0 then out:drawPixel(dx,dy,over(c,out:getPixel(dx,dy))) end
  end
 end end
end
local base=resize(Image{fromFile=root..'/context/approved_clean_panorama.png'},cfg.width,cfg.height)
local background=sprite.layers[1];background.name='Approved v5 clean panorama - fixed';background.isContinuous=true
local shadows=sprite:newLayer();shadows.name='Painted contact shadows';shadows.isContinuous=true
local shadow=Image(cfg.width,cfg.height,ColorMode.RGB)
for _,s in ipairs(cfg.shadow_contacts or {}) do
 for y=math.floor(s.center[2]-s.radius[2]),math.ceil(s.center[2]+s.radius[2]) do
  for x=math.floor(s.center[1]-s.radius[1]),math.ceil(s.center[1]+s.radius[1]) do
   local d=((x-s.center[1])/s.radius[1])^2+((y-s.center[2])/s.radius[2])^2
   if d<1 then shadow:drawPixel(x,y,pc.rgba(36,74,69,math.floor(62*(1-d)))) end
  end
 end
end
local layers={}
local images={}
for _,item in ipairs(cfg.cards) do
 local layer=sprite:newLayer();layer.name=item.name;layers[item.id]=layer
 layer.isContinuous=not item.frames
 images[item.id]={}
 if item.frames then
  for n=0,item.frames-1 do
   images[item.id][n+1]=resize(Image{fromFile=root..'/objects/'..item.id..string.format('/frames/frame_%02d.png',n)},512*item.scale,512*item.scale)
  end
 else
  local img=Image{fromFile=root..'/'..item.path}
  images[item.id][1]=resize(img,img.width*item.scale,img.height*item.scale)
 end
end
local castleSource=Image{fromFile=root..'/context/current_castle.png'}
local castleLayer=sprite:newLayer();castleLayer.name='Existing four-tower castle - door and window studies'
local gates={}
for n=0,5 do gates[n+1]=Image{fromFile=root..string.format('/objects/09_gate/frames/frame_%02d.png',n)} end
local function pose_at(item,tick)
 local total=0;for _,n in ipairs(item.durations) do total=total+n end
 local t=(tick+(item.phase or 0))%total
 for i,duration in ipairs(item.durations) do
  if t<duration then return item.order[i]+1 end
  t=t-duration
 end
 return 1
end
local function castle_at(tick)
 local out=Image(castleSource)
 local gate=gates[pose_at(cfg.gate,tick)]
 local b=cfg.gate_crop
 -- The original arch/bridge stays fixed. Door samples are cropped into its
 -- existing aperture, solely to compare the motion at environmental scale.
 for y=570,765 do for x=412,591 do
  local inside=y>=659 or ((x-502)^2+(y-659)^2<=89^2)
  if inside then
   local sx=math.floor(b[1]+(x-412)/180*(b[3]-b[1]))
   local sy=math.floor(b[2]+(y-570)/196*(b[4]-b[2]))
   local c=gate:getPixel(sx,sy)
   out:drawPixel(x,y,over(c,pc.rgba(49,30,65,255)))
  end
 end end
 -- Preserve the castle's exact portrait pixels; only a low-intensity light
 -- band moves over the colored panes. Do not substitute a new portrait.
 local phase=(tick%48)/4
 local center=410+phase*29
 for y=252,540 do for x=426,607 do
  local inside=y>=347 or ((x-516)^2+(y-347)^2<=90^2)
  local c=out:getPixel(x,y)
  local strength=math.max(0,1-math.abs(x+.35*(y-252)-center)/27)*.18
  if inside and strength>0 and math.max(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c))>85 then
   local function ch(v)return math.floor(v+(255-v)*strength+.5)end
   out:drawPixel(x,y,pc.rgba(ch(pc.rgbaR(c)),ch(pc.rgbaG(c)),ch(pc.rgbaB(c)),pc.rgbaA(c)))
  end
 end end
 return resize(out,castleSource.width*cfg.castle.scale,castleSource.height*cfg.castle.scale)
end
for tick=0,cfg.frame_count-1 do
 local frame=tick==0 and sprite.frames[1] or sprite:newFrame();frame.duration=1/cfg.fps
 if tick==0 then sprite:newCel(background,frame,base,Point(0,0));sprite:newCel(shadows,frame,shadow,Point(0,0)) end
 for _,item in ipairs(cfg.cards) do
  local idx=item.frames and pose_at(item,tick) or 1
  local img=images[item.id][idx]
  assert(img,'Missing scene pose '..item.id..' index '..tostring(idx)..' tick '..tostring(tick))
  if tick==0 or item.frames then sprite:newCel(layers[item.id],frame,img,Point(math.floor(item.x+.5),math.floor(item.y+.5))) end
 end
 local castle=castle_at(tick)
 sprite:newCel(castleLayer,frame,castle,Point(math.floor(cfg.castle.x+.5),math.floor(cfg.castle.y+.5)))
 local flat=Image(cfg.width,cfg.height,ColorMode.RGB)
 flat:drawSprite(sprite,frame.frameNumber)
 flat:saveAs(root..string.format('/scene/frames/frame_%03d.png',tick))
 if tick==0 then
  flat:saveAs(root..'/scene/sky_lagoon_sample.png')
  for panel=0,2 do
   local crop=Image(640,640,ColorMode.RGB)
   for y=0,639 do for x=0,639 do crop:drawPixel(x,y,flat:getPixel(panel*640+x,y)) end end
   crop:saveAs(root..'/review/screen_'..panel..'.png')
  end
 end
end
local tag=sprite:newTag(sprite.frames[1],sprite.frames[#sprite.frames]);tag.name='Four-second environment study'
sprite:saveAs(root..'/scene/sky_lagoon_sample.aseprite')
print('Sky Lagoon: '..cfg.frame_count..' frames, '..cfg.width..'x'..cfg.height..', layered Aseprite reference.')
