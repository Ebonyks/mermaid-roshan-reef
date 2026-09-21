local p=app.params.base
local W,H=640,426
local px,py=798*640/1537,917*640/1537
local names={'right_outer','left_outer','center','right_upper','left_upper','right_mid','left_mid','roots_fixed'}
local angles={{0,-1.2,.8,.3},{0,-1.1,.7,.2},{0,-1.8,1.3,.3},{0,-1.6,1.1,.2},{0,-1.4,1.0,.4},{0,-1.0,.7,.2},{0,-.9,.6,.3},{0,0,0,0}}
local s=Sprite(W,H,ColorMode.RGB)
local layers={}
local sources={}
for j,name in ipairs(names) do
 local l=j==1 and s.layers[1] or s:newLayer();l.name=name;layers[j]=l
 local t=app.open(p..'/'..name..'-working.png');local source=Image(W,H,ColorMode.RGB);local c=t.cels[1];source:drawImage(c.image,c.position);t:close();sources[j]=source
end
local pc=app.pixelColor
local function sample(src,x,y)
 local ix,iy=math.floor(x),math.floor(y)
 local fx,fy=x-ix,y-iy
 local rr,gg,bb,aa=0,0,0,0
 for dy=0,1 do for dx=0,1 do
  local sx,sy=ix+dx,iy+dy
  if sx>=0 and sy>=0 and sx<W and sy<H then
   local c=src:getPixel(sx,sy)
   local wt=(dx==0 and 1-fx or fx)*(dy==0 and 1-fy or fy)
   local aw=pc.rgbaA(c)*wt
   rr=rr+pc.rgbaR(c)*aw;gg=gg+pc.rgbaG(c)*aw;bb=bb+pc.rgbaB(c)*aw;aa=aa+aw
  end
 end end
 if aa<.5 then return 0 end
 return pc.rgba(math.floor(rr/aa+.5),math.floor(gg/aa+.5),math.floor(bb/aa+.5),math.floor(aa+.5))
end
for k=1,4 do
 if k>1 then s:newEmptyFrame() end
 s.frames[k].duration=.65
 for j,name in ipairs(names) do
  local source=sources[j];local im=Image(W,H,ColorMode.RGB)
  if k==1 then im:drawImage(source,Point(0,0)) else
   for y=0,H-1 do for x=0,W-1 do
    local dx,dy=x-px,y-py
    local distance=math.sqrt(dx*dx+dy*dy)
    local lock=math.max(0,math.min(1,(distance-14)/65))
    lock=lock*math.max(0,math.min(1,(375-y)/45))
    local angle=-angles[j][k]*2*math.pi/180*lock
    local cs,sn=math.cos(angle),math.sin(angle)
    local sx,sy=px+dx*cs-dy*sn,py+dx*sn+dy*cs
    if angle==0 then im:drawPixel(x,y,source:getPixel(x,y)) else im:drawPixel(x,y,sample(source,sx,sy)) end
   end end
  end
  s:newCel(layers[j],k,im,Point(0,0)); im:saveAs(p..'/'..name..string.format('-cel-%02d.png',k-1))
 end
 local log=io.open(p..'/author-progress.txt','a');log:write('POSE '..k..' authored\n');log:close()
end
app.activeSprite=s
s:newTag(1,4).name='grass_fan_breeze_study'
s:saveAs(p..'/grass-fan-four-cels.aseprite')
for k=1,4 do
 local flat=Image(W,H,ColorMode.RGB);flat:drawSprite(s,k);flat:saveAs(p..string.format('/cel-%02d.png',k-1))
end
s:close()
