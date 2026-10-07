-- Static A2 matte derivative; no generated pixels, spatial changes or repainting.
local sourcePath = app.params['source']
local destination = app.params['destination']
local reviewDir = app.params['review']
assert(sourcePath and destination and reviewDir)
local src = Image{fromFile=sourcePath}
assert(src.width == 1024 and src.height == 1536)
local pc = app.pixelColor
local clean = Image(src)
local mask = Image(src.width, src.height, ColorMode.RGB)
local low, high = 64, 240
local removed, softened, unchanged = 0, 0, 0
for it in clean:pixels() do
  local p = it()
  local a = pc.rgbaA(p)
  local outA = a
  if a <= low then
    outA = 0
    if p ~= 0 then removed = removed + 1 end
    it(0) -- erase invisible colored RGB as well as low-alpha fringe
  elseif a < high then
    outA = math.floor(a * (a - low) / (high - low) + 0.5)
    it(pc.rgba(pc.rgbaR(p), pc.rgbaG(p), pc.rgbaB(p), outA))
    softened = softened + 1
  else
    unchanged = unchanged + 1 -- exact RGBA, including original alpha
  end
  local keep = (a == 0) and 0 or math.floor(outA * 255 / a + 0.5)
  mask:drawPixel(it.x, it.y, pc.rgba(255, 255, 255, keep))
end

local sprite = Sprite(src.width, src.height, ColorMode.RGB)
local original = sprite.layers[1]
original.name = 'Original A2 — hidden, unchanged'
sprite:newCel(original, 1, src, Point(0, 0))
original.isVisible = false
original.isEditable = false
local matteLayer = sprite:newLayer()
matteLayer.name = 'Editable alpha keep mask — hidden'
sprite:newCel(matteLayer, 1, mask, Point(0, 0))
matteLayer.isVisible = false
local cleanLayer = sprite:newLayer()
cleanLayer.name = 'Clean RGBA — static derivative'
sprite:newCel(cleanLayer, 1, clean, Point(0, 0))
sprite.data = 'A2 source hash and rights in JOB_CARD.json; alpha-only derivative, preserve painted contours; not motion or runtime acceptance.'
sprite:saveAs(destination .. '/berry_pickup_a2_clean.aseprite')
clean:saveAs(destination .. '/berry_pickup_a2_clean.png')
mask:saveAs(destination .. '/alpha_keep_mask.png')
src:saveAs(destination .. '/original_layer_export.png')

local function flat(image, color)
  local out = Image(image.width, image.height, ColorMode.RGB)
  out:clear(color)
  out:drawImage(image, Point(0, 0))
  return out
end
local light = pc.rgba(246, 240, 252, 255)
local dark = pc.rgba(25, 24, 40, 255)
flat(src, light):saveAs(reviewDir .. '/original_native_light.png')
flat(clean, light):saveAs(reviewDir .. '/clean_native_light.png')
flat(src, dark):saveAs(reviewDir .. '/original_native_dark.png')
flat(clean, dark):saveAs(reviewDir .. '/clean_native_dark.png')

local background = Image{fromFile=app.params['background']}
background:resize{width=1280, height=720, method='bilinear'}
local function atGameScale(image, kind, name)
  local small = Image(image)
  small:resize{width=167, height=250, method='bilinear'}
  local out
  if kind == 'game' then
    out = Image(background)
  else
    out = Image(1280, 720, ColorMode.RGB)
    out:clear(kind == 'light' and light or dark)
  end
  -- Fit within the actual captured 250x250 actor box; center the portrait.
  out:drawImage(small, Point(539, 306))
  out:saveAs(reviewDir .. '/' .. name .. '_250px_' .. kind .. '.png')
end
for _, kind in ipairs({'light', 'dark', 'game'}) do
  atGameScale(src, kind, 'original')
  atGameScale(clean, kind, 'clean')
end
Image(src, Rectangle(710, 260, 314, 210)):saveAs(reviewDir .. '/original_tongs_detail.png')
Image(clean, Rectangle(710, 260, 314, 210)):saveAs(reviewDir .. '/clean_tongs_detail.png')
sprite:close()
print('CANDY_STATIC_MATTE|removed_or_cleared=' .. removed .. '|edge_softened=' .. softened .. '|exact_core=' .. unchanged)
