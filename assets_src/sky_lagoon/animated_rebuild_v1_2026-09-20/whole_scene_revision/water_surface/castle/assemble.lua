local p=app.params.base
local s=Sprite(1624,620,ColorMode.RGB)
local ground=s.layers[1];ground.name='Original fixed shoreline'
local surface=s:newLayer();surface.name='Whole painted water surface - baked trial'
local t=app.open(p..'/original.png');local base=Image(1624,620,ColorMode.RGB);base:drawImage(t.cels[1].image,t.cels[1].position);t:close()
for k=0,11 do
 if k>0 then s:newEmptyFrame() end
 s.frames[k+1].duration=.16;s:newCel(ground,k+1,base,Point(0,0))
 local t=app.open(p..string.format('/surface-%02d.png',k));local im=Image(1624,620,ColorMode.RGB);im:drawImage(t.cels[1].image,t.cels[1].position);t:close();s:newCel(surface,k+1,im,Point(0,0))
end
app.activeSprite=s;s:newTag(1,12).name='whole_water_surface_trial';s:saveAs(p..'/whole-water-12-cels.aseprite')
for k=1,12 do local im=Image(s.spec);im:drawSprite(s,k);im:saveAs(p..string.format('/export-%02d.png',k-1)) end
s:close()
