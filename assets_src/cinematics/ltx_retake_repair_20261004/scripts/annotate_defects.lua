local s=app.open(app.params.input)
local ghost=s:newTag(11,16);ghost.name='REJECT ghost raised arm global 50-55'
local seam=s:newTag(1,3);seam.name='REJECT early pose jump global 40-42'
s:saveAs(app.params.input);s:close()
