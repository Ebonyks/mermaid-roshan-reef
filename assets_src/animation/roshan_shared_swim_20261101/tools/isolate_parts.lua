-- Native RGBA isolation. Source sheets remain unchanged and are retained separately.
local file = assert(io.open(app.params['spec'], 'r'))
local specs = json.decode(file:read('*a'))
file:close()
local sources = {}
local masters = {}
for _, spec in ipairs(specs) do
  local source = sources[spec.source]
  if not source then
    source = Image{fromFile=spec.source}
    sources[spec.source] = source
  end
  local b = spec.box
  local part = Image(source, Rectangle(b[1], b[2], b[3]-b[1], b[4]-b[2]))
  for y=0,part.height-1 do
    local ranges = spec.rows[y+1]
    local j=1
    for x=0,part.width-1 do
      while j<=#ranges and x>=ranges[j][2] do j=j+1 end
      if j>#ranges or x<ranges[j][1] then part:putPixel(x,y,0) end
    end
  end
  local master = masters[spec.master]
  if not master then
    master = Sprite(source.width,source.height,ColorMode.RGB)
    master.layers[1].name='transparent_base'
    masters[spec.master]=master
  end
  local layer=master:newLayer()
  layer.name=spec.name
  master:newCel(layer,1,part,Point(b[1],b[2]))
  local exported=Image(part)
  if exported.width~=spec.size[1] or exported.height~=spec.size[2] then
    exported:resize{width=spec.size[1],height=spec.size[2],method='bilinear'}
  end
  exported:saveAs(spec.output)
end
for filename, sprite in pairs(masters) do
  sprite:saveAs(filename)
  sprite:close()
end
print('ASEPRITE_NATIVE_PARTS_EXPORTED '..#specs)
