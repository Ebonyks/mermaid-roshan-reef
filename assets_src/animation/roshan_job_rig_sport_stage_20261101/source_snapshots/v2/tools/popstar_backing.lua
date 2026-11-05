local root=assert(app.params.root);local pc=app.pixelColor
local src=app.open(root..'/masters/popstar_skin_v1.aseprite');local body=Image(1024,1024,ColorMode.RGB);local tail=Image(1024,1024,ColorMode.RGB)
for _,l in ipairs(src.layers) do if l.name=='body' then body:drawImage(l:cel(1).image,l:cel(1).position) end;if l.name=='tail' then tail:drawImage(l:cel(1).image,l:cel(1).position) end end;src:close()
local original=Image(body);local own=Image{fromFile=root..'/demo/art/ownership.png'};local anatomy=Image{fromFile=root..'/demo/art/anatomy.png'};local scalp=Image{fromFile=root..'/demo/art/popstar_scalp.png'}
local p={{436,326},{459,324},{469,334},{467,353},{450,358},{436,347}}
local function inside(x,y) local odd=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then odd=not odd end;j=i end;return odd end
local backing=Image(1024,1024,ColorMode.RGB)
for y=324,360 do for x=434,471 do if inside(x+.5,y+.5) then local c=original:getPixel(x+22,y+31);if pc.rgbaA(c)>0 then backing:drawPixel(x,y,c) end end end end
body:drawImage(backing);body:saveAs(root..'/demo/art/popstar_body.png');backing:saveAs(root..'/demo/art/popstar_sleeve_backing.png')
local composite=Image(anatomy);composite:drawImage(tail);composite:drawImage(body)
for y=0,1023 do for x=0,1023 do local o=own:getPixel(x,y);if pc.rgbaA(o)>128 then composite:drawPixel(x,y,anatomy:getPixel(x,y)) end;if pc.rgbaB(o)>128 then composite:drawPixel(x,y,scalp:getPixel(x,y)) end end end
composite:saveAs(root..'/demo/art/popstar_composed.png')
local sp=Sprite(1024,1024,ColorMode.RGB);sp.layers[1].name='anatomy_clean';sp:newCel(sp.layers[1],1,anatomy,Point(0,0));for _,e in ipairs({{'tail',tail},{'body',body},{'headwear',Image{fromFile=root..'/demo/art/popstar_head.png'}},{'local_backing_source',backing}}) do local l=sp:newLayer();l.name=e[1];sp:newCel(l,1,e[2],Point(0,0));if e[1]=='local_backing_source' then l.isVisible=false end end;sp:saveAs(root..'/masters/popstar_skin_bound_v1.aseprite');sp:close()
print('POPSTAR_LOCAL_BACKING_COMPLETE; one translated own-fabric patch behind original curl, no repeated rows/no old clothing')
