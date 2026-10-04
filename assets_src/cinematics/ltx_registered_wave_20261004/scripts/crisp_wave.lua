local root=app.params.packet
local rgb=app.pixelColor
local plate=Image{fromFile=root..'/inputs/fixed_body_plate.png'}
local arms={};for i=0,3 do arms[i+1]=Image{fromFile=root..string.format('/inputs/registered_arm_%02d.png',i)} end
local joints={
 {{437,225},{416,277},{397,306},{399,335}},
 {{437,225},{414,226},{399,181},{399,140}},
 {{437,225},{420,159},{401,103},{392,40}},
 {{437,225},{410,229},{384,186},{383,121}}
}
local radii={28,28,28,31}
local keys={0,7,17,27,36,40};local pose={1,2,3,4,1,1}
local function atan2(y,x) return math.atan(y,x) end
local function geometry(points)
 local g={};for i=1,3 do local dx=points[i+1][1]-points[i][1];local dy=points[i+1][2]-points[i][2];g[i]={angle=atan2(dy,dx),length=math.sqrt(dx*dx+dy*dy)} end;return g
end
local function mesh(points)
 local g=geometry(points);local v={}
 for i=1,4 do
  local angle
  if i==1 then angle=g[1].angle elseif i==4 then angle=g[3].angle else
   local a=g[i-1].angle;local delta=(g[i].angle-a+math.pi)%(2*math.pi)-math.pi;angle=a+delta/2
  end
  local nx=-math.sin(angle)*radii[i];local ny=math.cos(angle)*radii[i]
  v[#v+1]={points[i][1]+nx,points[i][2]+ny};v[#v+1]={points[i][1]-nx,points[i][2]-ny}
 end;return v
end
local tris={{1,2,3},{2,4,3},{3,4,5},{4,6,5},{5,6,7},{6,8,7}}
local function sample(im,x,y)
 local ix=math.floor(x);local iy=math.floor(y);local fx=x-ix;local fy=y-iy
 local ra,ga,ba,aa=0,0,0,0
 for dy=0,1 do for dx=0,1 do
  local sx=ix+dx;local sy=iy+dy
  if sx>=0 and sy>=0 and sx<896 and sy<512 then
   local c=im:getPixel(sx,sy);local a=rgb.rgbaA(c)/255;local w=(dx==0 and 1-fx or fx)*(dy==0 and 1-fy or fy)
   ra=ra+rgb.rgbaR(c)*a*w;ga=ga+rgb.rgbaG(c)*a*w;ba=ba+rgb.rgbaB(c)*a*w;aa=aa+a*w
  end
 end end
 if aa<0.001 then return 0 end
 return rgb.rgba(math.floor(ra/aa+0.5),math.floor(ga/aa+0.5),math.floor(ba/aa+0.5),math.floor(aa*255+0.5))
end
local function mapArm(source,src,dst)
 local im=Image(896,512,ColorMode.RGB);local sm=mesh(src);local dm=mesh(dst)
 for _,t in ipairs(tris) do
  local a,b,c=dm[t[1]],dm[t[2]],dm[t[3]];local sa,sb,sc=sm[t[1]],sm[t[2]],sm[t[3]]
  local den=(b[2]-c[2])*(a[1]-c[1])+(c[1]-b[1])*(a[2]-c[2])
  if math.abs(den)>0.001 then
   local x0=math.max(0,math.floor(math.min(a[1],b[1],c[1])));local x1=math.min(895,math.ceil(math.max(a[1],b[1],c[1])))
   local y0=math.max(0,math.floor(math.min(a[2],b[2],c[2])));local y1=math.min(511,math.ceil(math.max(a[2],b[2],c[2])))
   for y=y0,y1 do for x=x0,x1 do
    local u=((b[2]-c[2])*(x-c[1])+(c[1]-b[1])*(y-c[2]))/den
    local v=((c[2]-a[2])*(x-c[1])+(a[1]-c[1])*(y-c[2]))/den;local w=1-u-v
    if u>=-0.0001 and v>=-0.0001 and w>=-0.0001 then im:drawPixel(x,y,sample(source,u*sa[1]+v*sb[1]+w*sc[1],u*sa[2]+v*sb[2]+w*sc[2])) end
   end end
  end
 end;return im
end
local s=Sprite(896,512,ColorMode.RGB);local armLayer=s.layers[1];armLayer.name='Crisp approved source arm; authored joint in-betweens'
local bodyLayer=s:newLayer();bodyLayer.name='Approved source body; fixed opaque pixels'
local nativeLayer=s:newLayer();nativeLayer.name='Rejected LTX strength 2 motion reference (hidden)';nativeLayer.isVisible=false
local rows={}
for index=0,40 do
 local seg=1;while seg<#keys-1 and index>keys[seg+1] do seg=seg+1 end
 local t=(index-keys[seg])/(keys[seg+1]-keys[seg]);t=math.max(0,math.min(1,t));local eased=t*t*(3-2*t)
 local a=pose[seg];local b=pose[seg+1];local selected=eased<0.5 and a or b
 local ga=geometry(joints[a]);local gb=geometry(joints[b]);local target={{437,225}}
 for k=1,3 do
  local delta=(gb[k].angle-ga[k].angle+math.pi)%(2*math.pi)-math.pi;local angle=ga[k].angle+delta*eased
  if k==3 then
   local la=(ga[3].angle-ga[2].angle+math.pi)%(2*math.pi)-math.pi
   local lb=(gb[3].angle-gb[2].angle+math.pi)%(2*math.pi)-math.pi
   local ld=(lb-la+math.pi)%(2*math.pi)-math.pi
   local lowerDelta=(gb[2].angle-ga[2].angle+math.pi)%(2*math.pi)-math.pi
   angle=ga[2].angle+lowerDelta*eased+la+ld*eased
  end
  local length=ga[k].length+(gb[k].length-ga[k].length)*eased
  target[k+1]={target[k][1]+math.cos(angle)*length,target[k][2]+math.sin(angle)*length}
 end
 local arm
 if a==b or t==0 or t==1 then selected=t==1 and b or a;arm=Image(arms[selected]) else arm=mapArm(arms[selected],joints[selected],target) end
 if index>0 then s:newFrame() end
 s.frames[index+1].duration=(math.floor((index+1)*1000/24+0.5)-math.floor(index*1000/24+0.5))/1000
 s:newCel(armLayer,index+1,arm,Point(0,0));s:newCel(bodyLayer,index+1,plate,Point(0,0))
 local native=Image{fromFile=root..string.format('/results/registered_strong/native_frames/%04d.png',index)};s:newCel(nativeLayer,index+1,native,Point(0,0))
 local final=Image(arm);final:drawImage(plate,Point(0,0));final:saveAs(root..string.format('/results/crisp_authored/frames/%04d.png',index))
 rows[#rows+1]={index=index,source_arm=selected-1,segment=seg,eased=eased,target_joints=target,temporal_pixel_blending=false}
end
for _,x in ipairs({{1,8,'raise_to_shoulder'},{9,18,'raise_above_head'},{19,28,'lower_greeting'},{29,37,'return_to_rest'},{38,41,'intentional_rest_settle'}}) do local tag=s:newTag(x[1],x[2]);tag.name=x[3] end
local slice=s:newSlice(Rectangle(0,0,896,512));slice.name='STUDY_ONLY_shoulder';slice.pivot=Point(437,225)
s:saveAs(root..'/results/crisp_authored/wave.aseprite')
local file=io.open(root..'/results/crisp_authored/frame_mapping.json','w');file:write(json.encode{method='Aseprite authored cutout mesh; single spatial bilinear resample, no temporal blending',fps=24,frames=rows,source_joints=joints,body='inputs/fixed_body_plate.png',native_role='Hidden diagnostic reference only; no generated pixels in visible result',acceptance='REFERENCE_ONLY'});file:close();s:close()
