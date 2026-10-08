local base = 'assets_src/imagegen/astronaut_engineering_devices_20261007/'
local sprite = assert(app.open(base .. 'FLUID_RAW_TAKE_01.png'))
local source = Image(sprite)
sprite.layers[1].name = 'Original built-in ImageGen fluid - preserved'
sprite:saveAs(base .. 'FLUID_NATIVE.aseprite')
sprite:close()
local native = assert(app.open(base .. 'FLUID_NATIVE.aseprite'))
assert(Image(native):isEqual(source), 'Native master pixels changed')
app.command.SpriteSize { ui=false, width=1024, height=1024, lockRatio=true, method='bilinear' }
native:saveCopyAs('assets/opera/worlds/widgets/astronaut_radioactive_fluid_v1.png')
native:close()
local file = assert(io.open(base .. 'FLUID_ASEPRITE_RECEIPT.json','w'))
file:write(json.encode { version=tostring(app.version), native_roundtrip_exact=true, runtime_dimensions={1024,1024}, method='Whole-canvas bilinear scaling, no repaint or crop' })
file:close()
