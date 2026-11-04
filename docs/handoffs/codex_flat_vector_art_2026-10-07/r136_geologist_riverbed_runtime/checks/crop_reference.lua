local sprite = app.activeSprite
if not sprite then error("An exact baseline reference is required") end
sprite:crop(Rectangle(353, 130, 807, 554))
sprite:saveCopyAs(app.params["output"])
