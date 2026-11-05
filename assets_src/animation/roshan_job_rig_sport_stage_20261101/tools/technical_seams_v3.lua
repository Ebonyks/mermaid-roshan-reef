local root=assert(app.params.root);local pc=app.pixelColor
local own=Image{fromFile=root..'/demo/art/ownership.png'};local anatomy=Image{fromFile=root..'/demo/art/anatomy.png'}
local sp=app.open(root..'/masters/racer_skin_v1.aseprite');local body=Image(1024,1024,ColorMode.RGB);local tail=Image(1024,1024,ColorMode.RGB)
for _,l in ipairs(sp.layers) do if l.name=='body' then body:drawImage(l:cel(1).image,l:cel(1).position) end;if l.name=='tail' then tail:drawImage(l:cel(1).image,l:cel(1).position) end end;sp:close()
local p={{590,447},{613,450},{631,466},{643,487},{637,516},{618,523},{595,506},{585,483}}
local function inside(x,y) local odd=false;local j=#p;for i=1,#p do local a,b=p[i],p[j];if ((a[2]>y)~=(b[2]>y)) and x<(b[1]-a[1])*(y-a[2])/(b[2]-a[2])+a[1] then odd=not odd end;j=i end;return odd end
local function edge_distance(x,y)
 local best=1000;local j=#p
 for i=1,#p do local a,b=p[i],p[j];local vx,vy=b[1]-a[1],b[2]-a[2];local t=math.max(0,math.min(1,((x-a[1])*vx+(y-a[2])*vy)/(vx*vx+vy*vy)));local d=math.sqrt((x-a[1]-t*vx)^2+(y-a[2]-t*vy)^2);best=math.min(best,d);j=i end
 return best
end
for y=440,535 do for x=574,659 do if inside(x+.5,y+.5) and pc.rgbaA(own:getPixel(x,y))<128 and edge_distance(x+.5,y+.5)>5 then body:drawPixel(x,y,0);tail:drawPixel(x,y,0) end end end
body:saveAs(root..'/demo/art/racer_body.png');tail:saveAs(root..'/demo/art/racer_tail.png')
local function over(u,f)
 local af,au=pc.rgbaA(f)/255,pc.rgbaA(u)/255;local a=af+au*(1-af);if a<=0 then return 0 end
 return pc.rgba(math.floor((pc.rgbaR(f)*af+pc.rgbaR(u)*au*(1-af))/a+.5),math.floor((pc.rgbaG(f)*af+pc.rgbaG(u)*au*(1-af))/a+.5),math.floor((pc.rgbaB(f)*af+pc.rgbaB(u)*au*(1-af))/a+.5),math.floor(a*255+.5))
end
for _,theme in ipairs({'ballet','magician','boxer','racer','popstar'}) do
 local b=Image{fromFile=root..'/demo/art/'..theme..'_body.png'};local t=Image{fromFile=root..'/demo/art/'..theme..'_tail.png'};local scalp=Image{fromFile=root..'/demo/art/'..theme..'_scalp.png'};local result=Image(anatomy);result:drawImage(t);result:drawImage(b)
 for y=0,1023 do for x=0,1023 do local o=own:getPixel(x,y);if pc.rgbaA(o)>128 then result:drawPixel(x,y,over(over(t:getPixel(x,y),b:getPixel(x,y)),anatomy:getPixel(x,y))) end;if pc.rgbaB(o)>128 then result:drawPixel(x,y,scalp:getPixel(x,y)) end end end
 result:saveAs(root..'/demo/art/'..theme..'_composed.png')
 if theme=='racer' or theme=='popstar' then
  local master=Sprite(1024,1024,ColorMode.RGB);master.layers[1].name='anatomy_clean';master:newCel(master.layers[1],1,anatomy,Point(0,0))
  for _,e in ipairs({{'tail',t},{'body',b},{'headwear',Image{fromFile=root..'/demo/art/'..theme..'_head.png'}}}) do local l=master:newLayer();l.name=e[1];master:newCel(l,1,e[2],Point(0,0)) end
  if theme=='racer' then local l=master:newLayer();l.name='hip_panel_Torso';master:newCel(l,1,Image{fromFile=root..'/demo/art/racer_hip_panel.png'},Point(574,440)) end
  master:saveAs(root..'/masters/'..theme..'_skin_bound_v3.aseprite');master:close()
 end
end
print('TECHNICAL_SEAMS_V3_COMPLETE; five-pixel own-fabric underlap; anatomy foreground composited once; no new painted pixels')
