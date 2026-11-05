local root=assert(app.params.root);local pc=app.pixelColor
local right=Image{fromFile=root..'/demo/art/body.png'};local left=Image{fromFile=root..'/demo/art/upper_clean.png'};left:drawImage(Image{fromFile=root..'/demo/art/forearm.png'})
local sp=Sprite(1024,1024,ColorMode.RGB)
for i,e in ipairs({{'LeftElbowCap',left,435,480,449,454,11.5},{'RightElbowCap',right,652,470,636,454,12.5}}) do
 local im=Image(1024,1024,ColorMode.RGB)
 for dy=-13,13 do for dx=-13,13 do local d=math.sqrt(dx*dx+dy*dy);local factor=math.max(0,math.min(1,(e[7]-.5-d)/5.0));if factor>0 then local c=e[2]:getPixel(e[3]+dx,e[4]+dy);im:drawPixel(e[5]+dx,e[6]+dy,pc.rgba(pc.rgbaR(c),pc.rgbaG(c),pc.rgbaB(c),math.floor(pc.rgbaA(c)*factor+.5))) end end end
 im:saveAs(root..'/demo/art/'..e[1]..'.png');local layer=i==1 and sp.layers[1] or sp:newLayer();layer.name=e[1];sp:newCel(layer,1,im,Point(0,0))
end
sp:saveAs(root..'/masters/shared_joint_caps.aseprite');sp:close()
local card=Image{fromFile=assert(app.params.popstar)};local crop=Image(80,100,ColorMode.RGB);crop:drawImage(card,Point(-50,-130));local detail=Sprite(80,100,ColorMode.RGB);detail:newCel(detail.layers[1],1,crop,Point(0,0));app.command.SpriteSize{width=320,height=400,method='bilinear'};detail:saveAs(root..'/review/popstar_hand_source_detail.png');detail:close()
local grip=Image(512,512,ColorMode.RGB)
local polygon={{86,168},{93,165},{101,170},{106,179},{108,188},{107,195},{102,202},{98,211},{90,212},{83,205},{82,198},{88,191},{79,187},{78,179},{80,173}}
local function inside(x,y) local odd=false;local j=#polygon;for i=1,#polygon do local a,b=polygon[i],polygon[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then odd=not odd end;j=i end;return odd end
for y=160,215 do for x=74,111 do if inside(x+.5,y+.5) then grip:drawPixel(x,y,card:getPixel(x,y)) end end end
grip:saveAs(root..'/demo/art/popstar_grip.png')
local handmaster=Sprite(512,512,ColorMode.RGB);handmaster.layers[1].name='approved_hand_and_contact_sliver';handmaster:newCel(handmaster.layers[1],1,grip,Point(0,0));handmaster:saveAs(root..'/masters/popstar_grip.aseprite');handmaster:close()
print('SOURCE_BOUND_JOINT_CAPS_COMPLETE')
