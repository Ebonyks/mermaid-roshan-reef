local base = app.params.base
local clips = {{'arrival',256,256},{'castle',512,256}}
-- Uneven light pulses travel through distinct painted ridge groups, never translating the plate.
local intensity = {28,46,78,126,190,238,216,166,108,66,38,24}
for _,clip in ipairs(clips) do
 local name,w,h=clip[1],clip[2],clip[3]
 local sprite=Sprite(w,h,ColorMode.RGB)
 for n=0,3 do
  local layer = n==0 and sprite.layers[1] or sprite:newLayer()
  layer.name='painted_ridges_'..n
  local input=app.open(base..'/water/'..name..'-highlight-'..n..'.png')
  local img=Image(input.cels[1].image)
  local pos=input.cels[1].position
  input:close()
  for frame=1,12 do
   if #sprite.frames<frame then sprite:newEmptyFrame() end
   sprite.frames[frame].duration=0.18
   local cel=sprite:newCel(layer,frame,img,pos)
   cel.opacity=intensity[((frame-1+n*3)%12)+1]
  end
 end
 sprite:newTag(1,12).name='calm_painted_shimmer'
 app.activeSprite=sprite
 sprite:saveAs(base..'/water/'..name..'-highlights.aseprite')
 app.command.ExportSpriteSheet{ui=false,type=SpriteSheetType.ROWS,columns=4,textureFilename=base..'/water/'..name..'-highlights-atlas.png',dataFilename=base..'/water/'..name..'-highlights-atlas.json',listLayers=true,listTags=true}
 sprite:close()
end
