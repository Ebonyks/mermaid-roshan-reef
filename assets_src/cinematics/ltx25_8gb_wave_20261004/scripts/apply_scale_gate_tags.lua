local p=app.params.packet
local f=assert(io.open(p..'/scale_continuity/filter_verification.json','rb'));local report=json.decode(f:read('*a'));f:close()
local s=app.open(p..'/scale_continuity/decoded_filtered_review.aseprite')
for _,tag in ipairs(s.tags) do
 local index=tag.fromFrame.frameNumber-1
 tag.name=string.format('%s_%04d',report.decoded_frames[index+1].pass and 'GEOMETRY_PASS_VISUAL_PENDING' or 'REDRAW_REQUIRED',index)
end
for _,slice in ipairs(s.slices) do
 local data=json.decode(slice.data);data.export_geometry_pass=report.decoded_frames[data.timeline_index+1].pass;data.accepted=false;slice.data=json.encode(data)
end
s:saveAs(p..'/scale_continuity/decoded_filtered_review.aseprite');s:close()
s=app.open(p..'/scale_continuity/decoded_filtered_review.aseprite')
local tags={}
for _,tag in ipairs(s.tags) do table.insert(tags,{index=tag.fromFrame.frameNumber-1,name=tag.name}) end
local check=assert(io.open(p..'/scale_continuity/aseprite_tag_roundtrip.json','wb'));check:write(json.encode{tags=tags,frame_count=#s.frames,slice_count=#s.slices,review_only=true});check:close();s:close()
print('Post-export results written into editable Aseprite tags; failed geometry blocks acceptance.')
