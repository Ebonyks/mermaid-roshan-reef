local source = app.params.source
local master = app.params.master
local output = app.params.output
local receipt = app.params.receipt
local spr = app.open(source)
assert(spr and spr.colorMode == ColorMode.RGB)
assert(spr.width == 1328 and spr.height == 1184 and #spr.frames == 1)
local oldCel = spr.cels[1]
local raw = oldCel.image
local cleaned = Image(raw)
local removed = 0
for pixel in cleaned:pixels() do
  local c = pixel()
  local a = app.pixelColor.rgbaA(c)
  if a > 0 and a < 16 then
    pixel(app.pixelColor.rgba(app.pixelColor.rgbaR(c), app.pixelColor.rgbaG(c), app.pixelColor.rgbaB(c), 0))
    removed = removed + 1
  end
end
local original = oldCel.layer
original.name = "Original take02 - preserved hidden"
original.isVisible = false
local layer = spr:newLayer()
layer.name = "Matte01 - only alpha1to15 cleared"
layer.isVisible = true
spr:newCel(layer, 1, cleaned, oldCel.position)
spr:saveAs(master)
local f = io.open(receipt, "w")
f:write("aseprite_version=" .. tostring(app.version) .. "\n")
f:write("removed_low_alpha_pixels=" .. removed .. "\n")
f:write("master_width=" .. spr.width .. "\nmaster_height=" .. spr.height .. "\n")
f:write("layers=" .. #spr.layers .. "\n")
f:write("original_visible=" .. tostring(original.isVisible) .. "\n")
f:write("cleaned_visible=" .. tostring(layer.isVisible) .. "\n")
f:close()
-- Saved native master retains the full canvas and unmodified imported source layer.
-- Crop only the exported working document, with16transparent pixels around retained body.
spr:crop(Rectangle(219, 93, 970, 1015))
spr:saveCopyAs(output)
spr:close()
