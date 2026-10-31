-- Connected neutral-field isolation only. Coloured pale skin/highlights are preserved.
local root=app.params.root;local source=app.params.source;local count=tonumber(app.params.count or '41');local out=app.params.output
app.fs.makeDirectory(out);app.fs.makeDirectory(out..'/frames')
local board=Image(256*8,256*math.ceil(count/8),ColorMode.RGB);board:clear(app.pixelColor.rgba(45,55,68,255))
local sprite=Sprite(256,256,ColorMode.RGB);sprite.layers[1].name='Whole isolated native figure'
local pc=app.pixelColor
for n=0,count-1 do
 local im=Image{fromFile=source..string.format('/%04d.png',n)};local w,h=im.width,im.height
 local eligible={};local visited={};local queue={};local removed=0
 for y=0,h-1 do for x=0,w-1 do
  local c=im:getPixel(x,y);local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
  if math.max(r,g,b)-math.min(r,g,b)<=10 and math.min(r,g,b)>=205 then eligible[y*w+x+1]=true end
 end end
 local function push(k) if eligible[k] and not visited[k] then visited[k]=true;queue[#queue+1]=k end end
 for x=0,w-1 do push(x+1);push((h-1)*w+x+1) end
 for y=0,h-1 do push(y*w+1);push(y*w+w) end
 local q=1
 while q<=#queue do
  local k=queue[q];q=q+1;local x=(k-1)%w;local y=math.floor((k-1)/w)
  im:drawPixel(x,y,0);removed=removed+1
  if x>0 then push(k-1) end;if x<w-1 then push(k+1) end
  if y>0 then push(k-w) end;if y<h-1 then push(k+w) end
 end
 -- One whole-image uniform reduction and integer translation, from SIFT correspondence.
 im:resize{width=200,height=280,method='bilinear'}
 local canvas=Image(256,256,ColorMode.RGB);canvas:drawImage(im,Point(55,-10))
 if n>0 then sprite:newFrame() end;sprite.cels[n+1].image=canvas
 local tick=function(i) return math.floor((i*1000+12)/24) end
 sprite.frames[n+1].duration=(tick(n+1)-tick(n))/1000
 canvas:saveAs(out..string.format('/frames/%04d.png',n))
 board:drawImage(canvas,Point(n%8*256,math.floor(n/8)*256))
end
sprite:saveAs(out..'/wave.aseprite');board:saveAs(out..'/contact_on_dark.png');sprite:close()
