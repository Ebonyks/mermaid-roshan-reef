local root=app.params["packet"];local f=io.open(root.."/evidence/aseprite-version.txt","w");f:write(tostring(app.version));f:close()
