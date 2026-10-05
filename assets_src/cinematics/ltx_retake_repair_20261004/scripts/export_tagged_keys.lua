local ok,err=pcall(function()
local s=app.open(app.params.input)
local rows={};local width=s.width;local height=s.height
for _,tag in ipairs(s.tags) do
 local global=tag.name:match('^native_frame_(%d+)') or tag.name:match('^repair_key_(%d+)')
 if global then
  if tag.fromFrame.frameNumber~=tag.toFrame.frameNumber then error('Each repair key tag must identify one complete frame') end
  local frame=tag.fromFrame.frameNumber;local image=Image(width,height,ColorMode.RGB);image:clear(app.pixelColor.rgba(0,0,0,0))
  for _,layer in ipairs(s.layers) do
   if layer.isVisible then local cel=layer:cel(frame);if cel then image:drawImage(cel.image,cel.position) end end
  end
  local name=string.format('key_%04d.png',tonumber(global));image:saveAs(app.params.output..'/'..name)
  rows[#rows+1]={source_global_frame=tonumber(global),aseprite_frame=frame,tag=tag.name,path=name,duration_seconds=s.frames[frame].duration}
 end
end
if #rows==0 then error('No native_frame_N or repair_key_N single-frame tags found') end
local f=io.open(app.params.output..'/tagged_keys.json','w');f:write(json.encode{status='EXPORTED_SOURCE_GUIDES_NOT_ACCEPTED',dimensions={width,height},keys=rows});f:close();s:close()

end)
if not ok then local f=io.open(app.params.output.."/export_error.txt","w");f:write(tostring(err));f:close();error(err) end
