local sprite = app.open(app.params.source)
assert(sprite ~= nil, "Source did not open")
sprite.layers[1].name = "Existing painted grain - unchanged native pixels"
sprite:saveAs(app.params.master)
sprite:saveAs(app.params.roundtrip)
sprite:close()
local native = Image{fromFile=app.params.source}
assert(native.width == 1024 and native.height == 683, "Expected exact existing whole source")
local scaled = Image(native)
scaled:resize{width=512,height=342,method="bilinear"}
local output = Image(512,512,ColorMode.RGB)
output:drawImage(scaled,Point(0,85))
output:saveAs(app.params.output)
