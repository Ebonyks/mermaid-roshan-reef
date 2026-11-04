local sprite = app.open(app.params["source"])
local original = sprite.cels[1].image
assert(original.width == 1672 and original.height == 941)
for column = 0, 1 do
  local image = Image(832, 936, ColorMode.RGB)
  image:drawImage(original, Point(-4 - column * 832, -2))
  local tile = Sprite(832, 936, ColorMode.RGB)
  tile:newCel(tile.layers[1], 1, image, Point(0, 0))
  tile:saveCopyAs(app.params["output"] .. tostring(column) .. ".png")
  tile:close()
end

