local s=assert(app.open('assets_src/characters/baby_eagle_2026-09-26/eagle_original_isolated.png'))
app.command.SpriteSize{ui=false,width=290,height=512,method="bilinear"}
s:saveAs('assets_src/characters/baby_eagle_2026-09-26/baby_eagle_runtime.aseprite')
s:saveCopyAs('assets/characters/companions/baby_eagle.png');s:close()
