local root=assert(app.params.root);local pc=app.pixelColor
local src=app.open(root..'/masters/racer_skin_v1.aseprite');local body=Image(1024,1024,ColorMode.RGB);local tail=Image(1024,1024,ColorMode.RGB);for _,l in ipairs(src.layers) do if l.name=='body' then body:drawImage(l:cel(1).image,l:cel(1).position) end;if l.name=='tail' then tail:drawImage(l:cel(1).image,l:cel(1).position) end end;src:close();local originalbody=Image(body);local originaltail=Image(tail)
local ownership=Image{fromFile=root..'/demo/art/ownership.png'};local anatomy=Image{fromFile=root..'/demo/art/anatomy.png'};local scalp=Image{fromFile=root..'/demo/art/racer_scalp.png'}
local p={{590,447},{613,450},{631,466},{643,487},{637,516},{618,523},{595,506},{585,483}}
local function inside(x,y) local odd=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then odd=not odd end;j=i end;return odd end
local panel=Image(128,128,ColorMode.RGB)
for y=440,535 do for x=574,659 do if inside(x+.5,y+.5) and pc.rgbaA(ownership:getPixel(x,y))<128 then
 local c=pc.rgbaA(originalbody:getPixel(x,y))>0 and originalbody:getPixel(x,y) or originaltail:getPixel(x,y)
 panel:drawPixel(x-574,y-440,c);body:drawPixel(x,y,0);tail:drawPixel(x,y,0)
end end end
body:saveAs(root..'/demo/art/racer_body.png');tail:saveAs(root..'/demo/art/racer_tail.png');panel:saveAs(root..'/demo/art/racer_hip_panel.png')
local composite=Image(anatomy);composite:drawImage(tail);composite:drawImage(body)
for y=0,1023 do for x=0,1023 do local o=ownership:getPixel(x,y);if pc.rgbaA(o)>128 then composite:drawPixel(x,y,anatomy:getPixel(x,y)) end;if pc.rgbaB(o)>128 then composite:drawPixel(x,y,scalp:getPixel(x,y)) end end end
composite:saveAs(root..'/demo/art/racer_composed.png')
local master=Sprite(128,128,ColorMode.RGB);master.layers[1].name='racer_jacket_panel_Torso';master:newCel(master.layers[1],1,panel,Point(0,0));master:saveAs(root..'/masters/racer_hip_panel.aseprite');master:close()
local bound=Sprite(1024,1024,ColorMode.RGB);bound.layers[1].name='anatomy_clean';bound:newCel(bound.layers[1],1,anatomy,Point(0,0))
for _,e in ipairs({{'tail',tail},{'body',body},{'headwear',Image{fromFile=root..'/demo/art/racer_head.png'}}}) do local layer=bound:newLayer();layer.name=e[1];bound:newCel(layer,1,e[2],Point(0,0)) end
local layer=bound:newLayer();layer.name='hip_panel_Torso';bound:newCel(layer,1,panel,Point(574,440));bound:saveAs(root..'/masters/racer_skin_bound_v1.aseprite');bound:close()
print('RACER_PANEL_BOUND_TO_EXISTING_TORSO; source region[574,440],128square; no mesh weight/rest change')
