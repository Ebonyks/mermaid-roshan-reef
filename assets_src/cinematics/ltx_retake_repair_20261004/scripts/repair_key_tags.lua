local s=app.open(app.params.input)
for _,tag in ipairs(s.tags) do if tag.name:match('^native_frame_') then tag.toFrame=tag.fromFrame end end
s:saveAs(app.params.input);s:close()
