local directory=app.params.directory
local output=app.params.output
local count=tonumber(app.params.count)
local canvasWidth=tonumber(app.params.width) or 896
local canvasHeight=tonumber(app.params.height) or 512
local s=Sprite(canvasWidth,canvasHeight,ColorMode.RGB)
s.layers[1].name='Native output preserved (hidden)';s.layers[1].isVisible=false
local rawLayer=s.layers[1]
local cleanLayer=s:newLayer();cleanLayer.name='Connected neutral backdrop removed; geometry unchanged'
local rgb=app.pixelColor
for frame=1,count do
 local raw=Image{fromFile=directory..string.format('/raw_%04d.png',frame)}
 local clean=Image(raw)
 local width=raw.width;local height=raw.height
 local q={};local head=1;local tail=0
 local function add(x,y)
  if x<0 or y<0 or x>=width or y>=height then return end
  local pixel=clean:getPixel(x,y)
  if rgb.rgbaA(pixel)==0 then return end
  local r=rgb.rgbaR(pixel);local g=rgb.rgbaG(pixel);local b=rgb.rgbaB(pixel)
  if math.max(math.abs(r-238),math.abs(g-238),math.abs(b-238))<=12 then
   clean:drawPixel(x,y,rgb.rgba(r,g,b,0))
   tail=tail+1;q[tail]=y*width+x
  end
 end
 for x=0,width-1 do add(x,0);add(x,height-1) end
 for y=1,height-2 do add(0,y);add(width-1,y) end
 while head<=tail do
  local index=q[head];q[head]=nil;head=head+1
  local x=index%width;local y=math.floor(index/width)
  add(x-1,y);add(x+1,y);add(x,y-1);add(x,y+1)
 end
 if frame>1 then s:newFrame() end
 s:newCel(rawLayer,frame,raw,Point(0,0));s:newCel(cleanLayer,frame,clean,Point(0,0))
 s.frames[frame].duration=(math.floor(frame*1000/24+0.5)-math.floor((frame-1)*1000/24+0.5))/1000
 clean:saveAs(directory..string.format('/clean_%04d.png',frame))
end
local tag=s:newTag(1,count);tag.name='reference_study'
local slice=s:newSlice(Rectangle(0,0,canvasWidth,canvasHeight));slice.name='Shared canvas reference (not an accepted gameplay socket)';slice.pivot=Point(canvasWidth/2,canvasHeight/2)
s:saveAs(output..'/bridge.aseprite')
s:close()
