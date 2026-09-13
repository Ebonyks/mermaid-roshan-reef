-- Reference-only first-frame layout proposals. Never character animation.
-- Aseprite performs only a uniform whole-cutout scale and placement; no redraw.
local src = app.open(app.params.source)
assert(src and #src.frames == 1, "expected a single source frame")
app.activeSprite = src
app.command.SpriteSize { ui=false, width=640, height=640, method="bilinear" }
local scaled = Image(src.cels[1].image)
local target = Sprite(1280,720,ColorMode.RGB)
local bg = Image(1280,720,ColorMode.RGB)
bg:clear(app.pixelColor.rgba(17,37,54,255))
target:newCel(target.layers[1],1,bg,Point(0,0))
target.layers[1].name = "neutral observation field - no location canon"
local actor = target:newLayer()
actor.name = "source cutout - uniform scale only - pending opening approval"
target:newCel(actor,1,scaled,Point(120,40))
app.activeSprite = target
target:saveAs(app.params.output)
target:close()
src:close()
