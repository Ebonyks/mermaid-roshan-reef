local src=app.params["src"]
local dst=app.params["dst"]
local sprite=app.open(src)
assert(sprite.width==1672 and sprite.height==941)
sprite:resize{width=1024,height=576,method="bilinear"}
assert(sprite.width==1024 and sprite.height==576)
sprite:saveCopyAs(dst)
sprite:close()
