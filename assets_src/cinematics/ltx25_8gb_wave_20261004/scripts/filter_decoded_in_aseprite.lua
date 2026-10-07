local packet=app.params.packet
local f=assert(io.open(packet..'/scale_continuity/decoded_registration_plan.json','rb'));local plan=json.decode(f:read('*a'));f:close()
local out=packet..'/scale_continuity/decoded_filtered'
app.fs.makeDirectory(out)
local s=Sprite(576,832,ColorMode.RGB);s.layers[1].name='Whole-figure registration candidates; failures unchanged'
for k,row in ipairs(plan.frames) do
 if k>1 then s:newFrame() end
 local im=Image{fromFile=packet..'/'..row.source};local frame
 if row.pass then
  assert(row.scaled_canvas[1]*832==row.scaled_canvas[2]*576,'Nonuniform transform forbidden')
  im:resize{width=row.scaled_canvas[1],height=row.scaled_canvas[2],method='bilinear'}
  frame=Image(576,832,ColorMode.RGB);frame:clear(Color{r=238,g=238,b=238,a=255})
  frame:drawImage(im,Point(row.placement[1],row.placement[2]))
 else frame=im end
 s.cels[k].image=frame;s.frames[k].duration=(math.floor(k*1000/24+.5)-math.floor((k-1)*1000/24+.5))/1000
 frame:saveAs(out..string.format('/%04d.png',row.index))
 local tag=s:newTag(k,k);tag.name=string.format('%s_%04d',row.pass and row.export_check_pass~=false and 'CHECK_EXPORTED_ANCHORS' or 'REDRAW_REQUIRED',row.index)
 for name,xy in pairs(row.target_landmarks) do
  local slice=s:newSlice(Rectangle(math.floor(xy[1]+.5)-3,math.floor(xy[2]+.5)-3,7,7));slice.name=string.format('f%04d/%s',row.index,name);slice.pivot=Point(3,3)
  slice.data=json.encode{timeline_index=row.index,target=xy,proportion_fit_pass=row.pass,review_only=true}
 end
end
s:saveAs(packet..'/scale_continuity/decoded_filtered_review.aseprite');s:close()
print('Decoded Aseprite review exported; failed frames preserved and tagged.')
