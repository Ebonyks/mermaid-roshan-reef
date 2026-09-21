local P=app.params.out
local pc=app.pixelColor
local originals={};local bounds={}
for j=1,3 do
 local s=app.open(P..string.format('/tuft-%d-rest.png',j-1));local im=Image(s.spec);im:drawSprite(s,1);s:close();originals[j]=im
 local top,bottom=im.height,0
 for y=0,im.height-1 do for x=0,im.width-1 do if pc.rgbaA(im:getPixel(x,y))>127 then top=math.min(top,y);bottom=math.max(bottom,y) end end end
 bounds[j]={top=top,stop=bottom-8}
end
local W,H=originals[1].width,originals[1].height
local s=Sprite(W,H,ColorMode.RGB);local layers={}
for j=1,3 do
 local moving=j==1 and s.layers[1] or s:newLayer();moving.name='Tuft '..j..' whole crown'
 local fixed=s:newLayer();fixed.name='Tuft '..j..' fixed root';layers[j]={moving=moving,fixed=fixed}
end
local function sample(im,x,y)
 if x<0 or x>W-1 then return 0 end
 local x0=math.floor(x);local t=x-x0;local c0=im:getPixel(x0,y);local c1=im:getPixel(math.min(W-1,x0+1),y)
 local a0=pc.rgbaA(c0)*(1-t);local a1=pc.rgbaA(c1)*t;local aa=a0+a1
 if aa<.5 then return 0 end
 return pc.rgba(math.floor((pc.rgbaR(c0)*a0+pc.rgbaR(c1)*a1)/aa+.5),math.floor((pc.rgbaG(c0)*a0+pc.rgbaG(c1)*a1)/aa+.5),math.floor((pc.rgbaB(c0)*a0+pc.rgbaB(c1)*a1)/aa+.5),math.floor(aa+.5))
end
for k=1,4 do
 if k>1 then s:newEmptyFrame() end;s.frames[k].duration=.35
 for j=1,3 do
  local orig=originals[j];local stop=bounds[j].stop;local top=bounds[j].top;local moving=Image(W,H,ColorMode.RGB);local fixed=Image(W,H,ColorMode.RGB)
  local phase=(j-1)*.3;local amplitude=({7,10,8.5})[j]
  for y=0,H-1 do for x=0,W-1 do
   if y>=stop then fixed:drawPixel(x,y,orig:getPixel(x,y)) else
    local weight=math.max(0,math.min(1,(stop-y)/math.max(1,stop-top)));weight=weight*weight*(3-2*weight)
    local dx=(math.sin((k-1)*math.pi/2+phase)-math.sin(phase))*amplitude*weight
    moving:drawPixel(x,y,dx==0 and orig:getPixel(x,y) or sample(orig,x-dx,y))
   end
  end end
  s:newCel(layers[j].moving,k,moving,Point(0,0));s:newCel(layers[j].fixed,k,fixed,Point(0,0))
  moving:saveAs(P..string.format('/tuft-%d-upper-%d.png',j-1,k-1));fixed:saveAs(P..string.format('/tuft-%d-base.png',j-1))
  local flat=Image(W,H,ColorMode.RGB);flat:drawImage(moving);flat:drawImage(fixed);flat:saveAs(P..string.format('/tuft-%d-cel-%d.png',j-1,k-1))
 end
 local flat=Image(s.spec);flat:drawSprite(s,k);flat:saveAs(P..string.format('/group-cel-%d.png',k-1))
end
s:saveAs(P..'/three-grass-tufts-four-cels.aseprite');s:close();s=app.open(P..'/three-grass-tufts-four-cels.aseprite');assert(#s.frames==4 and #s.layers==6)
for k=1,4 do local flat=Image(s.spec);flat:drawSprite(s,k);flat:saveAs(P..string.format('/group-reopen-%d.png',k-1)) end
s:close();print('PASS native 4 frames, 6 layers, three complete crowns and fixed roots')
