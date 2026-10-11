-- Same connected neutral-field isolation as the root's isolate_native.lua.
-- Whole-image native isolation/reduction for the three representative cels only.
local source=assert(app.params.source);local out=assert(app.params.output)
app.fs.makeAllDirectories(out);app.fs.makeAllDirectories(out..'/native_rgba');app.fs.makeAllDirectories(out..'/frames256')
local indices={8,26,32};local pc=app.pixelColor
local master=Sprite(640,896,ColorMode.RGB);master.layers[1].name='Complete painted native cel, connected field isolation'
local board=Image(768,256,ColorMode.RGB);board:clear(pc.rgba(45,55,68,255))
for i,n in ipairs(indices) do
 local im=Image{fromFile=source..string.format('/%04d.png',n)};local w,h=im.width,im.height
 local eligible,visited,queue={},{},{}
 for y=0,h-1 do for x=0,w-1 do local c=im:getPixel(x,y);local r,g,b=pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c)
  if math.max(r,g,b)-math.min(r,g,b)<=10 and math.min(r,g,b)>=205 then eligible[y*w+x+1]=true end
 end end
 local function push(k) if eligible[k] and not visited[k] then visited[k]=true;queue[#queue+1]=k end end
 for x=0,w-1 do push(x+1);push((h-1)*w+x+1) end
 for y=0,h-1 do push(y*w+1);push(y*w+w) end
 local q=1
 while q<=#queue do local k=queue[q];q=q+1;local x=(k-1)%w;local y=math.floor((k-1)/w);im:drawPixel(x,y,0)
  if x>0 then push(k-1) end;if x<w-1 then push(k+1) end;if y>0 then push(k-w) end;if y<h-1 then push(k+w) end
 end
 if i>1 then master:newEmptyFrame(i) end
 master:newCel(master.layers[1],i,im,Point(0,0));master.frames[i].duration=.25
 im:saveAs(out..string.format('/native_rgba/%04d.png',n))
 local small=Image(im);small:resize{width=200,height=280,method='bilinear'}
 local canvas=Image(256,256,ColorMode.RGB);canvas:drawImage(small,Point(55,-10));canvas:saveAs(out..string.format('/frames256/%04d.png',n))
 board:drawImage(canvas,Point((i-1)*256,0))
end
master:saveAs(out..'/native_rgba.aseprite');board:saveAs(out..'/contact256_on_dark.png');master:close()
