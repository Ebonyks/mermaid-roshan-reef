local sprite = app.open(app.params.source)
assert(sprite ~= nil, "Source did not open")
sprite.layers[1].name = "Generated native source - unchanged"
sprite:saveAs(app.params.master)
sprite:saveAs(app.params.roundtrip)
sprite:close()
local native = Image{fromFile=app.params.source}
assert(native.width == native.height, "Expected complete square source")
local output = Image(native)
output:resize{width=512,height=512,method="bilinear"}
output:saveAs(app.params.output)
