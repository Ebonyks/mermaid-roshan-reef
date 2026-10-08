local base = 'assets_src/imagegen/astronaut_pipe_raster_repair_20261007/'
local started = os.clock()
local sprite = assert(app.open(base .. 'RAW_TAKE_01.png'))
assert(sprite.width == 1254 and sprite.height == 1254)
local before = Image(sprite)
local clean = Image(before)
local removed = 0
for pixel in clean:pixels() do
 local c = pixel()
 if app.pixelColor.rgbaA(c) <= 1 then
  if app.pixelColor.rgbaA(c) == 1 then removed = removed + 1 end
  pixel(app.pixelColor.rgba(0, 0, 0, 0))
 end
end
sprite.layers[1].name = 'Raw ImageGen source - preserved hidden'
sprite.layers[1].isVisible = false
local layer = sprite:newLayer()
layer.name = 'Painted whole pipe - alpha1 fringe removed'
sprite:newCel(layer, 1, clean, Point(0, 0))
sprite:saveAs(base .. 'STRAIGHT_EDITABLE_NATIVE.aseprite')
sprite:saveCopyAs(base .. 'STRAIGHT_CLEAN_NATIVE.png')
app.command.SpriteSize { ui = false, width = 1024, height = 1024, lockRatio = true, method = 'bilinear' }
assert(sprite.width == 1024 and sprite.height == 1024)
sprite:saveCopyAs(base .. 'STRAIGHT_RUNTIME_CANDIDATE_1024.png')
sprite:close()
local native = assert(app.open(base .. 'STRAIGHT_EDITABLE_NATIVE.aseprite'))
local rendered = Image(native)
local exact = rendered:isEqual(clean)
assert(exact, 'Editable native round-trip changed pixels')
local f = assert(io.open(base .. 'STRAIGHT_CLEANUP_V1_ASEPRITE_RECEIPT.json', 'w'))
f:write(json.encode { result = 'PASS_ASEPRITE_ONLY', version = tostring(app.version), alpha1_removed_pixels = removed, native_dimensions = { 1254, 1254 }, export_dimensions = { 1024, 1024 }, master_round_trip_exact = exact, source_pixels_not_repainted = true, cpu_seconds = os.clock() - started })
f:close()
native:close()
