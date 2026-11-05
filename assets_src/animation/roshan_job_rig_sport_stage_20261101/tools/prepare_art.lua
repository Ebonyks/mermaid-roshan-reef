local root=assert(app.params.root)
local pc=app.pixelColor
local function load(p) return Image{fromFile=root..p} end
local original=load('/demo/art/body.png');local own=load('/demo/art/ownership.png');local anatomy=load('/demo/art/anatomy.png')
local function poly(px,py,p)
 local inside=false;local j=#p
 for i=1,#p do local a,b=p[i],p[j];if ((a[2]>py)~=(b[2]>py)) and px<(b[1]-a[1])*(py-a[2])/(b[2]-a[2])+a[1] then inside=not inside end;j=i end
 return inside
end
local function resize(im,w,h)
 local sp=Sprite(im.width,im.height,ColorMode.RGB);sp:newCel(sp.layers[1],1,im,Point(0,0));app.command.SpriteSize{width=w,height=h,method='bilinear'}
 local out=Image(w,h,ColorMode.RGB);out:drawImage(sp.cels[1].image,sp.cels[1].position);sp:close();return out
end
local polygons={
 boxer={{603,405},{624,389},{682,390},{734,407},{769,417},{786,470},{730,515},{750,543},{752,570},{770,605},{792,690},{831,788},{826,875},{797,958},{738,1028},{640,1085},{525,1090},{473,1042},{528,1041},{587,1016},{637,975},{653,915},{646,842},{619,770},{590,688},{580,624},{599,563},{565,543},{557,510},{579,456},{595,419}},
 racer={{586,399},{620,381},{649,377},{688,381},{724,400},{759,403},{788,441},{797,475},{780,506},{752,518},{742,554},{783,569},{805,611},{811,652},{796,668},{816,750},{828,830},{810,925},{768,1004},{688,1063},{587,1083},{518,1075},{478,1045},{538,1041},{600,1012},{644,960},{656,894},{643,813},{612,746},{587,680},{583,631},{603,568},{582,536},{561,527},{548,503},{534,470},{533,442},{551,413}},
 popstar={{583,367},{619,343},{650,342},{699,350},{728,367},{774,367},{797,389},{817,430},{826,465},{803,488},{774,495},{767,528},{795,557},{814,598},{798,623},{819,695},{849,777},{861,850},{837,940},{791,1025},{712,1081},{606,1100},{530,1085},{477,1046},{536,1049},{595,1020},{645,976},{659,912},{649,841},{625,778},{598,709},{590,649},{597,614},{614,565},{600,541},{576,520},{556,505},{542,477},{522,459},{516,430},{528,392},{549,374}}
}
local heads={
 boxer={{548,234},{565,195},{616,165},{681,159},{735,174},{771,212},{790,258},{788,317},{768,298},{753,250},{714,224},{655,216},{603,226},{567,250}},
 racer={{525,270},{521,225},{544,158},{590,108},{640,78},{700,76},{754,99},{791,150},{808,208},{808,300},{785,343},{747,329},{746,280},{720,243},{675,218},{618,220},{573,240},{553,278}},
 popstar={{529,135},{557,119},{581,135},{591,161},{580,185},{553,189},{531,172}}
}
for _,theme in ipairs({'boxer','racer','popstar'}) do
 local native=load('/native/'..theme..'_garment_take01.png');local garment=Image(native.width,native.height,ColorMode.RGB)
 for y=330,1120 do for x=440,890 do if x<native.width and y<native.height and poly(x+.5,y+.5,polygons[theme]) then garment:drawPixel(x,y,native:getPixel(x,y)) end end end
 local small=resize(garment,828,828);local raw=Image(1024,1024,ColorMode.RGB);raw:drawImage(small,Point(126,66))
 local dx={};local measured={}
 for y=0,1023 do
  local sl,sr,tl,tr=nil,nil,nil,nil
  for x=0,1023 do local c=raw:getPixel(x,y);local o=own:getPixel(x,y)
   if pc.rgbaA(c)>96 then sl=sl or x;sr=x end
   if (pc.rgbaR(o)>128 or pc.rgbaG(o)>128) and pc.rgbaA(original:getPixel(x,y))>96 then tl=tl or x;tr=x end
  end
  if sl and tl then measured[y]=(tl+tr-sl-sr)/2 end
 end
 local last=0;for y=0,1023 do if measured[y] then last=measured[y] end;dx[y]=last end
 -- Smooth whole RGBA row registration; no old-clothing-alpha silhouette constraint.
 for y=0,1023 do local sum,weight=0,0;for k=math.max(0,y-24),math.min(1023,y+24) do local w=math.exp(-((k-y)/10)^2/2);sum=sum+dx[k]*w;weight=weight+w end;measured[y]=sum/weight end
 local shifted=Image(1024,1024,ColorMode.RGB)
 for y=0,1023 do for x=0,1023 do local t=math.max(0,math.min(1,(y-700)/85));t=t*t*(3-2*t);local sy=y-math.floor((theme=="popstar" and 30 or 40)*t+.5);local sx=x-math.floor(measured[math.max(0,sy)]-(theme=="popstar" and 50 or 70)*t+.5);if sx>=0 and sx<1024 and sy>=0 then shifted:drawPixel(x,y,raw:getPixel(sx,sy)) end end end
 local body=Image(1024,1024,ColorMode.RGB);local tail=Image(1024,1024,ColorMode.RGB)
 for y=0,1023 do for x=0,1023 do local c=shifted:getPixel(x,y);if y<=489 then body:drawPixel(x,y,c) end;if y>=462 then tail:drawPixel(x,y,c) end end end
 body:saveAs(root..'/demo/art/'..theme..'_body.png');tail:saveAs(root..'/demo/art/'..theme..'_tail.png')
 local headnative=Image(native.width,native.height,ColorMode.RGB)
 for y=0,360 do for x=490,840 do if poly(x+.5,y+.5,heads[theme]) then headnative:drawPixel(x,y,native:getPixel(x,y)) end end end
 local headsmall=resize(headnative,1024,1024);local head=Image(1024,1024,ColorMode.RGB);head:drawImage(headsmall,theme=="popstar" and Point(20,42) or Point(0,7));head:saveAs(root..'/demo/art/'..theme..'_head.png')
 local scalp=load('/demo/art/ballet_scalp.png');scalp:saveAs(root..'/demo/art/'..theme..'_scalp.png')
 local composite=Image(anatomy);composite:drawImage(tail);composite:drawImage(body)
 for y=0,1023 do for x=0,1023 do local o=own:getPixel(x,y);if pc.rgbaA(o)>128 then composite:drawPixel(x,y,anatomy:getPixel(x,y)) end;if pc.rgbaB(o)>128 then composite:drawPixel(x,y,scalp:getPixel(x,y)) end end end
 composite:saveAs(root..'/demo/art/'..theme..'_composed.png')
 local preview=Image(1024,1024,ColorMode.RGB);preview:drawImage(load('/demo/art/forearm.png'));preview:drawImage(load('/demo/art/upper_clean.png'));preview:drawImage(composite);preview:drawImage(head);preview:saveAs(root..'/review/'..theme..'_fit_v3.png')
 local master=Sprite(1024,1024,ColorMode.RGB);master.layers[1].name='anatomy_clean';master:newCel(master.layers[1],1,anatomy,Point(0,0))
 for _,e in ipairs({{'tail',tail},{'body',body},{'headwear',head},{'identity_restore',composite}}) do local l=master:newLayer();l.name=e[1];master:newCel(l,1,e[2],Point(0,0));if e[1]=='identity_restore' then l.isVisible=false end end
 master:saveAs(root..'/masters/'..theme..'_skin_v1.aseprite');master:close()
 local f=io.open(root..'/evidence/'..theme..'_row_registration.json','w');f:write('{"uniform_scale":0.66,"offset":[126,66],"rounding":"nearest whole RGBA row, Gaussian sigma10", "dx":[');local vals={};for y=0,1023 do vals[#vals+1]=string.format('%.5f',measured[y]) end;f:write(table.concat(vals,','));f:write(']}\n');f:close()
end
-- Authored glove views remain distinct; make bounded 512 canvases without changing perspective.
local gloves=load('/native/glove_views_take01.png')
for i,n in ipairs({'guard','jab','palm'}) do
 local left=math.floor((i-1)*gloves.width/3);local width=math.floor(gloves.width/3)
 local part=Image(width,gloves.height,ColorMode.RGB);part:drawImage(gloves,Point(-left,0));local scaled=resize(part,512,math.floor(gloves.height*512/width+.5));local out=Image(512,512,ColorMode.RGB);out:drawImage(scaled,Point(0,math.floor((512-scaled.height)/2)));out:saveAs(root..'/demo/art/glove_'..n..'.png')
end
local wheel=resize(load('/native/wheel_take01.png'),512,512);wheel:saveAs(root..'/demo/art/wheel.png')
print('ASEPRITE_ART_PREPARED')
