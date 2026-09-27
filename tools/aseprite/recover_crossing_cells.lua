local f=assert(io.open(app.params.spec,"r"));local spec=json.decode(f:read("*a"));f:close()
for _,e in ipairs(spec.assets) do
 local original=assert(app.open(e.source));local before=Image(original);local out=Image(before)
 local r=e.source_rect;local t=e.target_cell;local w=r[3]-r[1];local h=r[4]-r[2]
 local cell=Sprite(w,h,ColorMode.RGB);local im=Image(w,h,ColorMode.RGB);im:drawImage(before,Point(-r[1],-r[2]));cell.cels[1].image=im
 local ratio=math.min((t[3]-8)/w,(t[4]-8)/h,1)
 app.command.SpriteSize{ui=false,width=math.floor(w*ratio),height=math.floor(h*ratio),method="bilinear"}
 local recovered=Image(cell);cell:close()
 for y=t[2],t[2]+t[4]-1 do for x=t[1],t[1]+t[3]-1 do out:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0)) end end
 for _,c in ipairs(e.erase_rects) do for y=c[2],c[4]-1 do for x=c[1],c[3]-1 do out:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0)) end end end
 out:drawImage(recovered,Point(t[1]+math.floor((t[3]-recovered.width)/2),t[2]+t[4]-4-recovered.height))
 original.layers[1].name="Original crossing cells (hidden)";original.layers[1].isVisible=false
 local layer=original:newLayer();layer.name="Complete source silhouette with gutter";original:newCel(layer,1,out,Point(0,0))
 original:saveAs(e.native);original:saveCopyAs(e.output);original:close()
end
