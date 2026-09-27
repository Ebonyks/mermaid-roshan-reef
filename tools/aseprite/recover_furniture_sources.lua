-- Recover complete source objects, retaining the shipped canvas and center.
local f=assert(io.open(app.params.spec,"r"));local spec=json.decode(f:read("*a"));f:close()
local master=assert(app.open(spec.source));local full=Image(master)
for _,e in ipairs(spec.assets) do
 local r=e.rect;local w=r[3]-r[1];local h=r[4]-r[2]
 local cropped=Image(w,h,ColorMode.RGB);cropped:drawImage(full,Point(-r[1],-r[2]))
 local s=Sprite(w,h,ColorMode.RGB);s.cels[1].image=cropped
 local ratio=math.min((e.size[1]-8)/w,(e.size[2]-8)/h,1)
 app.command.SpriteSize{ui=false,width=math.floor(w*ratio),height=math.floor(h*ratio),method="bilinear"}
 local recovered=Image(s);s:close()
 local target=assert(app.open(e.original));target.layers[1].name="Original clipped card (hidden)";target.layers[1].isVisible=false
 local layer=target:newLayer();layer.name="Complete source silhouette"
 local im=Image(e.size[1],e.size[2],ColorMode.RGB)
 im:drawImage(recovered,Point(math.floor((e.size[1]-recovered.width)/2),math.floor((e.size[2]-recovered.height)/2)))
 target:newCel(layer,1,im,Point(0,0));target:saveAs(e.native);target:saveCopyAs(e.output);target:close()
end
master:close()
