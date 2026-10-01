-- Reference pilot: fresh generated seat drawings plus raster-painted suspension.
-- No deformation of the old seat, interpolation, 3D nodes or cinematic delivery.
local root=app.params.root;local pc=app.pixelColor
local sheet=Image{fromFile=root..'/seat_isolation_native.png'}
local fixed=Image{fromFile=root..'/fixed_frame_source.png'}
local cfg=dofile(root..'/pose_coordinates.lua')
local sprite=Sprite(256,256,ColorMode.RGB)
local layer=sprite.layers[1];layer.name='Fresh pose draft - fixed frame and authored suspension'
local source=sprite:newLayer();source.name='Preserved generated pose sheet - hidden reference';source.isVisible=false
local scale=5/16;local yoff=54
local function over(a,b)
 local aa=pc.rgbaA(a)/255;local ba=pc.rgbaA(b)/255;local out=aa+ba*(1-aa)
 if out==0 then return 0 end
 local function ch(c)return math.floor((c(a)*aa+c(b)*ba*(1-aa))/out+.5)end
 return pc.rgba(ch(pc.rgbaR),ch(pc.rgbaG),ch(pc.rgbaB),math.floor(out*255+.5))
end
local function rope(x,y,ax,ay,bx,by)
 if y<69 then return 0 end
 local dx,dy=bx-ax,by-ay;local len=dx*dx+dy*dy
 local t=math.max(0,math.min(1,((x-ax)*dx+(y-ay)*dy)/len))
 local distance=math.sqrt((x-ax-t*dx)^2+(y-ay-t*dy)^2)
 local alpha=math.max(0,math.min(1,1.6-distance))
 if alpha==0 then return 0 end
 local braid=math.sin(t*math.sqrt(len)*2.1)*.5+.5
 return pc.rgba(math.floor(167+68*braid),math.floor(112+71*braid),math.floor(46+62*braid),math.floor(alpha*255+.5))
end
app.transaction('Raster author eight new seat-pose states',function()
 for n=0,7 do
  local frame=n==0 and sprite.frames[1] or sprite:newEmptyFrame();frame.duration=cfg.duration[n+1]
  local out=Image(256,256,ColorMode.RGB);local b=cfg.bounds[n+1]
  local xoff=128-scale*(b[1]+b[3])/2
  local sockets=cfg.sockets[n+1]
  local lx=xoff+scale*sockets[1];local ly=yoff+scale*sockets[2]
  local rx=xoff+scale*sockets[3];local ry=yoff+scale*sockets[4]
  for y=0,255 do for x=0,255 do
   local sx=math.floor((x-xoff)/scale);local sy=math.floor((y-yoff)/scale);local p=0
   if sx>=0 and sx<384 and sy>=0 and sy<512 and sx>=b[1]-4 and sx<b[3]+4 and sy>=b[2]-4 and sy<b[4]+4 then
    p=sheet:getPixel(n%4*384+sx,math.floor(n/4)*512+sy)
    if pc.rgbaA(p)==0 then p=0 end
   end
   p=over(rope(x,y,99,69,lx,ly),p);p=over(rope(x,y,159,69,rx,ry),p)
   -- Discard stale rope fragments from the older fixed-frame isolation only.
   local f=fixed:getPixel(x,y)
   if y>=70 and y<134 and ((x>=90 and x<=106) or (x>=150 and x<=166)) then f=0 end
   if y<69 then p=f else p=over(f,p) end
   if pc.rgbaA(p)==0 then p=0 end
   out:drawPixel(x,y,p)
  end end
  sprite:newCel(layer,frame,out,Point(0,0));sprite:newCel(source,frame,sheet,Point(0,0))
  out:saveAs(root..string.format('/frames/frame_%02d.png',n))
 end
end)
source.isVisible=false
local tag=sprite:newTag(sprite.frames[1],sprite.frames[8]);tag.name='Fresh seat poses - fore and aft draft'
sprite:saveAs(root..'/swing_pose_v2.aseprite')
print('Eight new seat-pose states painted in Aseprite. Draft reference; creative review remains open.')
