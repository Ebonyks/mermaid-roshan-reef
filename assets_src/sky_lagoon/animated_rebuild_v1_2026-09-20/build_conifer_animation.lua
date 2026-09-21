local base=app.params.base
local input=app.open(base..'/conifer/rest-prepared.png');local source=Image(256,384,ColorMode.RGB);source:drawImage(input.cels[1].image,input.cels[1].position);input:close()
local sprite=Sprite(256,384,ColorMode.RGB);local layers={}
for n,name in ipairs({'trunk_and_garden_fixed','left_boughs','right_boughs'}) do local l=n==1 and sprite.layers[1] or sprite:newLayer();l.name=name;layers[n]=l end
local left={0,2.8,1.6,-.2,-2.4,-1};local right={0,.7,2.4,1.1,-1.3,-1.8};local pc=app.pixelColor
for frame=1,6 do
 if frame>1 then sprite:newEmptyFrame() end
 sprite.frames[frame].duration=.36
 local images={Image(256,384,ColorMode.RGB),Image(256,384,ColorMode.RGB),Image(256,384,ColorMode.RGB)}
 for y=0,383 do for x=0,255 do
  local weight=math.max(0,math.min(1,(math.abs(x-128)-12)/55))*math.max(0,math.min(1,(240-y)/55))
  local dx=weight*(x<128 and left[frame] or right[frame]);local sx=x-dx
  local x0=math.floor(sx);local t=sx-x0;local r,g,b,a=0,0,0,0
  for j=0,1 do local xx=x0+j
   if xx>=0 and xx<256 then local c=source:getPixel(xx,y);local aa=pc.rgbaA(c)*(j==0 and 1-t or t);a=a+aa;r=r+pc.rgbaR(c)*aa;g=g+pc.rgbaG(c)*aa;b=b+pc.rgbaB(c)*aa end
  end
  local group=(y>=240 or math.abs(x-128)<=12) and 1 or (x<128 and 2 or 3)
  if a>=.5 then images[group]:drawPixel(x,y,pc.rgba(math.floor(r/a+.5),math.floor(g/a+.5),math.floor(b/a+.5),math.floor(a+.5))) end
 end end
 for n=1,3 do sprite:newCel(layers[n],frame,images[n],Point(0,0)) end
end
sprite:newTag(1,6).name='outer_bough_breeze';app.activeSprite=sprite;sprite:saveAs(base..'/conifer/conifer-six-cels.aseprite')
app.command.ExportSpriteSheet{ui=false,type=SpriteSheetType.ROWS,columns=3,textureFilename=base..'/conifer/conifer-atlas.png',dataFilename=base..'/conifer/conifer-atlas.json',listLayers=true,listTags=true};sprite:close()
