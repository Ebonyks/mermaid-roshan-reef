local sprite=app.open(app.params.source)
assert(sprite ~= nil,"Native source did not open")
sprite.layers[1].name="Whole painted ammonite slab - native take01"
sprite:saveAs(app.params.master)
sprite:saveAs(app.params.roundtrip)
sprite:close()
local source=Image{fromFile=app.params.source}
local crop=Image(source,Rectangle(31,93,1557,797))
crop:resize{width=756,height=387,method="bilinear"}
local whole=Image(900,540,ColorMode.RGB)
whole:drawImage(crop,Point(72,76))
whole:saveAs(app.params.whole)
for i=0,2 do
 local piece=Image(whole,Rectangle(i*300,0,300,540))
 piece:resize{width=250,height=450,method="bilinear"}
 local canvas=Image(512,512,ColorMode.RGB)
 canvas:drawImage(piece,Point(131,31))
 canvas:saveAs(app.params["piece"..i])
end
