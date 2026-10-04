local root=app.params.packet
local count=41
local take=app.params.take or 'registered'
local rgb=app.pixelColor
local plate=Image{fromFile=root..'/inputs/fixed_body_plate.png'}
local s=Sprite(896,512,ColorMode.RGB)
s.layers[1].name='Native decoded LTX frames (hidden, unchanged)';s.layers[1].isVisible=false
local rawLayer=s.layers[1]
local isolatedLayer=s:newLayer();isolatedLayer.name='Full generated matte (hidden diagnostic)';isolatedLayer.isVisible=false
local armLayer=s:newLayer();armLayer.name='Generated waving region; approved source arm at endpoints 0 and 40'
local bodyLayer=s:newLayer();bodyLayer.name='Approved source body plate; unchanged opaque pixels'
local poly={{240,25},{455,25},{455,340},{240,340}}
local function inside(x,y)
 local c=false;local j=#poly
 for i=1,#poly do local a=poly[i];local b=poly[j]
  if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then c=not c end
  j=i
 end
 return c
end
for index=0,count-1 do
 local raw=Image{fromFile=root..string.format('/results/'..take..'/native_frames/%04d.png',index)}
 local clean=Image(raw);local q={};local head=1;local tail=0
 local function add(x,y)
  if x<0 or y<0 or x>=896 or y>=512 then return end
  local px=clean:getPixel(x,y)
  if rgb.rgbaA(px)==0 then return end
  if math.max(math.abs(rgb.rgbaR(px)-238),math.abs(rgb.rgbaG(px)-238),math.abs(rgb.rgbaB(px)-238))<=12 then
   clean:drawPixel(x,y,0);tail=tail+1;q[tail]=y*896+x
  end
 end
 for x=0,895 do add(x,0);add(x,511) end
 for y=1,510 do add(0,y);add(895,y) end
 while head<=tail do local k=q[head];q[head]=nil;head=head+1;local x=k%896;local y=math.floor(k/896);add(x-1,y);add(x+1,y);add(x,y-1);add(x,y+1) end
 local arm=Image(896,512,ColorMode.RGB)
 for y=25,339 do for x=240,454 do if inside(x+0.5,y+0.5) then arm:drawPixel(x,y,clean:getPixel(x,y)) end end end
 if index>0 then s:newFrame() end
 if index==0 or index==40 then arm=Image{fromFile=root..'/inputs/registered_arm_00.png'} end
 s:newCel(rawLayer,index+1,raw,Point(0,0));s:newCel(isolatedLayer,index+1,clean,Point(0,0));s:newCel(armLayer,index+1,arm,Point(0,0));s:newCel(bodyLayer,index+1,plate,Point(0,0))
 s.frames[index+1].duration=(math.floor((index+1)*1000/24+0.5)-math.floor(index*1000/24+0.5))/1000
 local final=Image(arm);final:drawImage(plate,Point(0,0))
 final:saveAs(root..string.format('/results/finished_'..take..'/frames/%04d.png',index))
 clean:saveAs(root..string.format('/results/isolated_'..take..'/frames/%04d.png',index))
end
for _,x in ipairs({{1,7,'rest_and_anticipation'},{8,18,'raise'},{19,28,'lower'},{29,41,'settle'}}) do local t=s:newTag(x[1],x[2]);t.name=x[3] end
local joint=s:newSlice(Rectangle(0,0,896,512));joint.name='STUDY_ONLY_shoulder';joint.pivot=Point(437,207)
s:saveAs(root..'/results/finished_'..take..'/wave.aseprite');s:close()
