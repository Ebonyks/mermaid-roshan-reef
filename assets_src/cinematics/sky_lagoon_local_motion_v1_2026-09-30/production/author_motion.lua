-- Scripted source-based reference animation, not hand-painted or AI-generated poses.
-- Every output pixel is painted into a new RGBA image with Aseprite Image.drawPixel.
local root=app.params.root;local id=app.params.id
local pc=app.pixelColor;local src=Image{fromFile=root..'/source.png'}
local b=dofile(root..'/bounds.lua');local count=32;local duration=1/12
local sprite=Sprite(256,256,ColorMode.RGB)
local moving=sprite.layers[1];moving.name='Scripted motion study - RGBA pixels'
local original=sprite:newLayer();original.name='Preserved source - reference';original.isVisible=false
local function clamp(v,a,z)return math.max(a,math.min(z,v))end
local function pixel(x,y,image)
 if x<0 or y<0 or x>255 or y>255 then return 0 end
 return (image or src):getPixel(x,y)
end
local function sample(x,y,image)
 local ix,iy=math.floor(x),math.floor(y);local fx,fy=x-ix,y-iy
 local values={pixel(ix,iy,image),pixel(ix+1,iy,image),pixel(ix,iy+1,image),pixel(ix+1,iy+1,image)}
 local weights={(1-fx)*(1-fy),fx*(1-fy),(1-fx)*fy,fx*fy}
 local alpha,r,g,bl=0,0,0,0
 for k=1,4 do
  local p=values[k];local a=pc.rgbaA(p)*weights[k]
  alpha=alpha+a;r=r+pc.rgbaR(p)*a;g=g+pc.rgbaG(p)*a;bl=bl+pc.rgbaB(p)*a
 end
 if alpha<.5 then return 0 end
 return pc.rgba(math.floor(r/alpha+.5),math.floor(g/alpha+.5),math.floor(bl/alpha+.5),math.floor(alpha+.5))
end
local rootY=b[4]-18
if id=='04_bellflower' then rootY=b[4]-52 end
if id=='02_huckleberry' then rootY=b[4]-12 end
local amplitudes={['01_fir']=16,['02_huckleberry']=11,['03_hydrangea']=18,['04_bellflower']=17,['06_smoke']=20}
local function sway(x,y,phase)
 local sy=y;local dx,dy=0,0
 for k=1,2 do
  local t=clamp((rootY-sy)/math.max(1,rootY-b[2]),0,1)
  local wave=math.sin(phase)
  if id=='02_huckleberry' then wave=math.sin(phase+(x-128)*.003) end
  if id=='06_smoke' then wave=math.sin(phase-t*math.pi*1.6) end
  dx=amplitudes[id]*wave*t^1.55
  dy=1.4*wave*wave*t*t;sy=y-dy
 end
 return sample(x-dx,sy)
end
local function inPolygon(x,y,points)
 local inside=false;local j=#points
 for i=1,#points do
  local a,z=points[i],points[j]
  if ((a[2]>y)~=(z[2]>y)) and x<(z[1]-a[1])*(y-a[2])/(z[2]-a[2])+a[1] then inside=not inside end
  j=i
 end
 return inside
end
local function swingRegion(x,y)
 local p=pixel(math.floor(x),math.floor(y));local r,g=pc.rgbaR(p),pc.rgbaG(p)
 if pc.rgbaA(p)==0 then return 0 end
 if x>=72 and x<=184 and y>=119 and y<=216 and r>=g*.80 then return 1 end
 if y>=66 and y<=176 then
  if math.abs(x-96.5)<=3.5 or math.abs(x-157)<=3.5 then return 1 end
 end
 return 0
end
local swingFixed;local swingParts
if id=='07_swing' then
 swingFixed=Image(256,256,ColorMode.RGB);swingParts={Image(256,256,ColorMode.RGB)}
 for y=0,255 do for x=0,255 do
  local part=swingRegion(x,y);local p=pixel(x,y)
  if part==0 then swingFixed:drawPixel(x,y,p) else swingParts[part]:drawPixel(x,y,p) end
 end end
 -- Transfer disconnected seat/rope edge pixels left by the coarse isolation.
 -- Keep the connected support frame and all top anchors in the fixed plate.
 local reached={};local queue={};local read=1
 local function mark(x,y)
  if x<0 or y<0 or x>255 or y>255 then return end
  local key=y*256+x+1
  if not reached[key] and pc.rgbaA(swingFixed:getPixel(x,y))>0 then
   reached[key]=true;queue[#queue+1]={x,y}
  end
 end
 for y=0,64 do for x=0,255 do mark(x,y) end end
 while read<=#queue do
  local point=queue[read];read=read+1
  for oy=-1,1 do for ox=-1,1 do mark(point[1]+ox,point[2]+oy) end end
 end
 for y=65,218 do for x=66,194 do
  if not reached[y*256+x+1] then
   local p=swingFixed:getPixel(x,y)
   if pc.rgbaA(p)>0 then swingParts[1]:drawPixel(x,y,p);swingFixed:drawPixel(x,y,0) end
  end
 end end
 swingFixed:saveAs(root..'/fixed_frame_isolated.png')
 swingParts[1]:saveAs(root..'/moving_seat_isolated.png')
end
if app.params.parts_only=='1' then return end
local function swing(x,y,phase)
 local out=pixel(x,y,swingFixed)
 for part=1,1 do
  local wave=math.sin(phase);local dx=12*wave;local dy=-(110-math.sqrt(110^2-dx^2))
  local t=clamp((y-66)/110,0,1)
  local sy=y-dy*t
  local sx=x-dx*clamp((sy-66)/110,0,1)
  local p=sample(sx,sy,swingParts[part]);if pc.rgbaA(p)>0 then out=p end
 end
 return out
end
local function plank(x,y)
 return y<134 and ((x-128)^2+(y-128)^2>11^2)
end
local function seesaw(x,y,phase)
 local fixed=not plank(x,y) and pixel(x,y) or 0
 local angle=.16*math.sin(phase);local c,ss=math.cos(angle),math.sin(angle)
 local rx,ry=x-128,y-128
 local sx=128+c*rx+ss*ry;local sy=128-ss*rx+c*ry
 local p=plank(sx,sy) and sample(sx,sy) or 0
 if pc.rgbaA(p)>0 and not ((x-128)^2+(y-128)^2<=11^2) then return p end
 return fixed
end
local function door(x,y)
 if x<103 or x>157 or y>222 then return false end
 local top=139-math.sqrt(math.max(0,27^2-(x-130)^2))
 return y>=top
end
local function gate(x,y,phase)
 local out=door(x,y) and 0 or pixel(x,y)
 local angle=.98*(.5-.5*math.cos(phase));local compression=math.cos(angle)
 local sx
 if x<=130 then sx=103+(x-103)/compression else sx=157+(x-157)/compression end
 if door(sx,y) and ((x<=130 and sx<=130)or(x>130 and sx>130)) then return sample(sx,y) end
 return out
end
local function cloud(x,y,phase)
 local cx=(b[1]+b[3])/2;local cy=(b[2]+b[4])/2
 local dx=3*math.sin(phase);local swell=1+.05*math.sin(phase)
 local sx=cx+(x-cx-dx)/swell
 local t=clamp((y-b[2])/math.max(1,b[4]-b[2]),0,1)
 local sy=cy+(y-cy)/(1+.07*math.sin(phase+.8))+2*math.sin(phase+(x-cx)*.04)*math.sin(t*math.pi)
 return sample(sx,sy)
end
local function glass(x,y,phase)
 local p=pixel(x,y);local a=pc.rgbaA(p)
 if a==0 then return 0 end
 if x>=111 and x<=151 and y>=70 and y<=130 then
  local r,g,bl=pc.rgbaR(p),pc.rgbaG(p),pc.rgbaB(p)
  if (r+g+bl)/3>85 then
   local center=103+60*phase/(2*math.pi)+(y-100)*.22
   local glint=math.exp(-((x-center)/4.2)^2)*math.sin(phase/2)^2
   local amount=glint*.40
   return pc.rgba(math.floor(r+(255-r)*amount+.5),math.floor(g+(248-g)*amount+.5),math.floor(bl+(242-bl)*amount+.5),a)
  end
 end
 return p
end
app.transaction('Author explicit source-based motion reference poses',function()
 for n=0,count-1 do
  local frame=n==0 and sprite.frames[1] or sprite:newEmptyFrame();frame.duration=duration
  local phase=n/count*2*math.pi;local out=Image(256,256,ColorMode.RGB)
  for y=0,255 do for x=0,255 do
   local p
   if amplitudes[id] then p=sway(x,y,phase)
   elseif id=='05_cloud' then p=cloud(x,y,phase)
   elseif id=='07_swing' then p=swing(x,y,phase)
   elseif id=='08_seesaw' then p=seesaw(x,y,phase)
   elseif id=='09_gate' then p=gate(x,y,phase)
   elseif id=='10_glass' then p=glass(x,y,phase)
   else p=pixel(x,y) end
   if pc.rgbaA(p)==0 then p=0 end
   out:drawPixel(x,y,p)
  end end
  sprite:newCel(moving,frame,out,Point(0,0));sprite:newCel(original,frame,src,Point(0,0))
  out:saveAs(root..string.format('/frames/frame_%02d.png',n))
 end
end)
original.isVisible=false
local tag=sprite:newTag(sprite.frames[1],sprite.frames[count]);tag.name='Scripted reference cycle';tag.aniDir=AniDir.FORWARD
sprite:saveAs(root..'/'..id..'.aseprite')
local f=io.open(root..'/AUTHORING_RECEIPT.json','w')
f:write(string.format('{"method":"Scripted per-pixel RGBA source-based motion: explicit deformation, rigid articulation or traveling light; Aseprite Image.drawPixel","human_hand_drawn":false,"ai_generated_motion":false,"source_appearance_reused":true,"reference_only":true,"production_accepted":false,"frames":32,"frame_seconds":%.12f,"pixels_painted":2097152,"root_lock_y":%d,"aseprite_version":"%s"}',duration,rootY,tostring(app.version)))
f:close();print(id..': 32 explicit motion poses painted in Aseprite')
