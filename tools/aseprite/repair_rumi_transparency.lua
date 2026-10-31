local src=app.open('assets_src/characters/rumi_2026-08-22/rumi_eight_pose_atlas.png');local im=Image(src)
local f=io.open('assets_src/repairs/rumi_transparency_2026-09-30/ownership.json');local runs=json.decode(f:read('*a'));f:close()
local owned={}
for i,spans in ipairs(runs) do local a=Image(1024,768,ColorMode.RGB);for _,r in ipairs(spans) do for x=r[2],r[3]-1 do a:drawPixel(x,r[1],im:getPixel(x,r[1])) end end;owned[i]=a end
local out=Image(1024,768,ColorMode.RGB)
for i,a in ipairs(owned) do
 local delta=({[1]=-215,[3]=249,[4]=485})[i];local dy=({[1]=0,[3]=7,[4]=2})[i]
 if delta then
  for sy=181,370 do
   local left=345
   if sy>=220 then left=math.floor(345-(sy-220)*1.1) end
   left=math.max(290,left)
   local right=(sy<230) and 425 or 445
   for sx=left,right do a:drawPixel(sx+delta,sy+dy,owned[2]:getPixel(sx,sy)) end
  end
 end
 -- Preserve the prior 240/256 pixel scale except the wider curled swimming pose.
 local cell=Image(320,384,ColorMode.RGB);cell:drawImage(a,Point(-((i-1)%4)*256+48,-math.floor((i-1)/4)*384))
 local s=Sprite(320,384,ColorMode.RGB);s.cels[1].image=cell
 local scale=(i==7) and 0.85 or 0.9375
 app.command.SpriteSize{ui=false,width=math.floor(320*scale),height=math.floor(384*scale),method='bilinear'}
 local pic=Image(s);s:close()
 local dx=({0,0,0,19,0,12,34,21})[i]
 out:drawImage(pic,Point(((i-1)%4)*256+8-math.floor(48*scale)+dx,math.floor((i-1)/4)*384+12))
end
local s=app.open('assets_src/repairs/rumi_transparency_2026-09-30/rumi_before.png');s.layers[1].name='Previous export (hidden)';s.layers[1].isVisible=false
local layer=s:newLayer();layer.name='Source-owned poses with complete tails';s:newCel(layer,1,out,Point(0,0))
s:saveAs('assets_src/repairs/rumi_transparency_2026-09-30/rumi.aseprite');s:saveCopyAs('assets/characters/rumi/rumi_eight_pose_runtime.png');s:close();src:close()
local pool=app.open('assets_src/repairs/rumi_transparency_2026-09-30/rumi_pool_before.png');local pooled=Image(pool)
for i=0,3 do
 local frame=Image(256,384,ColorMode.RGB);frame:drawImage(out,Point(-(i%2)*256,0))
 local left=256;local right=0;local top=384;local bottom=0
 for y=0,383 do for x=0,255 do if app.pixelColor.rgbaA(frame:getPixel(x,y))>8 then left=math.min(left,x);right=math.max(right,x);top=math.min(top,y);bottom=math.max(bottom,y) end end end
 local cropped=Image(right-left+9,bottom-top+9,ColorMode.RGB);cropped:drawImage(frame,Point(4-left,4-top))
 local small=Sprite(cropped.width,cropped.height,ColorMode.RGB);small.cels[1].image=cropped
 app.command.SpriteSize{ui=false,width=math.floor(cropped.width*0.75+0.5),height=math.floor(cropped.height*0.75+0.5),method='bilinear'}
 local art=Image(small);small:close()
 for y=0,255 do for x=i*256,(i+1)*256-1 do pooled:drawPixel(x,y,0) end end
 pooled:drawImage(art,Point(i*256+math.floor((256-art.width)/2),250-art.height))
end
pool.layers[1].name='Previous atlas (hidden)';pool.layers[1].isVisible=false;local layer=pool:newLayer();layer.name='Complete idle fins; swimming row preserved';pool:newCel(layer,1,pooled,Point(0,0));pool:saveAs('assets_src/repairs/rumi_transparency_2026-09-30/rumi_pool.aseprite');pool:saveCopyAs('assets/characters/rumi/rumi_pool_idle_swim_atlas.png');pool:close()
local board=app.open('assets_src/repairs/rumi_transparency_2026-09-30/board_before.png');local before=Image(board);local repaired=Image(before)
for _,i in ipairs({2,6}) do
 local ox=(i%4)*256;local oy=math.floor(i/4)*188
 local cell=Image(256,188,ColorMode.RGB);cell:drawImage(before,Point(-ox,-oy))
 for _,r in ipairs({{10,112,19,145},{10,160,19,172}}) do for y=r[2],r[4]-1 do for x=r[1],r[3]-1 do cell:drawPixel(x,y,0) end end end
 for y=0,187 do for x=0,255 do repaired:drawPixel(ox+x,oy+y,0) end end
 local moved=Image(256,188,ColorMode.RGB);moved:drawImage(cell,Point(-4,0));repaired:drawImage(moved,Point(ox,oy))
end
-- Solid board backing from the approved room reference. Fill only the reviewed inner polygon.
local polygon={{42,58},{92,42},{128,36},{163,42},{216,58},{216,132},{42,132}}
local function inside(x,y)
 local yes=false;local j=#polygon
 for i=1,#polygon do local a=polygon[i];local b=polygon[j]
  if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then yes=not yes end;j=i
 end
 return yes
end
for i=0,7 do
 local ox=(i%4)*256;local oy=math.floor(i/4)*188
 local sample=repaired:getPixel(ox+47,oy+113)
 for y=36,131 do for x=42,215 do if inside(x,y) then
  local c=repaired:getPixel(ox+x,oy+y);local alpha=app.pixelColor.rgbaA(c)
  if alpha<255 then
   local t=alpha/255
   local function mix(channel) return math.floor(channel(c)*t+channel(sample)*(1-t)+0.5) end
   repaired:drawPixel(ox+x,oy+y,app.pixelColor.rgba(mix(app.pixelColor.rgbaR),mix(app.pixelColor.rgbaG),mix(app.pixelColor.rgbaB),255))
  end
 end end end
end
board.layers[1].name='Previous export (hidden)';board.layers[1].isVisible=false;local layer=board:newLayer();layer.name='Remaining foreign slivers removed';board:newCel(layer,1,repaired,Point(0,0));board:saveAs('assets_src/repairs/rumi_transparency_2026-09-30/board.aseprite');board:saveCopyAs('assets/flats/castle/interactions_v2/craft_room_idea_board_sheet.png');board:close()
