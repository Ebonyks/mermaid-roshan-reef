local sprite = app.activeSprite
sprite:crop(Rectangle(430, 14, 423, 373))
sprite:saveCopyAs(app.params["output"])
