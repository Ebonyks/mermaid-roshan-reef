local source = app.open(app.params["source"])
local native = source.cels[1].image
assert(native.width == 1254 and native.height == 1254)
local atlas = Sprite(512, 256, ColorMode.RGB)
local assembled = Image(512, 256, ColorMode.RGB)
local pc = app.pixelColor
local tiles = {
  { "wet_junction", 218, 233, 65, 80, 315, 301 },
  { "wet_horizontal", 625, 229, 435, 130, 390, 211 },
  { "wet_vertical", 1020, 218, 905, 58, 236, 341 },
  { "dry_junction", 215, 618, 68, 473, 322, 306 },
  { "dry_horizontal", 620, 625, 435, 524, 385, 208 },
  { "dry_vertical", 1020, 622, 902, 451, 239, 344 },
  { "dry_indent", 220, 1022, 116, 929, 216, 188 },
}
for index, tile in ipairs(tiles) do
  local name, sx, sy, left, top, width, height = table.unpack(tile)
  local stack = { (sy - top) * width + sx - left }
  local visited = { [stack[1]] = true }
  local min_x, min_y, max_x, max_y = width, height, 0, 0
  local n = 0
  local cropped = Image(width, height, ColorMode.RGB)
  while #stack > 0 do
    local key = table.remove(stack)
    local x = key % width
    local y = math.floor(key / width)
    local pixel = native:getPixel(x + left, y + top)
    if pc.rgbaA(pixel) > 0 then
      assert(x > 0 and y > 0 and x < width - 1 and y < height - 1, name .. " touches technical crop boundary")
      n = n + 1
      min_x, min_y = math.min(min_x, x), math.min(min_y, y)
      max_x, max_y = math.max(max_x, x), math.max(max_y, y)
      cropped:drawPixel(x, y, pixel)
      for dy = -1, 1 do
        for dx = -1, 1 do
          local next_key = (y + dy) * width + x + dx
          if not visited[next_key] then
            visited[next_key] = true
            stack[#stack + 1] = next_key
          end
        end
      end
    end
  end
  assert(n > 20000, name .. " has no intact source component")
  local cw, ch = max_x - min_x + 5, max_y - min_y + 5
  local sprite = Sprite(cw, ch, ColorMode.RGB)
  local image = Image(cw, ch, ColorMode.RGB)
  image:drawImage(cropped, Point(2 - min_x, 2 - min_y))
  sprite:newCel(sprite.layers[1], 1, image, Point(0, 0))
  local scale = 112 / math.max(cw, ch)
  local out_w, out_h = math.floor(cw * scale + 0.5), math.floor(ch * scale + 0.5)
  app.activeSprite = sprite
  app.command.SpriteSize{ ui = false, width = out_w, height = out_h, method = "bilinear" }
  local slot_x, slot_y = ((index - 1) % 4) * 128, math.floor((index - 1) / 4) * 128
  local x = slot_x + math.floor((128 - out_w) / 2)
  local y = slot_y + math.floor((128 - out_h) / 2)
  assembled:drawImage(sprite.cels[1].image, Point(x, y))
  print(string.format("%s %d %d %d %d %d %d %d %d %d", name,
    n, left + min_x, top + min_y, max_x - min_x + 1, max_y - min_y + 1, x, y, out_w, out_h))
  sprite:close()
end
atlas:newCel(atlas.layers[1], 1, assembled, Point(0, 0))
atlas:saveCopyAs(app.params["master"])
atlas:saveCopyAs(app.params["output"])

