local packet=app.params.packet
local fh=assert(io.open(packet..'/scale_continuity/registration_plan.json','rb'))
local plan=json.decode(fh:read('*a'));fh:close()
local out=packet..'/scale_continuity'
app.fs.makeDirectory(out..'/anchor_review')
local sprite=Sprite(576,832,ColorMode.RGB)
local figure=sprite.layers[1];figure.name='Original whole figures; preserved pixels'
local marks=sprite:newLayer();marks.name='Five anchors: cyan measured, yellow target; QA only'
local function point(image,xy,color)
 local x=math.floor(xy[1]+0.5);local y=math.floor(xy[2]+0.5)
 for d=-5,5 do
  if x+d>=0 and x+d<576 and y>=0 and y<832 then image:drawPixel(x+d,y,color) end
  if x>=0 and x<576 and y+d>=0 and y+d<832 then image:drawPixel(x,y+d,color) end
 end
end
local cyan=app.pixelColor.rgba(0,170,220,255)
local yellow=app.pixelColor.rgba(245,180,0,255)
for k,row in ipairs(plan.guides) do
 if k>1 then sprite:newFrame() end
 local source=Image{fromFile=app.params.repo..'/'..row.source}
 sprite.cels[k].image=source
 sprite.frames[k].duration=((plan.guides[k+1] and plan.guides[k+1].index or 41)-row.index)/24
 local overlay=Image(576,832,ColorMode.RGB);overlay:clear(app.pixelColor.rgba(0,0,0,0))
 for _,name in ipairs(plan.anchor_names) do
  point(overlay,row.source_landmarks[name],cyan);point(overlay,row.target_landmarks[name],yellow)
  local xy=row.source_landmarks[name]
  local slice=sprite:newSlice(Rectangle(math.floor(xy[1]+0.5)-3,math.floor(xy[2]+0.5)-3,7,7))
  slice.name=string.format('f%04d/%s',row.index,name);slice.pivot=Point(3,3)
  slice.data=json.encode{timeline_index=row.index,anchor_name=name,measured=row.source_landmarks[name],target=row.target_landmarks[name],registration_pass=row.pass}
 end
 sprite:newCel(marks,k,overlay,Point(0,0))
 local annotated=Image(source);annotated:drawImage(overlay,Point(0,0));annotated:saveAs(out..string.format('/anchor_review/guide_%04d.png',row.index))
 local tag=sprite:newTag(k,k);tag.name=string.format('%s_guide_%04d',row.pass and 'ANCHOR_REFERENCE' or 'REDRAW_REQUIRED',row.index)
end
marks.isVisible=false
sprite:saveAs(out..'/multi_anchor_guides.aseprite')
for k,row in ipairs(plan.guides) do local frame=Image(576,832,ColorMode.RGB);frame:drawSprite(sprite,k);frame:saveAs(out..string.format('/anchor_review/original_roundtrip_%04d.png',row.index)) end
sprite:close()
local guide=Image(576,832,ColorMode.RGB);guide:clear(Color{r=238,g=238,b=238,a=255})
local target=plan.guides[5].target_landmarks
for _,name in ipairs(plan.anchor_names) do point(guide,target[name],cyan) end
guide:saveAs(out..'/position_guide_only_key22_neckline_v2.png')
print('Created editable five-anchor Aseprite master; original pixels retained, rejected key22 marked.')
