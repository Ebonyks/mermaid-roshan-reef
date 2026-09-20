local base=app.params.base
for _,spec in ipairs({{'arrival',256},{'castle',512}}) do
 local name,w=spec[1],spec[2];local sprite=Sprite(w,256,ColorMode.RGB);sprite.layers[1].name='painted_shore_lap'
 for n=0,7 do
  if n>0 then sprite:newEmptyFrame() end
  local input=app.open(base..'/water/'..name..string.format('-shore-%02d.png',n))
  sprite:newCel(sprite.layers[1],n+1,Image(input.cels[1].image),input.cels[1].position);input:close();sprite.frames[n+1].duration=.32
 end
 sprite:newTag(1,8).name='gentle_shore_lap';app.activeSprite=sprite;sprite:saveAs(base..'/water/'..name..'-shoreline.aseprite')
 app.command.ExportSpriteSheet{ui=false,type=SpriteSheetType.ROWS,columns=4,textureFilename=base..'/water/'..name..'-shore-atlas.png',dataFilename=base..'/water/'..name..'-shore-atlas.json',listTags=true};sprite:close()
end
