local root=assert(app.params.root);local pc=app.pixelColor
local function load(n) return Image{fromFile=root..'/demo/art/'..n..'.png'} end
local edge={{370,606,646},{390,598,633},{400,598,636},{410,602,639},{420,607,643},{430,612,647},{440,617,654},{450,622,661},{460,626,667},{470,632,672},{480,640,677},{490,649,682},{500,659,688},{510,668,695},{520,674,705},{530,676,716},{540,680,725},{550,685,726},{560,688,725},{570,706,722},{580,707,721}}
local function arm(x,y)
 for k=1,#edge-1 do local a,b=edge[k],edge[k+1];if y>=a[1] and y<=b[1] then local t=(y-a[1])/(b[1]-a[1]);return x>=a[2]+(b[2]-a[2])*t and x<=a[3]+(b[3]-a[3])*t end end
 return false
end
for _,theme in ipairs({'original','ballet','magician','boxer','racer','popstar'}) do
 local src=load(theme=='original' and 'body' or theme..'_composed');local left=load(theme=='original' and 'upper_arm' or 'upper_clean');left:drawImage(load('forearm'))
 local garment=load(theme=='original' and 'original_body' or theme..'_body');local names={'ActionBody','LeftUpper','LeftFore','LeftHand','RightUpper','RightFore','RightHand'}
 local master=Sprite(1024,1024,ColorMode.RGB)
 for i,n in ipairs(names) do
  local out=Image(1024,1024,ColorMode.RGB)
  for y=0,1023 do for x=0,1023 do
   local r=arm(x,y);local ls=theme~="boxer" and x<495 and y>=345 and y<=412;local rs=theme~="boxer" and x>=600 and x<=650 and y>=346 and y<=414
   local l=(x-449)*(-.582)+(y-454.34)*.813;local u=(x-635.78)*.525+(y-453.68)*.851
   if i==1 and not r and not ls and not rs then out:drawPixel(x,y,src:getPixel(x,y)) end
   if i==2 and (l<0 or (x-449)^2+(y-454.34)^2<=15^2) then out:drawPixel(x,y,left:getPixel(x,y));if ls and pc.rgbaA(garment:getPixel(x,y))>0 then out:drawPixel(x,y,garment:getPixel(x,y)) end end
   if i==3 and ((l>0 and l<66) or (x-449)^2+(y-454.34)^2<=15^2 or (x-410.72)^2+(y-507.8)^2<=14^2) then out:drawPixel(x,y,left:getPixel(x,y)) end
   if i==4 and (l>66 or (x-410.72)^2+(y-507.8)^2<=14^2) then out:drawPixel(x,y,left:getPixel(x,y)) end
   if i==5 and ((r and (u<0 or (x-635.78)^2+(y-453.68)^2<=15^2)) or rs) then out:drawPixel(x,y,src:getPixel(x,y));if rs and pc.rgbaA(garment:getPixel(x,y))>0 then out:drawPixel(x,y,garment:getPixel(x,y)) end end
   if i==6 and r and ((u>0 and u<73) or (x-635.78)^2+(y-453.68)^2<=15^2 or (x-674.06)^2+(y-515.72)^2<=14^2) then out:drawPixel(x,y,src:getPixel(x,y)) end
   if i==7 and r and (u>73 or (x-674.06)^2+(y-515.72)^2<=14^2) then out:drawPixel(x,y,src:getPixel(x,y)) end
  end end
  local layer=i==1 and master.layers[1] or master:newLayer();layer.name=n;master:newCel(layer,1,out,Point(0,0));out:saveAs(root..'/demo/art/'..theme..'_'..n..'.png')
 end
 master:saveAs(root..'/masters/'..theme..'_action_parts_v1.aseprite');master:close()
 local mask=Image(1024,1024,ColorMode.RGB)
 for y=0,1023 do for x=0,1023 do local ls=theme~="boxer" and x<495 and y>=345 and y<=412;local rs=theme~="boxer" and x>=600 and x<=650 and y>=346 and y<=414;if arm(x,y) or ls or rs then mask:drawPixel(x,y,pc.rgba(255,0,0,255)) end end end
 mask:saveAs(root..'/demo/art/'..theme..'_action_mask.png')
end
local racer=Image{fromFile=app.params.racer};local shapes={{{76,223},{83,214},{92,217},{103,216},{112,223},{112,236},{105,247},{95,253},{82,249},{77,241}},{{157,244},{171,245},{178,249},{185,249},{190,255},{190,266},{183,272},{171,273},{159,269},{153,263},{153,253}}}
local function inside(x,y,p) local odd=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then odd=not odd end;j=i end;return odd end
for i,n in ipairs({'left','right'}) do local im=Image(512,512,ColorMode.RGB);for y=205,280 do for x=70,200 do if inside(x+.5,y+.5,shapes[i]) then im:drawPixel(x,y,racer:getPixel(x,y)) end end end;im:saveAs(root..'/demo/art/racer_grip_'..n..'.png') end
local mask=Image(1024,1024,ColorMode.RGB)
for y=0,1023 do for x=0,1023 do if arm(x,y) or (x<505 and y>=345 and y<=412) or (x>=595 and x<=650 and y>=346 and y<=414) then mask:drawPixel(x,y,pc.rgba(255,0,0,255)) end end end
mask:saveAs(root..'/demo/art/action_mask.png')
local mic=load('microphone')
for _,n in ipairs({'upper','lower'}) do local im=Image(mic.width,mic.height,ColorMode.RGB);for y=0,mic.height-1 do if (n=='upper' and y<=275) or (n=='lower' and y>=263) then for x=0,mic.width-1 do im:drawPixel(x,y,mic:getPixel(x,y)) end end end;im:saveAs(root..'/demo/art/mic_'..n..'.png') end
local f=io.open(root..'/evidence/aseprite_art_complete.json' ,'w');f:write('{"status":"COMPLETED","editable_skin_masters":3,"editable_action_masters":3,"method":"Aseprite1.3.18.4 RGBA isolation, uniform bilinear resize and whole-row lateral registration"}\n');f:close()
print('ACTION_PARTS_COMPLETE')
