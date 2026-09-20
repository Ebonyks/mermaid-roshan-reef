local base = app.params.base
local source = app.open(base .. '/bridge/reference_locked.png')
assert(source, 'source missing')
local width,height = source.width,source.height
source:close()
local target = Sprite(width,height,ColorMode.RGB)
target.layers[1].name = 'contact_shadow'
local names = {'supports_fixed','deck_boards','rear_chain','front_chain','front_posts','reference_locked'}
for _,name in ipairs(names) do
 local input = app.open(base .. '/bridge/' .. name .. '.png')
 local layer = target:newLayer()
 layer.name = name
 target:newCel(layer,1,Image(input.cels[1].image),input.cels[1].position)
 layer.isVisible = name ~= 'reference_locked'
 if name == 'reference_locked' then layer.isEditable = false end
 input:close()
end
target.frames[1].duration = 0.1
local tag = target:newTag(1,1)
tag.name = 'rest'
app.activeSprite = target
target:saveAs(base .. '/bridge/bridge-authoring-v1.aseprite')
target:close()
