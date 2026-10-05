local root=app.params.root
local out=app.params.out
local atlas=app.open(root..'/assets/characters/roshan_25d/roshan_gesture_a.png')
local rgb=app.pixelColor
local polygons={
 {{426,222},{445,222},{444,242},{438,258},{431,275},{421,295},{422,320},{414,331},{392,331},{383,317},{388,300},{401,275},{409,251},{420,228}},
 {{417,194},{436,206},{420,233},{396,241},{385,230},{367,180},{366,149},{393,147},{398,175},{404,193}},
 {{388,197},{404,217},{385,230},{369,210},{354,176},{339,124},{323,87},{326,59},{355,52},{371,74},{367,99},{383,150}},
 {{365,193},{386,207},{372,228},{339,240},{320,227},{308,189},{296,165},{296,133},{326,128},{337,159},{337,191}}
}
local shifts={{0,0},{23,-3},{50,-9},{74,-6}}
local function inside(x,y,poly)
 local c=false;local j=#poly
 for i=1,#poly do
  local a=poly[i];local b=poly[j]
  if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then c=not c end
  j=i
 end
 return c
end
local originals={};local arms={}
for i=1,4 do
 local cell=Image(atlas.cels[1].image,Rectangle((i-1)*256,0,256,256))
 local temp=Sprite(256,256,ColorMode.RGB);temp.cels[1].image=cell
 app.command.SpriteSize{width=460,height=460,method='bilinear'}
 local full=Image(896,512,ColorMode.RGB);full:drawImage(temp.cels[1].image,Point(218,26));originals[i]=full
 local arm=Image(896,512,ColorMode.RGB)
 for y=0,511 do for x=0,895 do
  if inside(x+0.5,y+0.5,polygons[i]) then
   local tx=x+shifts[i][1];local ty=y+shifts[i][2]
   if tx>=0 and tx<896 and ty>=0 and ty<512 then arm:drawPixel(tx,ty,full:getPixel(x,y)) end
  end
 end end
 arms[i]=arm
 full:saveAs(out..string.format('/source_rgba_%02d.png',i-1))
 temp:close()
end
local plate=Image(originals[1])
for y=0,511 do for x=0,895 do if inside(x+0.5,y+0.5,polygons[1]) then plate:drawPixel(x,y,0) end end end
plate:saveAs(out..'/fixed_body_plate.png')
local s=Sprite(896,512,ColorMode.RGB)
s.layers[1].name='Neutral gray for local video conditioning'
local bgLayer=s.layers[1]
local armLayer=s:newLayer();armLayer.name='Source-bound moving arm; registered study shoulder'
local bodyLayer=s:newLayer();bodyLayer.name='Approved face torso tail and opposite arm; fixed pixels'
local sourceLayer=s:newLayer();sourceLayer.name='Original authored keys (hidden)';sourceLayer.isVisible=false
for k=1,5 do
 local i=k==5 and 1 or k
 if k>1 then s:newFrame() end
 local bg=Image(896,512,ColorMode.RGB);bg:clear(Color{r=238,g=238,b=238,a=255})
 s:newCel(bgLayer,k,bg,Point(0,0));s:newCel(armLayer,k,arms[i],Point(0,0));s:newCel(bodyLayer,k,plate,Point(0,0));s:newCel(sourceLayer,k,originals[i],Point(0,0))
 s.frames[k].duration=({0.3,0.4,0.4,0.4,0.208333333})[k]
 local composite=Image(896,512,ColorMode.RGB);composite:drawImage(arms[i],Point(0,0));composite:drawImage(plate,Point(0,0))
 composite:saveAs(out..string.format('/registered_rgba_%02d.png',k-1))
 local gray=Image(bg);gray:drawImage(composite,Point(0,0));gray:saveAs(out..string.format('/registered_key_%02d.png',k-1))
 arms[i]:saveAs(out..string.format('/registered_arm_%02d.png',k-1))
end
local tag=s:newTag(1,5);tag.name='one_shot_greeting_source_keys'
local slice=s:newSlice(Rectangle(0,0,896,512));slice.name='STUDY_ONLY_shoulder';slice.pivot=Point(437,207)
s:saveAs(out..'/registered_keys.aseprite')
s:saveAs(out..'/registered_keys.gif')
s:close();atlas:close()
