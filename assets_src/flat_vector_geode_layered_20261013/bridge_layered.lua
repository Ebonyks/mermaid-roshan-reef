local closed=Image{fromFile=app.params.closed}
local opened=Image{fromFile=app.params.opened}
assert(closed.width==1024 and closed.height==1024 and opened.width==1024 and opened.height==1024)
local curve=json.decode(app.params.curve)
local function cut(y)
 for i=1,#curve-1 do
  local a=curve[i];local b=curve[i+1]
  if y>=a[2] and y<=b[2] then return math.floor(a[1]+(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+0.5) end
 end
 error("Missing curve row")
end
local left=Image(1024,1024,ColorMode.RGB);local right=Image(1024,1024,ColorMode.RGB)
for it in closed:pixels() do
 if it.x<cut(it.y) then left:drawPixel(it.x,it.y,it()) else right:drawPixel(it.x,it.y,it()) end
end
local cavity=Image(opened,Rectangle(260,240,220,560))
local s=Sprite(1024,1024,ColorMode.RGB)
local ref=s.layers[1];ref.name="Closed source reference hidden";s:newCel(ref,1,closed,Point(0,0));ref.isVisible=false
local openref=s:newLayer();openref.name="Opened source reference hidden";s:newCel(openref,1,opened,Point(0,0));openref.isVisible=false
local l=s:newLayer();l.name="Fixed left shell exclusive source mask";s:newCel(l,1,left,Point(0,0))
local r=s:newLayer();r.name="Moving right shell exclusive source mask";s:newCel(r,1,right,Point(0,0))
s:saveAs(app.params.master);s:close()
local reopened=assert(app.open(app.params.master));assert(#reopened.layers==4 and #reopened.frames==1)
local out=Image(1024,1024,ColorMode.RGB);out:drawSprite(reopened,1);out:saveAs(app.params.roundtrip)
left:saveAs(app.params.left);right:saveAs(app.params.right);cavity:saveAs(app.params.cavity)
local proof=assert(io.open(app.params.proof,"wb"));proof:write(json.encode{size={1024,1024},layers=#reopened.layers,frames=1,curve=curve,cavity_rect={260,240,220,560},partition="exclusive binary original RGBA; no appearance pixels painted",new_generation_calls=0});proof:close();reopened:close()
print("GEODE_LAYERED_ASEPRITE|exclusive shell partition and exact cavity rectangle exported")
