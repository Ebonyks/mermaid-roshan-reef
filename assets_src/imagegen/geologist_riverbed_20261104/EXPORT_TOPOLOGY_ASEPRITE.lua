local src = app.open(app.params["junctions"])
local art = src.cels[1].image
local prior = app.open(app.params["atlas01"])
local previous = prior.cels[1].image
local atlas = Sprite(512, 512, ColorMode.RGB)
local assembled = Image(512, 512, ColorMode.RGB)
local pc = app.pixelColor
local function place(index, image, pivot_x, pivot_y, name)
  local x = (index % 4) * 128 + math.floor((128 - image.width) / 2)
  local y = math.floor(index / 4) * 128 + math.floor((128 - image.height) / 2)
  assembled:drawImage(image, Point(x, y))
  print(string.format("%02d %s %d %d %d %d %.4f %.4f",
    index, name, x, y, image.width, image.height, pivot_x, pivot_y))
end
-- Retain exact pixels for the already reviewed materials, straight joins and indent.
local exact = {
  { 0, "wet_cross", 8, 11, 112, 106 },
  { 1, "wet_horizontal", 136, 35, 112, 58 },
  { 2, "wet_vertical", 284, 8, 72, 112 },
  { 6, "dry_cross", 392, 9, 112, 109 },
  { 7, "dry_horizontal", 8, 163, 112, 57 },
  { 8, "dry_vertical", 153, 136, 77, 112 },
  { 12, "dry_indent", 264, 144, 112, 96 },
}
for _, tile in ipairs(exact) do
  local index, name, x, y, w, h = table.unpack(tile)
  local image = Image(w, h, ColorMode.RGB)
  image:drawImage(previous, Point(-x, -y))
  place(index, image, w * 0.5, h * 0.5, name)
end
-- Rectangles isolate complete authored cutouts. Outside alpha <= 4 is haze.
-- The measured pivot is the intersection of actual painted mouth centerlines.
local additions = {
  { 3, "wet_cap", 70, 65, 390, 355, 226, 237 },
  { 4, "wet_elbow", 570, 72, 370, 352, 692.5, 206.5 },
  { 5, "wet_tee", 1063, 82, 402, 343, 1263.5, 215 },
  { 9, "dry_cap", 70, 573, 390, 350, 225, 744 },
  { 10, "dry_elbow", 572, 575, 369, 359, 693.5, 714 },
  { 11, "dry_tee", 1063, 584, 402, 347, 1263.5, 722 },
}
for _, tile in ipairs(additions) do
  local index, name, x, y, w, h, pivot_x, pivot_y = table.unpack(tile)
  local min_x, min_y, max_x, max_y = w, h, 0, 0
  local pixels = Image(w, h, ColorMode.RGB)
  for row = 0, h - 1 do
    for col = 0, w - 1 do
      local pixel = art:getPixel(x + col, y + row)
      if pc.rgbaA(pixel) > 4 then
        pixels:drawPixel(col, row, pixel)
        min_x, min_y = math.min(min_x, col), math.min(min_y, row)
        max_x, max_y = math.max(max_x, col), math.max(max_y, row)
      end
    end
  end
  assert(min_x > 0 and min_y > 0 and max_x < w - 1 and max_y < h - 1, name .. " crosses crop")
  local bw, bh = max_x - min_x + 5, max_y - min_y + 5
  local sprite = Sprite(bw, bh, ColorMode.RGB)
  local cropped = Image(bw, bh, ColorMode.RGB)
  cropped:drawImage(pixels, Point(2 - min_x, 2 - min_y))
  sprite:newCel(sprite.layers[1], 1, cropped, Point(0, 0))
  local scale = 112 / math.max(bw, bh)
  local scaled_w, scaled_h = math.floor(bw * scale + 0.5), math.floor(bh * scale + 0.5)
  app.activeSprite = sprite
  app.command.SpriteSize{ ui = false, width = scaled_w, height = scaled_h, method = "bilinear" }
  local px = (pivot_x - x - min_x + 2) * scaled_w / bw
  local py = (pivot_y - y - min_y + 2) * scaled_h / bh
  place(index, sprite.cels[1].image, px, py, name)
  sprite:close()
end
atlas:newCel(atlas.layers[1], 1, assembled, Point(0, 0))
atlas:saveCopyAs(app.params["master"])
atlas:saveCopyAs(app.params["output"])

