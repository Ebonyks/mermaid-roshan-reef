local src=app.open(app.params.source)
local W,H=src.width,src.height
local original=Image(src.spec);original:drawSprite(src,1);src:close()
local pc=app.pixelColor
local ymin,ymax=H,0
for y=0,H-1 do for x=0,W-1 do if pc.rgbaA(original:getPixel(x,y))>127 then ymin=math.min(ymin,y);ymax=math.max(ymax,y) end end end
local function sample(x,y)
 if x<0 or x>W-1 then return 0 end
 local left=math.floor(x);local t=x-left
 local c0=original:getPixel(left,y);local c1=original:getPixel(math.min(W-1,left+1),y)
 local a0=pc.rgbaA(c0)*(1-t);local a1=pc.rgbaA(c1)*t;local aa=a0+a1
 if aa<.5 then return 0 end
 return pc.rgba(math.floor((pc.rgbaR(c0)*a0+pc.rgbaR(c1)*a1)/aa+.5),math.floor((pc.rgbaG(c0)*a0+pc.rgbaG(c1)*a1)/aa+.5),math.floor((pc.rgbaB(c0)*a0+pc.rgbaB(c1)*a1)/aa+.5),math.floor(aa+.5))
end
local s=Sprite(W,H,ColorMode.RGB);s.layers[1].name='Complete berry canopy - breeze';local root=s:newLayer();root.name='Connected root - fixed'
local fixed=Image(W,H,ColorMode.RGB);local stop=math.max(ymin,ymax-8)
for y=stop,H-1 do for x=0,W-1 do fixed:drawPixel(x,y,original:getPixel(x,y)) end end
local durations={.30,.24,.30,.30,.32,.24,.30,.30};local amp=4.5
for k=1,8 do
 if k>1 then s:newEmptyFrame() end;s.frames[k].duration=durations[k]
 local moving=Image(W,H,ColorMode.RGB)
 for y=0,stop-1 do for x=0,W-1 do
  local t=math.max(0,math.min(1,(stop-y)/math.max(1,stop-ymin)));t=t*t*(3-2*t)
  local edge=math.min(1,math.min(x,W-1-x)/8);edge=math.max(0,edge)
  local offset=(x/W-.5)*.8
  local dx=(math.sin((k-1)*math.pi/4+offset)-math.sin(offset))*amp*t*edge
  if dx==0 then moving:drawPixel(x,y,original:getPixel(x,y)) else moving:drawPixel(x,y,sample(x-dx,y)) end
 end end
 s:newCel(s.layers[1],k,moving,Point(0,0));s:newCel(root,k,fixed,Point(0,0))
 local flat=Image(s.spec);flat:drawSprite(s,k);flat:saveAs(app.params.out..string.format('/cel-%02d.png',k-1));moving:saveAs(app.params.out..string.format('/upper-%02d.png',k-1))
end
fixed:saveAs(app.params.out..'/base-fixed.png');s:saveAs(app.params.out..'/huckleberry-restyled-eight-cels.aseprite');s:close()
s=app.open(app.params.out..'/huckleberry-restyled-eight-cels.aseprite');assert(#s.frames==8 and #s.layers==2)
for k=1,8 do local f=Image(s.spec);f:drawSprite(s,k);f:saveAs(app.params.out..string.format('/reopen-%02d.png',k-1)) end
s:close();print('PASS 8 frames, 2 layers, amplitude '..amp..' native pixels, base fixed from '..stop)
