local sprite = app.open(app.params.source)
assert(sprite ~= nil, "Source did not open")
sprite.layers[1].name = "Painted overhead stone slab - complete native take02"
sprite:saveAs(app.params.master)
sprite:saveAs(app.params.roundtrip)
sprite:close()
local native = Image{fromFile=app.params.source}
assert(native.width == 1254 and native.height == 1254, "Expected exact generated whole source")
local output = Image(native)
output:resize{width=1024,height=1024,method="bilinear"}
output:saveAs(app.params.output)
