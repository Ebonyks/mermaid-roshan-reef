local p=app.params.base
local s=Sprite(500,208,ColorMode.RGB)
local soil=s.layers[1];soil.name='fixed_soil';local blades=s:newLayer();blades.name='painted_blades'
for k=0,3 do if k>0 then s:newEmptyFrame() end;s.frames[k+1].duration=.35
for j,name in ipairs({'soil-fixed.png',string.format('blades-%02d.png',k)}) do local t=app.open(p..'/'..name);local c=t.cels[1];local im=Image(500,208,ColorMode.RGB);im:drawImage(c.image,c.position);t:close();s:newCel(j==1 and soil or blades,k+1,im,Point(0,0)) end end
app.activeSprite=s;s:newTag(1,4).name='painted_grass_breeze';s:saveAs(p..'/grass-four-cels.aseprite');s:close()
