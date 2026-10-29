local canvas = Image(576,456,ColorMode.RGB)
canvas:clear(app.pixelColor.rgba(tonumber(app.params.r),tonumber(app.params.g),tonumber(app.params.b),255))
local sources = {app.params.mint,app.params.blue,app.params.lavender}
local sizes = {56,96,160}
local ys = {20,112,270}
for row,sz in ipairs(sizes) do
 for col,path in ipairs(sources) do
  local image = Image{fromFile=path}
  image:resize{width=sz,height=sz,method="bilinear"}
  canvas:drawImage(image,Point(math.floor((col-1)*192+(192-sz)/2),ys[row]))
 end
end
canvas:saveAs(app.params.output)
