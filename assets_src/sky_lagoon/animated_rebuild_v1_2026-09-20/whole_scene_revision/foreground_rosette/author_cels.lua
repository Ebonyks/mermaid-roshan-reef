local p=app.params.base
local W,H=640,504
local px,py=690*640/1414,530*640/1414
local names={'back_leaf_fan','right_rear_tip','lower_hanging','right_broad','left_broad','front_small_right','front_main','bud_cluster'}
local angles={
 {0,-.55,-.9,-.2,.7,.45},
 {0,-.8,-1.3,-.25,1.0,.65},
 {0,-.35,-.7,-.2,.5,.35},
 {0,-.7,-1.25,-.3,.85,.65},
 {0,-1.0,-1.6,-.3,1.1,.7},
 {0,-.55,-.9,-.2,.65,.4},
 {0,-.4,-.8,-.2,.55,.35},
 {0,-.3,-1.0,-.65,.5,.65}
}
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
for k=1,6 do
 if k>1 then s:newEmptyFrame() end
 s.frames[k].duration=.38
 for j,name in ipairs(names) do
  local source=sources[j];local im=Image(W,H,ColorMode.RGB)
  if k==1 then im:drawImage(source,Point(0,0)) else
   for y=0,H-1 do for x=0,W-1 do
    local dx,dy=x-px,y-py
    local distance=math.sqrt(dx*dx+dy*dy)
    local lock=math.max(0,math.min(1,(distance-14)/65))
    local angle=-angles[j][k]*2*math.pi/180*lock
    local cs,sn=math.cos(angle),math.sin(angle)
    local sx,sy=px+dx*cs-dy*sn,py+dx*sn+dy*cs
    im:drawPixel(x,y,sample(source,sx,sy))
   end end
  end
  s:newCel(layers[j],k,im,Point(0,0)); im:saveAs(p..'/'..name..string.format('-cel-%02d.png',k-1))
 end
 local log=io.open(p..'/author-progress.txt','a');log:write('POSE '..k..' authored\n');log:close()
end
app.activeSprite=s
s:newTag(1,6).name='coordinated_rosette_breeze_study'
s:saveAs(p..'/rosette-six-cels.aseprite')
for k=1,6 do
 local flat=Image(W,H,ColorMode.RGB);flat:drawSprite(s,k);flat:saveAs(p..string.format('/cel-%02d.png',k-1))
end
s:close()
