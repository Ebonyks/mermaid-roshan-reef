-- Bounded STATIC contact feasibility: approved work10 body unchanged, approved single berry only.
-- This is not an authored cinematic frame, animation key sequence, or runtime bind.
local r,s,e=app.params['root'],app.params['destination'],app.params['review']
local pc=app.pixelColor
local body=Image{fromFile=s .. '/approved_work_10.png'}
local berrySource=Image{fromFile=r .. '/assets/chapter2/birthday/sky_lagoon_strawberry_single.png'}
local berryCrop=Image(berrySource,Rectangle(183,85,657,866))
berryCrop:saveAs(s .. '/approved_berry_native_crop.png')
local light,dark=pc.rgba(246,240,252,255),pc.rgba(25,24,40,255)
local function flat(im,col)
  local out=Image(im.width,im.height,ColorMode.RGB);out:clear(col);out:drawImage(im,Point(0,0));return out
end
local tests={
  {name='a',x=29,y=41,w=17,h=23},
  {name='b',x=29,y=40,w=18,h=24},
  {name='c',x=28,y=39,w=19,h=25}
}
for _,t in ipairs(tests) do
  local berry=Image(berryCrop)
  berry:resize{width=t.w,height=t.h,method='bilinear'}
  local comp=Image(256,256,ColorMode.RGB)
  comp:drawImage(berry,Point(t.x,t.y));comp:drawImage(body,Point(0,0))
  comp:saveAs(e .. '/trial_' .. t.name .. '_rgba.png')
  flat(comp,light):saveAs(e .. '/trial_' .. t.name .. '_light.png')
  flat(comp,dark):saveAs(e .. '/trial_' .. t.name .. '_dark.png')
  local detail=Image(flat(comp,light),Rectangle(18,34,46,65))
  detail:resize{width=368,height=520,method='nearest'}
  detail:saveAs(e .. '/trial_' .. t.name .. '_contact_8x.png')
end
print('CANDY_STATIC_CONTACT_TRIALS|approved_body=work10_exact|berry=existing_single|placements=3|generated_takes=0')
