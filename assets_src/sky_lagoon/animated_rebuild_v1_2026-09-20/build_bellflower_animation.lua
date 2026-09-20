-- Source-preserving gameplay cel animation, directly authored in Aseprite.
local base=app.params.base
local names={'stems','bell_tall','bell_middle','bell_right','bud','leaves_fixed'}
local pivots={{281,281},{166,81},{209,159},{339,209},{364,164},{0,0}}
local stemAngles={0,.75,1.5,.8,0,-.75,-1.5,-.8}
local angles={{0,0,0,0,0,0,0,0},{0,2.6,4,2.2,0,-3,-4.2,-2},{0,.6,2.4,4,1.6,-.8,-3,-1.6},{0,-.6,1.4,2.6,1.2,-.4,-1.8,-.8},{0,.4,1,.6,0,-.4,-1,-.6},{0,0,0,0,0,0,0,0}}
local durations={.26,.24,.30,.26,.22,.24,.30,.26}
local sources={};local layers={};local target=Sprite(512,512,ColorMode.RGB)
for i,name in ipairs(names) do
 local input=app.open(base..'/bellflower/'..name..'.png');local im=Image(512,512,ColorMode.RGB)
 im:drawImage(input.cels[1].image,input.cels[1].position);input:close();sources[i]=im
 local layer=i==1 and target.layers[1] or target:newLayer();layer.name=name;layers[i]=layer
end
local pc=app.pixelColor
local function rotate(x,y,p,a)
 local c,s=math.cos(a),math.sin(a);local dx,dy=x-p[1],y-p[2]
 return p[1]+c*dx-s*dy,p[2]+s*dx+c*dy
end
local function sample(im,x,y)
 local x0,y0=math.floor(x),math.floor(y);local fx,fy=x-x0,y-y0
 local ra,ga,ba,aa=0,0,0,0
 for dy=0,1 do for dx=0,1 do
  local px,py=x0+dx,y0+dy
  if px>=0 and px<512 and py>=0 and py<512 then
   local w=(dx==0 and 1-fx or fx)*(dy==0 and 1-fy or fy)
   local c=im:getPixel(px,py);local a=pc.rgbaA(c)*w
   aa=aa+a;ra=ra+pc.rgbaR(c)*a;ga=ga+pc.rgbaG(c)*a;ba=ba+pc.rgbaB(c)*a
  end
 end end
 if aa<.5 then return 0 end
 return pc.rgba(math.floor(ra/aa+.5),math.floor(ga/aa+.5),math.floor(ba/aa+.5),math.floor(aa+.5))
end
for f=1,8 do
 if f>1 then target:newEmptyFrame() end
 target.frames[f].duration=durations[f]
 for i,name in ipairs(names) do
  local image=sources[i]
  if f>1 and name~='leaves_fixed' then
   image=Image(512,512,ColorMode.RGB)
   for y=0,511 do for x=0,511 do
    local sx,sy=rotate(x,y,pivots[1],-math.rad(stemAngles[f]))
    sx,sy=rotate(sx,sy,pivots[i],-math.rad(angles[i][f]))
    image:drawPixel(x,y,sample(sources[i],sx,sy))
   end end
  end
  target:newCel(layers[i],f,image,Point(0,0))
 end
end
local tag=target:newTag(1,8);tag.name='gentle_bells'
app.activeSprite=target;target:saveAs(base..'/bellflower/bellflower-eight-cels.aseprite');target:close()
