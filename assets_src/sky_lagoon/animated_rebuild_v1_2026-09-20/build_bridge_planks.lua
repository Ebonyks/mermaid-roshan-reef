-- Direct Aseprite gameplay cels: rigid board images, cel-position motion only.
local base=app.params.base
local function loadImage(path)
 local s=app.open(path);local im=Image(s.width,s.height,ColorMode.RGB)
 im:drawImage(s.cels[1].image,s.cels[1].position);s:close();return im
end
local floor=loadImage(base..'/bridge/deck-complete-v2.png')
local supports=loadImage(base..'/bridge/castle-supports-v2.png')
local source=loadImage(base..'/bridge/reference_locked.png')
local bounds={822,844,865,887,909,928,943}
local sprite=Sprite(source.width,source.height,ColorMode.RGB)
local backing=sprite.layers[1];backing.name='concealed_deck_backing'
local fixed=sprite:newLayer();fixed.name='deck_fixed_ends'
local endImage=Image(source.width,source.height,ColorMode.RGB)
local pieces={}
for i=1,6 do pieces[i]=Image(source.width,source.height,ColorMode.RGB) end
local pc=app.pixelColor
local backingImage=Image(floor)
for y=0,floor.height-1 do for x=0,floor.width-1 do
 local c=floor:getPixel(x,y)
 if pc.rgbaA(c)>0 then
  local b=y-.16*x;local found=false
  for i=1,6 do if b>=bounds[i] and b<bounds[i+1] then pieces[i]:drawPixel(x,y,c);found=true;break end end
  if not found then endImage:drawPixel(x,y,c)
  else backingImage:drawPixel(x,y,pc.rgba(156,112,77,pc.rgbaA(c))) end
 end
end end
local layers={};for i=1,6 do local l=sprite:newLayer();l.name='plank_'..i;layers[i]=l end
local structure=sprite:newLayer();structure.name='castle_posts_chains_fixed'
-- Per-frame authored integer offsets. Contact advances from near to next board,
-- then settles; no mesh, texture stretch, interpolated pixels or whole-bridge motion.
local offsets={
 {0,0,0,0,0,0},{0,0,0,0,-1,0},{0,0,0,0,1,1},
 {0,0,0,1,3,2},{0,0,1,2,4,2},{0,0,2,3,3,1},
 {0,1,2,2,1,0},{0,1,1,0,0,0},{0,0,-1,-1,0,0},
 {0,0,0,1,1,0},{0,0,0,0,1,0},{0,0,0,0,0,0}}
local durations={.05,.05,.04,.05,.07,.07,.06,.06,.05,.06,.06,.10}
for f=1,12 do
 if f>1 then sprite:newEmptyFrame() end
 sprite.frames[f].duration=durations[f]
 sprite:newCel(backing,f,backingImage,Point(0,0));sprite:newCel(fixed,f,endImage,Point(0,0))
 for i=1,6 do sprite:newCel(layers[i],f,pieces[i],Point(0,offsets[f][i])) end
 sprite:newCel(structure,f,supports,Point(0,0))
end
local tag=sprite:newTag(1,12);tag.name='footstep_contact'
app.activeSprite=sprite;sprite:saveAs(base..'/bridge/bridge-planks-v3.aseprite');sprite:close()
