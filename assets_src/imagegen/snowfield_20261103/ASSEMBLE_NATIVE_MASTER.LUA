local paths={}
paths.tl="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowfield_20261103/native/snowfield_02_02_tl.png"
paths.tr="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowfield_20261103/native/snowfield_02_03_tr.png"
paths.bl="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowfield_20261103/native/snowfield_02_04_bl.png"
paths.br="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowfield_20261103/native/snowfield_02_05_br.png"
local root="C:/Users/Peter/.codex/worktrees/flat-vector-critter-book-runtime-20261017/mermaid-roshan-reef/assets_src/imagegen/snowfield_20261103"
local sxTop=1053
local sxBottom=1085
local syLeft=922
local syRight=935
local pc=app.pixelColor
local native={tl=Image{fromFile=paths.tl},tr=Image{fromFile=paths.tr},bl=Image{fromFile=paths.bl},br=Image{fromFile=paths.br}}
local anchors={tl=Point(0,0),tr=Point(794,0),bl=Point(0,794),br=Point(794,794)}
local order={"tl","tr","bl","br"}
local out=Image(2048,2048,ColorMode.RGB)
local function byte(v) return math.max(0,math.min(255,math.floor(v+0.5))) end
local function fade(v)
 if v<=794 then return 0 end
 if v>=1253 then return 1 end
 local t=(v-794)/459
 return t*t*(3-2*t)
end
local function at(k,x,y)
 local p=anchors[k]
 local xx=x-p.x local yy=y-p.y
 if xx<0 or yy<0 or xx>=1254 or yy>=1254 then return 0 end
 return native[k]:getPixel(xx,yy)
end
for y=0,2047 do
 local wy=fade(y)
 local sx=sxTop+(sxBottom-sxTop)*y/2047
 for x=0,2047 do
  local wx=fade(x)
  local sy=syLeft+(syRight-syLeft)*x/2047
  local owner
  if y<sy then owner=(x<sx) and "tl" or "tr"
  else owner=(x<sx) and "bl" or "br" end
  local alpha=pc.rgbaA(at(owner,x,y))
  if alpha>0 then
   local p=at("tl",x,y) local q=at("tr",x,y) local r=at("bl",x,y) local s=at("br",x,y)
   local a=pc.rgbaA(p)*(1-wx)*(1-wy)
   local b=pc.rgbaA(q)*wx*(1-wy)
   local c=pc.rgbaA(r)*(1-wx)*wy
   local e=pc.rgbaA(s)*wx*wy
   local total=a+b+c+e
   if total>0 then
    local rr=(pc.rgbaR(p)*a+pc.rgbaR(q)*b+pc.rgbaR(r)*c+pc.rgbaR(s)*e)/total
    local gg=(pc.rgbaG(p)*a+pc.rgbaG(q)*b+pc.rgbaG(r)*c+pc.rgbaG(s)*e)/total
    local bb=(pc.rgbaB(p)*a+pc.rgbaB(q)*b+pc.rgbaB(r)*c+pc.rgbaB(s)*e)/total
    out:drawPixel(x,y,pc.rgba(byte(rr),byte(gg),byte(bb),alpha))
   end
  end
 end
end
local sprite=Sprite(2048,2048,ColorMode.RGB)
sprite.layers[1].name="composite_untrimmed"
sprite.cels[1].image=out
sprite:saveCopyAs(root.."/snowfield_master_native_untrimmed.png")
sprite.layers[1].isVisible=false
-- Keep the main painted surface and its adjacent authored antialiasing; remove only detached matte debris.
local mask=Image(2048,2048,ColorMode.INDEXED)
local queue={1024+1024*2048}
mask:drawPixel(1024,1024,1)
local head=1
while head<=#queue do
 local index=queue[head]
 local x=index%2048 local y=math.floor(index/2048)
 head=head+1
 for yy=math.max(0,y-1),math.min(2047,y+1) do
  for xx=math.max(0,x-1),math.min(2047,x+1) do
   if mask:getPixel(xx,yy)==0 and pc.rgbaA(out:getPixel(xx,yy))>3 then
    mask:drawPixel(xx,yy,1)
    queue[#queue+1]=xx+yy*2048
   end
  end
 end
end
local clean=Image(2048,2048,ColorMode.RGB)
local removed=0 local removedStrong=0 local kept=0
for y=0,2047 do
 for x=0,2047 do
  local p=out:getPixel(x,y) local a=pc.rgbaA(p)
  if a>0 then
   local keep=mask:getPixel(x,y)==1
   if not keep then
    for yy=math.max(0,y-1),math.min(2047,y+1) do
     for xx=math.max(0,x-1),math.min(2047,x+1) do
      if mask:getPixel(xx,yy)==1 then keep=true end
     end
    end
   end
   if keep then clean:drawPixel(x,y,p) kept=kept+1
   else removed=removed+1 if a>3 then removedStrong=removedStrong+1 end end
  end
 end
end
for _,k in ipairs(order) do
 local layer=sprite:newLayer()
 layer.name="source_native_"..k
 sprite:newCel(layer,1,native[k],anchors[k])
 layer.isVisible=false
end
local final=sprite:newLayer()
final.name="native_composite_matte_cleaned"
sprite:newCel(final,1,clean,Point(0,0))
sprite:saveCopyAs(root.."/masters/snowfield_native_2048.aseprite")
sprite:saveCopyAs(root.."/snowfield_master_native.png")
local f=io.open(root.."/ASEPRITE_NATIVE_ASSEMBLY_RESULT.json","w")
f:write('{"state":"ACTUAL_NATIVE_ASSEMBLY_MATTE_CLEANED_REVIEW_PENDING","native_width":2048,"native_height":2048,"source_regions":4,"source_resampling":false,"guide_pixels_used":false,"whole_reference_pixels_used":false,"main_component_pixels":'..#queue..',"kept_alpha_pixels":'..kept..',"removed_detached_alpha_pixels":'..removed..',"removed_detached_alpha_gt3_pixels":'..removedStrong..'}\n')
f:close()
sprite:close()
