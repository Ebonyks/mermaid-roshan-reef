-- Exact approved source-cell isolation for static contact feasibility, not animation.
local r, s, e = app.params['root'], app.params['destination'], app.params['review']
local atlas = Image{fromFile=r .. '/assets/opera/worlds/actors/animation/roshan_candymaker_sheet_a.png'}
local pc = app.pixelColor
local function flat(im, color)
  local out=Image(im.width, im.height, ColorMode.RGB)
  out:clear(color); out:drawImage(im, Point(0,0)); return out
end
local light, dark = pc.rgba(246,240,252,255), pc.rgba(25,24,40,255)
for frame=8,11 do
  local cell=Image(atlas, Rectangle((frame%4)*256,512,256,256))
  local name='approved_work_' .. frame
  cell:saveAs(s .. '/' .. name .. '.png')
  flat(cell,light):saveAs(e .. '/' .. name .. '_light.png')
  flat(cell,dark):saveAs(e .. '/' .. name .. '_dark.png')
  local detail=Image(flat(cell,light),Rectangle(16,45,70,85))
  detail:resize{width=280,height=340,method='nearest'}
  detail:saveAs(e .. '/' .. name .. '_tongs_4x.png')
end
Image(atlas,Rectangle(0,0,256,256)):saveAs(s .. '/approved_idle_0.png')
local berry=Image{fromFile=r .. '/assets/chapter2/birthday/sky_lagoon_strawberry_single.png'}
berry:saveAs(s .. '/approved_single_berry_source_export.png')
print('CANDY_IDENTITY_INVENTORY|exact_runtime_work_keys=4|whole_body_redraws=0')
