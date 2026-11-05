local root=app.params["packet"]
local only=app.params["only"]
local built=0
if only==nil or only=="fir" then
do local sheet=Image{fromFile=root.."/demo_project/items/fir.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="fir"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/fir.aseprite");s:close() end
built=built+1 end
if only==nil or only=="huckleberry" then
do local sheet=Image{fromFile=root.."/demo_project/items/huckleberry.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="huckleberry"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/huckleberry.aseprite");s:close() end
built=built+1 end
if only==nil or only=="hydrangea" then
do local sheet=Image{fromFile=root.."/demo_project/items/hydrangea.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="hydrangea"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/hydrangea.aseprite");s:close() end
built=built+1 end
if only==nil or only=="bellflower" then
do local sheet=Image{fromFile=root.."/demo_project/items/bellflower.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="bellflower"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/bellflower.aseprite");s:close() end
built=built+1 end
if only==nil or only=="cloud" then
do local sheet=Image{fromFile=root.."/demo_project/items/cloud.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="cloud"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/cloud.aseprite");s:close() end
built=built+1 end
if only==nil or only=="smoke" then
do local sheet=Image{fromFile=root.."/demo_project/items/smoke.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="smoke"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/smoke.aseprite");s:close() end
built=built+1 end
if only==nil or only=="seesaw" then
do local sheet=Image{fromFile=root.."/demo_project/items/seesaw.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="seesaw"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/seesaw.aseprite");s:close() end
built=built+1 end
if only==nil or only=="gate" then
do local sheet=Image{fromFile=root.."/demo_project/items/gate.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="gate"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/gate.aseprite");s:close() end
built=built+1 end
if only==nil or only=="glass" then
do local sheet=Image{fromFile=root.."/demo_project/items/glass.png"}
local s=Sprite(256,256,ColorMode.RGB)
local layer=s.layers[1];layer.name="glass"
for i=0,39 do if i>0 then s:newEmptyFrame() end
local im=Image(256,256,ColorMode.RGB);im:drawImage(sheet,Point(-(i%8)*256,-math.floor(i/8)*256))
s:newCel(layer,i+1,im,Point(0,0));s.frames[i+1].duration=0.1 end
s:saveAs(root.."/glass.aseprite");s:close() end
built=built+1 end
local f=io.open(root.."/evidence/aseprite-build.txt","w");f:write("Aseprite "..tostring(app.version).."; masters_built="..built.."; 40 cels each at 100ms");f:close()
