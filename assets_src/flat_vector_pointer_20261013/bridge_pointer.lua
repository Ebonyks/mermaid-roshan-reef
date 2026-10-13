local s=assert(app.open(app.params.source))
assert(s.width==1254 and s.height==1254 and #s.frames==1 and #s.layers==1)
s.layers[1].name="Complete preserved generated hand"
s:saveAs(app.params.native_master)
local native=Image(s.width,s.height,ColorMode.RGB);native:drawSprite(s,1);native:saveAs(app.params.native_roundtrip)
local w,h=s.width,s.height
local labels={};local component=0;local largest=0;local largest_count=0
for y=0,h-1 do for x=0,w-1 do
 local idx=y*w+x+1
 if not labels[idx] and app.pixelColor.rgbaA(native:getPixel(x,y))>=16 then
  component=component+1;local q={idx};labels[idx]=component;local head=1
  while head<=#q do
   local v=q[head];head=head+1;local vy=math.floor((v-1)/w);local vx=(v-1)%w
   for _,off in ipairs({{-1,0},{1,0},{0,-1},{0,1}}) do
    local nx,ny=vx+off[1],vy+off[2]
    if nx>=0 and ny>=0 and nx<w and ny<h then
     local ni=ny*w+nx+1
     if not labels[ni] and app.pixelColor.rgbaA(native:getPixel(nx,ny))>=16 then labels[ni]=component;q[#q+1]=ni end
    end
   end
  end
  if #q>largest_count then largest=component;largest_count=#q end
 end
end end
local clean=Image(native);local removed=0
for y=0,h-1 do for x=0,w-1 do
 if app.pixelColor.rgbaA(native:getPixel(x,y))>0 and labels[y*w+x+1]~=largest then
  local near=false
  for dy=-2,2 do for dx=-2,2 do
   local nx,ny=x+dx,y+dy
   if nx>=0 and ny>=0 and nx<w and ny<h and labels[ny*w+nx+1]==largest then near=true end
  end end
  if not near then clean:putPixel(x,y,app.pixelColor.rgba(0,0,0,0));removed=removed+1 end
 end
end end
s:close()
local out=Sprite(w,h,ColorMode.RGB);out.layers[1].name="Complete hand; isolated alpha specks retired"
out:newCel(out.layers[1],1,clean,Point(0,0));out:saveAs(app.params.clean_master);clean:saveAs(app.params.clean_png)
app.command.SpriteSize{ui=false,width=1024,height=1024,method="bilinear"}
out:saveAs(app.params.normalized_master)
local output=Image(1024,1024,ColorMode.RGB);output:drawSprite(out,1);output:saveAs(app.params.output)
local proof=assert(io.open(app.params.proof,"wb"))
proof:write(json.encode{native_size={1254,1254},normalized_size={1024,1024},layers=#out.layers,frames=#out.frames,method="bilinear",matte_cleanup={alpha_component_threshold=16,retained_component=largest,main_alpha_pixels=largest_count,component_count=component,antialias_neighbor_radius=2,removed_nonzero_alpha_pixels=removed},crop=false,recolor=false,repaint=false,part_separation=false})
proof:close();out:close();print("POINTER_ASEPRITE|Whole hand preserved; isolated alpha specks cleaned; proportional1024 export")
