-- Owner 2026-09-26: exact native Aseprite pixel edits, no generated sprites.
-- Each rectangle is reviewed source ownership, not a whole-image heuristic.
local f=assert(io.open(app.params.spec,"r"))
local spec=json.decode(f:read("*a"));f:close()
for _,entry in ipairs(spec.assets) do
 local src=assert(app.open(entry.source))
 local before=Image(src)
 local layer=src:newLayer(); layer.name="Reviewed pixel repairs 2026-09-26"
 local repaired=Image(before)
 for _,rect in ipairs(entry.erase_rects) do
  for y=rect[2],rect[4]-1 do
   for x=rect[1],rect[3]-1 do
    repaired:drawPixel(x,y,app.pixelColor.rgba(0,0,0,0))
   end
  end
 end
 for _,rect in ipairs(entry.opaque_rects or {}) do
  for y=rect[2],rect[4]-1 do
   for x=rect[1],rect[3]-1 do
    local c=repaired:getPixel(x,y)
    local a=app.pixelColor.rgbaA(c)
    local interior=true
    for dy=-2,2 do
     for dx=-2,2 do
      local nx=x+dx;local ny=y+dy
      if nx<0 or ny<0 or nx>=before.width or ny>=before.height or app.pixelColor.rgbaA(before:getPixel(nx,ny))<90 then interior=false end
     end
    end
    if interior and a>=100 and a<250 then
     repaired:drawPixel(x,y,app.pixelColor.rgba(app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c),255))
    end
   end
  end
 end
 for _,xy in ipairs(entry.force_opaque_pixels or {}) do
  local c=repaired:getPixel(xy[1],xy[2]);repaired:drawPixel(xy[1],xy[2],app.pixelColor.rgba(app.pixelColor.rgbaR(c),app.pixelColor.rgbaG(c),app.pixelColor.rgbaB(c),255))
 end
 for _,p in ipairs(entry.paint_pixels or {}) do
  repaired:drawPixel(p.xy[1],p.xy[2],app.pixelColor.rgba(p.rgba[1],p.rgba[2],p.rgba[3],p.rgba[4]))
 end
 src.layers[1].name="Original source (hidden, immutable)";src.layers[1].isVisible=false
 src:newCel(layer,1,repaired,Point(0,0))
 src:saveAs(entry.native)
 src:saveCopyAs(entry.output)
 src:close()
 print("ASEPRITE_PIXEL_REPAIR|"..entry.output)
end
