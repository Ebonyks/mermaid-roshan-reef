local s=app.open(app.params.input)
local f=io.open(app.params.output,'w');f:write('frames='..#s.frames..' tags='..#s.tags..'\n')
for _,tag in ipairs(s.tags) do f:write(tag.name..' '..tag.fromFrame.frameNumber..' '..tag.toFrame.frameNumber..'\n') end
f:close();s:close()
