local p=app.params.base
local t=app.open(p..'/near-bank-original.png');local W,H=t.width,t.height;local original=Image(t.spec);original:drawSprite(t,1);t:close()
t=app.open(p..'/near-bank-mask.png');local mask=Image(W,H,ColorMode.RGB);mask:drawSprite(t,1);t:close()
t=app.open(p..'/motion-weight.png');local weight=Image(W,H,ColorMode.RGB);weight:drawSprite(t,1);t:close()
local pc=app.pixelColor;local fixed=Image(W,H,ColorMode.RGB)
for y=0,H-1 do for x=0,W-1 do if pc.rgbaR(mask:getPixel(x,y))==0 then fixed:drawPixel(x,y,original:getPixel(x,y)) end end end
local function sample(x,y)
 local ix,iy=math.floor(x),math.floor(y);local fx,fy=x-ix,y-iy;local rr,gg,bb=0,0,0
 for dy=0,1 do for dx=0,1 do local c=original:getPixel(math.max(0,math.min(W-1,ix+dx)),math.max(0,math.min(H-1,iy+dy)));local w=(dx==0 and 1-fx or fx)*(dy==0 and 1-fy or fy);rr=rr+pc.rgbaR(c)*w;gg=gg+pc.rgbaG(c)*w;bb=bb+pc.rgbaB(c)*w end end
 return pc.rgba(math.floor(rr+.5),math.floor(gg+.5),math.floor(bb+.5),255)
end
local s=Sprite(W,H,ColorMode.RGB);local background=s.layers[1];background.name='Protected landscape - fixed';local bank=s:newLayer();bank.name='Near cloud bank - material flow';local poses={0,1,.25,-.8}
for k=1,4 do
 if k>1 then s:newEmptyFrame() end;s.frames[k].duration=1.2;local im=Image(W,H,ColorMode.RGB)
 for y=0,H-1 do for x=0,W-1 do
  if pc.rgbaR(mask:getPixel(x,y))>0 then
   local w=pc.rgbaR(weight:getPixel(x,y))/255;local dx=poses[k]*5*w*(.7+.3*math.cos(y/90));local dy=poses[k]*.8*w*math.sin(x/220)
   im:drawPixel(x,y,(dx==0 and dy==0) and original:getPixel(x,y) or sample(x-dx,y-dy))
  end
 end end
 s:newCel(background,k,fixed,Point(0,0));s:newCel(bank,k,im,Point(0,0));im:saveAs(p..string.format('/bank-%02d.png',k-1));local out=Image(s.spec);out:drawSprite(s,k);out:saveAs(p..string.format('/frame-%02d.png',k-1))
end
fixed:saveAs(p..'/fixed-landscape.png');s:saveAs(p..'/near-cloud-bank-four-cels.aseprite');s:close();s=app.open(p..'/near-cloud-bank-four-cels.aseprite');assert(#s.frames==4 and #s.layers==2)
for k=1,4 do local out=Image(s.spec);out:drawSprite(s,k);out:saveAs(p..string.format('/reopen-%02d.png',k-1)) end;s:close();print('PASS four frames, two layers, fixed boundaries, 4.8 second source cycle')
