local root=assert(app.params.root)
local original=Image{fromFile=root.."/demo/art/upper_clean.png"}
for y=520,1023 do for x=0,1023 do original:drawPixel(x,y,0) end end
original:saveAs(root.."/demo/art/upper_work.png")
local fore=Image{fromFile=root.."/demo/art/forearm.png"}
for y=518,1023 do for x=0,1023 do fore:drawPixel(x,y,0) end end
fore:saveAs(root.."/demo/art/fore_work.png")
local s=Sprite{fromFile=root.."/native/grip_take01.png"};app.activeSprite=s
app.command.SpriteSize{ui=false,width=69,height=69,lockRatio=true,method="bilinear"}
local scaled=Image(s.width,s.height,ColorMode.RGB);scaled:drawImage(s.cels[1].image,s.cels[1].position)
local out=Image(1024,1024,ColorMode.RGB)
for y=0,68 do for x=0,36 do local p=scaled:getPixel(x,y);if app.pixelColor.rgbaA(p)>24 then out:drawPixel(x+377,y+491,p) end end end
out:saveAs(root.."/demo/art/grip_front.png");s:close()
local hand=Sprite(1024,1024,ColorMode.RGB);hand.layers[1].name="Generated grip / registered source hand view";hand:newCel(hand.layers[1],1,out,Point(0,0));hand:saveAs(root.."/masters/grip_registered.aseprite");hand:close()
local glass=Image{fromFile=root.."/demo/art/magnifier.png"}
for y=0,glass.height-1 do for x=0,glass.width-1 do
 local dx=(x-177)/106;local dy=(y-151)/110
 if dx*dx+dy*dy<1 then
  local p=glass:getPixel(x,y);glass:drawPixel(x,y,app.pixelColor.rgba(app.pixelColor.rgbaR(p),app.pixelColor.rgbaG(p),app.pixelColor.rgbaB(p),65))
 end
end end
glass:saveAs(root.."/demo/art/magnifier_glass.png")
print("GRIP_AND_GLASS_DERIVATIVES_COMPLETE")
