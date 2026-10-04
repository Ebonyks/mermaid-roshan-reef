local s=app.open(app.params.input)
for i=1,#s.cels do s.cels[i].image:saveAs(app.params.output..string.format('/wave_key_%02d.png',i-1)) end
s:close()
