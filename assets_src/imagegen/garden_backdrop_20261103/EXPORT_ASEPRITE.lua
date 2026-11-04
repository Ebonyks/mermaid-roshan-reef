local sprite=app.open(app.params["src"])
assert(sprite.width==1672 and sprite.height==941)
sprite:resize{width=1025,height=576,method="bilinear"}
sprite:crop(Rectangle(0,0,1024,576))
assert(sprite.width==1024 and sprite.height==576)
sprite:saveCopyAs(app.params["dst"])
sprite:close()
