local root=app.params["packet"]
do local sheet=Image{fromFile=root.."/demo_project/items/fir.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="fir"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/fir.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/huckleberry.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="huckleberry"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/huckleberry.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/hydrangea.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="hydrangea"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/hydrangea.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/bellflower.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="bellflower"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/bellflower.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/cloud.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="cloud"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/cloud.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/smoke.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="smoke"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/smoke.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/seesaw.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="seesaw"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/seesaw.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/gate.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="gate"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/gate.aseprite");s:close() end
do local sheet=Image{fromFile=root.."/demo_project/items/glass.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="glass"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/glass.aseprite");s:close() end
local f=io.open(root.."/evidence/aseprite-build.txt","w");f:write("Aseprite "..tostring(app.version).."; nine masters; 360 cels at 100ms");f:close()
