local sprite=app.open(app.params.source)
assert(sprite ~= nil,"Native source did not open")
sprite.layers[1].name="Whole painted soil - native take02"
sprite:saveAs(app.params.master)
sprite:saveAs(app.params.roundtrip)
sprite:close()
local source=Image{fromFile=app.params.source}
local crop=Image(source,Rectangle(71,52,1519,839))
crop:resize{width=822,height=454,method="bilinear"}
local whole=Image(1008,540,ColorMode.RGB)
whole:drawImage(crop,Point(93,43))
whole:saveAs(app.params.whole)
