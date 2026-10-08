local rows = {}
local function hist(image)
 local values = {}
 for pixel in image:pixels() do
  local alpha = app.pixelColor.rgbaA(pixel())
  local key = tostring(alpha)
  values[key] = (values[key] or 0) + 1
 end
 return values
end
for _,c in ipairs({{8,5,255,'bilinear'},{8,5,128,'bilinear'},{1254,1024,255,'bilinear'},{8,5,255,'nearest'}}) do
 local sprite = Sprite(c[1],c[1],ColorMode.RGB)
 local image = Image(c[1],c[1],ColorMode.RGB)
 image:clear(app.pixelColor.rgba(99,170,180,c[3]))
 sprite.cels[1].image = image
 local before = hist(image)
 app.command.SpriteSize{ui=false,width=c[2],height=c[2],method=c[4]}
 rows[#rows+1] = { source_side=c[1],target_side=c[2],constant_alpha=c[3],algorithm=c[4],before=before,cel_after=hist(sprite.cels[1].image),rendered_after=hist(Image(sprite)) }
 sprite:close()
end
local file = assert(io.open('assets_src/imagegen/astronaut_pipe_raster_repair_20261007/ALPHA_DIAGNOSTIC_ASEPRITE.json','w'))
file:write(json.encode{version=tostring(app.version),cases=rows,appearance_images_saved=0,source_art_modified=false})
file:close()
