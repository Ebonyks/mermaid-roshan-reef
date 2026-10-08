local base = 'assets_src/imagegen/astronaut_engineering_devices_20261007/'
local sprite = assert(app.open(base .. 'GEAR_RAW_TAKE_01.png'))
local original = Image(sprite)
local clean = Image(original)
local removed = 0
for pixel in clean:pixels() do
 local c = pixel()
 if app.pixelColor.rgbaA(c) <= 1 then
  if app.pixelColor.rgbaA(c) == 1 then removed = removed + 1 end
  pixel(app.pixelColor.rgba(0,0,0,0))
 end
end
sprite.layers[1].name = 'Raw ImageGen source - preserved hidden'
sprite.layers[1].isVisible = false
local layer = sprite:newLayer(); layer.name = 'Painted gear - alpha1 fringe removed'
sprite:newCel(layer,1,clean,Point(0,0))
sprite:saveAs(base .. 'GEAR_NATIVE.aseprite'); sprite:close()
local native = assert(app.open(base .. 'GEAR_NATIVE.aseprite'))
assert(Image(native):isEqual(clean))
app.command.SpriteSize {ui=false,width=1024,height=1024,lockRatio=true,method='bilinear'}
native:saveCopyAs('assets/opera/worlds/widgets/astronaut_gear_v1.png'); native:close()
local file = assert(io.open(base .. 'GEAR_ASEPRITE_RECEIPT.json','w'))
file:write(json.encode { version=tostring(app.version), native_roundtrip_exact=true, alpha1_removed=removed, runtime_dimensions={1024,1024}, method='Alpha<=1 cleanup; whole-canvas bilinear scaling, no repaint/crop' }); file:close()
