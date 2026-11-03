-- Non-destructive native garment registration. All geometry belongs to clothing.
local root=assert(app.params.root)
local function part(path,scale,dx,dy,ymin,ymax,xmin,xmax)
 local s=Sprite{fromFile=path};app.activeSprite=s
 app.command.SpriteSize{ui=false,width=math.floor(s.width*scale+0.5),height=math.floor(s.height*scale+0.5),lockRatio=true,method="bilinear"}
 local src=Image(s.width,s.height,ColorMode.RGB)
 src:drawImage(s.cels[1].image,s.cels[1].position)
 local out=Image(1024,1024,ColorMode.RGB)
 for y=0,src.height-1 do for x=0,src.width-1 do
  local px=src:getPixel(x,y);local a=app.pixelColor.rgbaA(px)
  if a>24 and y>=ymin*scale and y<ymax*scale and x>=xmin*scale and x<xmax*scale then
   local tx=x+dx;local ty=y+dy
   if tx>=0 and tx<1024 and ty>=0 and ty<1024 then out:drawPixel(tx,ty,px) end
  end
 end end
 s:close();return out
end
local configs={
 {name="detective",s=0.72,dx=38,dy=61,head_s=0.68,hx=62,hy=39,body_end=620,tail_start=570},
 {name="geologist",s=0.72,dx=60,dy=49,head_s=0.72,hx=48,hy=0,body_end=620,tail_start=570}
}
for _,c in ipairs(configs) do
 local native=root.."/native/"..c.name.."_take01.png"
 local head=part(native,c.head_s,c.hx,c.hy,80,335,520,850)
 local body=part(native,c.s,c.dx,c.dy,350,c.body_end,480,930)
 local tail
 if c.name=="geologist" then tail=part(native,0.83,-4,-11,c.tail_start,1100,200,850)
 else tail=part(native,c.s,c.dx,c.dy,c.tail_start,1150,200,930) end
 local master=Sprite(1024,1024,ColorMode.RGB)
 for i,item in ipairs({{name="tail",image=tail},{name="body",image=body},{name="head",image=head}}) do
  local l=i==1 and master.layers[1] or master:newLayer();l.name=item.name
  master:newCel(l,1,item.image,Point(0,0));item.image:saveAs(root.."/demo/art/"..c.name.."_"..item.name..".png")
 end
 master:saveAs(root.."/masters/"..c.name.."_registered.aseprite");master:close()
end
-- Clean anatomy has no former blouse/tail clothing. Exclude old fin when new
-- complete tail is selected. Ownership is source identity, not old clothes alpha.
local anatomy=Image{fromFile=root.."/demo/art/anatomy.png"}
local owner=Image{fromFile=root.."/demo/art/ownership.png"}
for y=590,1023 do for x=0,1023 do anatomy:drawPixel(x,y,0);owner:drawPixel(x,y,0) end end
anatomy:saveAs(root.."/demo/art/investigation_anatomy.png")
owner:saveAs(root.."/demo/art/investigation_ownership.png")
-- Original brush/clue fixtures are copied losslessly by prepare_demo.py.
print("REGISTERED_GARMENTS_COMPLETE")
