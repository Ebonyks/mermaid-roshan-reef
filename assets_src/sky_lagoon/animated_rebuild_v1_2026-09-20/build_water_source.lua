local base = app.params.base
local input = app.open(app.params.atlas)
local atlas = Image(input.cels[1].image)
input:close()
local sprite = Sprite(256,256,ColorMode.RGB)
sprite.layers[1].name = 'approved_water_ring'
for frame=1,8 do
 if frame > 1 then sprite:newEmptyFrame() end
 local image = Image(256,256,ColorMode.RGB)
 image:drawImage(atlas, Point(-((frame-1)%4)*256,-math.floor((frame-1)/4)*256))
 sprite:newCel(sprite.layers[1],frame,image,Point(0,0))
 sprite.frames[frame].duration = 0.12
end
local tag = sprite:newTag(1,8)
tag.name = 'tap_once_fade'
sprite:saveAs(base .. '/water/ripple-eight-cels.aseprite')
sprite:close()
