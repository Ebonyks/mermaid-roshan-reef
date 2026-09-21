local p=app.params.base
local s=Sprite(488,196,ColorMode.RGB);s.layers[1].name='Arrival tall cloud painted cel'
for k=0,2 do if k>0 then s:newEmptyFrame() end;s.frames[k+1].duration=1.1;local t=app.open(p..string.format('/cel-%02d.png',k));local im=Image(488,196,ColorMode.RGB);im:drawImage(t.cels[1].image,t.cels[1].position);t:close();s:newCel(s.layers[1],k+1,im,Point(0,0)) end
s:saveAs(p..'/arrival-cloud-three-cels.aseprite');s:close();s=app.open(p..'/arrival-cloud-three-cels.aseprite');assert(#s.frames==3)
for k=1,3 do local im=Image(s.spec);im:drawSprite(s,k);im:saveAs(p..string.format('/reopen-%02d.png',k-1)) end;s:close()
