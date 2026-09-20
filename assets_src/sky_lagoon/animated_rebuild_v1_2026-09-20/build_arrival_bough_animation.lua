local base=app.params.base
local input=app.open(base..'/tip-rest.png');local source=Image(512,256,ColorMode.RGB);source:drawImage(input.cels[1].image,input.cels[1].position);input:close()
local sprite=Sprite(512,256,ColorMode.RGB);local layers={}
for n,name in ipairs({'central_stem_and_lower_tier_fixed','left_outer_tips','right_outer_tips'}) do local l=n==1 and sprite.layers[1] or sprite:newLayer();l.name=name;layers[n]=l end
local left={0,2.0,-1.5};local right={0,1.4,-2.0};local pc=app.pixelColor
for frame=1,3 do
 if frame>1 then sprite:newEmptyFrame() end
 sprite.frames[frame].duration=.5
 local images={Image(512,256,ColorMode.RGB),Image(512,256,ColorMode.RGB),Image(512,256,ColorMode.RGB)}
 for y=0,255 do for x=0,511 do
  local edge=math.max(0,math.min(1,(math.abs(x-120)-24)/60))
  local root=math.max(0,math.min(1,math.min((y-32)/40,(224-y)/40)));root=root*root*(3-2*root)
  local dx=edge*root*math.max(0,math.min(1,(x-8)/20))*(x<120 and left[frame] or right[frame]);local sx=x-dx
  local x0=math.floor(sx);local t=sx-x0;local r,g,b,a=0,0,0,0
  for j=0,1 do local xx=x0+j
   if xx>=0 and xx<512 then local c=source:getPixel(xx,y);local aa=pc.rgbaA(c)*(j==0 and 1-t or t);a=a+aa;r=r+pc.rgbaR(c)*aa;g=g+pc.rgbaG(c)*aa;b=b+pc.rgbaB(c)*aa end
  end
  local group=(x<8 or y<32 or y>=224 or math.abs(x-120)<=24) and 1 or (x<120 and 2 or 3)
  if a>=.5 then images[group]:drawPixel(x,y,pc.rgba(math.floor(r/a+.5),math.floor(g/a+.5),math.floor(b/a+.5),math.floor(a+.5))) end
 end end
 for n=1,3 do sprite:newCel(layers[n],frame,images[n],Point(0,0)) end
end
sprite:newTag(1,3).name='outer_tip_breeze';app.activeSprite=sprite;sprite:saveAs(base..'/tip-three-cels.aseprite')
app.command.ExportSpriteSheet{ui=false,type=SpriteSheetType.ROWS,columns=2,textureFilename=base..'/tip-atlas.png',dataFilename=base..'/tip-atlas.json',listLayers=true,listTags=true};sprite:close()
