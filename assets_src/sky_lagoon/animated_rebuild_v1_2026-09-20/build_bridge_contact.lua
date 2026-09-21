-- Gameplay-only contact trial: baked local deck flex, not cinematic delivery.
-- Source-locked castle and railings; no translation of the bridge sprite.
local base = app.params.base
local input = app.open(base .. '/bridge/reference_locked.png')
local original = Image(input.width,input.height,ColorMode.RGB)
original:drawImage(input.cels[1].image,input.cels[1].position)
input:close()
local ox,oy,w,h=136,872,192,112
local sprite=Sprite(w,h,ColorMode.RGB)
local layer=sprite.layers[1]; layer.name='front_planks_contact'
local offsets={0,-0.5,0,2,4,5,3,1,-1,0.6,0.2,0}
local durations={0.05,0.05,0.04,0.05,0.07,0.07,0.06,0.06,0.05,0.06,0.06,0.10}
local pc=app.pixelColor
local function sample(x,y)
 local y0=math.floor(y);local t=y-y0
 local a=original:getPixel(x,y0); local b=original:getPixel(x,y0+1)
 local function blend(fn)return math.floor(fn(a)*(1-t)+fn(b)*t+0.5)end
 return pc.rgba(blend(pc.rgbaR),blend(pc.rgbaG),blend(pc.rgbaB),blend(pc.rgbaA))
end
for f,offset in ipairs(offsets) do
 if f>1 then sprite:newEmptyFrame() end
 sprite.frames[f].duration=durations[f]
 local cel=Image(w,h,ColorMode.RGB)
 for y=0,h-1 do
  for x=0,w-1 do
   -- Compact ellipse wholly within exposed floor, with zero displacement at boundary.
   -- Its oblique centre follows the authored front plank field.
   local u=(x-96)/82;local v=(y-57)/39
   local q=math.max(0,1-u*u-v*v)
   local displacement=offset*q*q
   cel:drawPixel(x,y,sample(ox+x,oy+y-displacement))
  end
 end
 sprite:newCel(layer,f,cel,Point(0,0))
end
local tag=sprite:newTag(1,12);tag.name='front_contact'
app.activeSprite=sprite
sprite:saveAs(base .. '/bridge/bridge-contact-trial.aseprite')
sprite:close()
