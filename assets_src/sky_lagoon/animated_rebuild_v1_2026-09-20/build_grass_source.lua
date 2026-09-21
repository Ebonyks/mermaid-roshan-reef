local base = app.params.base
local target = Sprite(320,320,ColorMode.RGB)
local rootLayer = target.layers[1]
rootLayer.name = 'root_fixed'
local upperLayer = target:newLayer()
upperLayer.name = 'upper_blades'
local rootInput = app.open(base .. '/grass/root_fixed.png')
local rootImage = Image(rootInput.cels[1].image)
local rootPosition = rootInput.cels[1].position
rootInput:close()
local durations = {0.24,0.20,0.24,0.26}
for frame=1,4 do
 if frame > 1 then target:newEmptyFrame() end
 target.frames[frame].duration = durations[frame]
 target:newCel(rootLayer,frame,rootImage,rootPosition)
 local input = app.open(base .. string.format('/grass/upper_%02d.png',frame-1))
 target:newCel(upperLayer,frame,Image(input.cels[1].image),input.cels[1].position)
 input:close()
end
local tag = target:newTag(1,4)
tag.name = 'breeze'
app.activeSprite = target
target:saveAs(base .. '/grass/grass-four-cels.aseprite')
target:close()
