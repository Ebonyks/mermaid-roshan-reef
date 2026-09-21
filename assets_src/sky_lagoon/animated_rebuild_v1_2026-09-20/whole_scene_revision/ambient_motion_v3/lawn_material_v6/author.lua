local P=app.params.out
local pc=app.pixelColor
local src=app.open(P..'/rest.png');local im=Image(src.spec);im:drawSprite(src,1);src:close()
local W,H=im.width,im.height
local mask=Image{fromFile=P..'/motion-mask.png'}
local s=Sprite(W,H,ColorMode.RGB);s.layers[1].name='Grass paint inside protected lawn boundary'
local function smooth(v) v=math.max(0,math.min(1,v));return v*v*(3-2*v) end
local shifts={0,4,1,-3}
local function sample(x,y)
 local ix=math.floor(x);local f=x-ix;local a=im:getPixel(ix,y);local b=im:getPixel(math.min(ix+1,W-1),y)
 return pc.rgba(math.floor(pc.rgbaR(a)*(1-f)+pc.rgbaR(b)*f+.5),math.floor(pc.rgbaG(a)*(1-f)+pc.rgbaG(b)*f+.5),math.floor(pc.rgbaB(a)*(1-f)+pc.rgbaB(b)*f+.5),255)
end
for k=1,4 do
 if k>1 then s:newEmptyFrame() end;s.frames[k].duration=.35
 local out=Image(W,H,ColorMode.RGB)
 for y=0,H-1 do for x=0,W-1 do
  local edge=pc.rgbaR(mask:getPixel(x,y))/255
  local row=y%28;local bend=math.sin(row*math.pi/28)^2
  local dx=shifts[k]*edge*bend*(.65+.35*math.sin(x/145+y/100))
  out:drawPixel(x,y,(k==1 or dx==0) and im:getPixel(x,y) or sample(x-dx,y))
 end end
 s:newCel(s.layers[1],k,out,Point(0,0));out:saveAs(P..string.format('/cel-%d.png',k-1))
end
s:saveAs(P..'/whole-lawn-four-cels.aseprite');s:close()
s=app.open(P..'/whole-lawn-four-cels.aseprite');assert(#s.frames==4);for k=1,4 do local a=Image(s.spec);a:drawSprite(s,k);a:saveAs(P..'/reopened-'..(k-1)..'.png') end;s:close();print('NATIVE FOUR-CEL SOURCE PILOT; RUNTIME ACCEPTANCE OPEN')
