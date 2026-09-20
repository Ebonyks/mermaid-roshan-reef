local base=app.params.base
local input=app.open(base..'/bridge/chain-patch-source.png')
local source=Image(224,192,ColorMode.RGB);source:drawImage(input.cels[1].image,input.cels[1].position);input:close()
local sprite=Sprite(224,192,ColorMode.RGB)
local names={'posts_and_attachments_fixed','chain_near','chain_middle','chain_far'}
local layers={}
for n,name in ipairs(names) do local l=n==1 and sprite.layers[1] or sprite:newLayer();l.name=name;layers[n]=l end
local intervals={{6,76,1},{121,139,.75},{173,214,.55}}
local motion={0,0,.7,1.7,2.4,1.5,.2,-1,-.65,-.2,.08,0}
local durations={.05,.05,.04,.05,.07,.07,.06,.06,.05,.06,.06,.10}
local pc=app.pixelColor
for frame=1,12 do
 if frame>1 then sprite:newEmptyFrame() end
 sprite.frames[frame].duration=durations[frame]
 local images={Image(224,192,ColorMode.RGB),Image(224,192,ColorMode.RGB),Image(224,192,ColorMode.RGB),Image(224,192,ColorMode.RGB)}
 for x=0,223 do
  local dy,group=0,1
  for n,r in ipairs(intervals) do
   if x>r[1] and x<r[2] then
    dy=motion[frame]*r[3]*math.sin(math.pi*(x-r[1])/(r[2]-r[1]))^2;group=n+1
   end
  end
  for y=0,191 do
   local sy=y-dy;local y0=math.floor(sy);local t=sy-y0
   local r,g,b,a=0,0,0,0
   for j=0,1 do
    local yy=y0+j
    if yy>=0 and yy<192 then
     local c=source:getPixel(x,yy);local aa=pc.rgbaA(c)*(j==0 and 1-t or t)
     a=a+aa;r=r+pc.rgbaR(c)*aa;g=g+pc.rgbaG(c)*aa;b=b+pc.rgbaB(c)*aa
    end
   end
   if a>=.5 then images[group]:drawPixel(x,y,pc.rgba(math.floor(r/a+.5),math.floor(g/a+.5),math.floor(b/a+.5),math.floor(a+.5))) end
  end
 end
 for n=1,4 do sprite:newCel(layers[n],frame,images[n],Point(0,0)) end
end
sprite:newTag(1,12).name='footstep_secondary_settle'
app.activeSprite=sprite;sprite:saveAs(base..'/bridge/bridge-chains-twelve-cels.aseprite')
app.command.ExportSpriteSheet{ui=false,type=SpriteSheetType.ROWS,columns=4,textureFilename=base..'/bridge/chains-atlas.png',dataFilename=base..'/bridge/chains-atlas.json',listLayers=true,listTags=true}
sprite:close()
