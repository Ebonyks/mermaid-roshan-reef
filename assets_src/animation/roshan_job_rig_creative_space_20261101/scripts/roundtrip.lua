local root=app.params.root
local names={'painter_body','painter_head','painter_tail','astronaut_body','astronaut_head','astronaut_tail','neck_patch','brush','brush_grip'}
app.fs.makeAllDirectories(root..'/evidence/roundtrip')
for _,name in ipairs(names) do
 local s=assert(app.open(root..'/masters/'..name..'.aseprite'))
 assert(#s.frames==1 and s.width>0 and s.height>0)
 s:saveCopyAs(root..'/evidence/roundtrip/'..name..'.png');s:close()
 print('MASTER_REOPEN '..name)
end
