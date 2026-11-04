
local root="C:/Users/Peter/.codex/worktrees/recent-updates-dev-20261103/mermaid-roshan-reef"
local p=root.."/assets_src/imagegen/picture_reward_stars_20261103/"
local source=app.open(p.."take02_alpha_repair_native.png")
local image=source.cels[1].image:clone()
local names={"ice","mint","sky","coral","amber","lemon","leaf","violet","rose"}
local xs={79,467,855};local ys={85,470,857}
local report=io.open(p.."ASEPRITE_CLEANUP.csv","w")
report:write("name,source_x,source_y,crop_w,crop_h,erased_low_alpha_pixels,retained_core_pixels\n")
for row=0,2 do
 for col=0,2 do
  local core={};local keep={};local corecount=0
  local tx=col*418;local ty=row*418
  for y=0,417 do for x=0,417 do
   local a=app.pixelColor.rgbaA(image:getPixel(tx+x,ty+y))
   if a>=32 then core[y*418+x]=true;corecount=corecount+1 end
  end end
  assert(corecount>30000 and corecount<40000)
  for y=0,417 do for x=0,417 do
   if core[y*418+x] then
    for dy=-2,2 do for dx=-2,2 do
     local nx=x+dx;local ny=y+dy
     if nx>=0 and nx<418 and ny>=0 and ny<418 then keep[ny*418+nx]=true end
    end end
   end
  end end
  local erased=0
  for y=0,417 do for x=0,417 do
   local pixel=image:getPixel(tx+x,ty+y)
   local a=app.pixelColor.rgbaA(pixel)
   if a>0 and not keep[y*418+x] then
    assert(a<32);image:drawPixel(tx+x,ty+y,app.pixelColor.rgba(0,0,0,0));erased=erased+1
   end
  end end
  local n=row*3+col+1
  local slice=source:newSlice(Rectangle(xs[col+1],ys[row+1],320,320));slice.name=names[n]
  report:write(string.format("%s,%d,%d,320,320,%d,%d\n",names[n],xs[col+1],ys[row+1],erased,corecount))
 end
end
report:close()
source.cels[1].image=image
source:saveCopyAs(p.."painted_sparkles_master.aseprite")
source:saveCopyAs(p.."painted_sparkles_master.png")
for row=0,2 do for col=0,2 do
 local name=names[row*3+col+1]
 local cropped=Sprite(320,320,ColorMode.RGB)
 cropped.cels[1].image:drawImage(image,Point(-xs[col+1],-ys[row+1]))
 cropped:saveCopyAs(p.."native_cutouts/"..name..".png")
 app.activeSprite=cropped
 app.command.SpriteSize{ui=false,width=128,height=128,method="bilinear"}
 cropped:saveCopyAs(root.."/assets/mg/picture_feedback/sparkle_"..name.."_painted.png")
 cropped:close()
 print("R134_EXPORT|"..name.."|OK")
end end
source:close()
