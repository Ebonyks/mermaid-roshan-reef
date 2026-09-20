local base=app.params.base
local input=app.open(base..'/huckleberry/rest-prepared.png')
local source=Image(512,512,ColorMode.RGB);source:drawImage(input.cels[1].image,input.cels[1].position);input:close()
local sprite=Sprite(512,512,ColorMode.RGB)
local names={'branch_left','branch_middle','branch_right','root_fixed'}
local layers={}
for n,name in ipairs(names) do local layer=n==1 and sprite.layers[1] or sprite:newLayer();layer.name=name;layers[n]=layer end
local left={0,1.2,3.8,2.8,.6,-1.8,-3.2,-1.4}
local middle={0,.4,2.0,3.4,1.5,-.7,-2.5,-1.2}
local right={0,-.2,1.1,2.7,2.0,.1,-1.6,-.9}
local durations={.3,.24,.3,.3,.32,.24,.3,.3}
local pc=app.pixelColor
local function sample(x,y)
 local x0,y0=math.floor(x),math.floor(y);local fx,fy=x-x0,y-y0
 local ra,ga,ba,aa=0,0,0,0
 for dy=0,1 do for dx=0,1 do
  local px,py=x0+dx,y0+dy
  if px>=0 and px<512 and py>=0 and py<512 then
   local w=(dx==0 and 1-fx or fx)*(dy==0 and 1-fy or fy)
   local c=source:getPixel(px,py);local a=pc.rgbaA(c)*w
   aa=aa+a;ra=ra+pc.rgbaR(c)*a;ga=ga+pc.rgbaG(c)*a;ba=ba+pc.rgbaB(c)*a
  end
 end end
 if aa<.5 then return 0 end
 return pc.rgba(math.floor(ra/aa+.5),math.floor(ga/aa+.5),math.floor(ba/aa+.5),math.floor(aa+.5))
end
for frame=1,8 do
 if frame>1 then sprite:newEmptyFrame() end
 sprite.frames[frame].duration=durations[frame]
 local images={Image(512,512,ColorMode.RGB),Image(512,512,ColorMode.RGB),Image(512,512,ColorMode.RGB),Image(512,512,ColorMode.RGB)}
 for y=0,511 do for x=0,511 do
  local rootWeight=math.max(0,math.min(1,(375-y)/220))
  rootWeight=rootWeight*rootWeight*(3-2*rootWeight)
  local a=math.exp(-((x-112)/95)^2);local b=math.exp(-((x-254)/95)^2);local c=math.exp(-((x-413)/95)^2)
  local dx=(a*left[frame]+b*middle[frame]+c*right[frame])/(a+b+c)*rootWeight
  dx=dx*2.5
  local sx,sy=x-dx,y+dx*.13
  if y>=375 or frame==1 then sx,sy=x,y end
  local color=sample(sx,sy)
  local group=sy>=375 and 4 or (sx<195 and 1 or (sx<328 and 2 or 3))
  images[group]:drawPixel(x,y,color)
 end end
 for n=1,4 do sprite:newCel(layers[n],frame,images[n],Point(0,0)) end
end
sprite:newTag(1,8).name='branch_breeze'
app.activeSprite=sprite;sprite:saveAs(base..'/huckleberry/huckleberry-eight-cels.aseprite')
app.command.ExportSpriteSheet{ui=false,type=SpriteSheetType.ROWS,columns=4,textureFilename=base..'/huckleberry/huckleberry-atlas.png',dataFilename=base..'/huckleberry/huckleberry-atlas.json',listLayers=true,listTags=true}
sprite:close()
