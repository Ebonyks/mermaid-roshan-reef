local im = Image{fromFile=app.params.source}
local scaled = Image(im)
local height = 430
local width = math.floor(im.width * height / im.height + 0.5)
scaled:resize{width=width,height=height,method="bilinear"}
local canvas = Image(512,512,ColorMode.RGB)
canvas:clear(app.pixelColor.rgba(0,0,0,0))
canvas:drawImage(scaled,Point(math.floor((512-width)/2),math.floor((512-height)/2)))
canvas:saveAs(app.params.output)
