local p=app.params.packet;local f=assert(io.open(p..'/guide_plan.json','rb'));local plan=json.decode(f:read('*a'));f:close()
local s=app.open(p..'/structural_guide.aseprite');assert(#s.frames==41 and #s.slices==0)
for i,row in ipairs(plan.frames) do
 local tag=s:newTag(i,i);tag.name=string.format('STRUCTURAL_GUIDE_ONLY_%04d',row.index)
 for name,xy in pairs(row.anchors) do
  local slice=s:newSlice(Rectangle(math.floor(xy[1]+.5)-3,math.floor(xy[2]+.5)-3,7,7))
  slice.name=string.format('f%04d/%s',row.index,name);slice.pivot=Point(3,3)
  slice.data=json.encode{timeline_index=row.index,target=xy,role='structural_motion_control_only',delivery_pixels=false}
 end
end
assert(#s.slices==328 and #s.tags==41);s:saveAs(p..'/structural_guide.aseprite');s:close()
print('GUIDE_METADATA328 landmark slices41 index tags; no PNG changes')
