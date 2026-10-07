-- Selected STATIC contact study C. Exact source body over locally scaled existing berry.
local r,s,e=app.params['root'],app.params['destination'],app.params['review']
local pc=app.pixelColor
local body=Image{fromFile=s .. '/approved_work_10.png'}
local crop=Image{fromFile=s .. '/approved_berry_native_crop.png'}
local berry=Image(crop);berry:resize{width=19,height=25,method='bilinear'}
berry:saveAs(s .. '/berry_contact_prop_19x25.png')
local sprite=Sprite(256,256,ColorMode.RGB)
local fruit=sprite.layers[1];fruit.name='Editable existing berry — local static placement'
sprite:newCel(fruit,1,berry,Point(28,39))
local identity=sprite:newLayer();identity.name='Approved work10 identity — exact RGBA, locked'
sprite:newCel(identity,1,body,Point(0,0));identity.isEditable=false
sprite.data='STATIC STUDY ONLY. Work10 runtime cell exact; berry source crop183,85,657,866, resize19x25 at28,39 below original gold jaws. JOB_CARD.json owns hashes, rights and pending acting/phone/owner acceptance.'
sprite:saveAs(s .. '/candy_identity_locked_contact.aseprite')
sprite:saveCopyAs(s .. '/candy_identity_locked_contact.png')
sprite:close()
local reopened=app.open(s .. '/candy_identity_locked_contact.aseprite')
reopened:saveCopyAs(e .. '/master_roundtrip.png')
reopened.layers[2]:cel(1).image:saveAs(e .. '/approved_body_layer_roundtrip.png')
reopened.layers[1]:cel(1).image:saveAs(e .. '/berry_layer_roundtrip.png')
reopened:close()
local result=Image{fromFile=s .. '/candy_identity_locked_contact.png'}
local light,dark=pc.rgba(246,240,252,255),pc.rgba(25,24,40,255)
local function flat(im,col)
  local out=Image(im.width,im.height,ColorMode.RGB);out:clear(col);out:drawImage(im,Point(0,0));return out
end
for name,color in pairs({light=light,dark=dark}) do
  flat(result,color):saveAs(e .. '/selected_native_' .. name .. '.png')
  local detail=Image(flat(result,color),Rectangle(18,34,46,65))
  detail:resize{width=368,height=520,method='nearest'}
  detail:saveAs(e .. '/selected_contact_8x_' .. name .. '.png')
end
local world=Image{fromFile=r .. '/assets_src/imagegen/opera_codex_2026-08-02/native/world_candymaker_native.png'}
world:resize{width=1280,height=720,method='bilinear'}
for _,kind in ipairs({'light','dark','game'}) do
  for _,which in ipairs({'approved','selected'}) do
    local small=Image(which=='approved' and body or result)
    small:resize{width=250,height=250,method='bilinear'}
    local canvas
    if kind=='game' then canvas=Image(world)
    else canvas=Image(1280,720,ColorMode.RGB);canvas:clear(kind=='light' and light or dark) end
    canvas:drawImage(small,Point(498,306))
    canvas:saveAs(e .. '/' .. which .. '_250px_' .. kind .. '.png')
  end
end
print('CANDY_STATIC_MASTER|work10_exact|berry19x25_at28_39|layers=2|frames=1|new_generation=0|acting_acceptance=none')
