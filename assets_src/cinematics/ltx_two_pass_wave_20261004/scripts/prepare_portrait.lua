local root=app.params.packet
local source=app.params.source
local s=Sprite(576,832,ColorMode.RGB);local figure=s.layers[1];figure.name='Complete-figure cropped source; uniform scale16/9'
local bg=s:newLayer();bg.name='Neutral conditioning field';bg.stackIndex=1
for k=0,3 do
 if k>0 then s:newFrame() end
 local input=Image{fromFile=source..string.format('/inputs/figure_rgba_%02d.png',k)}
 local crop=Sprite(324,468,ColorMode.RGB);crop.cels[1].image:clear(app.pixelColor.rgba(0,0,0,0));crop.cels[1].image:drawImage(input,Point(-358,-25));app.activeSprite=crop
 app.command.SpriteSize{ui=false,width=576,height=832,method='bilinear'}
 local resized=Image(crop.cels[1].image);crop:close();app.activeSprite=s
 local gray=Image(576,832,ColorMode.RGB);gray:clear(Color{r=238,g=238,b=238,a=255})
 s:newCel(bg,k+1,gray,Point(0,0));s:newCel(figure,k+1,resized,Point(0,0));s.frames[k+1].duration=1/24
 resized:saveAs(root..string.format('/inputs/portrait_rgba_%02d.png',k));gray:drawImage(resized,Point(0,0));gray:saveAs(root..string.format('/inputs/portrait_key_%02d.png',k))
end
for k=1,4 do local tag=s:newTag(k,k);tag.name=({'SOURCE_rest','SOURCE_shoulder','SOURCE_above_head','SOURCE_lower'})[k] end
local slice=s:newSlice(Rectangle(0,0,576,832));slice.name='Root registration permits complete-figure acting';slice.pivot=Point(183,453)
s:saveAs(root..'/inputs/portrait_source_keys.aseprite');s:close()
